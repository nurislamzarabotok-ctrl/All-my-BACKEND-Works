from dataclasses import dataclass


@dataclass
class Message:
    id: int
    author: str
    text: str
    pinned: bool = False
