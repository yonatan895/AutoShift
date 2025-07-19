import httpx
from bs4 import BeautifulSoup
from typing import Optional


async def fetch_page_title(url: str) -> Optional[str]:
    """Fetch a page and return its title."""
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.title.string if soup.title else None
