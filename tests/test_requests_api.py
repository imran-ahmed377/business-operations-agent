"""API-level tests for the request-acceptance slice."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_submit_business_request_accepts_valid_question() -> None:
    """A valid business question should be acknowledged and returned as received."""

    response = client.post("/requests", json={"question": "Why did sales drop this month?"})

    assert response.status_code == 202
    payload = response.json()
    assert payload["status"] == "received"
    assert payload["result"] is None
    assert payload["error"] is None
    assert payload["request_id"]
    assert payload["created_at"]


def test_submit_business_request_rejects_blank_question() -> None:
    """Whitespace-only questions should be rejected by the request model."""

    response = client.post("/requests", json={"question": "   "})

    assert response.status_code == 422
