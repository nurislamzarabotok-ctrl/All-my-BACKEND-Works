class UserNotFound(Exception):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id


class UserExists(Exception):
    def __init__(self, name: str) -> None:
        self.name = name


class RoomNotFound(Exception):
    def __init__(self, room_id: int) -> None:
        self.room_id = room_id


class MessageNotFound(Exception):
    def __init__(self, message_id: int) -> None:
        self.message_id = message_id


class ChatFull(Exception):
    def __init__(self, limit: int) -> None:
        self.limit = limit
