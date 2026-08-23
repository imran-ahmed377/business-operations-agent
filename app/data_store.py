"""Read-only SQLite access to the reproducible sales fixture."""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path


class SalesDataStore:
    """Provide controlled reads from the local sales database."""

    _PERIODS = frozenset({"current", "previous"})

    def __init__(self, database_path: str | Path) -> None:
        """Create the database if needed and seed it once from the SQL fixture."""

        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _initialize_database(self) -> None:
        """Create the schema and insert fixture rows only into an empty store."""

        seed_path = Path(__file__).parents[1] / "data" / "sales.sql"
        seed_script = seed_path.read_text(encoding="utf-8")

        with sqlite3.connect(self.database_path) as connection:
            table_count = connection.execute(
                "SELECT COUNT(*) FROM sqlite_master "
                "WHERE type = 'table' AND name = 'sales'"
            ).fetchone()[0]
            if table_count == 0:
                connection.executescript(seed_script)

    def get_sales_period(self, period: str) -> list[dict[str, float | str]]:
        """Return sales rows for a known period using a parameterized query."""

        if not re.fullmatch(r"[a-z_]+", period):
            raise ValueError("unsupported sales period")

        if period not in self._PERIODS:
            return []

        with sqlite3.connect(self.database_path) as connection:
            rows = connection.execute(
                "SELECT region, amount FROM sales WHERE period = ? ORDER BY id",
                (period,),
            ).fetchall()

        return [{"region": str(region), "amount": float(amount)} for region, amount in rows]
