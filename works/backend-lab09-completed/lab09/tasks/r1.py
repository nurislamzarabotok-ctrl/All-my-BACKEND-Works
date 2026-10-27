# R1 · model_dump, from control work 1. Run: python check.py r1
from app.schemas import MessagePatch


def check() -> None:
    p = MessagePatch(text="fixed")
    print(p.model_dump())
    print(p.model_dump(exclude_unset=True))
    print(MessagePatch().model_dump(exclude_unset=True))
