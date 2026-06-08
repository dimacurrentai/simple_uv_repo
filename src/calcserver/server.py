from __future__ import annotations

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="CalcServer")

_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CalcServer</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; }
    body {
      font-family: system-ui, -apple-system, sans-serif;
      max-width: 420px;
      margin: 80px auto;
      padding: 0 24px;
      background: #f9fafb;
      color: #111;
    }
    h1 { font-size: 1.6rem; margin-bottom: 24px; }
    .inputs { display: flex; gap: 12px; margin-bottom: 12px; }
    input[type=number] {
      flex: 1;
      padding: 10px 12px;
      font-size: 1.1rem;
      border: 1px solid #d1d5db;
      border-radius: 6px;
      background: #fff;
    }
    .controls { display: flex; gap: 10px; }
    select#op {
      flex: 1;
      padding: 10px 12px;
      font-size: 1rem;
      border: 1px solid #d1d5db;
      border-radius: 6px;
      background: #fff;
      color: #111;
    }
    button {
      flex: 1;
      padding: 10px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      border: none;
      border-radius: 6px;
      background: #2563eb;
      color: #fff;
      transition: background 0.15s;
    }
    button:hover { background: #1d4ed8; }
    #result {
      margin-top: 24px;
      font-size: 1.4rem;
      font-weight: 700;
      min-height: 2rem;
    }
    #error { color: #dc2626; margin-top: 8px; font-size: 0.9rem; }
  </style>
</head>
<body>
  <h1>CalcServer</h1>
  <div class="inputs">
    <input id="a" type="number" placeholder="a" value="0" step="any">
    <input id="b" type="number" placeholder="b" value="0" step="any">
  </div>
  <div class="controls">
    <select id="op">
      <option value="add">+</option>
      <option value="subtract">−</option>
      <option value="multiply">×</option>
    </select>
    <button onclick="calc()">Compute</button>
  </div>
  <div id="result"></div>
  <div id="error"></div>
  <script>
    async function calc() {
      const op = document.getElementById('op').value;
      const a = parseFloat(document.getElementById('a').value);
      const b = parseFloat(document.getElementById('b').value);
      document.getElementById('error').textContent = '';
      document.getElementById('result').textContent = '';
      try {
        const resp = await fetch('/' + op, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ a, b }),
        });
        if (!resp.ok) throw new Error('HTTP ' + resp.status);
        const data = await resp.json();
        document.getElementById('result').textContent = '= ' + data.result;
      } catch (e) {
        document.getElementById('error').textContent = 'Error: ' + e.message;
      }
    }
  </script>
</body>
</html>"""


class Numbers(BaseModel):
    a: float
    b: float


class Result(BaseModel):
    result: float


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return _HTML


@app.post("/add", response_model=Result)
def add(nums: Numbers) -> Result:
    return Result(result=nums.a + nums.b)


@app.post("/subtract", response_model=Result)
def subtract(nums: Numbers) -> Result:
    return Result(result=nums.a - nums.b)


@app.post("/multiply", response_model=Result)
def multiply(nums: Numbers) -> Result:
    return Result(result=nums.a * nums.b)


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8888)


if __name__ == "__main__":
    main()
