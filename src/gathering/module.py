"""Crawer method to extract wiki links"""

import csv
import logging

import requests
from bs4 import BeautifulSoup


def request_link(
    url: str,
    url_base: str,
    wiki_special: str = "/wiki/Special:AllPages",
    url_wiki: list = list(),
    broken_url: list = list(),
    controller: list = list(),
):
    """
    Request link from `url` and extract all wiki links
    Args:
        url (str): The URL to request
        url_base (str): The base URL
        wiki_special (str): The special wiki URL
        url_wiki (list): The list of wiki URLs
        broken_url (list): The list of broken URLs
        controller (list): The controller list
    Returns:
        list: The list of wiki URLs
        list: The list of broken URLs
    """
    try:
        # request HTML page
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        soup = soup.find(class_="mw-body-content")
        # get page links
        links = soup.find_all("a")
        urls_and_titles = [(link.get("href")) for link in links]

        # controllers
        next_page_url = list()

        # for each page
        for i in urls_and_titles:
            logging.debug("website:", i)
            _url = i if i.startswith(url_base) else url_base + i

            # Get next page
            if _url.startswith(f"{url_base}{wiki_special}") and _url not in controller:
                controller.append(_url)
                next_page_url.append(_url)
            # Get useful content URL
            elif _url not in url_wiki and i is not None and "/wiki" in i:
                url_wiki.append(_url)

        # request next page
        if len(next_page_url):
            _next_page = next_page_url.pop()
            url_wiki, broken_url = request_link(
                url=_next_page,
                url_base=url_base,
                url_wiki=url_wiki,
                broken_url=broken_url,
                controller=controller,
            )

    except requests.exceptions.RequestException:
        broken_url.append(url)

    return url_wiki, broken_url


def create_csv(filename: str, urls: list):
    """
    Create a CSV from `urls`
    Args:
        filename (str): The filename
        urls (list): The list of URLs
    """
    with open(filename, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["url"])

        for _, url in enumerate(urls):
            if url is not None:
                writer.writerow([url])
