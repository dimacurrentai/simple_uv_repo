from __future__ import annotations

import argparse

import httpx


class CalcClient:
    def __init__(self, base_url: str = "http://localhost:8888") -> None:
        self.base_url = base_url.rstrip("/")

    def add(self, a: float, b: float) -> float:
        r = httpx.post(f"{self.base_url}/add", json={"a": a, "b": b})
        r.raise_for_status()
        return float(r.json()["result"])

    def subtract(self, a: float, b: float) -> float:
        r = httpx.post(f"{self.base_url}/subtract", json={"a": a, "b": b})
        r.raise_for_status()
        return float(r.json()["result"])

    def multiply(self, a: float, b: float) -> float:
        r = httpx.post(f"{self.base_url}/multiply", json={"a": a, "b": b})
        r.raise_for_status()
        return float(r.json()["result"])


def main() -> None:
    parser = argparse.ArgumentParser(description="CalcServer CLI client")
    parser.add_argument("operation", choices=["add", "subtract", "multiply"])
    parser.add_argument("a", type=float)
    parser.add_argument("b", type=float)
    parser.add_argument("--url", default="http://localhost:8888", metavar="URL")
    args = parser.parse_args()

    client = CalcClient(args.url)
    dispatch = {
        "add": client.add,
        "subtract": client.subtract,
        "multiply": client.multiply,
    }
    print(dispatch[args.operation](args.a, args.b))


if __name__ == "__main__":
    main()
