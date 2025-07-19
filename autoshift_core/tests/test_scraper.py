import pytest
import sys
from pathlib import Path
import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from autoshift_core.scraper import fetch_page_title


@pytest.mark.asyncio
async def test_fetch_page_title(monkeypatch):
    async def mock_send(request):
        html = '<html><head><title>Test</title></head><body></body></html>'
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

    monkeypatch.setattr(httpx, 'AsyncClient', DummyAsyncClient)
    title = await fetch_page_title('http://example.com')

    assert title == 'Test'
