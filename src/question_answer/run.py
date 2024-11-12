from ..module import OUTPUT_PATH
from .module import generate_qa

TESTING = True
question_pages = [
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

# fecthing the URLs
for wiki_page in question_pages:
    sport_name = wiki_page["sport_name"]
    generate_qa(
        input_file=(OUTPUT_PATH / f"{sport_name}-contexts.csv"),
        output_file=(OUTPUT_PATH / f"{sport_name}-qa.csv"),
        test=TESTING,
    )
