import yaml
import os
import logging
import asyncio
from tqdm.asyncio import tqdm_asyncio

from logger import init_logger
from fetcher import fetch_page
from parser import parse_items
from file_utils import save_to_csv, load_from_csv
from func_utils import timing


# load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# init logger
init_logger(config)


@timing
async def crawl_all():
    results = []
    sem = asyncio.Semaphore(config["concurrent_limit"])
    filename = f"{config['site_key']}_{config['keywords']}_{config['work_type']}.csv"

    # read existing job_id from csv
    existing_job_id = {job.get("job_id") for job in load_from_csv(config, filename)}
    logging.info(f"Existing jobs: {len(existing_job_id)}")

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

                # remove existing jobs
                new_jobs = [
                    job for job in jobs if job.get("job_id") not in existing_job_id
                ]
                results.extend(new_jobs)
                logging.debug(
                    f"Page {params['page']} fetched, {len(new_jobs)} new items."
                )
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

    if results:
        save_to_csv(results, config, filename)


if __name__ == "__main__":
    asyncio.run(crawl_all())
    logging.info("✅ Crawling completed!")
