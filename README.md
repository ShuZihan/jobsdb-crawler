# JobsDB Crawler

This is an asynchronous Python crawler designed to extract job listing data from the [JobsDB Hong Kong](https://hk.jobsdb.com) platform via its public API.

📖 中文说明请见：[README.zh.md](README_zh.md)

## 🚀 Features

- Async + aiohttp for high-speed crawling
- Configurable keywords, work types, concurrency, and max pages
- Auto-detects total pages from the first request
- Logs to file and console without interfering with tqdm progress bar
- Parses classification, location, work type, and application URL
- Saves to UTF-8 CSV with BOM (Excel-friendly)

## 🛠️ Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run the crawler
python main.py
```

## ⚙️ Configuration (`config.yaml`)

```yaml
site_key: HK-Main
locale: en-HK
keywords: Operation # Multiple selections allowed, e.g., Operation,Marketing
work_type: 242 # Multiple selections allowed, e.g., 242,243
page_size: 32
max_page: -1 # -1 means crawl all pages

concurrent_limit: 10
output_dir: output/
log_dir: logs/
log_level: INFO
enable_console: true
skip_existing: true
```

## 📁 Project Structure

```
.
├── config.yaml          # Crawl config
├── main.py              # Entry point
├── fetcher.py           # Async GET request
├── parser.py            # Parse JSON data
├── saver.py             # Write to CSV
├── logger.py            # Logging config
├── requirements.txt
├── output/              # Saved results
├── logs/                # Log files
```

## 📦 Dependencies

- `aiohttp`
- `pyyaml`
- `tqdm`

## 📌 Notes

- The first page is always fetched first to calculate `totalCount` and total pages.
- `max_page: -1` means "no upper limit" — will crawl everything available.
