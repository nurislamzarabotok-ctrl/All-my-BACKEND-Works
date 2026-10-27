from fastapi import APIRouter

from app.deps import StorageDep
from app.models import User
from app.schemas import UserIn

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[User])
def list_users(store: StorageDep) -> list[User]:
    return store.get_users()


@router.post("", response_model=User, status_code=201)
def create_user(payload: UserIn, store: StorageDep) -> User:
    return store.add_user(payload)


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, store: StorageDep) -> User:
    return store.get_user(user_id)
