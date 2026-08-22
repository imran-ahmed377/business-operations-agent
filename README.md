# Business Operations Agent

This repository is being built incrementally from the architecture in
[`MVP architecture.md`](MVP%20architecture.md). The current slice adds a
read-only sales comparison function that can measure current-vs-previous period
differences. It still does not retrieve documents or perform business actions,
but it does provide the first quantitative investigation capability.

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
python -m pytest tests/test_health.py tests/test_models.py tests/test_requests_api.py tests/test_sales_analysis.py
```

The new sales comparison helper supports a first analysis pass for questions like
"Why did our sales drop this month?" by calculating total sales change and the
largest regional decrease between periods. Later chunks will add company-document
evidence, recommendations, and approval-gated actions.
