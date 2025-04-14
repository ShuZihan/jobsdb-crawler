import csv
import os


def save_to_csv(data: list, config: dict):
    os.makedirs(config["output_dir"], exist_ok=True)
    filepath = os.path.join(
        config["output_dir"],
        f"{config['site_key']}_{config['keywords']}_{config['work_type']}.csv",
    )

    keys = data[0].keys()
    with open(filepath, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        if os.stat(filepath).st_size == 0:
            writer.writeheader()
        for row in data:
            writer.writerow(row)
