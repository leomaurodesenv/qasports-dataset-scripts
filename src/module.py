from pathlib import Path

# Global variables
OUTPUT_PATH = Path("./output")
RAW_HTML_PATH = OUTPUT_PATH / Path("raw_html/")
CLEAN_JSON_PATH = OUTPUT_PATH / Path("clean_json/")

# Wiki page config
TESTING = True


def generate_wiki_pages() -> list:
    """
    Generate a list of dictionaries containing the base pages for each sport.
    """
    base_pages = [
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
            "url": "https://baseball.fandom.com/wiki/Special:AllPages",
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
        },
        {
            "url": "https://cycling.fandom.com/wiki/Special:AllPages",
            "url_base": "https://cycling.fandom.com",
            "sport_name": "cycling",
        },
        {
            "url": "https://badminton.fandom.com/wiki/Special:AllPages",
            "url_base": "https://badminton.fandom.com",
            "sport_name": "badminton",
        },
        {
            "url": "https://wagymnastics.fandom.com/wiki/Special:AllPages",
            "url_base": "https://wagymnastics.fandom.com",
            "sport_name": "gymnastics",
        },
        {
            "url": "https://handball.fandom.com/wiki/Special:AllPages",
            "url_base": "https://handball.fandom.com",
            "sport_name": "handball",
        },
        {
            "url": "https://skipedia.fandom.com/wiki/Special:AllPages",
            "url_base": "https://skipedia.fandom.com",
            "sport_name": "skiing",
        },
        {
            "url": "https://thoroughbred-racing.fandom.com/wiki/Special:AllPages",
            "url_base": "https://thoroughbred-racing.fandom.com",
            "sport_name": "horse_racing",
        },
        {
            "url": "https://f1.fandom.com/wiki/Special:AllPages",
            "url_base": "https://f1.fandom.com",
            "sport_name": "f1",
        },
    ]

    for page in base_pages:
        page.update(
            {
                "csv_name": f'{page["sport_name"]}-links.csv',
                "context_name": f'{page["sport_name"]}-contexts.csv',
                "qa_name": f'{page["sport_name"]}-qa.csv',
                "sampling_name": f'{page["sport_name"]}-qa-sampling.csv',
            }
        )

    return base_pages


wiki_pages = generate_wiki_pages()
