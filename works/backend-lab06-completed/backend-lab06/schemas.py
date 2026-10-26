from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MessageIn(BaseModel):
    author: Annotated[str, Field(min_length=2, max_length=32)]
    text: Annotated[str, Field(min_length=1, max_length=500)]

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Text cannot be blank")
        return value


class MessagePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: Annotated[str, Field(min_length=1, max_length=500)] | None = None
    pinned: bool | None = None

    @field_validator("text", "pinned", mode="before")
    @classmethod
    def reject_null(cls, value: object) -> object:
        if value is None:
            raise ValueError("Field cannot be null")
        return value

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Text cannot be blank")
        return value
