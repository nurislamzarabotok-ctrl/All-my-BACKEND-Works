# Report, lesson 26

**Name:** Нурислам Ерланулы  
**Group:** ____________________  
**Date:** 25.10.2026

## Что работает

- [x] Баг найден и устранен.
- [x] TODO 1: текст только из пробелов выдает 422, пробелы по краям удаляются.
- [x] TODO 2: неизвестный ключ в PATCH выдает 422.
- [x] TODO 3: явно переданный `null` в PATCH выдает 422.
- [x] TODO 4 и 5: 404 с `"code": "message_not_found"`.
- [x] TODO 6: 409 с `"code": "chat_full"`.
- [x] Bruno на перезапущенном сервере: 13 of 13, assertions: 24 of 24.
- [x] Дополнительное задание: пробельный текст в PATCH выдает 422, обычный текст обрезается по краям.

## 1. Трейсбэк

До изменения файлов на исходном сервере выполнен `DELETE /messages/99`.
Последние строки ошибки (номера строк относятся к исходным файлам):

```text
  File "/data/lab06-venv/lib64/python3.13/site-packages/fastapi/telemetry/_api.py", line 244, in _run_sync_endpoint
    return function(**arguments)
  File "/vercel/sandbox/data/lab06-work/backend-lab06-nurislamzarabotok-ctrl-main/main.py", line 43, in delete_message  <- mine
    store.delete(message_id)
    ~~~~~~~~~~~~^^^^^^^^^^^^
  File "/vercel/sandbox/data/lab06-work/backend-lab06-nurislamzarabotok-ctrl-main/storage.py", line 36, in delete  <- mine
    self.messages.remove(self.get(message_id))
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
ValueError: list.remove(x): x not in list
```

- Последняя строка значит, что `remove()` пытается удалить элемент, которого нет в списке.
- Сначала нужно посмотреть `storage.py`, строку 36. Метод `get(99)` возвращает `None`, затем выполняется `self.messages.remove(None)`.
- Клиент получает 500 Internal Server Error.
- Исправление: в `Storage.get()` после цикла выбрасывается `MessageNotFound(message_id)`. Обработчик в `main.py` возвращает 404 и два поля: `detail`, `code`.

## 2. Баг

Запрос `02 Create second message` ожидает `id=2`, но второе сообщение получало `id=1`.

Остановка выполнена в `Storage.add()`, `storage.py`, строка 26 исходного файла, перед присваиванием `self.next_id = len(self.messages)`. Использован консольный отладчик `python -m pdb`: точка останова задана командой `b storage.py:26`. В исходный код `breakpoint()` не добавлялся.

Команды и полученные значения при первом добавлении:

```text
(Pdb) p message.id
1
(Pdb) p self.next_id
1
(Pdb) p len(self.messages)
1
(Pdb) n
(Pdb) p self.next_id
1
```

После `c`, при втором добавлении, на той же строке:

```text
(Pdb) p message.id
1
(Pdb) p self.next_id
1
(Pdb) p [m.id for m in self.messages]
[1, 1]
```

Ошибка была в строке:

```python
self.next_id = len(self.messages)
```

После первого добавления длина списка равна 1, поэтому следующий ID снова становится 1. Кроме того, длина списка уменьшается при удалении, поэтому она не подходит для счетчика ID.

Исправление:

```python
self.next_id += 1
```

Теперь ID растут независимо от удаления сообщений. В коллекции после удаления сообщения с ID 1 следующие новые сообщения получают ID 3 и 4.

## 3. Где застряли

Отдельной проверки потребовало различие между отсутствующим полем и `null` в PATCH. Пустой объект `{}` разрешен, но `{"text": null}` и `{"pinned": null}` должны возвращать 422.

Валидатор с `mode="before"` отклоняет явно переданный `None`. Для пропущенных полей он не запускается. Затем валидатор `text` удаляет пробелы и проверяет, что строка не пустая. Поэтому `None` не попадает в `.strip()`.

В `main.py` оставлен `model_dump(exclude_unset=True)`: меняются только переданные поля.

## 4. Результат проверки

Проверка проведена через Bruno CLI 4.3.0 на заново запущенном сервере с пустым хранилищем. Коллекция и ее assertions не изменялись. При запуске адрес сервера переопределен на `http://127.0.0.1:8016`.

```text
bru run --env local --env-var baseUrl=http://127.0.0.1:8016
Requests:   13 (13 Passed)
Assertions: 24/24
Status:     PASS
```

Полный вывод и JSON-результат находятся в `checks/`. Дополнительно выполнено `python -m unittest -v`: 20 тестов прошли успешно. Проверены границы длины, пробельный текст, `null`, лишние поля, пустой PATCH, отсутствие тела у DELETE и ID после удаления.

## Ресурсы

- `README.md` — требования задания и правила API.
- `bruno/` — исходная коллекция запросов и проверок.
- `python -m pdb` — проверка счетчика ID в исходном коде.

## Перед сдачей

Нужно заполнить группу. В исходном ZIP не было каталога `.git`, поэтому история Git не восстановлена и требование о минимум 7 коммитах этим архивом не подтверждается. Коммиты и отправка изменений выполняются в исходном репозитории.
