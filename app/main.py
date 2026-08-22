"""HTTP entry point for the Business Operations Agent MVP."""

from datetime import UTC, datetime
from uuid import uuid4

from fastapi import FastAPI

from app.models import BusinessRequest, RequestStatus, RequestStatusResponse

app = FastAPI(
    title="Business Operations Agent",
    version="0.1.0",
    description="A small, evidence-backed business investigation service.",
)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Report whether the API process is ready to receive requests."""

    return {"status": "ok"}


@app.post("/requests", response_model=RequestStatusResponse, status_code=202, tags=["requests"])
def submit_business_request(request: BusinessRequest) -> RequestStatusResponse:
    """Accept a business question and return its initial lifecycle state.

    This slice intentionally does not investigate data or perform actions yet;
    it only validates the input and acknowledges receipt.
    """

    return RequestStatusResponse(
        request_id=uuid4(),
        status=RequestStatus.RECEIVED,
        created_at=datetime.now(UTC),
        result=None,
        error=None,
    )
