-- The same chat as lab 08. Run it after schema.sql: python run_sql.py seed.sql

INSERT INTO users (name) VALUES ('Aida');
INSERT INTO users (name) VALUES ('Timur');
INSERT INTO users (name) VALUES ('Dana');

INSERT INTO rooms (title) VALUES ('general');
INSERT INTO rooms (title) VALUES ('homework');

INSERT INTO messages (room_id, user_id, text) VALUES (1, 1, 'hello everyone');
INSERT INTO messages (room_id, user_id, text) VALUES (1, 2, 'on my way');
INSERT INTO messages (room_id, user_id, text) VALUES (2, 1, 'lab 07 is done');
INSERT INTO messages (room_id, user_id, text, pinned) VALUES (1, 1, 'where is the meeting?', 1);
INSERT INTO messages (room_id, user_id, text, pinned) VALUES (1, 3, 'Room 204, see you there', 1);
INSERT INTO messages (room_id, user_id, text) VALUES (2, 2, 'lab 08 is harder');
