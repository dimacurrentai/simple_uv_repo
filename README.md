# CalcServer

A minimal calculator server with a REST API and web UI, built with [FastAPI](https://fastapi.tiangolo.com/) and [uv](https://docs.astral.sh/uv/).

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Quickstart

```bash
git clone <repo>
cd <repo>
uv sync
uv run calcserver
```

Open **http://localhost:8888** for the web UI.

## API

Both endpoints accept JSON with fields `a` and `b` (numbers) and return `{"result": <float>}`.

### `POST /add`

```bash
curl -s -X POST http://localhost:8888/add \
  -H 'Content-Type: application/json' \
  -d '{"a": 3, "b": 4}'
# {"result":7.0}
```

### `POST /subtract`

```bash
curl -s -X POST http://localhost:8888/subtract \
  -H 'Content-Type: application/json' \
  -d '{"a": 10, "b": 3}'
# {"result":7.0}
```

Auto-generated interactive docs (Swagger UI) are at **http://localhost:8888/docs**.

## CLI client

```bash
uv run calcclient add 3 4
uv run calcclient subtract 10 3

# target a different host/port
uv run calcclient --url http://other-host:8888 add 1.5 2.5
```

## Python client

```python
from calcserver.client import CalcClient

c = CalcClient()                     # default: http://localhost:8888
c = CalcClient("http://host:9000")   # custom URL

print(c.add(3, 4))        # 7.0
print(c.subtract(10, 3))  # 7.0
```

`CalcClient` uses `httpx` under the hood and raises `httpx.HTTPStatusError` on non-2xx responses.

## Development

Install all dependencies (including dev):

```bash
uv sync
```

### Running tests

```bash
uv run pytest        # all tests
uv run pytest -v     # verbose
```

Server endpoint tests use FastAPI's `TestClient` (no server process needed). Client tests use `respx` to mock HTTP calls.

## Project layout

```
src/calcserver/
  __init__.py
  server.py     – FastAPI app, /add and /subtract endpoints, inline web UI
  client.py     – CalcClient class + calcclient CLI entry point
tests/
  test_server.py  – endpoint + HTML tests
  test_client.py  – client unit tests (mocked)
pyproject.toml    – project metadata, deps, entry points
uv.lock           – pinned dependency lockfile
```
