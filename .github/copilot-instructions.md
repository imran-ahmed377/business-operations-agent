# Project Instructions

## Scope

This repository is the incremental MVP for a Business Operations Agent. Keep changes aligned with `MVP architecture.md` and the current slice described in `README.md`.

## Stack and commands

- Target Python 3.11 or newer.
- Use FastAPI for HTTP behavior, Pydantic for typed contracts, and pytest for tests.
- Install development dependencies with `python -m pip install -e '.[test]'`.
- Run the focused suite with `python -m pytest tests/test_health.py tests/test_models.py`.
- Run the complete suite with `python -m pytest`.
- Start the API locally with `python -m uvicorn app.main:app --reload`.

## Coding conventions

- Keep application code under `app/` and tests under `tests/`.
- Prefer small, typed functions and explicit Pydantic models over unvalidated dictionaries at API boundaries.
- Preserve existing public names and response shapes unless the architecture or a test requires a contract change.
- Keep modules focused: HTTP wiring belongs in `app/main.py`; shared request and response contracts belong in `app/models.py`.
- Use the standard library where it is sufficient. Add dependencies only when they provide clear value and update `pyproject.toml`.
- For every code change you generate or modify, add a concise comment or docstring before each logical code chunk, including application code, tests, classes, functions, control-flow blocks, and configuration blocks. Explain the chunk's purpose, behavior, or important decision so another developer can understand why it exists. Do not add comments for individual obvious statements, repeat the code verbatim, or omit comments from a new chunk unless the surrounding code already documents that exact chunk clearly.

## Product boundaries

- Add each capability incrementally and cover it with focused tests and README documentation.
- Business answers must be evidence-backed; do not invent data, citations, or operational outcomes.
- Treat business-data access, recommendations, and actions as separate boundaries.
- Any future write or external side effect must be explicit, auditable, and approval-gated.
- Do not add authentication, persistence, background processing, or agent behavior unless the architecture slice being implemented calls for it.

## Validation

After modifying code, run the narrowest relevant pytest test first, then run the full suite when the change crosses module or API boundaries. Also run `python3 -m py_compile` for changed Python files when practical.
