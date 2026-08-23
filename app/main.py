"""HTTP entry point for the Business Operations Agent MVP."""

from datetime import UTC, datetime
from uuid import uuid4

from fastapi import FastAPI

from app.agent.orchestrator import investigate_business_question
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
    """Investigate a supported question and return its request lifecycle state.

    The workflow remains synchronous and deterministic for this MVP. Unsupported
    questions become explicit failures instead of receiving invented answers.
    """

    request_id = uuid4()
    created_at = datetime.now(UTC)

    try:
        result = investigate_business_question(request.question)
    except ValueError as error:
        return RequestStatusResponse(
            request_id=request_id,
            status=RequestStatus.FAILED,
            created_at=created_at,
            error=str(error),
        )

    return RequestStatusResponse(
        request_id=request_id,
        status=RequestStatus.COMPLETED,
        created_at=created_at,
        result=result.model_dump(),
    )
