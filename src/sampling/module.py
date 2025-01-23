import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def recursive_sampling(df_questions, model, threshold, max_samples: int = 500):
    """Recursive sampling"""
    # Break the questions into two parts
    print(f"Sampling {len(df_questions)} questions")
    if len(df_questions) > max_samples + 1:
        selected_first = recursive_sampling(
            df_questions.iloc[:max_samples], model, threshold, max_samples
        )
        selected_last = recursive_sampling(
            df_questions.iloc[max_samples:], model, threshold, max_samples
        )
        # TODO: fix the recursive sampling
        df_questions = pd.concat([selected_first, selected_last])

    # Compute the similarity matrix
    embeddings = model.encode(df_questions["question"].tolist())
    similarity_matrix = cosine_similarity(embeddings)
    selected_questions, used_indices = list(), set()

    # Sampling the dataset
    for i, (_, row) in enumerate(df_questions.iterrows()):
        if i not in used_indices:
            values = {column: row[column] for column in df_questions.columns}
            values["embedding"] = embeddings[i]
            selected_questions.append(values)
            similar_indices = similarity_matrix[i] >= threshold
            used_indices.update(similar_indices)
    return pd.DataFrame(selected_questions)


def sampling(
    input_file: str,
    output_file: str,
    test: bool = False,
    threshold: int = 0.5,
    model_name: str = "all-MiniLM-L6-v2",
):
    """Sampling a Question-Answering dataset"""
    df = pd.read_csv(input_file, sep=",")
    print(f"Loaded {len(df)} samples from {input_file} (Testing={test})")
    if test:
        df = df.sample(10)

    model = SentenceTransformer(model_name)
    df_selected = recursive_sampling(df, model, threshold)
    df_selected.to_csv(output_file, index=False)
    print(df_selected)
    print(f"Saved {len(df_selected)} samples to {output_file}")
