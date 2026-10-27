from tests.db import make_db, query


def test_q1_rooms_by_title():
    assert query(make_db(), "queries/q1.sql") == [(1, "general"), (2, "homework")]


def test_q2_room_1():
    assert query(make_db(), "queries/q2.sql") == [
        (1, "hello everyone"),
        (2, "on my way"),
        (4, "where is the meeting?"),
        (5, "Room 204, see you there"),
    ]


def test_q3_aida_in_room_1_new_first():
    assert query(make_db(), "queries/q3.sql") == [(4, "where is the meeting?"), (1, "hello everyone")]


def test_q4_page_2():
    assert query(make_db(), "queries/q4.sql") == [(4, "where is the meeting?"), (5, "Room 204, see you there")]


def test_q5_pinned():
    assert query(make_db(), "queries/q5.sql") == [(4, 1, "where is the meeting?"), (5, 1, "Room 204, see you there")]


def test_q6_contains_lab():
    assert query(make_db(), "queries/q6.sql") == [(3, "lab 07 is done"), (6, "lab 08 is harder")]
