# A2 · Two validators on one field. Run: python check.py a2
from typing import Annotated

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas import MessageIn, RoomIn
from app.storage import Storage


class MessagePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: Annotated[str, Field(min_length=1, max_length=500)] | None = None
    pinned: bool | None = None

    @field_validator("text")
    @classmethod
    def not_blank(cls, v):
        if not v.strip():
            raise ValueError("text cannot be only spaces")
        return v.strip()

    @field_validator("text", "pinned")
    @classmethod
    def not_null(cls, v):
        if v is None:
            raise ValueError("may be left out, but not null")
        return v


app = FastAPI()
store = Storage()


@app.patch("/rooms/{room_id}/messages/{message_id}")
def patch_message(room_id: int, message_id: int, payload: MessagePatch):
    return store.update(room_id, message_id, payload.model_dump(exclude_unset=True))


def check() -> None:
    store.add_room(RoomIn(title="general"))
    store.add(1, MessageIn(author="Aida", text="hello"))
    client = TestClient(app, raise_server_exceptions=False)
    for name, body in [("a", {"pinned": True}), ("b", {"text": "  hi  "}),
                       ("c", {"text": None}), ("d", {"text": "   "})]:
        response = client.patch("/rooms/1/messages/1", json=body)
        answer = response.json() if response.headers.get("content-type") == "application/json" else response.text
        if response.status_code == 422:
            answer = response.json()["detail"][0]["msg"]
        print(f"({name}) {response.status_code}  {answer}")
