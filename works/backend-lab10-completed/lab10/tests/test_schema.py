import sqlite3

import pytest

from tests.db import make_db


def test_three_tables():
    conn = make_db(seed=False)

    rows = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name").fetchall()

    assert rows == [("messages",), ("rooms",), ("users",)]


def test_user_name_is_unique():
    conn = make_db(seed=False)
    conn.execute("INSERT INTO users (name) VALUES ('Aida')")

    with pytest.raises(sqlite3.IntegrityError, match="UNIQUE"):
        conn.execute("INSERT INTO users (name) VALUES ('Aida')")


def test_user_name_is_required():
    conn = make_db(seed=False)

    with pytest.raises(sqlite3.IntegrityError, match="NOT NULL"):
        conn.execute("INSERT INTO users (name) VALUES (NULL)")


def test_room_title_is_required():
    conn = make_db(seed=False)

    with pytest.raises(sqlite3.IntegrityError, match="NOT NULL"):
        conn.execute("INSERT INTO rooms (title) VALUES (NULL)")


def test_message_needs_a_real_room():
    conn = make_db(seed=False)
    conn.execute("INSERT INTO users (name) VALUES ('Aida')")

    with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY"):
        conn.execute("INSERT INTO messages (room_id, user_id, text) VALUES (99, 1, 'hi')")


def test_message_needs_a_real_user():
    conn = make_db(seed=False)
    conn.execute("INSERT INTO rooms (title) VALUES ('general')")

    with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY"):
        conn.execute("INSERT INTO messages (room_id, user_id, text) VALUES (1, 99, 'hi')")


def test_message_text_is_required():
    conn = make_db(seed=False)
    conn.execute("INSERT INTO users (name) VALUES ('Aida')")
    conn.execute("INSERT INTO rooms (title) VALUES ('general')")

    with pytest.raises(sqlite3.IntegrityError, match="NOT NULL"):
        conn.execute("INSERT INTO messages (room_id, user_id, text) VALUES (1, 1, NULL)")


def test_pinned_is_0_by_default():
    conn = make_db(seed=False)
    conn.execute("INSERT INTO users (name) VALUES ('Aida')")
    conn.execute("INSERT INTO rooms (title) VALUES ('general')")
    conn.execute("INSERT INTO messages (room_id, user_id, text) VALUES (1, 1, 'hi')")

    row = conn.execute("SELECT id, pinned FROM messages").fetchone()

    assert row == (1, 0)
