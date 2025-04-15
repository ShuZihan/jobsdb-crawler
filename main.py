import yaml
import os
import logging
import asyncio
from tqdm.asyncio import tqdm_asyncio

from logger import init_logger
from fetcher import fetch_page
from parser import parse_items
from saver import save_to_csv


# load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# init logger
init_logger(config)


# TODO: record mission elapsed time
async def crawl_all():
    results = []
    sem = asyncio.Semaphore(config["concurrent_limit"])

    # TODO: read existing jobs from csv

    first_page_param = {
        "siteKey": config["site_key"],
        "locale": config["locale"],
        "keywords": config["keywords"],
        "worktype": config["work_type"],
        "pageSize": config["page_size"],
        "page": 1,
    }

    await fetch_page(first_page_param)
    try:
        first_res = await fetch_page(first_page_param)
        total_count = first_res.get("totalCount", 0)
        total_pages = (total_count + config["page_size"] - 1) // config["page_size"]
        if config["max_page"] == -1:
            page_limit = total_pages  # crawl all pages
        else:
            page_limit = min(config["max_page"], total_pages)
        logging.info(
            f"totalCount: {total_count}, totalPages: {total_pages}, pages to crawl = {page_limit}"
        )
    except Exception as e:
        logging.error(f"❌ Failed to fetch first page: {e}")
        return

    async def crawl_one(params):
        async with sem:
            try:
                res = await fetch_page(params)
                jobs = parse_items(res["data"])
                results.extend(jobs)
                logging.debug(f"Page {params['page']} fetched, {len(jobs)} new items.")
            except Exception as e:
                logging.error(f"❌ Error on page: {params['page']}: {e}")

    tasks = [
        crawl_one(
            {
                "siteKey": config["site_key"],
                "locale": config["locale"],
                "keywords": config["keywords"],
                "worktype": config["work_type"],
                "pageSize": config["page_size"],
                "page": p,
            }
        )
        for p in range(1, page_limit + 1)
    ]
    await tqdm_asyncio.gather(*tasks)
    save_to_csv(results, config)


if __name__ == "__main__":
    asyncio.run(crawl_all())
    logging.info("✅ Crawling completed!")
