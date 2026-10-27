-- Q2. The messages of room 1: id and text, old first.

SELECT id, text FROM messages WHERE room_id = 1 ORDER BY id;
