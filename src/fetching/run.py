from ..module import OUTPUT_PATH, RAW_HTML_PATH
from .module import fetch_all_html

TESTING = True
fetching_pages = [
    {
        "folder_name": "basketball",
        "csv_name": "basketball-links.csv"
    },
    {
        "folder_name": "football",
        "csv_name": "football-links.csv"
    },
    {
        "folder_name": "americanfootball",
        "csv_name": "americanfootball-links.csv"
    },
]

# Get the URLs
for wiki_page in fetching_pages:
    folder_name, csv_name = wiki_page["folder_name"], wiki_page["csv_name"]
    fetch_all_html(
        links_file=(OUTPUT_PATH / csv_name),
        folder_path=(RAW_HTML_PATH / folder_name),
        test=TESTING,
    )
