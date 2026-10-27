"""Check one review task.

    python check.py a1        a trace task: prints the real answers
    python check.py b1        a task you edit: runs its checks, PASS or FAIL
    python check.py all       every task you edit, with a total

Write your answer in ANSWERS.md first. Run the check after.
"""
import importlib
import json
import os
import subprocess
import sys
import tempfile

TRACE = ["a1", "a2", "a3", "a4", "a5", "r1"]
EDIT = ["b1", "b2", "c1", "c2", "d1", "d2", "r2", "r3"]


def load(name):
    try:
        return importlib.import_module(f"tasks.{name}")
    except Exception as error:                  # a syntax error in the student's file, for example
        print(f"  FAIL  tasks/{name}.py does not import: {type(error).__name__}: {error}")
        return None


def run_checks(name, checks) -> tuple[int, int]:
    passed = 0
    for text, test in checks:
        try:
            ok = bool(test())
        except Exception as error:
            ok = False
            text += f"   ({type(error).__name__}: {error})"
        print(f"  {'PASS' if ok else 'FAIL'}  {text}")
        passed += ok
    print(f"  {name}: {passed} of {len(checks)}")
    return passed, len(checks)


def pytest_file(path: str, expect: str) -> bool:
    result = subprocess.run([sys.executable, "-m", "pytest", path, "-q", "-p", "no:cacheprovider"],
                            capture_output=True, text=True)
    last = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else result.stderr.strip()
    print(f"        pytest says: {last}")
    return last.startswith(expect) and "failed" not in last and "error" not in last


def check_b1():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from pydantic import ValidationError

    m = load("b1")
    if m is None:
        return 0, 3

    def blank_is_422():
        try:
            m.MessageIn(author="Aida", text="   ")
        except ValidationError:
            return True
        return False

    def handler_answers():
        app = m.app

        @app.get("/rooms/{room_id}")
        def get_room(room_id: int):
            raise m.RoomNotFound(room_id)

        response = TestClient(app, raise_server_exceptions=False).get("/rooms/99")
        return response.status_code == 404 and response.json() == {"detail": "Room 99 not found", "code": "room_not_found"}

    return run_checks("b1", [
        ("text of spaces gives a ValidationError, so 422", blank_is_422),
        ("RoomNotFound is an exception", lambda: issubclass(m.RoomNotFound, Exception)),
        ("GET /rooms/99 gives 404 with detail and code", handler_answers),
    ])


def check_b2():
    return run_checks("b2", [("tasks/test_b2.py: 2 tests, both pass", lambda: pytest_file("tasks/test_b2.py", "2 passed"))])


def check_c1():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from app.main import room_not_found
    from app.errors import RoomNotFound
    from app.schemas import RoomIn

    m = load("c1")
    if m is None:
        return 0, 2
    app = FastAPI()
    app.include_router(m.router)
    app.add_exception_handler(RoomNotFound, room_not_found)
    client = TestClient(app, raise_server_exceptions=False)

    def room_is_found():
        m.store.add_room(RoomIn(title="general"))
        response = client.get("/rooms/1")
        return response.status_code == 200 and response.json()["title"] == "general"

    return run_checks("c1", [
        ("store, get_storage, StorageDep and the route exist", lambda: all(hasattr(m, x) for x in ["store", "get_storage", "StorageDep", "get_room"])),
        ("a room put into store is found by GET /rooms/1", room_is_found),
    ])


def check_c2():
    return run_checks("c2", [("tasks/test_c2.py: 1 test, it passes", lambda: pytest_file("tasks/test_c2.py", "1 passed"))])


def check_d1():
    from pydantic import ValidationError

    m = load("d1")
    if m is None:
        return 0, 4

    def refused(name):
        try:
            m.UserIn(name=name)
        except ValidationError:
            return True
        return False

    return run_checks("d1", [
        ('"  Aida " is stored as "Aida"', lambda: m.UserIn(name="  Aida ").name == "Aida"),
        ('"Ai da" is refused', lambda: refused("Ai da")),
        ('"A1" is refused', lambda: refused("A1")),
        ('"A" and a 33-letter name are refused', lambda: refused("A") and refused("A" * 33)),
    ])


def check_d2():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from app.deps import get_storage
    from app.storage import Storage

    m = load("d2")
    if m is None:
        return 0, 4
    app = FastAPI()
    app.include_router(m.router)
    store = Storage()
    app.dependency_overrides[get_storage] = lambda: store
    client = TestClient(app)
    for title in ["general", "homework", "Big games"]:
        client.post("/rooms", json={"title": title})

    def titles(params):
        return [room["title"] for room in client.get("/rooms", params=params).json()]

    return run_checks("d2", [
        ("GET /rooms gives all three", lambda: titles({}) == ["general", "homework", "Big games"]),
        ("?q=ge gives general", lambda: titles({"q": "ge"}) == ["general"]),
        ("?q=GAME gives Big games: case does not matter", lambda: titles({"q": "GAME"}) == ["Big games"]),
        ("?q= (empty) and a 51-letter q give 422", lambda: client.get("/rooms?q=").status_code == 422
         and client.get("/rooms", params={"q": "x" * 51}).status_code == 422),
    ])


def check_r2():
    from app.models import Message

    m = load("r2")
    if m is None:
        return 0, 2
    path = os.path.join(tempfile.mkdtemp(), "room.txt")
    messages = [Message(id=1, room_id=1, author="Aida", text="hello"),
                Message(id=4, room_id=1, author="Тимур", text="привет")]

    def content():
        m.save_room(path, messages)
        with open(path, encoding="utf-8") as f:
            return f.read()

    def twice():
        m.save_room(path, messages)
        m.save_room(path, messages[:1])
        with open(path, encoding="utf-8") as f:
            return f.read() == "#1 Aida: hello\n"

    return run_checks("r2", [
        ("the file has one line per message, Cyrillic readable", lambda: content() == "#1 Aida: hello\n#4 Тимур: привет\n"),
        ("a second call replaces the file", twice),
    ])


def check_r3():
    m = load("r3")
    if m is None:
        return 0, 2
    folder = tempfile.mkdtemp()
    data = {"monday.json": [{"id": 1, "room_id": 1}, {"id": 2, "room_id": 2}, {"id": 3, "room_id": 1}],
            "tuesday.json": [{"id": 4, "room_id": 1}]}
    for name, rows in data.items():
        with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
            json.dump(rows, f)
    with open(os.path.join(folder, "notes.txt"), "w", encoding="utf-8") as f:
        f.write("not json")

    return run_checks("r3", [
        ("monday.json, tuesday.json, notes.txt give {1: 3, 2: 1}", lambda: m.count_by_room(folder) == {1: 3, 2: 1}),
        ("an empty folder gives {}", lambda: m.count_by_room(tempfile.mkdtemp()) == {}),
    ])


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        return
    name = sys.argv[1].lower()
    if name in TRACE:
        print(f"{name}: the real answers\n")
        load(name).check()
    elif name in EDIT:
        globals()[f"check_{name}"]()
    elif name == "all":
        got = total = 0
        for task in EDIT:
            print(task)
            p, n = globals()[f"check_{task}"]()
            got, total = got + p, total + n
            print()
        print(f"All tasks you edit: {got} of {total} checks pass")
    else:
        print(f"No task {name!r}.", __doc__)


if __name__ == "__main__":
    main()
