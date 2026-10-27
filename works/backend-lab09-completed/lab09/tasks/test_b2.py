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


def test_create_room():
    response = client.post("/rooms", json={"title": "general"})

    assert response.status_code == 201
    assert response.json()["title"] == "general"


def test_unknown_room():
    response = client.get("/rooms/99")

    assert response.status_code == 404
