# Multiplication endpoint and operator-dropdown UI

## Summary

Adds a `POST /multiply` arithmetic endpoint to `calcserver`, mirrors it as a
`multiply(a, b)` helper on the Python client, and reworks the inline HTML UI so
that the operation is picked from a `<select id="op">` and triggered by a single
`Compute` button. The change keeps server, client, and HTML diffs symmetric so
that a future `divide` (or any other binary float operation) follows the same
template: add a route, add a client method, add a `<select>` option, add tests.

## Rationale

- The existing server already supports `add` and `subtract`; multiplication is
  the next natural binary operation. The route, request body (`Numbers`), and
  response model (`Result`) are reused verbatim — no special handling for
  overflow, `inf`, or `NaN` beyond Python / FastAPI defaults.
- The current UI dedicates one `<button>` per operation. Each new operation
  would force another button, growing the row indefinitely. A `<select>` with
  one `Compute` button keeps the layout fixed regardless of operation count.
- The HTML is served inline by the server, so the UI changes ship with the
  server change — there is no second deploy and no backwards-compatibility
  shim for the old per-button layout.

## Implementation outline

### Server — `src/calcserver/server.py`

- Add a new route:

      @app.post("/multiply", response_model=Result)
      def multiply(nums: Numbers) -> Result:
          return Result(result=nums.a * nums.b)

  Placed after `subtract`, so the file reads `add` → `subtract` → `multiply`.

- Rewrite the body of `_HTML`:
  - Keep the two `<input type="number">` fields for `a` and `b`.
  - Replace the `.buttons` row with:
    - `<select id="op">` containing three `<option>` elements whose values are
      `add`, `subtract`, `multiply` and whose labels are `+`, `−`, `×`.
    - A single `<button onclick="calc()">Compute</button>`.
  - Keep the `#result` and `#error` `<div>`s unchanged.
  - Rewrite the inline `calc()` JS so it takes no arguments, reads the operator
    from `document.getElementById('op').value`, and POSTs to `'/' + op` with
    the same `{a, b}` body. Error handling is unchanged.
- Adjust the small amount of CSS that styled `.buttons` so the operator select
  and Compute button sit on a single row matching the existing visual style.

### Client — `src/calcserver/client.py`

- Add a third method on `CalcClient` that mirrors `add` / `subtract` exactly:

      def multiply(self, a: float, b: float) -> float:
          r = httpx.post(f"{self.base_url}/multiply", json={"a": a, "b": b})
          r.raise_for_status()
          return float(r.json()["result"])

- Extend the CLI in `main()` so `operation` accepts `multiply` in addition to
  `add` and `subtract`, and dispatches to the new helper. Replace the
  two-branch `add`/`subtract` ternary with a small dispatch dict so the CLI
  scales the same way the server does.

### Tests — `tests/test_server.py`

- Add positive- and signed-product tests against `POST /multiply`:
  `3 * 4 == 12.0` and `-2 * 5 == -10.0`.
- Add an HTML test that asserts the index page contains a `<select id="op">`
  whose `<option>` set includes `add`, `subtract`, and `multiply`, and that
  there is exactly one button bound to a no-arg `calc()` call.

### Tests — `tests/test_client.py`

- Add a `respx`-mocked `test_client_multiply` case asserting that
  `CalcClient().multiply(6, 7)` POSTs to `http://localhost:8888/multiply` and
  returns the mocked `result`.

## Acceptance criteria

The new behavior is correct when:

- `POST /multiply` with `{"a": 3, "b": 4}` → HTTP 200, `{"result": 12.0}`.
- `POST /multiply` with `{"a": -2, "b": 5}` → `{"result": -10.0}`.
- `CalcClient().multiply(a, b)` issues `POST /multiply` and returns the
  server's `result` as a `float`.
- `GET /` returns HTML containing a `<select id="op">` with options `add`,
  `subtract`, and `multiply`, and a single button wired to a no-arg `calc()`.
- All previously-passing tests (`test_server.py`, `test_client.py`) still pass.
- `uv sync && uv run pytest` succeeds from the repository root.

## How to rebuild from this document

1. In `src/calcserver/server.py`, add the `multiply` route after `subtract`
   following the same pattern (`Numbers` in, `Result` out, body `a * b`).
2. In the same file, replace the `<div class="buttons">` block in `_HTML` with
   a `<select id="op">` (options `add`/`+`, `subtract`/`−`, `multiply`/`×`)
   followed by a single `<button onclick="calc()">Compute</button>`. Rewrite
   `calc()` to be a no-arg function that reads the operator from `#op` and
   POSTs to `'/' + op`. Keep all other markup, CSS, and error-handling
   identical.
3. In `src/calcserver/client.py`, add a `multiply(a, b)` method on
   `CalcClient` that mirrors `add` / `subtract`. Update the CLI's
   `operation` choices and dispatch.
4. In `tests/test_server.py`, add `test_multiply_positive`,
   `test_multiply_signed`, and `test_index_has_operator_dropdown` covering the
   new endpoint and the new HTML structure.
5. In `tests/test_client.py`, add `test_client_multiply` mirroring
   `test_client_add` / `test_client_subtract`.
6. Run `uv sync && uv run pytest` from the repository root and confirm all
   tests pass.

## Out of scope

- Division, modulo, or any non-multiplication operation.
- Overflow / `NaN` / `inf` handling beyond Python's defaults.
- Persisting the operator selection in `localStorage` or query strings.
- Any change to the request/response models (`Numbers`, `Result`) — both are
  reused as-is.
