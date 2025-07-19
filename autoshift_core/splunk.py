import httpx
from typing import Any, Dict


class SplunkHECClient:
    def __init__(self, url: str, token: str) -> None:
        self.url = url.rstrip('/') + '/services/collector'
        self.token = token
        self.headers = {
            "Authorization": f"Splunk {self.token}"
        }

    async def send_event(self, event: Dict[str, Any], *, index: str = "main", sourcetype: str = "autoshift") -> None:
        payload = {
            "event": event,
            "index": index,
            "sourcetype": sourcetype,
        }
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(self.url, json=payload, headers=self.headers)
            response.raise_for_status()
