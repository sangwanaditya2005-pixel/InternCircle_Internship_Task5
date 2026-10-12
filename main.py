
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


def scrape_headlines():
    url = "https://quotes.toscrape.com/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")

        results = []

        for item in quotes:
            quote = item.find("span", class_="text")
            author = item.find("small", class_="author")

            if quote and author:
                results.append({
                    "quote": quote.get_text(strip=True),
                    "author": author.get_text(strip=True)
                })

        if not results:
            print("No quotes found.")
            return

        filename = "quotes.json"

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4, ensure_ascii=False)

        with open("quotes.txt", "w", encoding="utf-8") as file:
            for item in results:
                file.write(f"{item['quote']} — {item['author']}\n\n")

        print(f"Successfully extracted {len(results)} quotes.")
        print("Saved results to quotes.json and quotes.txt")

        for item in results:
            print(f"\n{item['quote']}")
            print(f"Author: {item['author']}")

    except requests.exceptions.RequestException as error:
        print("Network or HTTP error:", error)


def main():
    print("=== InternCircle Web Scraper ===")
    print("Extracting quotes from Quotes to Scrape...")

    scrape_headlines()


if __name__ == "__main__":
    main()
