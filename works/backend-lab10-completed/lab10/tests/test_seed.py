from tests.db import make_db


def count(conn, table: str) -> int:
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def test_how_many_rows():
    conn = make_db()

    assert count(conn, "users") == 3
    assert count(conn, "rooms") == 2
    assert count(conn, "messages") == 6


def test_all_six_messages():
    conn = make_db()

    rows = conn.execute("SELECT id, room_id, user_id, text, pinned FROM messages ORDER BY id").fetchall()

    assert rows == [
        (1, 1, 1, "hello everyone", 0),
        (2, 1, 2, "on my way", 0),
        (3, 2, 1, "lab 07 is done", 0),
        (4, 1, 1, "where is the meeting?", 1),
        (5, 1, 3, "Room 204, see you there", 1),
        (6, 2, 2, "lab 08 is harder", 0),
    ]
