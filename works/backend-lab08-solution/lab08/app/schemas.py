from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserIn(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=32)]


class RoomIn(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=50)]

    @field_validator("title")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title cannot be only spaces")
        return v.strip()


class MessageIn(BaseModel):
    author: Annotated[str, Field(min_length=2, max_length=32)]
    text: Annotated[str, Field(min_length=1, max_length=500)]

    @field_validator("text")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text cannot be only spaces")
        return v.strip()


class MessagePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: Annotated[str, Field(min_length=1, max_length=500)] | None = None
    pinned: bool | None = None

    @field_validator("text", "pinned")
    @classmethod
    def not_null(cls, v):
        if v is None:
            raise ValueError("may be left out, but not null")
        return v
