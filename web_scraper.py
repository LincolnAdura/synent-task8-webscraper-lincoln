# ============================================
# Synent Technologies - Python Internship
# Task 8: Web Scraper (Advanced Level)
# Developer: Lincoln Adura
# ============================================

import requests
from bs4 import BeautifulSoup # pyright: ignore[reportMissingImports]
import json
import csv
import os
from datetime import datetime

def scrape_quotes():
    print("\n" + "=" * 55)
    print("           SCRAPING QUOTES...")
    print("=" * 55)

    url = "http://quotes.toscrape.com"
    all_quotes = []
    page = 1

    while True:
        print(f"  📄 Scraping page {page}...")
        response = requests.get(f"{url}/page/{page}/")

        if response.status_code != 200:
            print(f"❌ Failed to fetch page {page}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")

        if not quotes:
            break

        for quote in quotes:
            text = quote.find("span", class_="text").get_text()
            author = quote.find("small", class_="author").get_text()
            tags = [tag.get_text() for tag in
                    quote.find_all("a", class_="tag")]

            all_quotes.append({
                "id": len(all_quotes) + 1,
                "quote": text,
                "author": author,
                "tags": tags,
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        next_page = soup.find("li", class_="next")
        if not next_page:
            break

        page += 1

    return all_quotes

def display_quotes(quotes, limit=5):
    print("\n" + "=" * 55)
    print("           SCRAPED QUOTES PREVIEW")
    print("=" * 55)

    for quote in quotes[:limit]:
        print(f"\n  📌 Quote #{quote['id']}")
        print(f"  {quote['quote']}")
        print(f"  — {quote['author']}")
        print(f"  🏷️  Tags: {', '.join(quote['tags'])}")
        print("-" * 55)

    print(f"\n  ✅ Total quotes scraped: {len(quotes)}")
    print("=" * 55)

def save_to_json(quotes):
    filename = "scraped_quotes.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(quotes, f, indent=4, ensure_ascii=False)
    print(f"\n✅ Data saved to {filename}")

def save_to_csv(quotes):
    filename = "scraped_quotes.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "quote", "author", "tags", "scraped_at"])
        writer.writeheader()
        for quote in quotes:
            quote_copy = quote.copy()
            quote_copy["tags"] = ", ".join(quote["tags"])
            writer.writerow(quote_copy)
    print(f"✅ Data saved to {filename}")

def web_scraper():
    print("=" * 55)
    print("   Synent Technologies - Web Scraper")
    print("          Advanced Level Task 8")
    print("=" * 55)
    print("  Scraping data from: quotes.toscrape.com")
    print("=" * 55)

    while True:
        print("\nOptions:")
        print("  1. Scrape quotes and preview data")
        print("  2. Scrape and save to JSON")
        print("  3. Scrape and save to CSV")
        print("  4. Scrape and save to both JSON and CSV")
        print("  5. Exit")
        print("-" * 55)

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            quotes = scrape_quotes()
            display_quotes(quotes)

        elif choice == "2":
            quotes = scrape_quotes()
            display_quotes(quotes)
            save_to_json(quotes)

        elif choice == "3":
            quotes = scrape_quotes()
            display_quotes(quotes)
            save_to_csv(quotes)

        elif choice == "4":
            quotes = scrape_quotes()
            display_quotes(quotes)
            save_to_json(quotes)
            save_to_csv(quotes)

        elif choice == "5":
            print("\nGoodbye! Happy scraping! 👋")
            break

        else:
            print("❌ Invalid choice! Please select 1-5.")

if __name__ == "__main__":
    web_scraper()