import pandas as pd
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def batch_sampling(df_questions: pd.DataFrame, model: any, threshold: int):
    """
    Batch sampling
    Args:
        df_questions (pd.DataFrame): The dataset to sample
        model (any): The sentence transformer model
        threshold (int): The similarity threshold
    Returns:
        pd.DataFrame: The sampled dataset
    """
    # Compute the similarity matrix
    embeddings = model.encode(df_questions["question"].tolist())
    selected_questions, used_indices = list(), set()

    # Sampling the dataset
    for i, (_, row) in tqdm(
        enumerate(df_questions.iterrows()), desc="Sampling", total=len(df_questions)
    ):
        if i not in used_indices:
            values = {column: row[column] for column in df_questions.columns}
            values["embedding"] = embeddings[i]
            selected_questions.append(values)
            # compute the similarity for the current question
            similarity_row = cosine_similarity([embeddings[i]], embeddings)[0]
            similar_indices = np.where(similarity_row >= threshold)[0]
            used_indices.update(similar_indices)
    return pd.DataFrame(selected_questions)


def sampling(
    input_file: str,
    output_file: str,
    test: bool = False,
    threshold: int = 0.4,
    model_name: str = "all-MiniLM-L6-v2",
):
    """Sampling a Question-Answering dataset"""
    df = pd.read_csv(input_file, sep=",")
    print(f"Loaded {len(df)} samples from {input_file} (Testing={test})")
    if test:
        df = df.sample(10)

    model = SentenceTransformer(model_name)
    df_selected = batch_sampling(df, model, threshold)
    df_selected.to_csv(output_file, index=False)
    print(df_selected)
    print(f"Saved {len(df_selected)} samples to {output_file}")
