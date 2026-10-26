class MessageNotFound(Exception):
    def __init__(self, message_id: int):
        self.message_id = message_id
        super().__init__(f"Message {message_id} not found")


class ChatFull(Exception):
    def __init__(self, limit: int):
        self.limit = limit
        super().__init__(f"Chat is full ({limit} messages)")
