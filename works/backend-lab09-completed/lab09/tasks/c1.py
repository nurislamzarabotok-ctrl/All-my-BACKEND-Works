from typing import Annotated

from fastapi import APIRouter, Depends

from app.models import Room
from app.storage import Storage

router = APIRouter(prefix="/rooms", tags=["rooms"])
store = Storage()


def get_storage() -> Storage:
    return store


StorageDep = Annotated[Storage, Depends(get_storage)]


@router.get("/{room_id}", response_model=Room)
def get_room(room_id: int, store: StorageDep) -> Room:
    return store.get_room(room_id)
