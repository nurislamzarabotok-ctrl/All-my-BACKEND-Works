"""Run an .sql file on chat.db and print what each SELECT returns.

    python run_sql.py schema.sql
    python run_sql.py seed.sql
    python run_sql.py queries/q1.sql
"""
import sqlite3
import sys

DB = "chat.db"


def show(cursor: sqlite3.Cursor) -> None:
    names = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    widths = [max(len(str(x)) for x in [name] + [row[i] for row in rows]) for i, name in enumerate(names)]
    print("  ".join(name.ljust(w) for name, w in zip(names, widths)))
    print("  ".join("-" * w for w in widths))
    for row in rows:
        print("  ".join(str(x).ljust(w) for x, w in zip(row, widths)))
    print(f"({len(rows)} rows)\n")


def split(script: str) -> list[str]:
    """Cut the file into statements. A ; inside 'text' does not end a statement."""
    statements, current = [], ""
    for line in script.splitlines(keepends=True):
        current += line
        if sqlite3.complete_statement(current):
            statements.append(current.strip())
            current = ""
    rest = "\n".join(l for l in current.splitlines() if not l.strip().startswith("--")).strip()
    if rest:
        statements.append(rest)
    return statements


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        return
    with open(sys.argv[1], encoding="utf-8") as f:
        script = f.read()
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    statements = split(script)
    for number, statement in enumerate(statements, 1):
        try:
            cursor = conn.execute(statement)
        except sqlite3.Error as error:
            conn.commit()
            conn.close()
            print(f"Statement {number} of {len(statements)} failed:\n\n{statement}\n")
            print(f"{type(error).__name__}: {error}")
            sys.exit(1)
        if cursor.description is not None:
            show(cursor)
    conn.commit()
    conn.close()
    word = "statement" if len(statements) == 1 else "statements"
    print(f"OK: {len(statements)} {word} from {sys.argv[1]}")


if __name__ == "__main__":
    main()
