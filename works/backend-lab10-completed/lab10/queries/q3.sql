-- Q3. Aida's messages (user 1) in room 1: id and text, new first.

SELECT id, text FROM messages WHERE room_id = 1 AND user_id = 1 ORDER BY id DESC;
