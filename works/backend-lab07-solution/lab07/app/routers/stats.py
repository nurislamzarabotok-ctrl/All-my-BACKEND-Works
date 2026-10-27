from fastapi import APIRouter

from app.deps import StorageDep

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("")
def get_stats(store: StorageDep) -> dict:
    messages = store.get_all()
    pinned = sum(m.pinned for m in messages)
    return {"messages": len(messages), "pinned": pinned}
