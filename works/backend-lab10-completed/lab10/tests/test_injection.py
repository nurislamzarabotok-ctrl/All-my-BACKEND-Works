import sqlite3

import pytest

from chat_db import add_user, find_user
from injection import find_user_unsafe
from tests.db import make_db

TRICK = "x' OR '1'='1"


def test_unsafe_version_returns_every_user():
    # This is the attack: one name, and the WHERE is true for every row.
    assert len(find_user_unsafe(make_db(), TRICK)) == 3


def test_safe_version_finds_nobody():
    assert find_user(make_db(), TRICK) is None


def test_unsafe_version_breaks_on_a_real_name():
    conn = make_db()
    add_user(conn, "O'Brien")

    with pytest.raises(sqlite3.OperationalError):
        find_user_unsafe(conn, "O'Brien")


def test_safe_version_finds_a_real_name():
    conn = make_db()
    add_user(conn, "O'Brien")

    assert find_user(conn, "O'Brien") == (4, "O'Brien")
