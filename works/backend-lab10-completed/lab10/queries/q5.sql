-- Q5. Every pinned message, in any room: id, room_id and text, old first.

SELECT id, room_id, text FROM messages WHERE pinned = 1 ORDER BY id;
