from ..module import OUTPUT_PATH, TESTING, wiki_pages
from .module import sampling

wiki_page = wiki_pages[8]  # basketball
# wiki_page = wiki_pages[14] #badminton
qa_name, sampling_name = wiki_page["qa_name"], wiki_page["sampling_name"]
sampling(
    input_file=(OUTPUT_PATH / qa_name),
    output_file=(OUTPUT_PATH / sampling_name),
    test=False,
)
