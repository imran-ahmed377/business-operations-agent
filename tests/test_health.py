"""Smoke tests for the first runnable service slice."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check_reports_ready_service() -> None:
    """The health route should provide a stable response for local checks."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
