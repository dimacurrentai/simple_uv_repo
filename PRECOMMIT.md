# Pre-commit checks

Run all checks from the repository root. They use the [uv](https://docs.astral.sh/uv/) toolchain documented in `README.md`; `uv` must be on `PATH` (`curl -LsSf https://astral.sh/uv/install.sh | sh`).

## Sync dependencies

Ensure the virtual environment matches `pyproject.toml` and `uv.lock`, including the `dev` dependency group used by the tests:

    uv sync

This is the install step the `README.md` Quickstart and Development sections both call out. It must succeed before the test step below.

## Tests

Run the full pytest suite from the repository root:

    uv run pytest

`pyproject.toml` pins `testpaths = ["tests"]`, so this picks up `tests/test_server.py` (FastAPI `TestClient` endpoint and HTML tests) and `tests/test_client.py` (`respx`-mocked client tests). All tests must pass.
