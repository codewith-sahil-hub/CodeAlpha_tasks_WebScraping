"""
Custom Dataset Example: Price/Product Comparison Analysis
============================================================
This builds on web_scraper_template.py to show what "tailoring a dataset
to a specific analysis need" actually means in practice.

ANALYSIS GOAL (defined up front, before writing any scraping code):
    "Which product categories have the best-rated items at the
    lowest prices, and how does availability affect that?"

That question drives every decision below:
  - WHICH fields to extract   -> price, rating, category, stock status
  - WHAT to compute            -> price bucket, value score
  - HOW to structure the CSV   -> one row per product, analysis-ready types

Target site: http://books.toscrape.com (a public sandbox site built for
practicing scraping — safe to use for learning).
"""

import csv
import re
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/catalogue/page-{page}.html"
MAX_PAGES = 5
DELAY_SECONDS = 1
OUTPUT_CSV = "product_price_analysis.csv"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; DataCollectionBot/1.0)"}

# Star ratings on the site are written as CSS classes like "One", "Two"...
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch_page(url: str) -> str | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.text
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {url}: {e}")
        return None


def price_bucket(price: float) -> str:
    """Turn a raw price into an analysis-friendly category."""
    if price < 15:
        return "budget"
    elif price < 35:
        return "mid-range"
    return "premium"


def parse_page(html: str) -> list[dict]:
    """
    Extract ONLY the fields the analysis question needs — not every
    field available on the page. This is the "tailoring" step.
    """
    soup = BeautifulSoup(html, "html.parser")
    records = []

    for product in soup.select("article.product_pod"):
        title = product.select_one("h3 a")["title"]

        price_text = product.select_one(".price_color").get_text(strip=True)
        price = float(re.sub(r"[^\d.]", "", price_text))

        rating_class = product.select_one("p.star-rating")["class"][1]
        rating = RATING_WORDS.get(rating_class, None)

        availability = product.select_one(".availability").get_text(strip=True)
        in_stock = "In stock" in availability

        # --- Derived fields, computed because the analysis needs them ---
        value_score = round((rating or 0) / price, 3) if price > 0 else None

        records.append({
            "title": title,
            "price_gbp": price,
            "price_bucket": price_bucket(price),
            "rating_stars": rating,
            "in_stock": in_stock,
            "value_score": value_score,  # higher = better rating per £ spent
        })

    return records


def scrape_dataset(max_pages: int = MAX_PAGES) -> list[dict]:
    all_records = []
    for page_num in range(1, max_pages + 1):
        url = BASE_URL.format(page=page_num)
        print(f"Scraping: {url}")
        html = fetch_page(url)
        if not html:
            break
        page_records = parse_page(html)
        if not page_records:
            break
        all_records.extend(page_records)
        time.sleep(DELAY_SECONDS)
    return all_records


def save_to_csv(records: list[dict], filename: str) -> None:
    if not records:
        print("No records to save.")
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(f"Saved {len(records)} records to {filename}")


if __name__ == "__main__":
    data = scrape_dataset()
    save_to_csv(data, OUTPUT_CSV)
