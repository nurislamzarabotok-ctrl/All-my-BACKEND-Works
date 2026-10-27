# A3 · Read the traceback. Run: python check.py a3
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.models import Message


class Storage:
    def __init__(self) -> None:
        self.messages: list[Message] = []

    def get(self, message_id: int) -> Message:
        return self.messages[message_id]


app = FastAPI()
store = Storage()


@app.get("/messages/{message_id}")
def get_message(message_id: int) -> Message:
    return store.get(message_id)


def check() -> None:
    store.messages.append(Message(id=1, room_id=1, author="Aida", text="hello"))
    client = TestClient(app, raise_server_exceptions=False)
    print("GET /messages/1 ->", client.get("/messages/1").status_code)
    print("GET /messages/0 ->", client.get("/messages/0").status_code, "(id 0 does not exist, and still 200)")
    print("Now the request from the slide, with the traceback the server prints:\n")
    import sys
    import traceback
    try:
        TestClient(app).get("/messages/1")
    except Exception:
        traceback.print_exc(limit=-3, file=sys.stdout)
    response = client.get("/messages/1")
    print("\nThe client gets:", response.status_code, response.text)
