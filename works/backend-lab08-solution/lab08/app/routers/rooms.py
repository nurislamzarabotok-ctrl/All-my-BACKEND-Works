from fastapi import APIRouter

from app.deps import StorageDep
from app.models import Room
from app.schemas import RoomIn

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("", response_model=list[Room])
def list_rooms(store: StorageDep) -> list[Room]:
    return store.get_rooms()


@router.post("", response_model=Room, status_code=201)
def create_room(payload: RoomIn, store: StorageDep) -> Room:
    return store.add_room(payload)


@router.get("/{room_id}", response_model=Room)
def get_room(room_id: int, store: StorageDep) -> Room:
    return store.get_room(room_id)
