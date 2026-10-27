# A4 · Routers and addresses. Run: python check.py a4
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

from app.deps import StorageDep
from app.schemas import RoomIn

rooms = APIRouter(prefix="/rooms", tags=["rooms"])
stats = APIRouter(prefix="/stats", tags=["stats"])


@rooms.get("/rooms/{room_id}")
def get_room(room_id: int, store: StorageDep):
    return store.get_room(room_id)


@stats.get("")
def get_stats(store: StorageDep):
    return {"rooms": len(store.get_rooms())}


app = FastAPI()
app.include_router(rooms)


def check() -> None:
    from app.deps import store
    store.add_room(RoomIn(title="general"))
    client = TestClient(app)
    for name, url in [("a", "/rooms/1"), ("b", "/rooms/rooms/1"), ("c", "/stats"), ("d", "/rooms")]:
        response = client.get(url)
        print(f"({name}) GET {url:16} {response.status_code}  {response.json()}")
