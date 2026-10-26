import unittest

from fastapi.testclient import TestClient

import main
from storage import Storage


class MessageTests(unittest.TestCase):
    def setUp(self):
        main.store = Storage()
        self.client = TestClient(main.app)

    def create(self, text="hello", author="Aida"):
        return self.client.post("/messages", json={"author": author, "text": text})

    def test_empty_list(self):
        response = self.client.get("/messages")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_create_trims_text(self):
        response = self.create("  hello  ")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "id": 1, "author": "Aida", "text": "hello", "pinned": False,
        })

    def test_create_rejects_blank_text(self):
        for text in ("", "   ", "\t\n"):
            with self.subTest(text=repr(text)):
                self.assertEqual(self.create(text).status_code, 422)
        self.assertEqual(self.client.get("/messages").json(), [])

    def test_create_length_limits(self):
        for author, text in (("A", "hello"), ("A" * 33, "hello"), ("Aida", "x" * 501)):
            with self.subTest(author=author, length=len(text)):
                self.assertEqual(self.create(text, author).status_code, 422)
        self.assertEqual(self.create("x", "AB").status_code, 201)
        self.assertEqual(self.create("x" * 500, "A" * 32).status_code, 201)

    def test_second_message_id(self):
        self.create()
        response = self.create("second", "Timur")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["id"], 2)
        self.assertEqual(self.client.get("/messages/2").json()["author"], "Timur")

    def test_ids_are_not_reused_after_delete(self):
        self.create()
        self.create()
        self.client.delete("/messages/1")
        self.assertEqual(self.create().json()["id"], 3)
        self.client.delete("/messages/3")
        self.assertEqual(self.create().json()["id"], 4)

    def test_chat_full(self):
        for _ in range(3):
            self.create()
        response = self.create()
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {
            "detail": "Chat is full (3 messages)", "code": "chat_full",
        })
        self.assertEqual(len(self.client.get("/messages").json()), 3)
        self.assertEqual(main.store.next_id, 4)

    def test_delete_frees_space(self):
        for _ in range(3):
            self.create()
        self.client.delete("/messages/2")
        response = self.create()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["id"], 4)

    def test_missing_message(self):
        for method in ("get", "patch", "delete"):
            with self.subTest(method=method):
                kwargs = {"json": {"text": "new"}} if method == "patch" else {}
                response = getattr(self.client, method)("/messages/99", **kwargs)
                self.assertEqual(response.status_code, 404)
                self.assertEqual(response.json(), {
                    "detail": "Message 99 not found", "code": "message_not_found",
                })

    def test_delete_has_no_body(self):
        self.create()
        response = self.client.delete("/messages/1")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertEqual(self.client.get("/messages").json(), [])

    def test_delete_again(self):
        self.create()
        self.client.delete("/messages/1")
        self.assertEqual(self.client.delete("/messages/1").status_code, 404)

    def test_empty_patch_does_not_change_message(self):
        original = self.create().json()
        response = self.client.patch("/messages/1", json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), original)

    def test_patch_pin_preserves_text(self):
        self.create()
        response = self.client.patch("/messages/1", json={"pinned": True})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["pinned"])
        self.assertEqual(response.json()["text"], "hello")

    def test_patch_false_is_allowed(self):
        self.create()
        self.client.patch("/messages/1", json={"pinned": True})
        response = self.client.patch("/messages/1", json={"pinned": False})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["pinned"])

    def test_patch_rejects_null(self):
        original = self.create().json()
        for field in ("text", "pinned"):
            with self.subTest(field=field):
                response = self.client.patch("/messages/1", json={field: None})
                self.assertEqual(response.status_code, 422)
        self.assertEqual(self.client.get("/messages/1").json(), original)

    def test_patch_rejects_unknown_fields(self):
        original = self.create().json()
        for changes in ({"txet": "hi"}, {"author": "Timur"}, {"id": 5},
                        {"text": "new", "extra": 1}):
            with self.subTest(changes=changes):
                response = self.client.patch("/messages/1", json=changes)
                self.assertEqual(response.status_code, 422)
        self.assertEqual(self.client.get("/messages/1").json(), original)

    def test_patch_rejects_blank_text(self):
        self.create()
        for text in ("", "   ", "\t\n"):
            with self.subTest(text=repr(text)):
                response = self.client.patch("/messages/1", json={"text": text})
                self.assertEqual(response.status_code, 422)
        self.assertEqual(self.client.get("/messages/1").json()["text"], "hello")

    def test_patch_trims_text(self):
        self.create()
        response = self.client.patch("/messages/1", json={"text": "  updated  "})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["text"], "updated")

    def test_patch_text_length(self):
        self.create()
        self.assertEqual(self.client.patch("/messages/1", json={"text": "x" * 501}).status_code, 422)
        self.assertEqual(self.client.patch("/messages/1", json={"text": "x" * 500}).status_code, 200)

    def test_patch_both_fields(self):
        self.create()
        response = self.client.patch("/messages/1", json={"text": "  new  ", "pinned": True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["text"], "new")
        self.assertTrue(response.json()["pinned"])


if __name__ == "__main__":
    unittest.main()
