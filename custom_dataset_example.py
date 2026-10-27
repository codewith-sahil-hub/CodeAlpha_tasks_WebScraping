"""
Custom Dataset Example: Price/Product Comparison Analysis
========================================================
Analysis goal:
    Which price tiers offer the best-rated books at the lowest
    prices, and how does stock availability vary by tier?

Extracts title, price, rating, and stock status.
Computes price tiers and rating-per-pound value scores.

Requires Python 3.10+.
Output: product_price_analysis.csv
"""

import csv
import math
import re
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{page}.html"
MAX_PAGES = 5
DELAY_SECONDS = 1
OUTPUT_CSV = "product_price_analysis.csv"

HEADERS = {
    "User-Agent": "DataCollectionBot/1.0 (educational project)"
}

RATING_WORDS = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

FIELDNAMES = [
    "title",
    "price_gbp",
    "price_bucket",
    "rating_stars",
    "in_stock",
    "value_score",
]


def fetch_page(url: str) -> str | None:
    """Fetch a page and report connection or HTTP errors."""
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15,
        )
        response.raise_for_status()
        response.encoding = "utf-8"
        return response.text
    except requests.exceptions.RequestException as error:
        print(f"[ERROR] Failed to fetch {url}: {error}")
        return None


def price_bucket(price: float) -> str:
    """Classify a price into a price tier."""
    if price < 15:
        return "budget"
    if price < 35:
        return "mid-range"
    return "premium"


def parse_page(html: str) -> list[dict]:
    """Extract book records while handling missing fields."""
    soup = BeautifulSoup(html, "html.parser")
    records = []

    for product in soup.select("article.product_pod"):
        title_element = product.select_one("h3 a")
        price_element = product.select_one(".price_color")

        if title_element is None or price_element is None:
            print("[WARNING] Skipping a book with no title or price.")
            continue

        title = (
            title_element.get("title")
            or title_element.get_text(strip=True)
        ).strip()

        if not title:
            print("[WARNING] Skipping a book with an empty title.")
            continue

        price_text = price_element.get_text(strip=True)
        cleaned_price = re.sub(r"[^\d.]", "", price_text)

        try:
            price = float(cleaned_price)
        except ValueError:
            print(f"[WARNING] Invalid price for {title!r}. Skipping.")
            continue

        if not math.isfinite(price) or price < 0:
            print(f"[WARNING] Invalid price for {title!r}. Skipping.")
            continue

        # Find the rating regardless of CSS class order.
        rating_element = product.select_one("p.star-rating")
        rating = None

        if rating_element is not None:
            rating = next(
                (
                    RATING_WORDS[class_name]
                    for class_name in rating_element.get("class", [])
                    if class_name in RATING_WORDS
                ),
                None,
            )

        # Leave unknown availability blank in the CSV.
        availability_element = product.select_one(".availability")
        in_stock = None

        if availability_element is not None:
            availability = " ".join(
                availability_element.stripped_strings
            ).casefold()

            if "out of stock" in availability:
                in_stock = False
            elif "in stock" in availability:
                in_stock = True

        # Unknown ratings must not become a misleading zero score.
        value_score = (
            round(rating / price, 3)
            if rating is not None and price > 0
            else None
        )

        records.append({
            "title": title,
            "price_gbp": price,
            "price_bucket": price_bucket(price),
            "rating_stars": rating,
            "in_stock": in_stock,
            "value_score": value_score,
        })

    return records


def scrape_dataset(max_pages: int = MAX_PAGES) -> list[dict]:
    """Collect book records from consecutive catalogue pages."""
    all_records = []

    for page_num in range(1, max_pages + 1):
        if page_num > 1:
            time.sleep(DELAY_SECONDS)

        url = BASE_URL.format(page=page_num)
        print(f"Scraping: {url}")

        html = fetch_page(url)
        if html is None:
            print("[WARNING] Stopping; collected data may be incomplete.")
            break

        page_records = parse_page(html)
        if not page_records:
            print("No book records found. Stopping.")
            break

        all_records.extend(page_records)
        print(f"Collected {len(page_records)} books from this page.")

    return all_records


def save_to_csv(records: list[dict], filename: str) -> None:
    """Save records as a UTF-8 CSV."""
    if not records:
        print("No records to save.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)

    print(f"Saved {len(records)} records to {filename}")


if __name__ == "__main__":
    data = scrape_dataset()
    save_to_csv(data, OUTPUT_CSV)
