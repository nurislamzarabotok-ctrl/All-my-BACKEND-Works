from fastapi.testclient import TestClient

from app.deps import get_storage
from app.main import app
from app.storage import MAX_MESSAGES, Storage

client = TestClient(app)


def setup_function():
    # Two rooms, four messages: 1, 2 and 4 in room 1 ("general"), 3 in room 2 ("homework").
    store = Storage()
    app.dependency_overrides[get_storage] = lambda: store
    client.post("/rooms", json={"title": "general"})
    client.post("/rooms", json={"title": "homework"})
    client.post("/rooms/1/messages", json={"author": "Aida", "text": "hello everyone"})
    client.post("/rooms/1/messages", json={"author": "Timur", "text": "on my way"})
    client.post("/rooms/2/messages", json={"author": "Aida", "text": "lab 07 is done"})
    client.post("/rooms/1/messages", json={"author": "Aida", "text": "where is the meeting?"})


def teardown_function():
    app.dependency_overrides.clear()


def ids(response) -> list[int]:
    return [message["id"] for message in response.json()]


def test_create_message_in_a_room():
    response = client.post("/rooms/2/messages", json={"author": "Dana", "text": "  me too  "})

    assert response.status_code == 201
    assert response.json() == {"id": 5, "room_id": 2, "author": "Dana", "text": "me too", "pinned": False}


def test_message_into_unknown_room_returns_404():
    response = client.post("/rooms/99/messages", json={"author": "Aida", "text": "hello"})

    assert response.status_code == 404
    assert response.json()["code"] == "room_not_found"


def test_list_shows_only_this_room():
    response = client.get("/rooms/1/messages")

    assert response.status_code == 200
    assert ids(response) == [1, 2, 4]


def test_list_of_unknown_room_returns_404():
    response = client.get("/rooms/99/messages")

    assert response.status_code == 404
    assert response.json()["code"] == "room_not_found"


def test_filter_and_order_inside_a_room():
    response = client.get("/rooms/1/messages", params={"author": "Aida", "order": "desc"})

    assert ids(response) == [4, 1]


def test_second_page_inside_a_room():
    response = client.get("/rooms/1/messages", params={"limit": 2, "offset": 2})

    assert ids(response) == [4]


def test_limit_zero_returns_422():
    response = client.get("/rooms/1/messages", params={"limit": 0})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "limit"]


def test_get_message_from_its_room():
    response = client.get("/rooms/2/messages/3")

    assert response.status_code == 200
    assert response.json()["text"] == "lab 07 is done"


def test_pin_message():
    response = client.patch("/rooms/1/messages/1", json={"pinned": True})

    assert response.status_code == 200
    assert response.json()["pinned"] is True


def test_delete_returns_204_then_404():
    first = client.delete("/rooms/2/messages/3")
    second = client.delete("/rooms/2/messages/3")

    assert first.status_code == 204
    assert second.status_code == 404
    assert second.json()["code"] == "message_not_found"


def test_full_room_returns_409():
    for n in range(MAX_MESSAGES - 1):           # room 2 already has one message
        client.post("/rooms/2/messages", json={"author": "Aida", "text": f"message {n}"})

    response = client.post("/rooms/2/messages", json={"author": "Aida", "text": "one more"})
    other_room = client.post("/rooms/1/messages", json={"author": "Aida", "text": "still fine"})

    assert response.status_code == 409
    assert response.json()["code"] == "chat_full"
    assert other_room.status_code == 201


def test_stats_counts_everything():
    client.post("/users", json={"name": "Aida"})
    client.patch("/rooms/1/messages/4", json={"pinned": True})

    response = client.get("/stats")

    assert response.json() == {"users": 1, "rooms": 2, "messages": 4, "pinned": 1}
