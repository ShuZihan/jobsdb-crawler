import csv
import os


def save_to_csv(data: list, config: dict, filename: str):
    os.makedirs(config["output_dir"], exist_ok=True)
    filepath = os.path.join(config["output_dir"], filename)

    keys = data[0].keys()
    with open(filepath, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        if os.stat(filepath).st_size == 0:
            writer.writeheader()
        for row in data:
            writer.writerow(row)


def load_from_csv(config: dict, filename: str):
    path = os.path.join(config["output_dir"], filename)
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)
