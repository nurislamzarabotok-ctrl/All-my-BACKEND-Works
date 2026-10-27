from app.schemas import MessageIn, RoomIn
from app.storage import Storage


def test_ids_go_up_across_rooms():
    # arrange
    store = Storage()
    store.add_room(RoomIn(title="general"))
    store.add_room(RoomIn(title="homework"))
    # act
    first = store.add(1, MessageIn(author="Aida", text="hello"))
    second = store.add(2, MessageIn(author="Timur", text="lab 07 is done"))
    # assert
    assert first.id == 1
    assert second.id == 2
    assert second.room_id == 2


def test_text_is_trimmed():
    data = MessageIn(author="Aida", text="  hello  ")

    assert data.text == "hello"
