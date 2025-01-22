import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def sampling(
    questions: list,
    test: bool = False,
    threshold: int = 0.6,
    model_name: str = "all-MiniLM-L6-v2",
):
    # def sampling(input_file: str, output_file: str, test: bool = False, model_name: str = 'all-MiniLM-L6-v2')
    """Sampling a Question-Answering dataset"""
    # df = pd.read_csv(input_file, sep=",")
    # questions = df["questions"]

    model = SentenceTransformer(model_name)
    embeddings = model.encode(questions)

    similarity_matrix = cosine_similarity(embeddings)
    selected_questions, used_indices = list(), set()

    for i in range(len(questions)):
        if i not in used_indices:
            selected_questions.append(
                {"text": questions[i], "embedding": embeddings[i]}
            )
            similar_indices = np.where(similarity_matrix[i] >= threshold)[0]
            used_indices.update(similar_indices)

    return pd.DataFrame(selected_questions)
