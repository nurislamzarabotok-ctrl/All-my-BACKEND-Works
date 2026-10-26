from errors import MessageNotFound, ChatFull
from models import Message
from schemas import MessageIn

MAX_MESSAGES = 3


class Storage:
    def __init__(self) -> None:
        self.messages: list[Message] = []
        self.next_id = 1

    def get_all(self) -> list[Message]:
        return self.messages

    def get(self, message_id: int) -> Message:
        for message in self.messages:
            if message.id == message_id:
                return message
        raise MessageNotFound(message_id)

    def add(self, data: MessageIn) -> Message:
        if len(self.messages) >= MAX_MESSAGES:
            raise ChatFull(MAX_MESSAGES)

        message = Message(
            id=self.next_id,
            author=data.author,
            text=data.text,
        )
        self.messages.append(message)
        self.next_id += 1
        return message

    def update(self, message_id: int, changes: dict) -> Message:
        message = self.get(message_id)
        for field, value in changes.items():
            setattr(message, field, value)
        return message

    def delete(self, message_id: int) -> None:
        self.messages.remove(self.get(message_id))
