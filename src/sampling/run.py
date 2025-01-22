from ..module import OUTPUT_PATH, TESTING, wiki_pages
from .module import sampling

questions = [
    "What are the primary benefits of regular training?",
    "What are the primary benefits of regular exercise?",
    "Discuss the advantages of a diet.",
    "Discuss the advantages of a balanced diet.",
    "How does sleep deprivation impact cognitive function?",
    "How does sleep impact cognitive function?",
    "Explain the importance of mariage.",
    "Explain the importance of stress management techniques.",
    "What are some effective strategies for money?",
    "What are some effective strategies for time management?",
    "What are the key components of work balance?",
    "What are the key components of a healthy lifestyle?",
]

df = sampling(questions=questions)
print(df)
