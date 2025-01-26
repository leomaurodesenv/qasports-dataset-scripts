"""Module to process and clean HTML textual data"""

import json
import os
import re
from pathlib import Path

from bs4 import BeautifulSoup
from tqdm import tqdm
from unidecode import unidecode


def clean_text(text: str):
    """
    Clean textual data
    Args:
        text (str): The text to clean
    Returns:
        str: The cleaned text
    """
    text = unidecode(text)
    text = text.replace("\n", " ")
    text = text.replace("\\", " ")
    text = re.sub(r"[ ]+", " ", text)
    return text.strip()


def process_html(file_path: str):
    """
    Process the HTML files
    Args:
        file_path (str): The file path containing the HTML files
    Returns:
        dict: The processed data
    """
    with open(file_path, "r") as file:
        data = json.load(file)

    # parse htlm
    soup = BeautifulSoup(data["html"], "html.parser")
    content = soup.find(class_="mw-parser-output")
    if content is not None:
        # infobox
        infobox = content.find(class_="infobox")
        if infobox is not None:
            infobox = infobox.extract().get_text()
            if infobox.startswith(" NOTE: This"):
                infobox = ""
        else:
            infobox = ""
        data["infobox"] = clean_text(infobox)

        # remove table content
        [table.extract() for table in content.find_all("table")]

        # body content
        body = content.get_text()
        body = clean_text(text=body)
        body = body.split("See also")[0]
        body = body.split("External links")[0]
        body = body.split("References")[0]

        data["text"] = body.strip()
        data["title"] = clean_text(data["title"][0])
        data["categories"] = [clean_text(item) for item in data["categories"]]
        data.pop("html")

        return data


def process_all_html(folder_path: str, output_path: str):
    """
    Process the HTML files
    Args:
        folder_path (str): The folder path containing the HTML files
        output_path (str): The output path to save the processed files
    """
    # create output path
    Path(output_path).mkdir(parents=True, exist_ok=True)
    print(f"Processing HTML files from {folder_path}")
    for filename in tqdm(os.listdir(folder_path), desc="Processing HTML"):
        file_path = str(Path(folder_path) / filename)
        data = process_html(file_path=file_path)

        # save output document
        file_output = str(Path(output_path) / filename)
        with open(file_output, "w") as file:
            file.write(json.dumps(data))
