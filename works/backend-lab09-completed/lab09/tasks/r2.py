from app.models import Message


def save_room(path: str, messages: list[Message]) -> None:
    with open(path, "w", encoding="utf-8") as file:
        for message in messages:
            file.write(f"#{message.id} {message.author}: {message.text}\n")
