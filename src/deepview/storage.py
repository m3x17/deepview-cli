import os
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

NAME_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def database_path() -> Path:
    home = Path(os.environ.get("DEEPVIEW_HOME", Path.home() / ".deepview"))
    home.mkdir(parents=True, exist_ok=True)
    return home / "data.db"


@contextmanager
def connect():
    conn = sqlite3.connect(database_path())
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS datasets ("
            "name TEXT PRIMARY KEY, source TEXT, rows INTEGER, columns INTEGER, imported_at TEXT)"
        )
        yield conn
        conn.commit()
    finally:
        conn.close()


def validate_name(name: str) -> None:
    if not NAME_PATTERN.match(name):
        raise ValueError(
            "Name must start with a letter or underscore and contain only letters, digits, and underscores"
        )
    if name == "datasets":
        raise ValueError("'datasets' is a reserved name")


def save_dataset(name: str, df: pd.DataFrame, source: str, replace: bool = False) -> None:
    validate_name(name)
    with connect() as conn:
        exists = conn.execute("SELECT 1 FROM datasets WHERE name = ?", (name,)).fetchone()
        if exists and not replace:
            raise ValueError(f"Dataset '{name}' already exists. Use --replace to overwrite it.")
        df.to_sql(name, conn, if_exists="replace", index=False)
        conn.execute(
            "INSERT OR REPLACE INTO datasets (name, source, rows, columns, imported_at) VALUES (?, ?, ?, ?, ?)",
            (name, source, len(df), len(df.columns), datetime.now(timezone.utc).isoformat(timespec="seconds")),
        )


def list_datasets() -> pd.DataFrame:
    with connect() as conn:
        return pd.read_sql_query(
            "SELECT name, source, rows, columns, imported_at FROM datasets ORDER BY imported_at", conn
        )

def stored_names() -> list[str]:
    with connect() as conn:
        rows = conn.execute("SELECT name FROM datasets").fetchall()
    return [row[0] for row in rows]


def load_stored(name: str) -> pd.DataFrame:
    validate_name(name)
    with connect() as conn:
        exists = conn.execute("SELECT 1 FROM datasets WHERE name = ?", (name,)).fetchone()
        if not exists:
            raise FileNotFoundError(f"No stored dataset named: {name}")
        return pd.read_sql_query(f'SELECT * FROM "{name}"', conn)