from ..module import CLEAN_JSON_PATH, RAW_HTML_PATH
from .module import process_html

processing_pages = [
    {
        "sport_name": "basketball",
    },
    {
        "sport_name": "football",
    },
    {
        "sport_name": "americanfootball",
    },
]

# processing the URLs
for wiki_page in processing_pages:
    sport_name = wiki_page["sport_name"]
    process_html(
        folder_path=(RAW_HTML_PATH / sport_name),
        output_path=(CLEAN_JSON_PATH / sport_name)
    )
