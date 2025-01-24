from ..module import CLEAN_JSON_PATH, RAW_HTML_PATH, wiki_pages
from .module import process_all_html

# Processing the URLs
for wiki_page in wiki_pages:
    sport_name = wiki_page["sport_name"]
    process_all_html(
        folder_path=(RAW_HTML_PATH / sport_name),
        output_path=(CLEAN_JSON_PATH / sport_name),
    )
