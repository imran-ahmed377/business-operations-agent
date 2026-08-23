"""Deterministic orchestration for the first sales investigation workflow.

This module implements the MVP's read-only sales comparison workflow. It recognizes
sales-drop questions, retrieves comparison analysis from fixture data, and produces
evidence-backed results grounded in measurable sales metrics. Later MVP slices will
replace these fixtures with real data adapters and add document evidence retrieval
and approval-gated action execution.
"""

from pathlib import Path

from app.data_store import SalesDataStore
from app.models import SalesInvestigationResult
from app.sales_analysis import compare_sales_periods


# The default store keeps local demo behavior reproducible while isolating data
# access behind the same adapter a future production connector can implement.
DEFAULT_DATASTORE = SalesDataStore(Path(__file__).parents[2] / "data" / "sales.db")


def _is_sales_drop_question(question: str) -> bool:
    """Recognize the narrow sales-drop question supported by this slice.
    
    This is a deliberate boundary that prevents the system from silently treating
    unsupported questions as if they had been investigated. Only questions that
    explicitly ask about sales declines, drops, or changes are recognized;
    all other questions are rejected with an explicit ValueError in the caller.
    
    Args:
        question: A user-submitted business question.
    
    Returns:
        True if the question appears to be about a sales drop or decline.
    """

    normalized_question = question.lower()
    return "sales" in normalized_question and any(
        term in normalized_question for term in ("drop", "decline", "decrease", "change")
    )


def investigate_business_question(question: str) -> SalesInvestigationResult:
    """Investigate a supported sales question using measurable demo evidence.

    This function orchestrates the core workflow of the first MVP slice. It takes a
    user question, validates that it falls within the narrow scope of supported
    sales-drop investigations, and returns a structured result containing:
    - an answer summarizing the measured sales change and largest regional drop
    - a recommendation grounded in that evidence
    - the underlying comparison metrics for audit and transparency
    
    The workflow is intentionally deterministic and read-only: it compares fixture
    data (representing current vs. previous period sales), extracts measurable facts,
    and constructs a response without inferring business actions or retrieving
    external documents. Unsupported questions fail explicitly with a ValueError
    to prevent silent fallbacks or invented answers.
    
    Args:
        question: The business question to investigate.
    
    Returns:
        A SalesInvestigationResult containing an answer, recommendation, and evidence.
    
    Raises:
        ValueError: If the question does not match the narrow sales-drop pattern
                    supported by this MVP slice.
    """

    # Validate that the question falls within scope; fail explicitly if not.
    # This prevents the workflow from implicitly treating unsupported questions
    # as if they had been investigated.
    if not _is_sales_drop_question(question):
        raise ValueError("this workflow currently supports sales-drop questions only")

    # Compute measurable sales metrics by comparing the current period fixture
    # against the previous period fixture. This produces totals, deltas, and
    # identifies the region with the largest absolute decrease.
    current_sales = DEFAULT_DATASTORE.get_sales_period("current")
    previous_sales = DEFAULT_DATASTORE.get_sales_period("previous")
    comparison = compare_sales_periods(current_sales, previous_sales)
    
    # Extract individual metrics from the comparison result for use in the response.
    # Casting ensures type safety and prevents downstream surprises.
    drop_percent = abs(float(comparison["delta_percent"]))
    current_total = float(comparison["current_total"])
    previous_total = float(comparison["previous_total"])
    drop_region = str(comparison["largest_drop_region"])
    drop_amount = abs(float(comparison["largest_drop_amount"]))

    # Construct a structured, evidence-backed result grounded in the measurable
    # metrics extracted above. The answer summarizes the total sales change and
    # the largest regional decrease; the recommendation directs the business user
    # to further investigation of that region without inventing actions or outcomes.
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
