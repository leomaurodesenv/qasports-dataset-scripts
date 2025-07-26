from ..module import OUTPUT_PATH, TESTING, wiki_pages
from .module import MODEL_SHORT_NAME, labeling_from_file


# labeling dataset
for wiki_page in wiki_pages:
    labeling_name, sampling_name = (
        wiki_page["labeling_name"],
        wiki_page["sampling_name"],
    )
    labeling_from_file(
        input_file=(OUTPUT_PATH / sampling_name),
        output_file=(OUTPUT_PATH / "labeling" / MODEL_SHORT_NAME / labeling_name),
        test=TESTING,
    )
