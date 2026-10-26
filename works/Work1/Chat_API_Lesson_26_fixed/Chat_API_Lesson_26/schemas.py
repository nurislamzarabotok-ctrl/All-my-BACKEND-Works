from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, field_validator


class MessageIn(BaseModel):
    author: Annotated[str, Field(min_length=2, max_length=32)]
    text: Annotated[str, Field(min_length=1, max_length=500)]

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Text cannot be empty")
        return value


class MessagePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: Annotated[str, Field(min_length=1, max_length=500)] | None = None
    pinned: bool | None = None

    @field_validator("text", mode="before")
    @classmethod
    def clean_patch_text(cls, value):
        if value is None:
            raise ValueError("Text cannot be null")
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Text cannot be empty")
        return value

    @field_validator("pinned", mode="before")
    @classmethod
    def check_pinned(cls, value):
        if value is None:
            raise ValueError("Pinned cannot be null")
        return value
