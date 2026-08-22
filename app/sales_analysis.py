"""Sales-period analysis for the first real business investigation slice."""

from __future__ import annotations


def _sum_amounts(rows: list[dict[str, object]]) -> float:
    """Add the numeric sales values from a period list."""

    return float(sum(float(row["amount"]) for row in rows))


def _largest_drop(rows_current: list[dict[str, object]], rows_previous: list[dict[str, object]]) -> tuple[str, float]:
    """Find the region with the largest absolute decrease between periods."""

    previous_by_region = {str(row["region"]): float(row["amount"]) for row in rows_previous}
    results: list[tuple[str, float]] = []

    for row in rows_current:
        region = str(row["region"])
        previous_amount = previous_by_region.get(region, 0.0)
        current_amount = float(row["amount"])
        delta = current_amount - previous_amount
        results.append((region, delta))

    if not results:
        return "", 0.0

    region, delta = min(results, key=lambda item: item[1])
    return region, delta


def compare_sales_periods(current_period: list[dict[str, object]], previous_period: list[dict[str, object]]) -> dict[str, float | str]:
    """Compare current and previous sales totals and highlight the largest regional drop.

    The function deliberately stays deterministic and read-only. It does not
    decide business actions or invent narrative reasoning; it only computes the
    measurable sales shift for later orchestration.
    """

    current_total = _sum_amounts(current_period)
    previous_total = _sum_amounts(previous_period)
    delta_amount = current_total - previous_total
    delta_percent = 0.0 if previous_total == 0 else (delta_amount / previous_total) * 100
    largest_region, largest_drop_amount = _largest_drop(current_period, previous_period)

    return {
        "current_total": current_total,
        "previous_total": previous_total,
        "delta_amount": delta_amount,
        "delta_percent": delta_percent,
        "largest_drop_region": largest_region,
        "largest_drop_amount": largest_drop_amount,
    }
