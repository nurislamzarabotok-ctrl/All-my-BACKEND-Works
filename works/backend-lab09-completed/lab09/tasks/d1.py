from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class UserIn(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=32)]

    @field_validator("name", mode="before")
    @classmethod
    def clean_name(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if not value.isalpha():
                raise ValueError("Name must contain only letters")
        return value
