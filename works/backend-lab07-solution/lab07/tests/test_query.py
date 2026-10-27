from fastapi.testclient import TestClient

from app.deps import get_storage
from app.main import app
from app.storage import Storage

client = TestClient(app)

# The same six messages as requests 01 to 06 in Bruno. Messages 3 and 4 are pinned.
MESSAGES = [
    ("Aida", "hello everyone"),
    ("Timur", "on my way"),
    ("Aida", "where is the meeting?"),
    ("Dana", "Room 204, see you there"),
    ("Timur", "I am late, sorry"),
    ("Aida", "see you at the meeting"),
]


def setup_function():
    store = Storage()
    app.dependency_overrides[get_storage] = lambda: store
    for author, text in MESSAGES:
        client.post("/messages", json={"author": author, "text": text})
    client.patch("/messages/3", json={"pinned": True})
    client.patch("/messages/4", json={"pinned": True})


def teardown_function():
    app.dependency_overrides.clear()


def ids(response) -> list[int]:
    return [message["id"] for message in response.json()]


# Test 1 is ready. Read it, run it.
def test_filter_by_author():
    response = client.get("/messages", params={"author": "Aida"})

    assert response.status_code == 200
    assert ids(response) == [1, 3, 6]


# Page 2 with two messages per page: ids 3 and 4.
def test_second_page():
    response = client.get("/messages", params={"limit": 2, "offset": 2})

    assert response.status_code == 200
    assert ids(response) == [3, 4]


def test_limit_zero_returns_422():
    response = client.get("/messages", params={"limit": 0})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "limit"]
