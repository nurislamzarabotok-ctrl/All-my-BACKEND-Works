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


def test_create_user_returns_201():
    response = client.post("/users", json={"name": "Aida"})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "Aida"}


def test_same_name_returns_409():
    client.post("/users", json={"name": "Aida"})

    response = client.post("/users", json={"name": "Aida"})

    assert response.status_code == 409
    assert response.json()["code"] == "user_exists"


def test_unknown_user_returns_404():
    response = client.get("/users/99")

    assert response.status_code == 404
    assert response.json()["code"] == "user_not_found"
