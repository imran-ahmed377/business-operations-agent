"""Focused tests for the controlled SQLite sales-data adapter."""

import sqlite3

import pytest

from app.data_store import SalesDataStore


def test_seeded_store_returns_sales_for_each_period(tmp_path) -> None:
    """A new store should seed reproducible current and previous sales rows."""

    store = SalesDataStore(tmp_path / "sales.db")

    current_sales = store.get_sales_period("current")
    previous_sales = store.get_sales_period("previous")

    assert current_sales == [
        {"region": "North", "amount": 120_000.0},
        {"region": "South", "amount": 95_000.0},
        {"region": "West", "amount": 80_000.0},
    ]
    assert sum(row["amount"] for row in previous_sales) == 350_000.0


def test_store_returns_empty_list_for_unknown_period(tmp_path) -> None:
    """An unavailable period should be explicit without inventing records."""

    store = SalesDataStore(tmp_path / "sales.db")

    assert store.get_sales_period("unknown") == []


def test_store_rejects_write_like_period_queries(tmp_path) -> None:
    """The adapter should reject values that could alter its query contract."""

    store = SalesDataStore(tmp_path / "sales.db")

    with pytest.raises(ValueError, match="unsupported sales period"):
        store.get_sales_period("current; DROP TABLE sales")

    with sqlite3.connect(tmp_path / "sales.db") as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM sales"
        ).fetchone() == (6,)
