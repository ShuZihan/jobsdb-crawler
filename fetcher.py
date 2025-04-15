import aiohttp
import logging


BASE_URL = "https://hk.jobsdb.com/api/jobsearch/v5/search"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


async def fetch_page(params: dict) -> dict:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(BASE_URL, params=params, timeout=10) as resp:
            logging.debug(f"Request URL: {resp.url}")
            return await resp.json()
