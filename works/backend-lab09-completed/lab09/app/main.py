from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.errors import ChatFull, MessageNotFound, RoomNotFound, UserExists, UserNotFound
from app.routers import messages, rooms, stats, users

app = FastAPI(title="Chat API")
app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(messages.router)
app.include_router(stats.router)


@app.exception_handler(UserNotFound)
def user_not_found(request: Request, exc: UserNotFound) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"User {exc.user_id} not found", "code": "user_not_found"},
    )


@app.exception_handler(UserExists)
def user_exists(request: Request, exc: UserExists) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": f"The name {exc.name} is taken", "code": "user_exists"},
    )


@app.exception_handler(RoomNotFound)
def room_not_found(request: Request, exc: RoomNotFound) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"Room {exc.room_id} not found", "code": "room_not_found"},
    )


@app.exception_handler(MessageNotFound)
def message_not_found(request: Request, exc: MessageNotFound) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"Message {exc.message_id} not found", "code": "message_not_found"},
    )


@app.exception_handler(ChatFull)
def chat_full(request: Request, exc: ChatFull) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": f"Chat is full ({exc.limit} messages)", "code": "chat_full"},
    )


# Debug in the IDE, or: python -m app.main
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
