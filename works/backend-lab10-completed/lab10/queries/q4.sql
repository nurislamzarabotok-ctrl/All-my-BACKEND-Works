-- Q4. Page 2 of room 1, two messages per page: id and text.

SELECT id, text FROM messages WHERE room_id = 1 ORDER BY id LIMIT 2 OFFSET 2;
