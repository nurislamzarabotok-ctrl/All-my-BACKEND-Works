from fastapi import APIRouter

from app.deps import StorageDep

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("")
def get_stats(store: StorageDep) -> dict:
    messages = store.get_all()
    pinned = sum(m.pinned for m in messages)
    return {
        "users": len(store.get_users()),
        "rooms": len(store.get_rooms()),
        "messages": len(messages),
        "pinned": pinned,
    }
