"""
preprocess.py

Loads the scraped data, cleans it, splits it into chunks,
and saves the processed data.

Author: Your Name
"""

import json
import os
import re

INPUT_FILE = "data/raw_data.json"
OUTPUT_FILE = "data/clean_data.json"

CHUNK_SIZE = 800  # characters


def clean_text(text):
    """
    Remove extra whitespace and unwanted characters.
    """

    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text


def split_into_chunks(text, chunk_size=CHUNK_SIZE):
    """
    Split long text into smaller chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start = end

    return chunks


def main():

    if not os.path.exists(INPUT_FILE):
        print(f"{INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        pages = json.load(f)

    processed_data = []

    seen = set()

    total_chunks = 0

    for page in pages:

        title = page["title"]
        url = page["url"]

        content = clean_text(page["content"])

        if not content:
            continue

        chunks = split_into_chunks(content)

        for chunk in chunks:

            chunk = clean_text(chunk)

            if len(chunk) < 50:
                continue

            if chunk in seen:
                continue

            seen.add(chunk)

            processed_data.append(
                {
                    "title": title,
                    "url": url,
                    "content": chunk
                }
            )

            total_chunks += 1

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            processed_data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("=" * 50)
    print("Preprocessing Complete")
    print("=" * 50)

    print(f"Original Pages : {len(pages)}")
    print(f"Final Chunks   : {total_chunks}")
    print(f"Saved File     : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()