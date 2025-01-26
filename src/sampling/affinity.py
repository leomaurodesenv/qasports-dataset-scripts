"""Affinity Propagation sampling algorithm"""

import pandas as pd
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer


def batch_affinity_sampling(df_questions: pd.DataFrame, model: any, threshold: int):
    pass


def affinity_sampling(
    input_file: str,
    output_file: str,
    test: bool = False,
    threshold: int = 0.4,
    model_name: str = "all-MiniLM-L6-v2",
):
    """
    Affinity sampling a Question-Answering dataset
    Args:
        input_file (str): The input file
        output_file (str): The output file
        test (bool): Whether to test the function
        threshold (int): The similarity threshold
        model_name (str): The sentence transformer model name
    """
    df = pd.read_csv(input_file, sep=",")
    print(f"Loaded {len(df)} samples from {input_file} (Testing={test})")
    if test:
        df = df.head()

    model = SentenceTransformer(model_name)
    df_selected = batch_affinity_sampling(df, model, threshold)
    df_selected.to_csv(output_file, index=False)
    print(df_selected.head())
    print(f"Saved {len(df_selected)} samples to {output_file}")
