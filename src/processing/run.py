from ..module import CLEAN_JSON_PATH, RAW_HTML_PATH
from .module import process_html

processing_pages = [
    {
        "folder_name": "basketball",
    },
    {
        "folder_name": "football",
    },
    {
        "folder_name": "americanfootball",
    },
]

# processing the URLs
for wiki_page in processing_pages:
    folder_name = wiki_page["folder_name"]
    process_html(
        folder_path=(RAW_HTML_PATH / folder_name),
        output_path=(CLEAN_JSON_PATH / folder_name)
    )
