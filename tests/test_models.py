"""Focused validation tests for the first request contracts."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.models import BusinessRequest, RequestStatus, RequestStatusResponse


def test_business_request_strips_outer_whitespace() -> None:
    request = BusinessRequest(question="  Why did sales change?  ")

    assert request.question == "Why did sales change?"


def test_business_request_rejects_blank_question() -> None:
    with pytest.raises(ValidationError):
        BusinessRequest(question="   ")


def test_business_request_rejects_question_over_limit() -> None:
    with pytest.raises(ValidationError):
        BusinessRequest(question="a" * 2_001)


def test_request_status_response_defaults_to_no_result() -> None:
    response = RequestStatusResponse(
        request_id=uuid4(),
        status=RequestStatus.RECEIVED,
        created_at=datetime.now(UTC),
    )

    assert response.result is None
    assert response.error is None
