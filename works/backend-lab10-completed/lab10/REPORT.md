# Report, lab 10

**Name:** Нурислам Ерланулы  
**Group:** ____________________  
**Date:** 25.10.2026

## What works

- [x] M1: `schema.sql`, три таблицы.
- [x] M2: `seed.sql`, шесть сообщений.
- [x] M3: q1–q6.
- [x] M4: `chat_db.py`.
- [x] M5: запуск `injection.py`, ответы на вопросы.
- [x] `pytest`: 29 passed, 0 failed.

## Broken on purpose (M2)

Ошибочные INSERT проверены в отдельных временных копиях `seed.sql`. В итоговом файле их нет. Перед каждым опытом база создавалась заново.

- Сообщение для комнаты 99: `IntegrityError: FOREIGN KEY constraint failed`.
  Ограничение в `schema.sql`: `room_id INTEGER NOT NULL REFERENCES rooms (id)`.
- Комната с `title = NULL`: `IntegrityError: NOT NULL constraint failed: rooms.title`.
  Ограничение: `title TEXT NOT NULL`.
- Повторный запуск `seed.sql`: `IntegrityError: UNIQUE constraint failed: users.name`, ошибка на первом INSERT. Ограничение: `name TEXT NOT NULL UNIQUE`.

После проверки снова выполнены `schema.sql` и `seed.sql` без ошибочных строк.

```text
python run_sql.py schema.sql
OK: 6 statements from schema.sql
python run_sql.py seed.sql
OK: 11 statements from seed.sql
```

## The lists and the tables

В архиве Lab 09 папка `app/` содержит готовое приложение из Lab 08. Сопоставление сделано по этому исходнику.

| Job | Lab 08: where | Lab 10: what does it |
|---|---|---|
| giving the next id | `Storage.add_user`, `add_room`, `add`: счетчики `next_user_id`, `next_room_id`, `next_id` и увеличение на 1 | `id INTEGER PRIMARY KEY`: SQLite назначает ID, когда его не передали |
| refusing a second user named Aida | цикл в `Storage.add_user()`, при совпадении имени `raise UserExists(data.name)` | `name TEXT NOT NULL UNIQUE` |
| refusing a message for a room that does not exist | `Storage.add()` сначала вызывает `get_room(room_id)`, при отсутствии — `RoomNotFound` | `room_id INTEGER NOT NULL REFERENCES rooms (id)` и включенный `PRAGMA foreign_keys = ON` |
| `pinned` is false when not sent | поле `pinned: bool = False` в `Message` | `pinned INTEGER NOT NULL DEFAULT 0` |

`INTEGER PRIMARY KEY` не гарантирует, что удаленный максимальный ID никогда не будет использован снова. Это не то же самое, что счетчик, который только увеличивается, или `AUTOINCREMENT`.

## Why ? (M5)

Реальный вывод `python injection.py`:

```text
'Aida'             unsafe: [(1, 'Aida')]
                   safe:   (1, 'Aida')
'Nobody'           unsafe: []
                   safe:   None
"x' OR '1'='1"     unsafe: [(1, 'Aida'), (2, 'Timur'), (3, 'Dana')]
                   safe:   None
```

1. Для третьего имени f-строка составляет запрос:

```sql
SELECT id, name FROM users WHERE name = 'x' OR '1'='1'
```

Условие `'1'='1'` истинно для каждой строки, поэтому небезопасная функция возвращает всех пользователей. В безопасной функции вся строка считается значением имени, и такого пользователя нет.

2. Для настоящего имени `O'Brien` небезопасный SQL получается таким:

```sql
SELECT id, name FROM users WHERE name = 'O'Brien'
```

Апостроф закрывает строковый литерал раньше времени, и SQLite выдает `OperationalError`. Параметр `?` передает имя отдельно от текста SQL, поэтому безопасный поиск работает. При отдельной проверке получено `OperationalError: near "Brien": syntax error`, а безопасный поиск вернул `(4, "O'Brien")`.

3. `DESC` — часть синтаксиса SQL, а `?` обозначает значение. `ORDER BY id ?` — синтаксическая ошибка. В коде направление выбирается через `if`, а пользовательские значения передаются через `?`. `ORDER BY ?` сортировал бы по одной и той же константе, а не по указанному столбцу.

## Результаты проверок

```text
python -m pytest -q
29 passed
```

По группам: схема — 8 тестов, данные — 2, запросы — 6, функции Python — 9, SQL-инъекция — 4. Все прошли. `tests/`, `run_sql.py` и учебный небезопасный пример `injection.py` не изменялись.

Пример из Python также проверен:

```text
find_messages(conn, 1, user_id=1, order="desc")
[(4, 1, 'where is the meeting?'), (1, 1, 'hello everyone')]
```

Подробный вывод — `checks/pytest.txt`, `checks/sql-runs.txt`, `checks/injection.txt`.

## Exit task

В архиве нет последних двух слайдов `backend-30-sql-sqlite`, поэтому формулировки A–D неизвестны. Первоначальные ответы и результаты для отсутствующих вопросов не придуманы.

| Task | My answer | Checked: right or wrong, and why |
|---|---|---|
| A (a) | Нужна формулировка со слайда | Не проверено |
| A (b) | Нужна формулировка со слайда | Не проверено |
| A (c) | Нужна формулировка со слайда | Не проверено |
| A (d) | Нужна формулировка со слайда | Не проверено |
| B | Нужна формулировка со слайда | Не проверено |
| C | Нужна формулировка со слайда | Не проверено |

D: нужен текст задания со слайда.

## Where I got stuck

Важные места в решении: внешние ключи проверяются только при включенном `PRAGMA foreign_keys = ON`; после INSERT нужен `commit()`; ключевые слова SQL нельзя передавать через `?`.

Для завершения Exit task нужен PDF. Истории коммитов в исходном ZIP нет; push и тег `lab10` в GitHub пока не выполнены.

## Sources

- `README.md`, `schema.sql`, `seed.sql`, `chat_db.py`, `injection.py`, `tests/` из задания.
- `app/storage.py` и `app/models.py` из Lab 09 — готовый чат из Lab 08.
- Помощь в подготовке решения: [чат](https://app.notion.com/chat?t=404405e58ff1802e9be200a989a9c5a3).
