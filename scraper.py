"""
scraper.py

Scrapes the official Python Tutorial documentation and stores
the extracted content in data/raw_data.json

Author: Your Name
"""

import os
import json
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

BASE_URL = "https://docs.python.org/3/tutorial/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Python Documentation Chatbot Project)"
}

visited = set()
documents = []


# ---------------------------------------------------
# Download a page
# ---------------------------------------------------

def get_soup(url):
    """
    Downloads a webpage and returns BeautifulSoup object.
    """

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

        return BeautifulSoup(response.text, "lxml")

    except Exception as e:
        print(f"Failed to open {url}")
        print(e)
        return None


# ---------------------------------------------------
# Extract title and paragraphs
# ---------------------------------------------------

def extract_page(url):
    """
    Extracts title and all paragraph text from a page.
    """

    if url in visited:
        return

    print(f"Scraping -> {url}")

    visited.add(url)

    soup = get_soup(url)

    if soup is None:
        return

    article = soup.find("div", class_="body")

    if article is None:
        print("No content found.")
        return

    title = soup.find("h1")

    if title:
        title = title.get_text(strip=True)
    else:
        title = "Untitled"

    paragraphs = []

    for p in article.find_all("p"):
        text = p.get_text(" ", strip=True)

        if len(text) > 30:
            paragraphs.append(text)

    content = "\n".join(paragraphs)

    if len(content) > 100:
        documents.append(
            {
                "title": title,
                "url": url,
                "content": content
            }
        )


# ---------------------------------------------------
# Collect tutorial chapter links
# ---------------------------------------------------

def collect_links():
    """
    Collects tutorial chapter links from the main page.
    """

    soup = get_soup(BASE_URL)

    links = []

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if href.endswith(".html"):

            full_url = urljoin(BASE_URL, href)

            if full_url.startswith(BASE_URL):

                if full_url not in links:
                    links.append(full_url)

    return links


# ---------------------------------------------------
# Save JSON
# ---------------------------------------------------

def save_json():
    """
    Saves scraped pages to data/raw_data.json.
    Creates the data folder if it doesn't exist.
    """

    os.makedirs("data", exist_ok=True)

    with open(
        "data/raw_data.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            documents,
            f,
            indent=4,
            ensure_ascii=False
        )

# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():

    print("=" * 60)
    print("Python Documentation Scraper")
    print("=" * 60)

    links = collect_links()

    print(f"\nFound {len(links)} tutorial pages.\n")

    for link in links:

        extract_page(link)

        time.sleep(1)

    save_json()

    print("\nFinished!")

    print(f"Pages scraped : {len(documents)}")

    print("Saved to data/raw_data.json")


if __name__ == "__main__":
    main()