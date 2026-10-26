from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from errors import ChatFull, MessageNotFound
from models import Message
from schemas import MessageIn, MessagePatch
from storage import Storage

app = FastAPI(title="Chat API")
store = Storage()


@app.exception_handler(MessageNotFound)
def message_not_found_handler(request: Request, exc: MessageNotFound) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc), "code": "message_not_found"},
    )


@app.exception_handler(ChatFull)
def chat_full_handler(request: Request, exc: ChatFull) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc), "code": "chat_full"},
    )


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
