from typing import Annotated

from fastapi import Depends

from app.storage import Storage

store = Storage()


def get_storage() -> Storage:
    return store


StorageDep = Annotated[Storage, Depends(get_storage)]
