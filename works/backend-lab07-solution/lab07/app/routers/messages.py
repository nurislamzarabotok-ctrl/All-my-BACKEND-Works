from typing import Annotated, Literal

from fastapi import APIRouter, Query

from app.deps import StorageDep
from app.models import Message
from app.schemas import MessageIn, MessagePatch

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("", response_model=list[Message])
def list_messages(
    store: StorageDep,
    author: str | None = None,
    pinned: bool | None = None,
    q: Annotated[str | None, Query(min_length=2, max_length=50)] = None,
    order: Literal["asc", "desc"] = "asc",
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Message]:
    return store.find(author=author, pinned=pinned, q=q, order=order, limit=limit, offset=offset)


@router.post("", response_model=Message, status_code=201)
def create_message(payload: MessageIn, store: StorageDep) -> Message:
    return store.add(payload)


@router.get("/{message_id}", response_model=Message)
def get_message(message_id: int, store: StorageDep) -> Message:
    return store.get(message_id)


@router.patch("/{message_id}", response_model=Message)
def patch_message(message_id: int, payload: MessagePatch, store: StorageDep) -> Message:
    return store.update(message_id, payload.model_dump(exclude_unset=True))


@router.delete("/{message_id}", status_code=204)
def delete_message(message_id: int, store: StorageDep) -> None:
    store.delete(message_id)
