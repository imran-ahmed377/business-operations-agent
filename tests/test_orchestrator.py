"""Focused tests for the first deterministic agent workflow."""

import pytest

from app.agent.orchestrator import investigate_business_question


def test_sales_question_returns_answer_recommendation_and_evidence() -> None:
    result = investigate_business_question("Why did our sales drop this month?")

    assert "15.7% decline" in result.answer
    assert "North" in result.answer
    assert "Review" in result.recommendation
    assert result.evidence["current_total"] == 295_000.0
    assert result.evidence["previous_total"] == 350_000.0


def test_unsupported_question_fails_explicitly() -> None:
    with pytest.raises(ValueError, match="sales-drop questions only"):
        investigate_business_question("What is our employee turnover?")
