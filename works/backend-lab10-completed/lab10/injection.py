"""Two ways to look up a user by name. Run it: python injection.py"""
import sqlite3

from chat_db import connect, find_user


def find_user_unsafe(conn: sqlite3.Connection, name: str) -> list[tuple]:
    # The name is glued into the SQL text with an f-string. Never do this.
    return conn.execute(f"SELECT id, name FROM users WHERE name = '{name}'").fetchall()


if __name__ == "__main__":
    conn = connect()
    for name in ["Aida", "Nobody", "x' OR '1'='1"]:
        print(f"{name!r:18} unsafe: {find_user_unsafe(conn, name)}")
        print(f"{'':18} safe:   {find_user(conn, name)}")
