-- Q6. The messages whose text contains "lab": id and text, old first.

SELECT id, text FROM messages WHERE text LIKE '%lab%' ORDER BY id;
