"""The chat's data in SQLite, from Python. Every value goes in through ?."""
import sqlite3


def connect(path: str = "chat.db") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def add_user(conn: sqlite3.Connection, name: str) -> int:
    cursor = conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    return cursor.lastrowid


def add_message(conn: sqlite3.Connection, room_id: int, user_id: int, text: str) -> int:
    cursor = conn.execute(
        "INSERT INTO messages (room_id, user_id, text) VALUES (?, ?, ?)",
        (room_id, user_id, text),
    )
    conn.commit()
    return cursor.lastrowid


def find_user(conn: sqlite3.Connection, name: str) -> tuple | None:
    return conn.execute("SELECT id, name FROM users WHERE name = ?", (name,)).fetchone()


def find_messages(
    conn: sqlite3.Connection,
    room_id: int,
    user_id: int | None = None,
    order: str = "asc",
    limit: int = 10,
    offset: int = 0,
) -> list[tuple]:
    sql = "SELECT id, user_id, text FROM messages WHERE room_id = ?"
    values = [room_id]
    if user_id is not None:
        sql += " AND user_id = ?"
        values.append(user_id)
    if order == "desc":
        sql += " ORDER BY id DESC"
    else:
        sql += " ORDER BY id"
    sql += " LIMIT ? OFFSET ?"
    values.extend([limit, offset])
    return conn.execute(sql, values).fetchall()
