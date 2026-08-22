"""Focused tests for the first sales-period comparison slice."""

from app.sales_analysis import compare_sales_periods


def test_compare_sales_periods_reports_change_and_largest_drop() -> None:
    current_period = [
        {"region": "North", "amount": 120_000},
        {"region": "South", "amount": 95_000},
        {"region": "West", "amount": 80_000},
    ]
    previous_period = [
        {"region": "North", "amount": 150_000},
        {"region": "South", "amount": 110_000},
        {"region": "West", "amount": 90_000},
    ]

    result = compare_sales_periods(current_period, previous_period)

    assert result["current_total"] == 295_000.0
    assert result["previous_total"] == 350_000.0
    assert result["delta_amount"] == -55_000.0
    assert result["delta_percent"] == -15.714285714285714
    assert result["largest_drop_region"] == "North"
    assert result["largest_drop_amount"] == -30_000.0
