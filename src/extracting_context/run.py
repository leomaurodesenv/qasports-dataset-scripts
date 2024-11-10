from ..module import CLEAN_JSON_PATH, OUTPUT_PATH
from .module import split_text_into_chunks

extracting_contx_pages = [
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
for wiki_page in extracting_contx_pages:
    sport_name = wiki_page["sport_name"]
    split_text_into_chunks(
        output_file=(OUTPUT_PATH / f"{sport_name}-contexts.csv"),
        input_folder=(CLEAN_JSON_PATH / sport_name)
    )
