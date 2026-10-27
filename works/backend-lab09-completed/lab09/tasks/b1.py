from typing import Annotated

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator


class MessageIn(BaseModel):
    author: Annotated[str, Field(min_length=2, max_length=32)]
    text: Annotated[str, Field(min_length=1, max_length=500)]

    @field_validator("text")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text cannot be only spaces")
        return v.strip()


class RoomNotFound(Exception):
    def __init__(self, room_id: int) -> None:
        self.room_id = room_id


app = FastAPI()


@app.exception_handler(RoomNotFound)
def room_not_found(request: Request, exc: RoomNotFound) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"Room {exc.room_id} not found", "code": "room_not_found"},
    )
