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
    base_parameters = {
        "random_state": 42,
        "damping": 0.5,
        "max_iter": 10_000,
        "convergence_iter": 10,
        "affinity": "euclidean",
    }
    # Divide the dataset into batches
    selected_questions, exemplar_indices = list(), set()
    for i in tqdm(range(0, len(df_questions), batch), desc="Batching"):
        df_questions_batch = df_questions.iloc[i : i + batch]
        batch_embeddings = model.encode(df_questions_batch["question"].tolist())
        clustering = AffinityPropagation(**base_parameters)
        clustering.fit(batch_embeddings)
        exemplar_batch = clustering.cluster_centers_indices_
        if exemplar_batch is not None:
            exemplar_batch = exemplar_batch.tolist()
            exemplar_idx = df_questions_batch.iloc[exemplar_batch].index.to_list()
            exemplar_indices.update(exemplar_idx)
    # Batch exemplar clustering
    print(f"Exemplar indices: {len(exemplar_indices)}")
    df_examplars = (
        df_questions.iloc[list(exemplar_indices)].copy(deep=True).reset_index(drop=True)
    )
    return df_examplars


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
    df_selected = batch_affinity_sampling(df_selected, model, batch)
    df_selected.to_csv(output_file, index=False)
    print(df_selected.head())
    print(f"Saved {len(df_selected)} samples to {output_file}")
