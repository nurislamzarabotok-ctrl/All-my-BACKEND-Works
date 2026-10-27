import sqlite3

import pytest

from chat_db import add_message, add_user, find_messages, find_user
from tests.db import make_db


def test_add_user_returns_the_new_id():
    conn = make_db()

    new_id = add_user(conn, "Erlan")

    assert new_id == 4
    assert find_user(conn, "Erlan") == (4, "Erlan")


def test_add_user_twice_fails():
    conn = make_db()

    with pytest.raises(sqlite3.IntegrityError):
        add_user(conn, "Aida")


def test_find_user_unknown_is_none():
    assert find_user(make_db(), "Nobody") is None


def test_add_message():
    conn = make_db()

    new_id = add_message(conn, 2, 3, "me too")

    assert new_id == 7
    assert find_messages(conn, 2, order="desc", limit=1) == [(7, 3, "me too")]


def test_add_message_into_unknown_room_fails():
    with pytest.raises(sqlite3.IntegrityError):
        add_message(make_db(), 99, 1, "hello")


def test_find_messages_of_a_room():
    rows = find_messages(make_db(), 1)

    assert [row[0] for row in rows] == [1, 2, 4, 5]


def test_find_messages_of_one_user_new_first():
    rows = find_messages(make_db(), 1, user_id=1, order="desc")

    assert [row[0] for row in rows] == [4, 1]


def test_find_messages_page_2():
    rows = find_messages(make_db(), 1, limit=2, offset=2)

    assert [row[0] for row in rows] == [4, 5]


def test_text_with_a_quote_is_stored_as_it_is():
    conn = make_db()

    add_message(conn, 1, 2, "it's Timur's turn")

    assert find_messages(conn, 1, order="desc", limit=1)[0][2] == "it's Timur's turn"
