# Business Operations Agent

This repository is being built incrementally from the architecture in
[`MVP architecture.md`](MVP%20architecture.md). The current slice provides a
FastAPI service with a health check, typed request models, and a minimal HTTP
submission endpoint for a business question. It still does not investigate data,
retrieve documents, or perform any business action.

## Setup

Create a virtual environment and install the application with its test tools:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
```

## Run the current slice

Start the local API:

```bash
python -m uvicorn app.main:app --reload
```

The health check is available at <http://127.0.0.1:8000/health>.

Submit a business question with a POST request to
<http://127.0.0.1:8000/requests> using JSON like:

```json
{"question": "Why did our sales drop this month?"}
```

The service returns a request ID and a `received` status. No investigation or
action execution occurs in this slice.

Run the focused test:

```bash
python -m pytest tests/test_health.py tests/test_models.py tests/test_requests_api.py
```

Later chunks will add controlled sales data access, company-document evidence,
recommendations, and approval-gated actions. Each capability will be tested and
documented before the next one is introduced.
