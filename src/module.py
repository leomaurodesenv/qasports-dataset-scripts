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
    {
        "url": "https://internationalcricket.fandom.com/wiki/Special:AllPages",
        "url_base": "https://internationalcricket.fandom.com",
        "sport_name": "cricket",
    },
    {
        "url": "https://internationalhockey.fandom.com/wiki/Special:AllPages",
        "url_base": "https://internationalhockey.fandom.com",
        "sport_name": "hockey",
    },
    {
        "url": "https://golf.fandom.com/wiki/Special:AllPages",
        "url_base": "https://golf.fandom.com",
        "sport_name": "golf",
    },
    {
        "url": "https://rugbyunion.fandom.com/wiki/Special:AllPages",
        "url_base": "https://rugbyunion.fandom.com",
        "sport_name": "rugbyunion",
    },
    {
        "url": "https://rugby.fandom.com/wiki/Special:AllPages",
        "url_base": "https://rugby.fandom.com",
        "sport_name": "rugby",
    },
    {
        "url": "https://baseball.fandom.com/wiki/Baseball",
        "url_base": "https://baseball.fandom.com",
        "sport_name": "baseball",
    },
    {
        "url": "https://martialarts.fandom.com/wiki/Special:AllPages",
        "url_base": "https://martialarts.fandom.com",
        "sport_name": "martialarts",
    },
    {
        "url": "https://boxing.fandom.com/wiki/Special:AllPages",
        "url_base": "https://boxing.fandom.com",
        "sport_name": "boxing",
    },
    {
        "url": "https://mixedmartialarts.fandom.com/wiki/Special:AllPages",
        "url_base": "https://mixedmartialarts.fandom.com",
        "sport_name": "mixedmartialarts",
    },
    {
        "url": "https://fitness.fandom.com/wiki/Special:AllPages",
        "url_base": "https://fitness.fandom.com",
        "sport_name": "fitness",
    }
]

wiki_pages = [dict(item, **{"csv_name": f'{item["sport_name"]}-links.csv'}) for item in wiki_pages]
wiki_pages = [dict(item, **{"context_name": f'{item["sport_name"]}-contexts.csv'}) for item in wiki_pages]
wiki_pages = [dict(item, **{"qa_name": f'{item["sport_name"]}-qa.csv'}) for item in wiki_pages]
