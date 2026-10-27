# Lab 08: Users, rooms, and messages inside rooms

Today is a practice lesson, and you work on your own. There is no new deck: everything comes from lessons 25 to 27 (routers, `Depends`, tests, query parameters).

Until now the chat had one long list of messages. A real chat has **rooms**: "general", "homework", and so on, each with its own messages. Today the chat gets three routers:

| Router | Addresses | State |
|---|---|---|
| `users` | `/users`, `/users/{user_id}` | **ready**: read it, it is your model |
| `rooms` | `/rooms`, `/rooms/{room_id}` | you write it (TODO 1, 2) |
| `messages` | `/rooms/{room_id}/messages`, `/rooms/{room_id}/messages/{message_id}` | it moves inside the rooms (TODO 3, 4) |

The ready tests and the Bruno collection are the contract. When both are green, the lab is done. One test you write yourself (TODO 6).

If you are stuck for more than five minutes:

1. Read [Troubleshooting](#troubleshooting).
2. Look at how `users` does the same thing.
3. Ask your neighbour.
4. Write down where you stopped in `REPORT.md`, and go on.

## Run it

macOS / Linux:

```bash
git clone https://github.com/kilc-po25/backend-lab08-YOUR-USERNAME.git
cd backend-lab08-YOUR-USERNAME
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app/main.py
```

Windows PowerShell:

```powershell
git clone https://github.com/kilc-po25/backend-lab08-YOUR-USERNAME.git
cd backend-lab08-YOUR-USERNAME
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev app/main.py
```

Two ways to check, both from the project folder:

- `pytest`: 22 tests. At the start, `18 failed, 4 passed`.
- Bruno: open `bruno/` as a collection, environment `local`, **restart the server before every run**. 26 requests. At the start, 5 of 26 pass.

## The contract

| Request | Success | Errors |
|---|---|---|
| `POST /users` | 201, the user | 422; 409 `user_exists` when the name is taken |
| `GET /users` | 200, the list | |
| `GET /users/{user_id}` | 200, the user | 404 `user_not_found` |
| `POST /rooms` | 201, the room | 422 |
| `GET /rooms` | 200, the list | |
| `GET /rooms/{room_id}` | 200, the room | 404 `room_not_found` |
| `POST /rooms/{room_id}/messages` | 201, the message | 404 `room_not_found`, 422, 409 `chat_full` |
| `GET /rooms/{room_id}/messages` | 200, one page of this room's messages, with the six query parameters from lab 07 | 404 `room_not_found`, 422 |
| `GET /rooms/{room_id}/messages/{message_id}` | 200, the message | 404 `room_not_found`, 404 `message_not_found` |
| `PATCH /rooms/{room_id}/messages/{message_id}` | 200, the message | 404, 422 |
| `DELETE /rooms/{room_id}/messages/{message_id}` | 204, no body | 404 |
| `GET /stats` | 200, `{"users": 2, "rooms": 2, "messages": 3, "pinned": 1}` | |

The shapes:

```json
{"id": 1, "name": "Aida"}
{"id": 1, "title": "general"}
{"id": 3, "room_id": 2, "author": "Aida", "text": "lab 07 is done", "pinned": false}
```

The rules:

- A user's `name` is 2 to 32 characters, and two users cannot have the same name.
- A room's `title` is 1 to 50 characters, stored without spaces at the ends. Only spaces is refused.
- Message ids are counted across the whole chat, as before: message 3 may be in room 2 while 1, 2 and 4 are in room 1.
- **A message is found only inside its own room.** Message 3 lives in room 2, so `GET /rooms/1/messages/3` is 404 `message_not_found`, even though message 3 exists.
- `MAX_MESSAGES` (100) is the limit for **one room**. A full room does not stop the others.

`models.py` and `schemas.py` already have `User`, `Room`, `UserIn` and `RoomIn`. `errors.py` has `UserNotFound` and `UserExists`.

## Read first: the users router (10 minutes)

Open these and follow one request, `POST /users`, from the router to the storage and back:

- `app/routers/users.py`: three routes, each one line that calls the storage.
- `app/storage.py`, the part `# users`: `get_users`, `get_user`, `add_user`. `add_user` raises `UserExists` for a taken name.
- `app/main.py`: `include_router(users.router)` and two handlers.
- `tests/test_users.py`: three tests, all green already.

Rooms work the same way. Messages are where today's new part is.

## TODO 1: rooms in the storage (10 minutes)

- `errors.py`: `RoomNotFound`, which keeps the `room_id`.
- `storage.py`, the part `# rooms`: `get_rooms`, `get_room(room_id)` (raises `RoomNotFound`), `add_room(data)` (uses `self.next_room_id`). Copy the user methods and change the names. `add_room` does not check for a taken title.

## TODO 2: the rooms router (10 minutes)

- `routers/rooms.py`: the router with `prefix="/rooms"` and `tags=["rooms"]`, and three routes, like `users.py`.
- `main.py`: `app.include_router(rooms.router)`, and a handler for `RoomNotFound`: 404 with `"code": "room_not_found"`.

- [ ] `/docs` shows a **rooms** section
- [ ] `pytest tests/test_rooms.py`: 4 passed
- [ ] Bruno, fresh server: **10 of 26**

Commit: `git add . && git commit -m "TODO 1, 2: rooms"`

## TODO 3: messages belong to a room, in the storage (20 minutes)

**`models.py`:** `Message` gets a field `room_id: int`, after `id`.

**`storage.py`:** every message method gets `room_id` as its **first** parameter, after `self`:

| Method | Now |
|---|---|
| `add(room_id, data)` | checks the room with `self.get_room(room_id)`, counts the messages **of this room** for `MAX_MESSAGES`, and makes the `Message` with `room_id=room_id` |
| `find(room_id, author=..., ...)` | checks the room, starts from the messages of this room only, then the lab 07 filters, sort and page |
| `get(room_id, message_id)` | checks the room, then finds a message with this id **and** this room_id. Otherwise `MessageNotFound` |
| `update(room_id, message_id, changes)` | `self.get(room_id, message_id)`, then the same as before |
| `delete(room_id, message_id)` | `self.get(room_id, message_id)`, then the same as before |

Keep `get_all()`: it returns the messages of all rooms, for `/stats`.

`self.get_room(room_id)` at the start of a method is a check: you do not need the room it returns. If there is no such room, it raises `RoomNotFound`, the handler from TODO 2 turns it into 404, and the method stops there.

Check it in the Python shell, without the server (`python`, or `py` on Windows, in the project folder):

```python
>>> from app.storage import Storage
>>> from app.schemas import MessageIn, RoomIn
>>> store = Storage()
>>> store.add_room(RoomIn(title="general"))
Room(id=1, title='general')
>>> store.add(1, MessageIn(author="Aida", text="hello"))
Message(id=1, room_id=1, author='Aida', text='hello', pinned=False)
>>> store.add(2, MessageIn(author="Aida", text="hello"))      # RoomNotFound
>>> store.get(1, 1)
Message(id=1, room_id=1, author='Aida', text='hello', pinned=False)
```

- [ ] All four lines behave as shown
- [ ] `pytest tests/test_storage.py`: 2 passed

Commit.

## TODO 4: the messages router moves inside the rooms (20 minutes)

The prefix of a router may contain a path parameter:

```python
router = APIRouter(prefix="/rooms/{room_id}/messages", tags=["messages"])
```

Now **every** route in this file has `{room_id}` in its address, so every route function must take `room_id: int`, the same way it takes `message_id: int`:

```python
@router.get("/{message_id}", response_model=Message)
def get_message(room_id: int, message_id: int, store: StorageDep) -> Message:
    return store.get(room_id, message_id)
```

Do the same for the other four routes. `list_messages` keeps its six query parameters from lab 07, and gets `room_id` in front of them.

- [ ] `/docs` shows `room_id` as a **path** parameter on all five message routes
- [ ] `pytest tests/test_room_messages.py`: 11 passed, 1 failed (the stats test, which is TODO 5)
- [ ] Bruno, fresh server: **25 of 26**

Commit.

## TODO 5: stats for the whole chat (5 minutes)

`GET /stats` answers `{"users": ..., "rooms": ..., "messages": ..., "pinned": ...}`. The messages and the pins are counted across all rooms.

- [ ] Bruno, fresh server: **26 of 26**

## TODO 6: your own test (15 minutes)

In `tests/test_mine.py`, write `test_message_from_another_room_returns_404`:

- **arrange:** two rooms, and one message in room 1
- **act:** `GET /rooms/2/messages/1` and `GET /rooms/1/messages/1`
- **assert:** the first is 404 with `"code": "message_not_found"`, the second is 200

Then break `get` in the storage on purpose: check only the id and not the room. Run `pytest tests/test_mine.py`, and write in `REPORT.md` what it said. Put it back.

- [ ] `pytest`: **22 passed**

Commit, push, tag (see below).

## If you finish early

- `GET /rooms/{room_id}/stats`: the same counts for one room.
- `GET /users/{user_id}/messages`: every message of this user, in all rooms. The user is found by id, and the messages by `author == user.name`. Which rule in the contract makes this unreliable? Write it in `REPORT.md`.

## Troubleshooting

| What you see | What it means |
|---|---|
| `AttributeError: module 'app.routers.rooms' has no attribute 'router'` | `rooms.py` has no `router = APIRouter(...)` yet, or it has another name |
| `ImportError: cannot import name 'RoomNotFound' from 'app.errors'` | TODO 1 is not done, but the class is already imported somewhere |
| `GET /rooms/99` gives 500, and the console ends in `RoomNotFound` | The handler from TODO 2 is missing, or it is registered for another class |
| `GET /rooms/99` gives 404 with only `{"detail": "Not Found"}` | `include_router(rooms.router)` is missing, so the address does not exist at all |
| `TypeError: Message.__init__() missing 1 required positional argument: 'room_id'` | `add` still makes a `Message` without `room_id=room_id` |
| `TypeError: Storage.get() missing 1 required positional argument: 'message_id'` | A route still calls `store.get(message_id)`. Pass `room_id` first |
| `/docs` shows `room_id` as a **query** parameter | The prefix still is `/messages`, so `{room_id}` is not in the address |
| `GET /rooms/1/messages/3` gives 200 | `get` checks only the id, not the room |
| `GET /rooms/2/messages` shows the messages of room 1 too | `find` starts from `self.messages` without keeping only `room_id` |
| Bruno 10 to 13 fail with 404 `room_not_found` | Requests 05 and 06 failed, or the server was not restarted |
| Bruno 01 or 05 fails with a wrong id | The server was not restarted |

## How to hand in

1. One commit per TODO, or per two, with the TODO numbers in the message.
2. Fill in [REPORT.md](REPORT.md).
3. Push and tag:

```bash
git add -A
git commit -m "lab 08: done"
git tag lab08
git push
git push --tags
```

The last commit before the deadline is graded. If you did not finish, write in `REPORT.md` where you stopped.
