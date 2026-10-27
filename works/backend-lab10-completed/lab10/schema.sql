-- The chat in three tables. Run it: python run_sql.py schema.sql

DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE rooms (
    id    INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);

CREATE TABLE messages (
    id      INTEGER PRIMARY KEY,
    room_id INTEGER NOT NULL REFERENCES rooms (id),
    user_id INTEGER NOT NULL REFERENCES users (id),
    text    TEXT NOT NULL,
    pinned  INTEGER NOT NULL DEFAULT 0
);
