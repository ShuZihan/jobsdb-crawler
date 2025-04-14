import logging


def parse_items(items: list):
    # logging.info(res["data"])
    return [parse_item(item) for item in items]


def parse_item(item: dict) -> dict:
    return {
        "job_id": item.get("id"),
        "title": item.get("title"),
        "classification": ", ".join(
            f"{c.get('subclassification', {}).get('description')} ({c.get('classification', {}).get('description')})"
            for c in item.get("classifications", [])
        ),
        "tags": ", ".join(tag.get("label", "") for tag in item.get("tags", [])),
        "teaser": item.get("teaser"),
        "company_name": item.get("companyName")
        or item.get("advertiser", {}).get("description"),
        "location": item.get("locations", [{}])[0].get("label"),
        "work_type": item.get("workTypes", [None])[0],
        "work_arrangement": item.get("workArrangements", {})
        .get("data", [{}])[0]
        .get("label", {})
        .get("text"),
        "listing_date": item.get("listingDate"),
        "bullet_points": "; ".join(item.get("bulletPoints", [])),
        "salary": item.get("salaryLabel") or "",
        "apply_url": f"https://hk.jobsdb.com/job/{item.get('id')}",
    }
