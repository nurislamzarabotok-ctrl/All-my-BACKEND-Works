# A5 · Query parameters inside a room. Run: python check.py a5
from fastapi.testclient import TestClient

from app.main import app


def check() -> None:
    client = TestClient(app)
    client.post("/rooms", json={"title": "general"})
    client.post("/rooms", json={"title": "homework"})
    for room, author, text in [(1, "Aida", "hello everyone"), (1, "Timur", "on my way"),
                               (2, "Aida", "lab 07 is done"), (1, "Aida", "where is the meeting?"),
                               (1, "Dana", "Room 204, see you there")]:
        client.post(f"/rooms/{room}/messages", json={"author": author, "text": text})
    for name, url in [("a", "/rooms/1/messages?author=Aida&order=desc"),
                      ("b", "/rooms/1/messages?limit=2&offset=2"),
                      ("c", "/rooms/2/messages?limit=1&offset=1"),
                      ("d", "/rooms/1/messages/3"),
                      ("e", "/rooms/1/messages?limit=100")]:
        response = client.get(url)
        body = response.json()
        answer = [m["id"] for m in body] if isinstance(body, list) else body
        if response.status_code == 422:
            answer = body["detail"][0]["msg"]
        print(f"({name}) GET {url:44} {response.status_code}  {answer}")
