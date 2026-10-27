from fastapi.testclient import TestClient

from app.deps import get_storage
from app.main import app
from app.storage import Storage

client = TestClient(app)


def teardown_function():
    app.dependency_overrides.clear()


def test_create_and_get_room():
    store = Storage()
    app.dependency_overrides[get_storage] = lambda: store
    created = client.post("/rooms", json={"title": "general"})
    assert created.status_code == 201

    response = client.get("/rooms/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "general"}
