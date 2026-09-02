"""
Web Scraper Template
=====================
A reusable, well-structured scraper built with requests + BeautifulSoup.

WHAT THIS DOES
--------------
1. Fetches a page (with polite headers + error handling)
2. Parses the HTML structure
3. Extracts data into a list of dictionaries
4. Saves the result to a CSV file for analysis

HOW TO CUSTOMIZE
-----------------
This script scrapes http://quotes.toscrape.com (a site built specifically
for practicing scraping) as a working example. To adapt it to a real target:

1. Change TARGET_URL below.
2. Open the target page in your browser, right-click an element you want
   to extract, and choose "Inspect" to see its HTML tag/class.
3. Update the `parse_page()` function's selectors to match.
4. Respect the site's robots.txt and Terms of Service before scraping.

INSTALL DEPENDENCIES
---------------------
    pip install requests beautifulsoup4 --break-system-packages
"""

import csv
import time
import requests
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------
TARGET_URL = "http://quotes.toscrape.com/page/{page}/"
MAX_PAGES = 3           # how many pages to crawl
DELAY_SECONDS = 1       # polite delay between requests
OUTPUT_CSV = "scraped_data.csv"

HEADERS = {
    # Identifying your scraper honestly is good practice
    "User-Agent": "Mozilla/5.0 (compatible; DataCollectionBot/1.0)"
}


def fetch_page(url: str) -> str | None:
    """Fetch raw HTML from a URL, handling common errors gracefully."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None


def parse_page(html: str) -> list[dict]:
    """
    Parse a single page's HTML and extract structured records.
    Customize the selectors here for your target site.
    """
    soup = BeautifulSoup(html, "html.parser")
    records = []

    for quote_block in soup.select(".quote"):
        text = quote_block.select_one(".text")
        author = quote_block.select_one(".author")
        tags = [tag.get_text(strip=True) for tag in quote_block.select(".tag")]

        records.append({
            "quote": text.get_text(strip=True) if text else None,
            "author": author.get_text(strip=True) if author else None,
            "tags": ", ".join(tags),
        })

    return records


def scrape_site(max_pages: int = MAX_PAGES) -> list[dict]:
    """Crawl multiple pages and collect all records."""
    all_records = []

    for page_num in range(1, max_pages + 1):
        url = TARGET_URL.format(page=page_num)
        print(f"Scraping: {url}")

        html = fetch_page(url)
        if not html:
            break

        page_records = parse_page(html)
        if not page_records:
            print("No more data found, stopping.")
            break

        all_records.extend(page_records)
        time.sleep(DELAY_SECONDS)  # be polite to the server

    return all_records


def save_to_csv(records: list[dict], filename: str) -> None:
    """Save extracted records to a CSV file."""
    if not records:
        print("No records to save.")
        return

    fieldnames = records[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Saved {len(records)} records to {filename}")


if __name__ == "__main__":
    data = scrape_site()
    save_to_csv(data, OUTPUT_CSV)
