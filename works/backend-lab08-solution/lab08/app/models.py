from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str


@dataclass
class Room:
    id: int
    title: str


@dataclass
class Message:
    id: int
    room_id: int
    author: str
    text: str
    pinned: bool = False
