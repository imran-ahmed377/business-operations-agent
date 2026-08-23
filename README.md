# Business Operations Agent

This repository is being built incrementally from the architecture in
[`MVP architecture.md`](MVP%20architecture.md). The current slice adds a
read-only sales comparison function and a deterministic workflow for supported
sales-drop questions. The HTTP submission route now returns a completed,
evidence-backed result for supported questions and an explicit failure for
unsupported questions. It still does not retrieve documents or perform business
actions.

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

The service returns a request ID and either a `completed` result or a `failed`
status. No document retrieval or action execution occurs in this slice.

Run the focused test:

```bash
python -m pytest tests/test_health.py tests/test_models.py tests/test_requests_api.py tests/test_sales_analysis.py tests/test_orchestrator.py
```

The new sales workflow supports a first analysis pass for questions like "Why
did our sales drop this month?" by calculating total sales change, identifying
the largest regional decrease, and returning a recommendation grounded in that
comparison. Later chunks will add company-document evidence and approval-gated
actions.
