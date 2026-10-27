from fastapi.testclient import TestClient

from app.deps import get_storage
from app.main import app
from app.storage import MAX_MESSAGES, Storage

client = TestClient(app)


def setup_function():
    store = Storage()
    app.dependency_overrides[get_storage] = lambda: store


def teardown_function():
    app.dependency_overrides.clear()


def test_create_returns_201():
    response = client.post("/messages", json={"author": "Aida", "text": "  hello  "})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "author": "Aida", "text": "hello", "pinned": False}


def test_list_has_the_message():
    client.post("/messages", json={"author": "Aida", "text": "hello"})

    response = client.get("/messages")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_blank_text_returns_422():
    response = client.post("/messages", json={"author": "Aida", "text": "   "})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "text"]


def test_unknown_message_returns_404():
    response = client.get("/messages/99")

    assert response.status_code == 404
    assert response.json()["code"] == "message_not_found"


def test_pin_with_patch():
    client.post("/messages", json={"author": "Aida", "text": "hello"})

    response = client.patch("/messages/1", json={"pinned": True})

    assert response.status_code == 200
    assert response.json()["pinned"] is True


def test_delete_returns_204_then_404():
    client.post("/messages", json={"author": "Aida", "text": "hello"})

    first = client.delete("/messages/1")
    second = client.delete("/messages/1")

    assert first.status_code == 204
    assert first.content == b""
    assert second.status_code == 404


def test_full_chat_returns_409():
    for n in range(MAX_MESSAGES):
        created = client.post("/messages", json={"author": "Aida", "text": f"message {n}"})
        assert created.status_code == 201

    response = client.post("/messages", json={"author": "Aida", "text": "one more"})

    assert response.status_code == 409
    assert response.json()["code"] == "chat_full"
