"""Affinity Propagation sampling algorithm"""

import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.cluster import AffinityPropagation
from sentence_transformers import SentenceTransformer


def batch_affinity_sampling(df_questions: pd.DataFrame, model: any, batch: int):
    """
    Batch affinity sampling
    Args:
        df_questions (pd.DataFrame): The dataset to sample
        model (any): The sentence transformer model
        batch (int): The batch size
    Returns:
        pd.DataFrame: The sampled dataset
    """
    # Base clustering parameters
    base_parameters = {"random_state": 42, "damping": 0.5, "max_iter": 1_000}
    # Compute the embeddings
    embeddings = model.encode(df_questions["question"].tolist())
    # Divide the dataset into batches
    selected_questions, exemplar_indices = list(), set()
    for i in tqdm(range(0, len(df_questions), batch), desc="Batching"):
        batch_embeddings = embeddings[i : i + batch]
        clustering = AffinityPropagation(**base_parameters)
        clustering.fit(batch_embeddings)
        exemplar = clustering.cluster_centers_indices_.tolist()
        exemplar_indices.update(exemplar)
    # Bacth examplar clustering
    exemplar_embeddings = embeddings[list(exemplar_indices)]
    clustering = AffinityPropagation(**base_parameters)
    clustering.fit(exemplar_embeddings)
    for idx in clustering.cluster_centers_indices_.tolist():
        row = df_questions.iloc[idx]
        values = {column: row[column] for column in df_questions.columns}
        values["embedding"] = embeddings[i]
        selected_questions.append(values)
    return pd.DataFrame(selected_questions)


def affinity_sampling(
    input_file: str,
    output_file: str,
    test: bool = False,
    batch: int = 1_000,
    model_name: str = "all-MiniLM-L6-v2",
):
    """
    Affinity sampling a Question-Answering dataset
    Args:
        input_file (str): The input file
        output_file (str): The output file
        test (bool): Whether to test the function
        batch (int): The batch size
        model_name (str): The sentence transformer model name
    """
    df = pd.read_csv(input_file, sep=",")
    print(f"Loaded {len(df)} samples from {input_file} (Testing={test})")
    if test:
        df = df.head()

    model = SentenceTransformer(model_name)
    df_selected = batch_affinity_sampling(df, model, batch)
    df_selected.to_csv(output_file, index=False)
    print(df_selected.head())
    print(f"Saved {len(df_selected)} samples to {output_file}")
