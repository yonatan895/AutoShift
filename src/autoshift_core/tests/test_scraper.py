import sys
from pathlib import Path


# isort: skip_file

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # noqa: E402
from autoshift_core.scraper import (  # noqa: E402
    fetch_metrics,
    fetch_page_title,
)  # isort: skip



@pytest.mark.asyncio
async def test_fetch_page_title(monkeypatch):
    async def mock_send(request):
        html = "<html><head><title>Test</title></head><body></body></html>"
        return httpx.Response(200, text=html)

    class DummyAsyncClient:
        def __init__(self, *a, **kw):
            self.transport = httpx.MockTransport(mock_send)

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

        async def get(self, url):
            request = httpx.Request("GET", url)
            response = await mock_send(request)
            response.request = request
            return response

    monkeypatch.setattr(httpx, "AsyncClient", DummyAsyncClient)
    title = await fetch_page_title("http://example.com")

    assert title == "Test"


@pytest.mark.asyncio
async def test_fetch_metrics(monkeypatch):
    async def mock_send(request):
        html = (
            '<table class="metrics">'
            "<tr><td>CPU</td><td>80%</td></tr>"
            "<tr><td>MEM</td><td>70%</td></tr>"
            "</table>"
        )
        return httpx.Response(200, text=html)

    class DummyAsyncClient:
        def __init__(self, *a, **kw):
            self.transport = httpx.MockTransport(mock_send)

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

        async def get(self, url):
            request = httpx.Request("GET", url)
            response = await mock_send(request)
            response.request = request
            return response

    monkeypatch.setattr(httpx, "AsyncClient", DummyAsyncClient)
    metrics = await fetch_metrics("http://example.com")

    assert metrics == {"CPU": "80%", "MEM": "70%"}
