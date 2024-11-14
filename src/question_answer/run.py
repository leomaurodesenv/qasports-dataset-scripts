from ..module import OUTPUT_PATH, TESTING, wiki_pages
from .module import generate_qa

# fecthing the URLs
for wiki_page in wiki_pages:
    qa_name, context_name = wiki_page["qa_name"], wiki_page["context_name"]
    generate_qa(
        input_file=(OUTPUT_PATH / context_name),
        output_file=(OUTPUT_PATH / qa_name),
        test=TESTING,
    )
