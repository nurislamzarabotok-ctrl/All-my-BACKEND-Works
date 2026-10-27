# Lab 10: The chat in SQLite

You work on your own today. The chat from lab 08 keeps users, rooms and messages in Python lists, so every restart empties it. A JSON file (lesson 13) survives a restart, but it has to be read and written whole for every change, and nothing stops a message from pointing to room 99.

Today the same chat goes into a **database**: three tables in one file, `chat.db`. You write the tables, the rows and the queries in SQL, and then the same queries from Python. There is no FastAPI and no server today.

**Before you start:** read the lesson 30 deck, `backend-30-sql-sqlite` (PDF in the group chat), up to the slide "Practice". It takes about 25 minutes.

If you are stuck for more than five minutes:

1. Read [Troubleshooting](#troubleshooting).
2. Open the deck slide that the milestone names.
3. Ask your neighbour.
4. Write down where you stopped in `REPORT.md`, and go on.

**In class: M1 to M3.** M4, M5 and the exit task go into `REPORT.md`, and anything you did not finish is homework.

## Run it

SQLite is built into Python: `import sqlite3`, nothing to install. Only `pytest` comes from pip.

macOS / Linux:

```bash
git clone https://github.com/kilc-po25/backend-lab10-YOUR-USERNAME.git
cd backend-lab10-YOUR-USERNAME
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
git clone https://github.com/kilc-po25/backend-lab10-YOUR-USERNAME.git
cd backend-lab10-YOUR-USERNAME
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

`run_sql.py` runs one `.sql` file on `chat.db` and prints what every `SELECT` returns as a table:

```bash
python run_sql.py schema.sql
python run_sql.py seed.sql
python run_sql.py queries/q1.sql
```

`schema.sql` starts by dropping the tables, so running it again gives you an empty database. After that, run `seed.sql` once to fill it again.

`pytest` checks everything in a fresh database in memory. It does not touch `chat.db`. At the start, `27 failed, 2 passed`.

| File | Its job | Milestone |
|---|---|---|
| `schema.sql` | the three tables | M1 |
| `seed.sql` | the rows: 3 users, 2 rooms, 6 messages | M2 |
| `queries/q1.sql` to `q6.sql` | one `SELECT` each | M3 |
| `chat_db.py` | the same work from Python, with `?` | M4 |
| `injection.py` | why `?` and not an f-string | M5 |
| `run_sql.py` | runs a file and prints the rows | do not change |
| `tests/` | the checks | do not change |

## M1: the tables (deck part 1, 20 minutes)

`schema.sql` already has `users`:

```sql
CREATE TABLE users (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
```

- `INTEGER PRIMARY KEY`: every row gets its own number, 1, 2, 3, and SQLite counts it for you. That is what `next_id` did in the storage.
- `NOT NULL`: the name is required.
- `UNIQUE`: two users cannot have the same name. That is what `UserExists` did in lab 08.

Write `rooms` and `messages` under it. The comments in the file list the columns. A column that points to another table:

```sql
    room_id INTEGER NOT NULL REFERENCES rooms (id),
```

`REFERENCES rooms (id)` makes `room_id` a **foreign key**: a message for room 99 is refused when there is no room 99. A default value: `pinned INTEGER NOT NULL DEFAULT 0`. SQLite has no `true` and `false`: `pinned` is `0` or `1`.

Keep the order users, rooms, messages: a table that points to another one comes after it. SQLite would let you create `messages` first, but the first `INSERT` into it then stops with `no such table: main.rooms`.

```bash
python run_sql.py schema.sql
pytest tests/test_schema.py
```

- [ ] `OK: 6 statements from schema.sql`
- [ ] `pytest tests/test_schema.py`: **8 passed**

Commit: `git add . && git commit -m "M1: tables"`

## M2: the rows (deck part 1, 10 minutes)

`seed.sql` has the users, the rooms, and messages 1 and 2. Add messages 3 to 6, one `INSERT` each, in this order:

| id | room_id | user_id | text | pinned |
|---|---|---|---|---|
| 3 | 2 | 1 | lab 07 is done | 0 |
| 4 | 1 | 1 | where is the meeting? | 1 |
| 5 | 1 | 3 | Room 204, see you there | 1 |
| 6 | 2 | 2 | lab 08 is harder | 0 |

Do not write the `id`: SQLite gives it. Write `pinned` only where it is 1. Text goes in single quotes: `'on my way'`.

```bash
python run_sql.py schema.sql
python run_sql.py seed.sql
```

- [ ] `OK: 11 statements from seed.sql`
- [ ] Run `seed.sql` a second time: it stops at statement 1 with `UNIQUE constraint failed: users.name`. `UNIQUE` works. Run `schema.sql` and `seed.sql` again to start clean
- [ ] `pytest tests/test_seed.py`: **2 passed**

Then break it on purpose, and write in `REPORT.md` what SQLite said:

- [ ] Add `INSERT INTO messages (room_id, user_id, text) VALUES (99, 1, 'hi');` at the end and run the two files again. Take the line out
- [ ] Add `INSERT INTO rooms (title) VALUES (NULL);` and do the same. Take the line out

Commit.

## M3: the questions (deck parts 1 and 2, 25 minutes)

Each file `queries/q1.sql` to `q6.sql` has one question in a comment. Write one `SELECT` under it that answers it, with exactly the columns it asks for, in that order. Check each one on `chat.db` as you go:

```bash
python run_sql.py queries/q3.sql
```

| File | Needs |
|---|---|
| q1 | `ORDER BY` |
| q2 | `WHERE`, `ORDER BY` |
| q3 | `WHERE ... AND ...`, `ORDER BY ... DESC` |
| q4 | `LIMIT` and `OFFSET`: the same page as `?limit=2&offset=2` in lab 07 |
| q5 | `WHERE pinned = 1` |
| q6 | `LIKE` with `%`: the same as `?q=lab` in lab 07, see the deck |

- [ ] `pytest tests/test_queries.py`: **6 passed**

Commit and push. That is the end of the work in class.

## M4: SQL from Python (deck part 2, homework)

`chat_db.py` has `connect` and `add_user` ready:

```python
def add_user(conn: sqlite3.Connection, name: str) -> int:
    cursor = conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    return cursor.lastrowid
```

- Every value goes in through a `?` mark, and the values come as a tuple in the second argument. `(name,)` with the comma is a tuple of one.
- `commit()` saves the change. Without it, the row is gone when the connection closes.
- `cursor.lastrowid` is the id SQLite just gave.

Write the other three:

- `add_message(conn, room_id, user_id, text)`: three `?` marks.
- `find_user(conn, name)`: `fetchone()` gives one row as a tuple, or `None`.
- `find_messages(conn, room_id, user_id=None, order="asc", limit=10, offset=0)`: this is `find()` from lab 07, on the database. Build the SQL text step by step with `+=`, and a list of values next to it. The comments in the file give the four steps.

**`?` is only for values.** `ORDER BY id ?` with `"DESC"` as a value does not work. `DESC` is a word of SQL, not a value. Choose it in Python with an `if`, as the deck shows.

Check it in the Python shell too. `connect()` opens `chat.db`, so run `schema.sql` and `seed.sql` first if you changed them:

```python
>>> from chat_db import connect, find_messages
>>> conn = connect()
>>> find_messages(conn, 1, user_id=1, order="desc")
[(4, 1, 'where is the meeting?'), (1, 1, 'hello everyone')]
```

- [ ] `pytest tests/test_chat_db.py`: **9 passed**

Commit.

## M5: why ? (deck part 2, homework)

`injection.py` has a second way to find a user: the name is glued into the SQL with an f-string. Run it:

```bash
python injection.py
```

It asks for three names. Copy its output into `REPORT.md`, and answer the questions there.

- [ ] `pytest`: **29 passed**

Commit, push, tag (see below).

## Exit task

The last two slides of the deck are the exit task. Write your answers in `REPORT.md` **before** you run anything. Then check them on `chat.db`, and write down what you got wrong. Your first answers are graded, so do not change them.

## Troubleshooting

| What you see | What it means |
|---|---|
| `sqlite3.OperationalError: near ")": syntax error` | A comma after the last column, before `)` |
| `sqlite3.OperationalError: no such table: rooms` | `schema.sql` was not run, or it has no `rooms` yet |
| `OperationalError: no such table: main.rooms` on an `INSERT INTO messages` | `messages` points to `rooms`, and `rooms` does not exist |
| `sqlite3.OperationalError: table users already exists` | The `DROP TABLE` lines at the top were deleted |
| `IntegrityError: UNIQUE constraint failed: users.name` | `seed.sql` was run twice. Run `schema.sql`, then `seed.sql` |
| `IntegrityError: FOREIGN KEY constraint failed` | A message points to a room or a user that does not exist yet |
| A message for room 99 is accepted | `REFERENCES` is missing. Or you ran SQL without `PRAGMA foreign_keys = ON`: SQLite checks foreign keys only when this is on. `run_sql.py`, the tests and `connect()` turn it on |
| `"on my way"` in double quotes works | SQLite lets it pass, but in SQL double quotes are for names of tables and columns, and other databases refuse it. Text goes in single quotes |
| A test of q3 fails with the right rows in the wrong order | `ORDER BY id DESC` is missing, or `DESC` is on the wrong column |
| `ProgrammingError: Incorrect number of bindings supplied` | The number of `?` marks and the number of values are different. Or `(name)` without a comma: that is a string, not a tuple |
| `OperationalError: near "?": syntax error` | A `?` stands for a word of SQL: `ORDER BY id ?` with `"DESC"`. Only values may be `?` |
| `ORDER BY ?` with `"id DESC"` gives no error, but the order is always old first | The same mistake, without an error: SQLite sorts by the text `'id DESC'`, which is the same for every row |
| The row is there in Python, and gone after a restart | `conn.commit()` is missing |

## How to hand in

1. One commit per milestone, with the milestone in the message. `chat.db` is in `.gitignore`: the tests make their own database.
2. Fill in [REPORT.md](REPORT.md).
3. Push and tag:

```bash
git add -A
git commit -m "lab 10: done"
git tag lab10
git push
git push --tags
```

The last commit before the deadline is graded. If you did not finish, write in `REPORT.md` where you stopped.
