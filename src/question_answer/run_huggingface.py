import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from ..module import OUTPUT_PATH, wiki_pages

# Constants
HUGGINGFACE_PATH = Path(OUTPUT_PATH / "huggingface")


def process_wiki_page(wiki_page):
    """Process a single wiki page to generate train, test, and validation datasets."""
    qa_name, sport_name = wiki_page["qa_name"], wiki_page["sport_name"]
    output_file = OUTPUT_PATH / qa_name

    # Load the dataset
    dataset = pd.read_csv(output_file, sep=",")
    print(f"Loaded {sport_name} dataset with {len(dataset)} rows.")

    # Split the dataset
    train, test = train_test_split(dataset, test_size=0.1, random_state=42)
    train, val = train_test_split(train, test_size=0.1112, random_state=42)
    print(
        f"Split dataset into {len(train)} train, {len(val)} validation, and {len(test)} test sets.\n"
    )

    # Save the datasets
    save_dataset(train, sport_name, "train")
    save_dataset(test, sport_name, "test")
    save_dataset(val, sport_name, "validation")


def save_dataset(data, sport_name, split):
    """Save a dataset to the specified split folder."""
    split_path = HUGGINGFACE_PATH / sport_name / split
    split_path.mkdir(parents=True, exist_ok=True)
    data.to_parquet(split_path / "data.parquet", index=False)
    # data.to_csv(split_path / "data.csv", index=False, header=True)


# Process each wiki page
for wiki_page in wiki_pages:
    process_wiki_page(wiki_page)
