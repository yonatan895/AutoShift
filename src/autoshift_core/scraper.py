from typing import Dict, Optional

import httpx
from bs4 import BeautifulSoup


async def fetch_page_title(url: str) -> Optional[str]:
    """Fetch a page and return its title."""
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.title.string if soup.title else None


async def fetch_metrics(url: str) -> Dict[str, str]:
    """Fetch a monitoring page and parse a table of key/value metrics."""
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        metrics = {}
        for row in soup.select("table.metrics tr"):
            cols = [c.get_text(strip=True) for c in row.find_all("td")]
            if len(cols) == 2:
                metrics[cols[0]] = cols[1]
        return metrics
