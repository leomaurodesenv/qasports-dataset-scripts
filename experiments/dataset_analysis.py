"""Document Analysis Script"""

import argparse
import numpy as np
from collections import Counter
from .module import Dataset, Sports, DatasetSplit, AbstactDataset, dataset_switch


def analyze_length_distributions(dataset: AbstactDataset):
    """Analyze length distributions for contexts, questions, and answers"""
    df_dataset = dataset.df_dataset

    # Count unique contexts, questions, and question-answer pairs
    context_col = dataset._columns["document"]
    question_col = dataset._columns["question"]

    # Get column names from the dataset
    if not context_col or not question_col:
        print("Warning: Could not find context or question columns")
        return {}

    # Calculate context lengths
    context_lengths = []
    for text in df_dataset[context_col]:
        if isinstance(text, str):
            context_lengths.append(len(text.split()))
        else:
            context_lengths.append(0)

    # Calculate question lengths
    question_lengths = []
    for text in df_dataset[question_col]:
        if isinstance(text, str):
            question_lengths.append(len(text.split()))
        else:
            question_lengths.append(0)

    # Calculate answer lengths
    answer_lengths = []
    empty_answers = 0

    for _, row in df_dataset.iterrows():
        answer = dataset._get_answers(row)
        if isinstance(answer, list):
            # Handle list of answers
            if len(answer) > 0 and answer[0]:
                answer_text = (
                    answer[0] if isinstance(answer[0], str) else str(answer[0])
                )
                answer_lengths.append(len(answer_text.split()))
            else:
                answer_lengths.append(0)
                empty_answers += 1
        elif isinstance(answer, str):
            answer_lengths.append(len(answer.split()))
        else:
            answer_lengths.append(0)
            empty_answers += 1

    # Calculate statistics
    stats = {
        "context": {
            "count": len(context_lengths),
            "mean": np.mean(context_lengths),
            "median": np.median(context_lengths),
            "min": np.min(context_lengths),
            "max": np.max(context_lengths),
            "std": np.std(context_lengths),
        },
        "question": {
            "count": len(question_lengths),
            "mean": np.mean(question_lengths),
            "median": np.median(question_lengths),
            "min": np.min(question_lengths),
            "max": np.max(question_lengths),
            "std": np.std(question_lengths),
        },
        "answer": {
            "count": len(answer_lengths),
            "mean": np.mean(answer_lengths),
            "median": np.median(answer_lengths),
            "min": np.min(answer_lengths),
            "max": np.max(answer_lengths),
            "std": np.std(answer_lengths),
            "empty_count": empty_answers,
            "empty_percentage": (empty_answers / len(answer_lengths)) * 100
            if answer_lengths
            else 0,
        },
    }

    return stats


def analyze_question_types(dataset: AbstactDataset):
    """Analyze question types based on WH-words"""
    df_dataset = dataset.df_dataset

    # Find question column
    question_col = dataset._columns["question"]

    if not question_col:
        print("Warning: Could not find question column")
        return {}

    # WH-words to look for
    wh_words = ["who", "whom", "whose", "why", "which", "what", "where", "when", "how"]

    # Count question types
    question_types = Counter()
    empty_answers_by_type = Counter()

    # Find answer column
    for _, row in df_dataset.iterrows():
        question = row[question_col]
        if not isinstance(question, str):
            question_types["none"] += 1
            continue

        question_lower = question.lower().strip()
        question_type = "none"

        # Check for WH-words at the beginning
        for wh_word in wh_words:
            if question_lower.startswith(wh_word):
                question_type = wh_word
                break

        question_types[question_type] += 1

        # Check if answer is empty for this question type
        answer = dataset._get_answers(row)
        is_empty = False
        if isinstance(answer, list):
            is_empty = len(answer) == 0 or (len(answer) > 0 and not answer[0])
        elif isinstance(answer, str):
            is_empty = not answer.strip()
        else:
            is_empty = True

        if is_empty:
            empty_answers_by_type[question_type] += 1

    # Calculate percentages
    total_questions = sum(question_types.values())
    question_type_stats = {}

    for q_type, count in question_types.items():
        percentage = (count / total_questions) * 100 if total_questions > 0 else 0
        empty_count = empty_answers_by_type.get(q_type, 0)
        empty_percentage = (empty_count / count) * 100 if count > 0 else 0

        question_type_stats[q_type] = {
            "count": count,
            "percentage": percentage,
            "empty_answers": empty_count,
            "empty_percentage": empty_percentage,
        }

    return question_type_stats


def analyze_dataset_overview(dataset: AbstactDataset):
    """Analyze overall dataset statistics"""
    df_dataset = dataset.df_dataset

    # Count unique contexts, questions, and question-answer pairs
    context_col = dataset._columns["document"]
    question_col = dataset._columns["question"]

    unique_contexts = df_dataset[context_col].nunique() if context_col else 0
    unique_questions = df_dataset[question_col].nunique() if question_col else 0
    total_pairs = len(df_dataset)

    # Count questions without answers
    questions_without_answers = 0
    for _, row in df_dataset.iterrows():
        answer = dataset._get_answers(row)
        if isinstance(answer, list):
            if len(answer) == 0 or (len(answer) > 0 and not answer[0]):
                questions_without_answers += 1
        elif isinstance(answer, str):
            if not answer.strip():
                questions_without_answers += 1
        else:
            questions_without_answers += 1

    percentage_without_answers = (
        (questions_without_answers / total_pairs) * 100 if total_pairs > 0 else 0
    )

    return {
        "total_examples": total_pairs,
        "unique_contexts": unique_contexts,
        "unique_questions": unique_questions,
        "questions_without_answers": questions_without_answers,
        "percentage_without_answers": percentage_without_answers,
    }


# Model setup
# DATASET = Dataset.QASports
# SPORT = Sports.SKIING
# SPLIT = DatasetSplit.TRAIN
parser = argparse.ArgumentParser(description="Run document reader experiments.")
parser.add_argument(
    "--dataset",
    type=str,
    default="QASports",
    choices=[attr.name for attr in Dataset],
    help="Dataset to use for the experiment.",
)

parser.add_argument(
    "--sport",
    type=str,
    default="ALL",
    choices=[attr.name for attr in Sports],
    help="Sport to filter for QASports dataset.",
)

parser.add_argument(
    "--split",
    type=str,
    default="TRAIN",
    choices=[attr.name for attr in DatasetSplit],
    help="Dataset split to use (train, validation, test).",
)

args = parser.parse_args()

DATASET = Dataset[args.dataset]
SPORT = Sports[args.sport]
SPLIT = DatasetSplit[args.split]
print(f"Dataset: {DATASET} // Sport: {SPORT} // Split: {SPLIT}")

# Get the dataset
dataset = dataset_switch(
    choice=DATASET, sport=SPORT, split=SPLIT, remove_empty_answers=False
)

# Perform comprehensive analysis
print("\n🔍 Analyzing dataset...")

# Overall statistics
overview_stats = analyze_dataset_overview(dataset)
print("Overall statistics")
print(overview_stats)

# Length distributions
length_stats = analyze_length_distributions(dataset)
print("\nLength distributions")
print(length_stats)

# Question type analysis
question_type_stats = analyze_question_types(dataset)
print("\nQuestion type analysis")
print(question_type_stats)
