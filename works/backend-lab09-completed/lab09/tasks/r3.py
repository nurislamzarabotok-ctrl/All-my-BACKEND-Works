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
