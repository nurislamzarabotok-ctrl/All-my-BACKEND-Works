from fastapi.testclient import TestClient

from app.deps import get_storage
from app.main import app
from app.storage import Storage

client = TestClient(app)


def setup_function():
    store = Storage()
    app.dependency_overrides[get_storage] = lambda: store


def teardown_function():
    app.dependency_overrides.clear()


def test_message_from_another_room_returns_404():
    # arrange
    first_room = client.post("/rooms", json={"title": "general"})
    second_room = client.post("/rooms", json={"title": "homework"})
    created = client.post("/rooms/1/messages", json={"author": "Aida", "text": "hello"})
    assert first_room.status_code == 201
    assert second_room.status_code == 201
    assert created.status_code == 201

    # act
    wrong_room = client.get("/rooms/2/messages/1")
    own_room = client.get("/rooms/1/messages/1")

    # assert
    assert wrong_room.status_code == 404
    assert wrong_room.json()["code"] == "message_not_found"
    assert own_room.status_code == 200
    assert own_room.json()["id"] == 1
    assert own_room.json()["room_id"] == 1
