"""Crawer Function to extract wiki links"""
import csv
import logging

import requests
from bs4 import BeautifulSoup


def Request(
    url: str,
    url_base: str,
    wiki_special: str = "/wiki/Special:AllPages",
    url_wiki: list = list(),
    other_url: list = list(),
    broken_url: list = list(),
    controller: list = list(),
):
    """Collect all wiki links"""
    # count number of links
    num_links = len(url_wiki)

    try:
        # request HTML page
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        soup = soup.body.contents[7].contents[5].contents[3]
        # get page links
        links = soup.find_all("a")
        urls_and_titles = [(link.get("href")) for link in links]

        # controllers
        alternador = 1
        proxima = -1

        # for each page
        for i in urls_and_titles:
            logging.debug("website:", i)
            if i not in url_wiki:
                if i is not None and "/wiki" in i:
                    if i.startswith(url_base):
                        num_links += 1
                        url_wiki.append(i)
                    else:
                        i = url_base + i  # adiciona o prefixo da URL
                        num_links += 1
                        url_wiki.append(i)

            elif i == "/Blog:Recent_posts":
                i = url_base + i
                num_links += 1
                url_wiki.append(i)
            else:
                other_url.append((i))

            if i.startswith(f"{url_base}{wiki_special}"):
                if alternador == -1 or num_links < 376:
                    # print(i)
                    if i not in controller:
                        controller.append(i)
                        proxima = i
                    alternador = alternador * -2
                else:
                    alternador = alternador * -1

        # request next page
        if proxima != -1:
            url_wiki, other_url, broken_url = Request(
                url=proxima,
                url_base=url_base,
                url_wiki=url_wiki,
                other_url=other_url,
                broken_url=broken_url,
                controller=controller,
            )

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        broken_url.append(url)

    return url_wiki, other_url, broken_url


def create_csv(filename: str, urls: list):
    """Create a CSV from `urls`"""
    with open(filename, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "url"])

        for i, url in enumerate(urls):
            if url != None:
                writer.writerow([i, url])
