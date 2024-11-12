from ..module import OUTPUT_PATH, RAW_HTML_PATH
from .module import fetch_all_html

TESTING = True
fetching_pages = [
    {
        "sport_name": "basketball",
        "csv_name": "basketball-links.csv"
    },
    {
        "sport_name": "football",
        "csv_name": "football-links.csv"
    },
    {
        "sport_name": "americanfootball",
        "csv_name": "americanfootball-links.csv"
    },
]

# fecthing the URLs
for wiki_page in fetching_pages:
    sport_name, csv_name = wiki_page["sport_name"], wiki_page["csv_name"]
    fetch_all_html(
        links_file=(OUTPUT_PATH / csv_name),
        folder_path=(RAW_HTML_PATH / sport_name),
        test=TESTING,
    )