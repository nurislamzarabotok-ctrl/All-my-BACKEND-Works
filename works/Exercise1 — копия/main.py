from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# TODO 5 and 6: import MessageNotFound and ChatFull from errors
from models import Message
from schemas import MessageIn, MessagePatch
from storage import Storage

app = FastAPI(title="Chat API")
store = Storage()


# TODO 5: an exception handler for MessageNotFound (lesson 25).
#   404 {"detail": "Message 99 not found", "code": "message_not_found"}


# TODO 6: an exception handler for ChatFull (lesson 25).
#   409 {"detail": "Chat is full (3 messages)", "code": "chat_full"}


@app.get("/messages", response_model=list[Message])
def list_messages() -> list[Message]:
    return store.get_all()


@app.post("/messages", response_model=Message, status_code=201)
def create_message(payload: MessageIn) -> Message:
    return store.add(payload)


@app.get("/messages/{message_id}", response_model=Message)
def get_message(message_id: int) -> Message:
    return store.get(message_id)


@app.patch("/messages/{message_id}", response_model=Message)
def patch_message(message_id: int, payload: MessagePatch) -> Message:
    return store.update(message_id, payload.model_dump(exclude_unset=True))


@app.delete("/messages/{message_id}", status_code=204)
def delete_message(message_id: int) -> None:
    store.delete(message_id)


# Start with the IDE's Debug button, or with: python main.py
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
