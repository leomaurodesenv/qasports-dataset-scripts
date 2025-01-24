"""Extract context from texts"""

import json
import os
from pathlib import Path
from tqdm import tqdm
import pandas as pd


def split_text_into_chunks(file_path: str, chunk_size: int):
    """
    Extract context from texts
    Args:
        file_path (str): The file path
        chunk_size (int): The size of the text chunks
    Returns:
        list: The text chunks
    """
    text_chunks = list()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = json.load(file)

            # split the content into chunks of 256 characters
            for i in range(0, len(file_content["text"]), chunk_size):
                text_chunk = file_content["text"][i : i + chunk_size]
                text_chunks.append(
                    {
                        "context": text_chunk,
                        "url": file_content["url"],
                        "title": file_content["title"],
                        "date": file_content["date"],
                        "categories": ", ".join(file_content["categories"]),
                    }
                )

    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return text_chunks


def split_text_from_files(input_folder: str, output_file: str, chunk_size: int = 256):
    """Extract chunks from files
    Args:
        input_folder (str): The input folder
        output_file (str): The output file
        chunk_size (int): The size of the text chunks
    """
    # initialize a list to hold all the text chunks
    every_chunks = list()

    # loop through each file in the input folder
    print(f"Reading files from {input_folder}")
    for filename in tqdm(os.listdir(input_folder), desc="Reading files"):
        file_path = Path(input_folder) / filename
        # only process text files
        if os.path.isfile(file_path) and filename.endswith(".json"):
            text_chunks = split_text_into_chunks(file_path, chunk_size)
            every_chunks = every_chunks + text_chunks

    # write the CSV file
    df = pd.DataFrame(every_chunks)
    df.to_csv(output_file, index=False, encoding="utf-8")

    print(df.sample())
    print(f"Saved {output_file}: {df.shape}")
