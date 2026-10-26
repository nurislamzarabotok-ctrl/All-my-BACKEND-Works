from typing import Annotated

from pydantic import BaseModel, Field

# TODO 1-3 need two more names from pydantic: ConfigDict and field_validator


class MessageIn(BaseModel):
    author: Annotated[str, Field(min_length=2, max_length=32)]
    text: Annotated[str, Field(min_length=1, max_length=500)]

    # TODO 1: a field_validator for text (lesson 23).
    #   A text of only spaces is refused with 422.
    #   The text is stored without the spaces at its ends: "  hello  " -> "hello".


class MessagePatch(BaseModel):
    # TODO 2: refuse fields the model does not have (lesson 23).
    #   {"txet": "hi"} must give 422, not 200.

    text: Annotated[str, Field(min_length=1, max_length=500)] | None = None
    pinned: bool | None = None

    # TODO 3: text and pinned may be left out, but not sent as null (lesson 23).
    #   {"text": null} must give 422.
