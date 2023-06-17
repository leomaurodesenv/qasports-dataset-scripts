import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def fetch_html(url: str, folder_path: str):
    """Fetching one url"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        Path(folder_path).mkdir(parents=True, exist_ok=True)
        file_name = (
            soup.title.contents[0]
            .split("|")[0][0:-1]
            .replace(" ", "_")
            .replace("/", "_")
            .replace(":", "_")
            .replace("?", "")
            .replace('"', "")
            .replace("'", "")
            + ".json"
        )
        file_name = str(Path(folder_path) / file_name)

        if len(file_name) > 90:
            file_name = file_name[0:80] + ".json"

        # if(not os.path.isfile(FileName)):
        f = open(file_name, "w")

        instance = {}

        instance["url"] = url
        instance["title"] = soup.title.contents

        # CATEGORIAS
        cat = soup.find(class_="page-header__categories")

        if cat != None:
            cat = cat.get_text().split("\n")
            if "\t" in cat[-1]:
                all_content = cat[2:-1][0]
            else:
                all_content = cat[2:][0]
        else:
            all_content = " "

        cat = soup.find(class_="page-header__categories-dropdown-content")
        if cat != None:
            cat = cat.get_text().split("\n")
            for i in range(0, len(cat)):
                if i != "":
                    all_content = all_content + "," + cat[i]
            all_content = all_content.split(",")
        else:
            if all_content != " ":
                all_content = all_content.split(",")

        categories = []
        if all_content != " ":
            for i in all_content:
                if i != "," and i != "and" and i != "" and i != " \t\t\t":
                    categories.append(i)

        # print(categorias)
        instance["categories"] = categories

        # DATA DE COLETA
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        instance["date"] = dt_string

        instance["html"] = str(response.content, encoding="UTF-8")

        f.write(json.dumps(instance))
        f.close()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)


def fetch_all_html(links_path: str, folder_path: str, test: bool = False):
    """Fetching all urls in CSV"""
    df = pd.read_csv(links_path)
    print(f"{folder_path}:", df.shape[0])
    for i, row in tqdm(df.iterrows()):
        fetch_html(url=row["url"], folder_path=folder_path)
        if test and i > 9:
            break
