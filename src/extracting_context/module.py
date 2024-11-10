import json
import os
from pathlib import Path

import pandas as pd


def split_text_into_chunks(input_folder, output_file, chunk_size = 256):
    """Extract context from texts"""
    # initialize a list to hold all the text chunks
    text_chunks = []

    # lLoop through each file in the input folder
    for filename in os.listdir(input_folder):
        file_path = Path(input_folder) / filename

        # only process text files
        if os.path.isfile(file_path) and filename.endswith('.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = json.load(file)

                    # split the content into chunks of 256 characters
                    for i in range(0, len(file_content["text"]), chunk_size):
                        text_chunk = file_content["text"][i:i+chunk_size]
                        text_chunks.append({
                            "context": text_chunk,
                            "url": file_content["url"],
                            "title": file_content["title"],
                            "date": file_content["date"],
                            "categories": ", ".join(file_content["categories"]),
                        })

            except Exception as e:
                print(f"Error reading {filename}: {e}")

    # write the CSV file
    df = pd.DataFrame(text_chunks)
    df.to_csv(output_file, index=False, encoding='utf-8')

    print(df.head(5))
    print(f"quantity: {df.shape}")
