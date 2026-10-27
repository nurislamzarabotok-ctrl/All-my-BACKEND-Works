from app.errors import ChatFull, MessageNotFound, RoomNotFound, UserExists, UserNotFound
from app.models import Message, Room, User
from app.schemas import MessageIn, RoomIn, UserIn

MAX_MESSAGES = 100          # in one room


class Storage:
    def __init__(self) -> None:
        self.users: list[User] = []
        self.rooms: list[Room] = []
        self.messages: list[Message] = []
        self.next_user_id = 1
        self.next_room_id = 1
        self.next_id = 1

    # users

    def get_users(self) -> list[User]:
        return self.users

    def get_user(self, user_id: int) -> User:
        for user in self.users:
            if user.id == user_id:
                return user
        raise UserNotFound(user_id)

    def add_user(self, data: UserIn) -> User:
        for user in self.users:
            if user.name == data.name:
                raise UserExists(data.name)
        user = User(id=self.next_user_id, name=data.name)
        self.users.append(user)
        self.next_user_id += 1
        return user

    # rooms

    def get_rooms(self) -> list[Room]:
        return self.rooms

    def get_room(self, room_id: int) -> Room:
        for room in self.rooms:
            if room.id == room_id:
                return room
        raise RoomNotFound(room_id)

    def add_room(self, data: RoomIn) -> Room:
        room = Room(id=self.next_room_id, title=data.title)
        self.rooms.append(room)
        self.next_room_id += 1
        return room

    # messages, always inside one room

    def get_all(self) -> list[Message]:
        return self.messages                        # every room: for /stats

    def find(
        self,
        room_id: int,
        author: str | None = None,
        pinned: bool | None = None,
        q: str | None = None,
        order: str = "asc",
        limit: int = 10,
        offset: int = 0,
    ) -> list[Message]:
        self.get_room(room_id)                      # RoomNotFound if there is no such room
        result = [m for m in self.messages if m.room_id == room_id]
        if author is not None:
            result = [m for m in result if m.author == author]
        if pinned is not None:
            result = [m for m in result if m.pinned == pinned]
        if q is not None:
            result = [m for m in result if q.lower() in m.text.lower()]
        result = sorted(result, key=lambda m: m.id, reverse=order == "desc")
        return result[offset:offset + limit]

    def get(self, room_id: int, message_id: int) -> Message:
        self.get_room(room_id)
        for message in self.messages:
            if message.id == message_id and message.room_id == room_id:
                return message
        raise MessageNotFound(message_id)

    def add(self, room_id: int, data: MessageIn) -> Message:
        self.get_room(room_id)
        in_room = [m for m in self.messages if m.room_id == room_id]
        if len(in_room) >= MAX_MESSAGES:
            raise ChatFull(MAX_MESSAGES)
        message = Message(id=self.next_id, room_id=room_id, author=data.author, text=data.text)
        self.messages.append(message)
        self.next_id += 1
        return message

    def update(self, room_id: int, message_id: int, changes: dict) -> Message:
        message = self.get(room_id, message_id)
        for field, value in changes.items():
            setattr(message, field, value)
        return message

    def delete(self, room_id: int, message_id: int) -> None:
        self.messages.remove(self.get(room_id, message_id))
