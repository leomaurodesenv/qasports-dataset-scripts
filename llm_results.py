#!/usr/bin/env python3
"""
Script to analyze accuracy of questions and answers from labeling CSV files.
Reads CSV files from output/labeling folder and computes accuracy metrics.
"""

import os
import pandas as pd
from pathlib import Path
from typing import Dict, Tuple, List
import argparse


def read_csv_file(file_path: Path) -> pd.DataFrame:
    """Read a CSV file and return a pandas DataFrame."""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame()


def calculate_accuracy(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate accuracy metrics for question and answer validation.

    Args:
        df: DataFrame with 'is_question_valid' and 'is_answer_correct' columns

    Returns:
        Dictionary with accuracy metrics
    """
    if df.empty:
        return {
            "question_accuracy": 0.0,
            "answer_accuracy": 0.0,
            "total_questions": 0,
            "valid_questions": 0,
            "correct_answers": 0,
        }

    # Count valid questions (1 = valid, 2 = invalid)
    total_questions = len(df)
    valid_questions = len(df[df["is_question_valid"] == 1])
    question_accuracy = (
        valid_questions / total_questions if total_questions > 0 else 0.0
    )

    # Count correct answers (1 = correct, 2 = wrong)
    # It only counts the answers that are valid (is_question_valid == 1)
    correct_answers = len(df[df["is_answer_correct"] == 1])
    answer_accuracy = (
        min(1.0, correct_answers / valid_questions) if valid_questions > 0 else 0.0
    )

    return {
        "question_accuracy": question_accuracy,
        "answer_accuracy": answer_accuracy,
        "total_questions": total_questions,
        "valid_questions": valid_questions,
        "correct_answers": correct_answers,
    }


def analyze_labeling_folder(
    base_path: str = "output/labeling",
) -> Dict[str, Dict[str, Dict[str, float]]]:
    """
    Analyze all CSV files in the labeling folder structure.

    Args:
        base_path: Path to the labeling folder

    Returns:
        Nested dictionary with results organized by folder and sport
    """
    results = {}
    base_path = Path(base_path)

    if not base_path.exists():
        print(f"Error: {base_path} does not exist")
        return results

    # Iterate through subfolders (e.g., qwen, mistral)
    for folder in base_path.iterdir():
        if folder.is_dir():
            folder_name = folder.name
            results[folder_name] = {}

            # Iterate through CSV files in the folder
            for csv_file in folder.glob("*.csv"):
                if csv_file.suffix.lower() == ".csv":
                    # Extract sport name from filename (e.g., "football-qa-labeling.csv" -> "football")
                    sport_name = csv_file.stem.replace("-qa-labeling", "")

                    # Read and analyze the CSV file
                    df = read_csv_file(csv_file)
                    accuracy_metrics = calculate_accuracy(df)
                    results[folder_name][sport_name] = accuracy_metrics

    return results


def print_results(
    results: Dict[str, Dict[str, Dict[str, float]]], detailed: bool = False
):
    """
    Print the analysis results in a formatted way.

    Args:
        results: Results dictionary from analyze_labeling_folder
        detailed: Whether to print detailed metrics
    """
    print("=" * 80)
    print("LLM LABELING ACCURACY ANALYSIS")
    print("=" * 80)

    for folder_name, sports_data in results.items():
        print(f"\n📁 FOLDER: {folder_name.upper()}")
        print("-" * 60)

        # Calculate folder-level summary
        folder_total_questions = list()
        folder_answer_accuracy = list()
        folder_question_accuracy = list()

        for sport_name, metrics in sports_data.items():
            folder_total_questions.append(metrics["total_questions"])
            folder_answer_accuracy.append(metrics["answer_accuracy"])
            folder_question_accuracy.append(metrics["question_accuracy"])

        sum_total_questions = sum(folder_total_questions)
        avg_question_accuracy = sum(folder_question_accuracy) / len(
            folder_question_accuracy
        )
        avg_answer_accuracy = sum(folder_answer_accuracy) / len(folder_answer_accuracy)

        print(f"📋 SPORT SUMMARY:")
        print(f"   Total Questions: {sum_total_questions:,}")
        print(f"   Question Accuracy: {avg_question_accuracy:.3%}")
        print(f"   Answer Accuracy: {avg_answer_accuracy:.3%}")

        # Print summary table
        print(f"{'Sport':<20} {'Questions':<12} {'Q Acc':<8} {'A Acc':<8}")
        print("-" * 50)
        for sport_name, metrics in sorted(sports_data.items()):
            print(
                f"{sport_name:<20} {metrics['total_questions']:<12,} "
                f"{metrics['question_accuracy']:<8.2%} "
                f"{metrics['answer_accuracy']:<8.2%}"
            )


def print_latex_table(results: Dict[str, Dict[str, Dict[str, float]]]):
    """
    Print the analysis results as a LaTeX table.

    Args:
        results: Results dictionary from analyze_labeling_folder
    """
    print("\n" + "=" * 80)
    print("LATEX TABLE OUTPUT")
    print("=" * 80)

    # Get all unique sports across all folders
    all_sports = set()
    for folder_data in results.values():
        all_sports.update(folder_data.keys())

    # Get all folders (models)
    folders = list(results.keys())

    # Print table header
    print("\\begin{tabular}{rlr|" + "cc|" * len(folders) + "}")
    print("\\toprule")

    # Print column headers
    header_parts = ["\\multicolumn{3}{c}{\\textbf{Sport}}"]
    for folder in folders:
        header_parts.append(f"\\multicolumn{{2}}{{c}}{{\\textbf{{{folder.title()}}}}}")
    print(" & ".join(header_parts) + " \\\\")

    # Print sub-headers
    sub_header_parts = ["", "Name", "Questions"]
    for folder in folders:
        sub_header_parts.extend(["Q Acc", "A Acc"])
    print(" & ".join(sub_header_parts) + " \\\\")
    print("\\midrule")

    # Print data rows
    for i, sport in enumerate(sorted(all_sports)):
        row_parts = [str(i + 1), sport, ""]  # Sport name, will be filled

        # Get question count from first available folder
        question_count = 0
        for folder in folders:
            if sport in results[folder]:
                question_count = results[folder][sport]["total_questions"]
                break

        row_parts[2] = str(question_count)

        # Add accuracy data for each folder
        for folder in folders:
            if sport in results[folder]:
                q_acc = results[folder][sport]["question_accuracy"]
                a_acc = results[folder][sport]["answer_accuracy"]
                row_parts.extend([f"{q_acc:.3f}", f"{a_acc:.3f}"])
            else:
                row_parts.extend(["", ""])

        print(" & ".join(row_parts) + " \\\\")

    print("\\bottomrule")
    print("\\end{tabular}")


def save_results_to_csv(
    results: Dict[str, Dict[str, Dict[str, float]]],
    output_file: str = "llm_accuracy_results.csv",
):
    """
    Save results to a CSV file for further analysis.

    Args:
        results: Results dictionary from analyze_labeling_folder
        output_file: Output CSV filename
    """
    rows = []

    for folder_name, sports_data in results.items():
        for sport_name, metrics in sports_data.items():
            rows.append(
                {
                    "folder": folder_name,
                    "sport": sport_name,
                    "total_questions": metrics["total_questions"],
                    "valid_questions": metrics["valid_questions"],
                    "correct_answers": metrics["correct_answers"],
                    "question_accuracy": metrics["question_accuracy"],
                    "answer_accuracy": metrics["answer_accuracy"],
                }
            )

    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False)
    print(f"\n💾 Results saved to: {output_file}")


def main():
    """Main function to run the analysis."""
    parser = argparse.ArgumentParser(
        description="Analyze LLM labeling accuracy from CSV files"
    )
    parser.add_argument(
        "--path",
        default="output/labeling",
        help="Path to the labeling folder (default: output/labeling)",
    )
    parser.add_argument(
        "--detailed", action="store_true", help="Print detailed results for each sport"
    )
    parser.add_argument(
        "--output",
        default="llm_accuracy_results.csv",
        help="Output CSV file for results (default: llm_accuracy_results.csv)",
    )

    args = parser.parse_args()

    # Run the analysis
    print("🔍 Analyzing labeling accuracy...")
    results = analyze_labeling_folder(args.path)

    if not results:
        print("❌ No results found. Please check the path and ensure CSV files exist.")
        return

    # Print results
    print_results(results, detailed=args.detailed)

    # Print LaTeX table if requested
    print_latex_table(results)

    # Save results to CSV
    save_results_to_csv(results, args.output)


if __name__ == "__main__":
    main()
