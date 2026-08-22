"""Typed contracts shared by the API and the future agent workflow."""

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class RequestStatus(StrEnum):
    """Lifecycle states exposed while a business request is processed."""

    RECEIVED = "received"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class BusinessRequest(BaseModel):
    """A single business question submitted to the agent."""

    question: str = Field(
        min_length=1,
        max_length=2_000,
        description="The business question the agent should investigate.",
    )

    @field_validator("question")
    @classmethod
    def question_must_contain_text(cls, value: str) -> str:
        """Reject whitespace-only questions while preserving useful spacing."""

        if not value.strip():
            raise ValueError("question must contain non-whitespace text")
        return value.strip()


class RequestStatusResponse(BaseModel):
    """Current state of a submitted request.

    The result is optional because later chunks will populate it only after the
    agent has completed its investigation.
    """

    request_id: UUID
    status: RequestStatus
    created_at: datetime
    result: dict[str, object] | None = None
    error: str | None = None
