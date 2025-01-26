from ..module import OUTPUT_PATH, RAW_HTML_PATH, TESTING, wiki_pages
from .module import fetch_all_html

# Fecthing the URLs
for wiki_page in wiki_pages:
    sport_name, csv_name = wiki_page["sport_name"], wiki_page["csv_name"]
    fetch_all_html(
        links_file=(OUTPUT_PATH / csv_name),
        folder_path=(RAW_HTML_PATH / sport_name),
        test=TESTING,
    )
