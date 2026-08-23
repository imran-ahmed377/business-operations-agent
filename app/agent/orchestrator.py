"""Deterministic orchestration for the first sales investigation workflow."""

from app.models import SalesInvestigationResult
from app.sales_analysis import compare_sales_periods


# These fixtures keep the first workflow reproducible until a real data adapter
# is introduced in a later chunk.
CURRENT_SALES = [
    {"region": "North", "amount": 120_000},
    {"region": "South", "amount": 95_000},
    {"region": "West", "amount": 80_000},
]
PREVIOUS_SALES = [
    {"region": "North", "amount": 150_000},
    {"region": "South", "amount": 110_000},
    {"region": "West", "amount": 90_000},
]


def _is_sales_drop_question(question: str) -> bool:
    """Recognize the narrow sales-drop question supported by this slice."""

    normalized_question = question.lower()
    return "sales" in normalized_question and any(
        term in normalized_question for term in ("drop", "decline", "decrease", "change")
    )


def investigate_business_question(question: str) -> SalesInvestigationResult:
    """Investigate a supported sales question using measurable demo evidence.

    Unsupported questions fail explicitly so the workflow cannot imply that a
    missing data source was checked.
    """

    if not _is_sales_drop_question(question):
        raise ValueError("this workflow currently supports sales-drop questions only")

    comparison = compare_sales_periods(CURRENT_SALES, PREVIOUS_SALES)
    drop_percent = abs(float(comparison["delta_percent"]))
    current_total = float(comparison["current_total"])
    previous_total = float(comparison["previous_total"])
    drop_region = str(comparison["largest_drop_region"])
    drop_amount = abs(float(comparison["largest_drop_amount"]))

    return SalesInvestigationResult(
        answer=(
            f"Sales decreased from ${previous_total:,.0f} to ${current_total:,.0f}, "
            f"a {drop_percent:.1f}% decline. {drop_region} had the largest "
            f"regional decrease at ${drop_amount:,.0f}."
        ),
        recommendation=(
            f"Review the drivers of the {drop_region} decline first, then compare "
            "regional pipeline and conversion performance before taking action."
        ),
        evidence=comparison,
    )
