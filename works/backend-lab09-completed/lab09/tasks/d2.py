from typing import Annotated

from fastapi import APIRouter, Query

from app.deps import StorageDep
from app.models import Room
from app.schemas import RoomIn

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("", response_model=Room, status_code=201)
def create_room(payload: RoomIn, store: StorageDep) -> Room:
    return store.add_room(payload)


@router.get("", response_model=list[Room])
def list_rooms(
    store: StorageDep,
    q: Annotated[str | None, Query(min_length=1, max_length=50)] = None,
) -> list[Room]:
    rooms = store.get_rooms()
    if q is not None:
        rooms = [room for room in rooms if q.lower() in room.title.lower()]
    return rooms
