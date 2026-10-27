# Lab 07: Query parameters in the chat

Today the teacher is away, and you work on your own. The chat API in this repository is where lessons 25 and 26 ended: the `app` package with the `messages` and `stats` routers, `deps.py`, and 9 tests.

Right now `GET /messages` returns every message at once. That is fine for 3 messages. A real chat has thousands. Today the client gets to ask for **only some** messages, and for **one page** of them:

```
GET /messages?author=Aida&q=meeting&order=desc&limit=10&offset=0
```

**Before you start:** read the lesson 27 deck, `backend-27-query-parameters` (PDF in the group chat), up to the slide "Practice". It takes about 20 minutes. Every pattern you need is on its slides. The deck uses `author` and `limit` as examples, and here you write all six parameters.

If you are stuck for more than five minutes:

1. Read [Troubleshooting](#troubleshooting).
2. Open the deck slide that the milestone names.
3. Ask your neighbour.
4. Write down where you stopped in `REPORT.md`, and go on.

**In class: M1 to M4.** M5 (tests) and the exit task go into `REPORT.md`, and anything you did not finish is homework.

## Run it

macOS / Linux:

```bash
git clone https://github.com/kilc-po25/backend-lab07-YOUR-USERNAME.git
cd backend-lab07-YOUR-USERNAME
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app/main.py
```

Windows PowerShell:

```powershell
git clone https://github.com/kilc-po25/backend-lab07-YOUR-USERNAME.git
cd backend-lab07-YOUR-USERNAME
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev app/main.py
```

Run every command from the project folder, the one with `app/` and `tests/` in it.

The Bruno collection in `bruno/` has 25 requests. Open the folder as a collection, choose the environment `local`, and run it with the Runner. The messages live in memory, so **restart the server before every run** (Ctrl+C, then `fastapi dev app/main.py` again).

At the start, 4 of 25 requests pass and `pytest` shows `3 failed, 9 passed`.

## The contract

`GET /messages` takes six query parameters. All of them are optional.

| Parameter | Type and default | Does | Wrong value |
|---|---|---|---|
| `author` | text, none | only this author's messages, exact match | |
| `pinned` | `true` or `false`, none | only pinned, or only not pinned | `pinned=maybe` gives 422 |
| `q` | text of 2 to 50 characters, none | only messages whose text contains `q`. `SEE` finds "see" | `q=a` gives 422 |
| `order` | `asc` or `desc`, `asc` | `asc`: old first (id 1, 2, 3). `desc`: new first | `order=newest` gives 422 |
| `limit` | number from 1 to 50, `10` | at most this many messages | `limit=0`, `limit=51` give 422 |
| `offset` | number from 0, `0` | skip this many messages first | `offset=-1` gives 422 |

Parameters work together. The work always goes in this order: **filter, then sort, then cut out the page.** `?author=Aida&order=desc&limit=1` is Aida's newest message.

A parameter the API does not know, such as `?autor=Aida`, is ignored: the answer is 200 with every message. Request 25 checks exactly that, and it passes from the start.

## Where the code goes

| File | What you change |
|---|---|
| `app/storage.py` | `MAX_MESSAGES`, and the body of `find()` |
| `app/routers/messages.py` | the parameters of `list_messages` |
| `tests/test_messages.py` | the 409 test (M1) |
| `tests/test_query.py` | tests 2 and 3 (M5) |

`find()` already has all six parameters with their defaults. It does nothing yet: it returns every message. The route decides what the client may send, and `find()` does the filtering. The storage still does not import anything from FastAPI.

## M1: a bigger chat, author and pinned (deck part 1, 20 minutes)

**The chat grows.** In `storage.py`, change `MAX_MESSAGES = 3` to `MAX_MESSAGES = 100`. Run `pytest`: `test_fourth_message_returns_409` now fails, because the fourth message is accepted. Rewrite that test so it fills the chat up to the limit, whatever the limit is:

```python
from app.storage import MAX_MESSAGES, Storage


def test_full_chat_returns_409():
    for n in range(MAX_MESSAGES):
        client.post("/messages", json={"author": "Aida", "text": f"message {n}"})
    ...
```

**author.** In `routers/messages.py`, add the parameter next to `store`, and pass it on:

```python
def list_messages(store: StorageDep, author: str | None = None) -> list[Message]:
    return store.find(author=author)
```

In `find()`, keep only the messages of that author, when `author` is not `None`. A list comprehension does it in one line.

**pinned.** The same pattern, with the type `bool | None`. FastAPI turns the text `true` from the address into the Python value `True`.

- [ ] `/docs` shows `author` and `pinned` under **Parameters** for `GET /messages`
- [ ] `http://127.0.0.1:8000/messages?pinned=maybe` answers 422 by itself. Read `loc`
- [ ] Bruno, fresh server: **13 of 25**
- [ ] `pytest`: the 409 test passes again

Commit: `git add . && git commit -m "M1: author and pinned"`

## M2: search with q (deck part 1, 15 minutes)

`q` is text like `author`, with two limits: 2 to 50 characters. Limits on a query parameter go into `Query(...)`, the same way as `Field(...)` in a schema:

```python
from typing import Annotated

from fastapi import Query

    limit: Annotated[int, Query(ge=1, le=50)] = 10      # the deck's example
```

Write `q` with `min_length` and `max_length`, and a default of `None`.

In `find()`: the search ignores case. Compare `q.lower()` with `m.text.lower()`, and use `in`.

- [ ] `?q=meeting` gives messages 3 and 6. `?q=SEE` gives 4 and 6
- [ ] `?q=a` answers 422
- [ ] Bruno, fresh server: **17 of 25**

Commit.

## M3: order (deck part 2, 10 minutes)

`order` may only be `asc` or `desc`. Any other word is a client mistake, so it must give 422. `Literal` says that in the type:

```python
from typing import Annotated, Literal

    order: Literal["asc", "desc"] = "asc"
```

In `find()`, sort the result by id with `sorted(result, key=..., reverse=...)`. The deck shows the line. `reverse` is `True` only when `order == "desc"`.

- [ ] `?order=desc` starts with message 6
- [ ] `?order=newest` answers 422, and the error lists the allowed values
- [ ] Bruno, fresh server: **19 of 25**

Commit.

## M4: one page with limit and offset (deck part 2, 15 minutes)

`limit` is a number from 1 to 50, default 10. `offset` is a number from 0, default 0. Both use `Query(...)` with `ge` and `le`.

The last line of `find()` cuts out the page with a slice. With 6 messages and `limit=2`:

| Page | offset | ids |
|---|---|---|
| 1 | 0 | 1, 2 |
| 2 | 2 | 3, 4 |
| 3 | 4 | 5, 6 |
| 4 | 6 | nothing: `[]`, still 200 |

- [ ] Without any parameters, the chat shows at most 10 messages
- [ ] `?limit=2&offset=2` gives 3 and 4
- [ ] `?limit=0`, `?limit=51`, `?offset=-1` answer 422
- [ ] Bruno, fresh server: **25 of 25**. Run it a second time after a restart: still 25

Commit and push.

## M5: tests (deck part 2, homework if you run out of time)

`tests/test_query.py` makes the same six messages as Bruno requests 01 to 08 before every test, and pins 3 and 4.

- **Test 1** is ready. Read it and run it.
- **Test 2** has three `___`. Replace them.
- **Test 3** is yours: `limit=0` answers 422, and `loc` is `["query", "limit"]`. TestClient sends query parameters with `params=`, as on the deck.

- [ ] `pytest`: **12 passed**
- [ ] Break `find()` on purpose (for example, take out the slice) and run `pytest`: tests 2 and 3 tell you what broke. Put it back

Commit and push.

## Exit task

The last two slides of the deck are the exit task. Write your answers in `REPORT.md` **before** you run anything. Then check them with the server, and write down what you got wrong. Your first answers are graded, not the checked ones, so do not change them.

## Troubleshooting

| What you see | What it means |
|---|---|
| `GET /messages?author=Aida` still returns every message | The parameter is in the route but not passed on: `store.find(author=author)`. Or `find()` does not use it yet |
| `NameError: name 'Query' is not defined` | `from fastapi import Query` is missing. `Annotated` and `Literal` come from `typing` |
| `422` with `"type": "missing"` for a query parameter | The parameter has no default, so it became required. Add `= None` or the default from the contract |
| `TypeError: '<' not supported between instances of 'Message' and 'Message'` | `sorted(result)` without `key=`. Python does not know how to compare two messages |
| `?order=desc` gives the same order as `asc` | `reverse=order == "desc"` is missing, or `order` is not passed into `find()` |
| The second page repeats the first one | The slice uses `limit` twice: it must start at `offset` |
| Bruno 01 to 08 fail with 409 | `MAX_MESSAGES` is still 3. Or the server was not restarted |
| Bruno: almost everything after 08 fails | The server was not restarted, so the old messages are still in memory |
| `AttributeError: 'TestClient' object has no attribute '___'` | Test 2 still has a blank |

## How to hand in

1. One commit per milestone, with the milestone in the message.
2. Fill in [REPORT.md](REPORT.md).
3. Push and tag:

```bash
git add -A
git commit -m "lab 07: done"
git tag lab07
git push
git push --tags
```

The last commit before the deadline is graded. If you did not finish, write in `REPORT.md` where you stopped.
