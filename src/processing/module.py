import json
import os
import re
from pathlib import Path

from bs4 import BeautifulSoup
from tqdm import tqdm
from unidecode import unidecode


def clean_text(text: str):
    """Clean textual data"""
    text = unidecode(text)
    text = text.replace("\n", " ")
    text = text.replace("\\", " ")
    text = re.sub(r"[ ]+", " ", text)
    return text.strip()


def process_html(folder_path: str, output_path: str):
    """Process and clen HTML textual data"""
    # create output path
    Path(output_path).mkdir(parents=True, exist_ok=True)
    for filename in tqdm(os.listdir(folder_path)):
        # open file
        file_path = str(Path(folder_path) / filename)
        with open(file_path, "r") as file:
            data = json.load(file)

        # parse htlm
        soup = BeautifulSoup(data["html"], "html.parser")
        content = soup.find(class_="mw-parser-output")
        if content != None:
            # infobox
            infobox = content.find(class_="infobox")
            if infobox != None:
                infobox = infobox.extract().get_text()
                infobox = clean_text(text=infobox)
                if infobox.startswith(" NOTE: This"):
                    infobox = ""
            else:
                infobox = ""
            data["infobox"] = clean_text(infobox)

            # body content
            body = content.get_text()
            body = clean_text(text=body)
            body = body.split("See also")[0]
            body = body.split("External links")[0]
            body = body.split("References")[0]

            data["text"] = body.strip()
            data["title"] = data["title"][0]
            data["categories"] = [clean_text(item) for item in data["categories"]]
            data.pop("html")

            file_output = str(Path(output_path) / filename)
            with open(file_output, "w") as file:
                file.write(json.dumps(data))
