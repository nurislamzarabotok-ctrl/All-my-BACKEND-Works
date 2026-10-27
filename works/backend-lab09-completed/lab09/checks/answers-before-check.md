# Answers, lab 09

**Name:** Нурислам Ерланулы  
**Group:** ____________________  
**Date:** 25.10.2026

Ответы ниже записаны по исходному коду до запуска проверок. Для точных подпунктов A3 и буквенного порядка C1/C2 нужен PDF `backend-29-review`: его в архиве нет. Код для C1/C2 приведен полностью, но соответствие строк буквам на слайдах не восстановлено.

## A1 · Optional, null, required (3)

| Model | `{}` | `{"text": null}` | `{"txt": "hi"}` |
|---|---|---|---|
| PatchA | OK | OK | 422 |
| PatchB | 422 | OK | 422 |
| PatchC | OK | 422 | 422 |

`str | None` разрешает `null`, но без значения по умолчанию поле остается обязательным. `extra="forbid"` запрещает неизвестный ключ `txt`.

Points: ожидается 3 / 3; подтвердить после проверки.

## A2 · Two validators on one field (4)

| | Status | text after |
|---|---|---|
| (a) | 200 | `hello`, `pinned=True` |
| (b) | 200 | `hi` |
| (c) | 500 | остается `hi`, обновления нет |
| (d) | 422 | остается `hi`, обновления нет |

При `text=None` первым запускается `not_blank`. Вызов `None.strip()` вызывает `AttributeError`, а не ошибку валидации. До `not_null` выполнение не доходит, клиент получает 500. Для пробелов выбрасывается `ValueError`, поэтому ответ 422. В (a) поле `text` не передано, его валидаторы не запускаются.

Points: ожидается 4 / 4; подтвердить после проверки.

## A3 · Read the traceback (4)

Точные вопросы (a)–(d) находятся только на слайде 7. Разбор исходника:

- Исключение: `IndexError: list index out of range`.
- Ошибка в `Storage.get()`, файл `tasks/a3.py`, строка `return self.messages[message_id]`.
- В списке одно сообщение. Его индекс 0, но ID равен 1. При запросе `/messages/1` обращение идет к индексу 1, которого нет. Клиент получает 500.
- `/messages/0` ошибочно возвращает 200 с сообщением ID 1: индекс списка не равен ID. Исправление: искать сообщение по `message.id`, а при отсутствии выбрасывать `MessageNotFound`, обрабатываемое как 404.

Points: ___ / 4 — нужны формулировки подпунктов со слайда.

## A4 · Routers and addresses (4)

| | Status | Body |
|---|---|---|
| (a) | 404 | `{"detail": "Not Found"}` |
| (b) | 200 | `{"id": 1, "title": "general"}` |
| (c) | 404 | `{"detail": "Not Found"}` |
| (d) | 404 | `{"detail": "Not Found"}` |

Префикс `/rooms` складывается с путем `/rooms/{room_id}`, поэтому реальный адрес — `/rooms/rooms/1`. Роутер `stats` не подключен через `include_router`, а маршрут для списка `/rooms` не объявлен.

Points: ожидается 4 / 4; подтвердить после проверки.

## A5 · Query parameters inside a room (5)

(a) 200, ID `[4, 1]`: сообщения Aida только в комнате 1, новые сначала.

(b) 200, ID `[4, 5]`: после фильтра по комнате порядок `[1, 2, 4, 5]`, первые два пропускаются.

(c) 200, `[]`: в комнате 2 одно сообщение; `offset=1` пропускает его.

(d) 404, `{"detail": "Message 3 not found", "code": "message_not_found"}`: сообщение 3 относится к комнате 2.

(e) 422: `limit` должен быть от 1 до 50, значение 100 не проходит валидацию.

Points: ожидается 5 / 5; подтвердить после проверки.

## B1 · Find the errors: schema and handler (3)

| Исходная строка | Исправление |
|---|---|
| `raise TypeError("text cannot be only spaces")` | `raise ValueError("text cannot be only spaces")` |
| `class RoomNotFound:` | `class RoomNotFound(Exception):` |
| `f"Room {exc.id} not found"` | `f"Room {exc.room_id} not found"` |

`ValueError` становится ошибкой валидации. Свое исключение должно наследовать `Exception`. В конструкторе сохранено поле `room_id`, а не `id`.

Points: ожидается 3 / 3; подтвердить после проверки.

## B2 · Find the errors: a test file (3)

| Исходная строка | Исправление |
|---|---|
| `app.dependency_overrides[get_storage] = Storage()` | `app.dependency_overrides[get_storage] = lambda: store` |
| `response.json["title"]` | `response.json()["title"]` |
| `def check_unknown_room():` | `def test_unknown_room():` |

Override должен быть вызываемой функцией. `json` — метод, его нужно вызвать. Pytest собирает функции с префиксом `test_`. Хранилище создается заново для каждого теста, override очищается после теста.

Points: ожидается 3 / 3; подтвердить после проверки.

## C1 · Lines in order: one storage (2)

Порядок по смыслу: один `store` на уровне модуля → `get_storage()` возвращает этот объект → `StorageDep` через `Depends` → декоратор маршрута → обработчик → `store.get_room(room_id)`. Лишней была бы строка, создающая новое хранилище на каждый вызов зависимости. Буквенные обозначения нужно сверить со слайдом 12.

```python
from typing import Annotated

from fastapi import APIRouter, Depends

from app.models import Room
from app.storage import Storage

router = APIRouter(prefix="/rooms", tags=["rooms"])
store = Storage()


def get_storage() -> Storage:
    return store


StorageDep = Annotated[Storage, Depends(get_storage)]


@router.get("/{room_id}", response_model=Room)
def get_room(room_id: int, store: StorageDep) -> Room:
    return store.get_room(room_id)
```

Points: ___ / 2 — код проверяется автоматически, буквенный порядок требует слайда.

## C2 · Lines in order: a test (2)

Рабочая последовательность: создать чистый `Storage` → заменить зависимость функцией → создать комнату → проверить 201 → получить комнату → проверить 200 и тело ответа. После теста очистить overrides. Точные предложенные строки и лишняя строка отсутствуют в архиве: нужен слайд 13.

```python
from fastapi.testclient import TestClient

from app.deps import get_storage
from app.main import app
from app.storage import Storage

client = TestClient(app)


def teardown_function():
    app.dependency_overrides.clear()


def test_create_and_get_room():
    store = Storage()
    app.dependency_overrides[get_storage] = lambda: store
    created = client.post("/rooms", json={"title": "general"})
    assert created.status_code == 201

    response = client.get("/rooms/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "general"}
```

Points: ___ / 2 — код проверяется автоматически, буквенный порядок требует слайда.

## D1 · UserIn (3)

Условия из `check.py`: убрать пробелы по краям, оставить только буквы, длина имени 2–32. Очистка выполняется до проверки длины.

```python
from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class UserIn(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=32)]

    @field_validator("name", mode="before")
    @classmethod
    def clean_name(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if not value.isalpha():
                raise ValueError("Name must contain only letters")
        return value
```

Points: ожидается 3 / 3; подтвердить после проверки.

## D2 · GET /rooms with q (3)

Без `q` возвращаются все комнаты. С `q` — поиск подстроки без учета регистра. Длина переданного `q` — от 1 до 50.

```python
from typing import Annotated

from fastapi import APIRouter, Query

from app.deps import StorageDep
from app.models import Room
from app.schemas import RoomIn

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("", response_model=Room, status_code=201)
def create_room(payload: RoomIn, store: StorageDep) -> Room:
    return store.add_room(payload)


@router.get("", response_model=list[Room])
def list_rooms(
    store: StorageDep,
    q: Annotated[str | None, Query(min_length=1, max_length=50)] = None,
) -> list[Room]:
    rooms = store.get_rooms()
    if q is not None:
        rooms = [room for room in rooms if q.lower() in room.title.lower()]
    return rooms
```

Points: ожидается 3 / 3; подтвердить после проверки.

## R1 · model_dump (3)

```text
{'text': 'fixed', 'pinned': None}
{'text': 'fixed'}
{}
```

`exclude_unset=True` исключает поля, которые не передали при создании модели. Это не то же самое, что исключать все `None`: явно переданное значение считалось бы заданным, но в этой модели явный `null` запрещен валидатором.

Points: ожидается 3 / 3; подтвердить после проверки.

## R2 · save_room (3)

```python
from app.models import Message


def save_room(path: str, messages: list[Message]) -> None:
    with open(path, "w", encoding="utf-8") as file:
        for message in messages:
            file.write(f"#{message.id} {message.author}: {message.text}\n")
```

Режим `w` заменяет содержимое, UTF-8 сохраняет кириллицу. Одна строка на сообщение, включая перевод строки после последнего.

Points: ожидается 3 / 3; подтвердить после проверки.

## R3 · count_by_room (4)

```python
import json
import os


def count_by_room(folder: str) -> dict[int, int]:
    counts = {}
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        if not name.endswith(".json") or not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as file:
            messages = json.load(file)
        for message in messages:
            room_id = message["room_id"]
            counts[room_id] = counts.get(room_id, 0) + 1
    return counts
```

Обрабатываются только обычные файлы с расширением `.json`. В каждом файле читается список сообщений, счетчик увеличивается по `room_id`. Для пустой папки результат `{}`.

Points: ожидается 4 / 4; подтвердить после проверки.

## Total

**Итоговая оценка: ___ / 46.** Это не сумма автоматических проверок: в `check.py` другая шкала. Окончательная самооценка A3/C1/C2 и общий балл требуют слайдов. Предварительно решены все задания, доступные по коду.

## Источники

- `README.md`, `check.py`, исходные файлы `app/` и `tasks/` из задания.
- Помощь в подготовке решения: [чат](https://app.notion.com/chat?t=404405e58ff1802e9be200a989a9c5a3).
