from ..module import CLEAN_JSON_PATH, OUTPUT_PATH, wiki_pages
from .module import split_text_into_chunks

# extracting text chunks
for wiki_page in wiki_pages:
    sport_name, context_name = wiki_page["sport_name"], wiki_page["context_name"]
    split_text_into_chunks(
        output_file=(OUTPUT_PATH / f"{context_name}"),
        input_folder=(CLEAN_JSON_PATH / sport_name),
    )
