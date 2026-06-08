import json

import httpx
import respx

from calcserver.client import CalcClient


@respx.mock
def test_client_add():
    respx.post("http://localhost:8888/add").mock(
        return_value=httpx.Response(200, json={"result": 7.0})
    )
    assert CalcClient().add(3, 4) == 7.0


@respx.mock
def test_client_subtract():
    respx.post("http://localhost:8888/subtract").mock(
        return_value=httpx.Response(200, json={"result": 3.0})
    )
    assert CalcClient().subtract(10, 7) == 3.0


@respx.mock
def test_client_multiply():
    route = respx.post("http://localhost:8888/multiply").mock(
        return_value=httpx.Response(200, json={"result": 42.0})
    )
    assert CalcClient().multiply(6, 7) == 42.0
    assert route.called
    sent_body = json.loads(route.calls.last.request.read())
    assert sent_body == {"a": 6, "b": 7}


@respx.mock
def test_client_custom_url():
    respx.post("http://example.com:9999/add").mock(
        return_value=httpx.Response(200, json={"result": 5.0})
    )
    assert CalcClient("http://example.com:9999").add(2, 3) == 5.0


@respx.mock
def test_client_raises_on_error():
    respx.post("http://localhost:8888/add").mock(
        return_value=httpx.Response(500)
    )
    import pytest
    with pytest.raises(httpx.HTTPStatusError):
        CalcClient().add(1, 2)
