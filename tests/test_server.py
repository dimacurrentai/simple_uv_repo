import pytest
from fastapi.testclient import TestClient

from calcserver.server import app

client = TestClient(app)


def test_add_integers():
    r = client.post("/add", json={"a": 3, "b": 4})
    assert r.status_code == 200
    assert r.json() == {"result": 7.0}


def test_subtract_integers():
    r = client.post("/subtract", json={"a": 10, "b": 3})
    assert r.status_code == 200
    assert r.json() == {"result": 7.0}


def test_add_floats():
    r = client.post("/add", json={"a": 1.5, "b": 2.5})
    assert r.status_code == 200
    assert r.json() == {"result": 4.0}


def test_subtract_floats():
    r = client.post("/subtract", json={"a": 5.5, "b": 2.2})
    assert r.status_code == 200
    assert abs(r.json()["result"] - 3.3) < 1e-9


def test_add_negative():
    r = client.post("/add", json={"a": -5, "b": 3})
    assert r.status_code == 200
    assert r.json() == {"result": -2.0}


def test_subtract_gives_negative():
    r = client.post("/subtract", json={"a": 3, "b": 10})
    assert r.status_code == 200
    assert r.json() == {"result": -7.0}


def test_add_zeros():
    r = client.post("/add", json={"a": 0, "b": 0})
    assert r.status_code == 200
    assert r.json() == {"result": 0.0}


def test_multiply_positive():
    r = client.post("/multiply", json={"a": 3, "b": 4})
    assert r.status_code == 200
    assert r.json() == {"result": 12.0}


def test_multiply_signed():
    r = client.post("/multiply", json={"a": -2, "b": 5})
    assert r.status_code == 200
    assert r.json() == {"result": -10.0}


def test_multiply_floats():
    r = client.post("/multiply", json={"a": 1.5, "b": 2.0})
    assert r.status_code == 200
    assert r.json() == {"result": 3.0}


def test_index_returns_html():
    r = client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert "<title>CalcServer</title>" in r.text


def test_index_has_operator_dropdown():
    r = client.get("/")
    assert r.status_code == 200
    text = r.text
    assert '<select id="op">' in text
    assert '<option value="add">' in text
    assert '<option value="subtract">' in text
    assert '<option value="multiply">' in text
    assert text.count("onclick=\"calc()\"") == 1


def test_invalid_payload_returns_422():
    r = client.post("/add", json={"a": "not_a_number", "b": 2})
    assert r.status_code == 422


def test_missing_field_returns_422():
    r = client.post("/add", json={"a": 1})
    assert r.status_code == 422
