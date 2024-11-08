from ..module import OUTPUT_PATH
from .module import create_csv, request_link

wiki_pages = [
    {
        "url": "https://basketball.fandom.com/wiki/Special:AllPages",
        "url_base": "https://basketball.fandom.com",
        "csv_name": "basketball-links.csv"
    },
    {
        "url": "https://football.fandom.com/wiki/Special:AllPages",
        "url_base": "https://football.fandom.com",
        "csv_name": "football-links.csv"
    },
    {
        "url": "https://americanfootball.fandom.com/wiki/Special:AllPages",
        "url_base": "https://americanfootball.fandom.com",
        "csv_name": "americanfootball-links.csv"
    },
]

# Get the URLs
for wiki_page in wiki_pages:
    url, url_base, csv_name = wiki_page["url"], wiki_page["url_base"], wiki_page["csv_name"]
    url_wiki, broken_url = request_link(url=url, url_base=url_base, url_wiki = list())
    print(f"{csv_name}:", len(url_wiki), "broken urls:", len(broken_url))
    create_csv(filename=(OUTPUT_PATH / csv_name), urls=url_wiki)
