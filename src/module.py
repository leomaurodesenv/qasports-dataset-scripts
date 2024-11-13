from pathlib import Path

# Global variables
OUTPUT_PATH = Path("./output")
RAW_HTML_PATH = OUTPUT_PATH / Path("raw_html/")
CLEAN_JSON_PATH = OUTPUT_PATH / Path("clean_json/")

# Wiki page config
TESTING = True
wiki_pages = [
    {
        "url": "https://basketball.fandom.com/wiki/Special:AllPages",
        "url_base": "https://basketball.fandom.com",
        "sport_name": "basketball",
    },
    {
        "url": "https://football.fandom.com/wiki/Special:AllPages",
        "url_base": "https://football.fandom.com",
        "sport_name": "football",
    },
    {
        "url": "https://americanfootball.fandom.com/wiki/Special:AllPages",
        "url_base": "https://americanfootball.fandom.com",
        "sport_name": "americanfootball",
    },
]

wiki_pages = [dict(item, **{"csv_name": f'{item["sport_name"]}-links.csv'}) for item in wiki_pages]
wiki_pages = [dict(item, **{"csv_name": f'{item["sport_name"]}-links.csv'}) for item in wiki_pages]
