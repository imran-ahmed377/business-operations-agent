"""API-level tests for the request-acceptance slice."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_submit_business_request_returns_completed_investigation() -> None:
    """A supported business question should return its evidence-backed result."""

    response = client.post("/requests", json={"question": "Why did sales drop this month?"})

    assert response.status_code == 202
    payload = response.json()
    assert payload["status"] == "completed"
    assert "15.7% decline" in payload["result"]["answer"]
    assert payload["result"]["evidence"]["current_total"] == 295_000.0
    assert payload["error"] is None
    assert payload["request_id"]
    assert payload["created_at"]


def test_submit_business_request_rejects_blank_question() -> None:
    """Whitespace-only questions should be rejected by the request model."""

    response = client.post("/requests", json={"question": "   "})

    assert response.status_code == 422


def test_submit_business_request_reports_unsupported_question() -> None:
    """An unsupported question should return an explicit workflow failure."""

    response = client.post("/requests", json={"question": "What is our employee turnover?"})

    assert response.status_code == 202
    payload = response.json()
    assert payload["status"] == "failed"
    assert payload["result"] is None
    assert payload["error"] == "this workflow currently supports sales-drop questions only"
