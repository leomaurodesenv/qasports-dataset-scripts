from ..module import OUTPUT_PATH, TESTING, wiki_pages

# from .semantic import semantic_sampling as sampling
from .affinity import affinity_sampling as sampling

# sampling the questions
for wiki_page in wiki_pages:
    qa_name, sampling_name = wiki_page["qa_name"], wiki_page["sampling_name"]
    sampling(
        input_file=(OUTPUT_PATH / qa_name),
        output_file=(OUTPUT_PATH / sampling_name),
        test=TESTING,
    )
