# CodeAlpha_WebScraping

## Task 1: Web Scraping — Data Analytics Internship (CodeAlpha)

This project scrapes structured data from a public website and exports it
into a clean CSV dataset for analysis.

## What it does

- Fetches HTML pages using `requests`
- Parses page structure using `BeautifulSoup`
- Extracts records (text fields + categorical tags) into structured rows
- Crawls multiple pages automatically
- Exports the collected dataset to `scraped_data.csv`
- Includes error handling and rate-limiting (1s delay) to scrape responsibly

## Tech stack

- Python 3.10 or newer
- `requests` — HTTP fetching
- `beautifulsoup4` — HTML parsing
- `csv` — dataset export

## How to run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python web_scraper_template.py
```

Output: `scraped_data.csv` in the same directory.

## Customizing for a different site

1. Update `TARGET_URL` in `web_scraper_template.py`.
2. Inspect the target page's HTML (right-click → Inspect) to find the
   CSS classes/tags around the data you want.
3. Update the selectors inside `parse_page()` to match.
4. Always check the site's `robots.txt` and Terms of Service before scraping.

## Example dataset produced

| quote | author | tags |
|---|---|---|
| (extracted quote text) | (extracted author) | (comma-separated tags) |

## Notes

This project was completed as part of the CodeAlpha Data Analytics
Internship — Task 1: Web Scraping.

## Product price analysis

Run from the project folder, with the virtual environment activated:

```bash
python custom_dataset_example.py
```

This collects up to five catalogue pages into `product_price_analysis.csv`.
Fields: title, price_gbp, price_bucket, rating_stars, in_stock, value_score.
Price tiers: budget below £15, mid-range £15 to below £35, premium £35+.
Value score is rating divided by price; unknown ratings and availability
are left blank. Product categories are not collected.

Both scripts require internet access. If a fetch fails, they stop and may
save a partial dataset; inspect the terminal warnings before using it.
CSV output is written to the current working directory and replaces any
existing file with the same name.
