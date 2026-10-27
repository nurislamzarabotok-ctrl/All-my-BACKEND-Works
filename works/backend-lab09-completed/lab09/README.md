# Lab 09: Review for control work 2

You work on your own today. Monday 26.10 is control work 2, on lessons 23 to 28. This lab is a practice paper that checks itself.

The tasks are on the slides of the lesson 29 deck, `backend-29-review` (PDF in the group chat). Each task has a file in `tasks/`, and `check.py` tells you whether your answer was right.

**The rule: answer first, check after.** Write each answer in [ANSWERS.md](ANSWERS.md) before you run anything. Then run the check, and write your points next to the answer. On Monday nothing will run, so practise without it.

## Run it

macOS / Linux:

```bash
git clone https://github.com/kilc-po25/backend-lab09-YOUR-USERNAME.git
cd backend-lab09-YOUR-USERNAME
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
git clone https://github.com/kilc-po25/backend-lab09-YOUR-USERNAME.git
cd backend-lab09-YOUR-USERNAME
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

`app/` is the chat from lab 08, finished: users, rooms, messages inside rooms. Several tasks use it. Do not change it.

## The tasks

| Task | Slide | Type | Points | You | Check |
|---|---|---|---|---|---|
| A1 | 5 | trace: optional, null, required | 3 | answer in ANSWERS.md | `python check.py a1` |
| A2 | 6 | trace: two validators on one field | 4 | answer | `python check.py a2` |
| A3 | 7 | read a traceback | 4 | answer | `python check.py a3` |
| A4 | 8 | trace: routers and addresses | 4 | answer | `python check.py a4` |
| A5 | 9 | trace: query parameters in a room | 5 | answer | `python check.py a5` |
| B1 | 10 | find the errors: schema and handler | 3 | answer, then fix `tasks/b1.py` | `python check.py b1` |
| B2 | 11 | find the errors: a test file | 3 | answer, then fix `tasks/test_b2.py` | `python check.py b2` |
| C1 | 12 | lines in order: one storage | 2 | answer, then write `tasks/c1.py` | `python check.py c1` |
| C2 | 13 | lines in order: a test | 2 | answer, then write `tasks/test_c2.py` | `python check.py c2` |
| D1 | 14 | write: UserIn with a validator | 3 | on paper, then `tasks/d1.py` | `python check.py d1` |
| D2 | 15 | write: GET /rooms with q | 3 | on paper, then `tasks/d2.py` | `python check.py d2` |
| R1 | 16 | control work 1: model_dump | 3 | answer | `python check.py r1` |
| R2 | 16 | control work 1: write a text file | 3 | on paper, then `tasks/r2.py` | `python check.py r2` |
| R3 | 17 | control work 1: a folder of JSON files | 4 | on paper, then `tasks/r3.py` | `python check.py r3` |
| | | | **46** | | |

`python check.py all` runs every task you edit: at the start, 0 of 19 checks pass.

A trace task's check prints the real answer. Compare it with yours. A check that says PASS or FAIL tests your file; the points come from the scoring on the slide, not from the number of PASS lines.

**In class:** A1 to A5, B1, B2, C1, C2. **Homework before Monday:** D1, D2, R1 to R3, and anything left.

## When a check is red

| What you see | What it means |
|---|---|
| `FAIL  tasks/d1.py does not import: SyntaxError` | Your file has a syntax error. The message names the line |
| `AttributeError: module 'tasks.d1' has no attribute 'UserIn'` | The class is not written yet, or it has another name |
| `ModuleNotFoundError: No module named 'app'` | Run `check.py` from the project folder, the one with `app/` and `tasks/` |
| `pytest says: no tests ran` | No function starts with `test_` |
| `pytest says: 1 failed` in C2 | The extra line is in your answer, or the order is wrong. Read the full output: `pytest tasks/test_c2.py` |

## How to hand in

1. ANSWERS.md filled in: your first answers, your points per task, and the total out of 46.
2. Commit and push, and tag:

```bash
git add -A
git commit -m "lab 09: done"
git tag lab09
git push
git push --tags
```
