"""
dataset_builder.py

Converts clean_data.json into a single training text file
for MiniGPT.

Author: Your Name
"""

import json
import os

INPUT_FILE = "data/clean_data.json"
OUTPUT_FILE = "dataset.txt"


def build_dataset():

    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)

    total_chunks = len(documents)

    print(f"Loaded {total_chunks} chunks.")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:

        for doc in documents:

            title = doc["title"]
            content = doc["content"]

            out.write(f"Title: {title}\n")
            out.write(content)
            out.write("\n\n")
            out.write("=" * 80)
            out.write("\n\n")

    print(f"\nDataset created successfully!")

    print(f"Saved as: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_dataset()