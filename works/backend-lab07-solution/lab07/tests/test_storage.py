from app.schemas import MessageIn
from app.storage import Storage


def test_ids_go_up():
    # arrange
    store = Storage()
    # act
    first = store.add(MessageIn(author="Aida", text="hello"))
    second = store.add(MessageIn(author="Timur", text="on my way"))
    # assert
    assert first.id == 1
    assert second.id == 2


def test_text_is_trimmed():
    data = MessageIn(author="Aida", text="  hello  ")

    assert data.text == "hello"
