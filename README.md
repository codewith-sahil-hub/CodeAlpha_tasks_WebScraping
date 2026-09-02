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

- Python 3
- `requests` — HTTP fetching
- `beautifulsoup4` — HTML parsing
- `csv` — dataset export

## How to run

```bash
pip install requests beautifulsoup4
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
