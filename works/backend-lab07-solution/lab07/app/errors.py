class MessageNotFound(Exception):
    def __init__(self, message_id: int) -> None:
        self.message_id = message_id


class ChatFull(Exception):
    def __init__(self, limit: int) -> None:
        self.limit = limit
