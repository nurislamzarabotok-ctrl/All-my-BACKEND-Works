import sqlite3


def run_file(conn: sqlite3.Connection, path: str) -> None:
    with open(path, encoding="utf-8") as f:
        conn.executescript(f.read())


def make_db(seed: bool = True) -> sqlite3.Connection:
    """A fresh chat in memory: schema.sql, then seed.sql. chat.db is not touched."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    run_file(conn, "schema.sql")
    if seed:
        run_file(conn, "seed.sql")
    return conn


def query(conn: sqlite3.Connection, path: str) -> list[tuple]:
    with open(path, encoding="utf-8") as f:
        return conn.execute(f.read()).fetchall()
