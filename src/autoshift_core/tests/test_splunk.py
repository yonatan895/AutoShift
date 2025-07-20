import sys
from pathlib import Path

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # noqa: E402
from autoshift_core.splunk import SplunkHECClient  # noqa: E402


@pytest.mark.asyncio
async def test_send_event_success(monkeypatch):
    events = {}

    async def mock_send(request):
        events["request"] = request
        return httpx.Response(200)

    transport = httpx.MockTransport(mock_send)
    client = SplunkHECClient("https://splunk.example.com", "token")

    class DummyAsyncClient:
        def __init__(self, *a, **kw):
            self.transport = transport

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

        async def post(self, url, json=None, headers=None):
            request = httpx.Request("POST", url, json=json, headers=headers)
            events["request"] = request
            return httpx.Response(200, request=request)

    monkeypatch.setattr(httpx, "AsyncClient", DummyAsyncClient)
    await client.send_event({"foo": "bar"})

    assert events["request"].method == "POST"
    assert events["request"].url.path.endswith("/services/collector")
