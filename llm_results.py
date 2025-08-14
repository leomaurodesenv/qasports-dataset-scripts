#!/usr/bin/env python3
"""
Script to analyze accuracy of questions and answers from labeling CSV files.
Reads CSV files from output/labeling folder and computes accuracy metrics.
"""

import os
import argparse
import pandas as pd
from pathlib import Path
from typing import Dict, Tuple, List
from statsmodels.stats.inter_rater import aggregate_raters, fleiss_kappa


def read_csv_file(file_path: Path, index_column: str = "qa_id") -> pd.DataFrame:
    """Read a CSV file and return a pandas DataFrame."""
    try:
        df = pd.read_csv(file_path).drop_duplicates(subset=[index_column], keep="first")
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


def analyze_fleiss_results(
    base_path: str = "output/labeling",
    labeling_group: list = ["llama", "mistral", "qwen", "human"],
    labeling_column: str = "is_question_valid",
    index_column: str = "qa_id",
    print_output: bool = True,
):
    """
    Reads the sports from the first item in labeling_group and loads it as a pandas DataFrame.

    Args:
        base_path: Path to the labeling folder
        labeling_group: List of folder names to consider (default: ["human", "llama", "mistral", "qwen"])
        labeling_column: Column name to analyze
        index_column: Column to use as index
        print_output: Whether to print the analysis output

    Returns:
        Dictionary containing results summary and overall statistics
    """
    if print_output:
        print("=" * 80)
        print("🔍 FLEISS KAPPA INTER-RATER RELIABILITY ANALYSIS")
        print("=" * 80)
        print(f"📊 Column: {labeling_column}")
        print(f"👥 Groups: {', '.join(labeling_group)}")
        print(f"📁 Base path: {base_path}")
        print("-" * 80)

    if not labeling_group or not isinstance(labeling_group, list):
        if print_output:
            print("❌ Error: labeling_group must be a non-empty list.")
        return None

    first_group = labeling_group[0]
    group_folder = Path(base_path) / first_group

    if not group_folder.exists() or not group_folder.is_dir():
        if print_output:
            print(f"❌ Error: Folder {group_folder} does not exist.")
        return None

    # Collect all CSV files in the group folder
    csv_files = list(group_folder.glob("*.csv"))
    if not csv_files:
        if print_output:
            print(f"❌ Error: No CSV files found in {group_folder}.")
        return None

    if print_output:
        print(f"📋 Found {len(csv_files)} CSV files to analyze")
        print()

    # Store results for summary
    results_summary = []

    # Concatenate labeling from each sport
    for csv_file in csv_files:
        df = pd.read_csv(csv_file).drop_duplicates(subset=[index_column], keep="first")
        # Convert to numeric, coerce errors to NaN, then fill NaN with -1 (or another placeholder), then cast to int
        df[labeling_column] = (
            pd.to_numeric(df[labeling_column], errors="coerce").fillna(-1).astype(int)
        )
        df = df.set_index(index_column)[[labeling_column]]
        filename = csv_file.name
        sport_name = filename.replace("-qa-labeling.csv", "")

        for group in labeling_group[1:]:
            csv_file_another = Path(base_path) / group / filename
            df_another = pd.read_csv(csv_file_another).drop_duplicates(
                subset=[index_column], keep="first"
            )
            df_another[labeling_column] = (
                pd.to_numeric(df_another[labeling_column], errors="coerce")
                .fillna(-1)
                .astype(int)
            )
            df_another = df_another.set_index(index_column)[[labeling_column]]
            # To avoid duplicate column names, rename the column in df_another before joining
            df_another = df_another.rename(
                columns={labeling_column: f"{labeling_column}_{group}"}
            )
            df = df.join(df_another, how="inner")

        data = df.reset_index(drop=True).to_numpy()
        agg_rate = aggregate_raters(data)
        kappa = fleiss_kappa(agg_rate[0], method="fleiss")

        # Store result for summary
        results_summary.append(
            {"sport": sport_name, "kappa": kappa, "sample_size": len(data)}
        )

    # Calculate overall statistics
    overall_stats = {}
    if results_summary:
        avg_kappa = sum(r["kappa"] for r in results_summary) / len(results_summary)
        total_samples = sum(r["sample_size"] for r in results_summary)
        overall_stats = {
            "avg_kappa": avg_kappa,
            "total_samples": total_samples,
            "num_sports": len(results_summary),
        }

    if print_output:
        # Print summary table
        print("=" * 80)
        print("📊 SUMMARY TABLE")
        print("=" * 80)
        print(f"{'Sport':<20} {'Kappa':<12} {'Interpretation':<15} {'Sample Size':<12}")
        print("-" * 65)

        for result in results_summary:
            kappa = result["kappa"]
            kappa_interpretation = (
                "Poor"
                if kappa < 0.0
                else "Slight"
                if kappa < 0.2
                else "Fair"
                if kappa < 0.4
                else "Moderate"
                if kappa < 0.6
                else "Substantial"
                if kappa < 0.8
                else "Almost Perfect"
            )
            print(
                f"{result['sport']:<20} {kappa:<12.4f} {kappa_interpretation:<15} {result['sample_size']:<12,}"
            )

        # Print overall statistics
        if overall_stats:
            print("-" * 65)
            print(
                f"{'OVERALL':<20} {overall_stats['avg_kappa']:<12.4f} {'Average':<15} {overall_stats['total_samples']:<12,}"
            )

        print("=" * 80)

    return {
        "column": labeling_column,
        "groups": labeling_group,
        "results": results_summary,
        "overall": overall_stats,
    }


def print_fleiss_latex_table(question_results: dict, answer_results: dict):
    """
    Generate a LaTeX table comparing Fleiss Kappa results for both question and answer validation.

    Args:
        question_results: Results from analyze_fleiss_results for question validation
        answer_results: Results from analyze_fleiss_results for answer validation
    """
    print("\n" + "=" * 80)
    print("📊 FLEISS KAPPA LATEX TABLE")
    print("=" * 80)

    if not question_results or not answer_results:
        print("❌ Error: Both question and answer results are required.")
        return

    # Get all unique sports from both analyses
    question_sports = {r["sport"] for r in question_results["results"]}
    answer_sports = {r["sport"] for r in answer_results["results"]}
    all_sports = sorted(question_sports.union(answer_sports))

    # Create lookup dictionaries for quick access
    question_lookup = {r["sport"]: r for r in question_results["results"]}
    answer_lookup = {r["sport"]: r for r in answer_results["results"]}

    # Helper function to get kappa interpretation
    def get_kappa_interpretation(kappa):
        if kappa < 0.0:
            return "Poor"
        elif kappa < 0.2:
            return "Slight"
        elif kappa < 0.4:
            return "Fair"
        elif kappa < 0.6:
            return "Moderate"
        elif kappa < 0.8:
            return "Substantial"
        else:
            return "Almost Perfect"

    # Print LaTeX table
    print("\\begin{table}[htb]")
    print("\\centering")
    print("\\caption{Fleiss Kappa Inter-rater Reliability Analysis}")
    print("\\label{tab:fleiss_kappa}")
    print("\\begin{tabular}{rll|cc|cc}")
    print("\\toprule")
    print(
        "\\multicolumn{3}{c}{\\textbf{Sport}} & \\multicolumn{2}{c|}{\\textbf{Question Validity}} & \\multicolumn{2}{c}{\\textbf{Answer Correctness}} \\\\"
    )
    print("\\cline{4-7}")
    print(
        "& & \\textbf{Q Count} & \\textbf{Kappa} & \\textbf{Agreement} & \\textbf{Kappa} & \\textbf{Agreement} \\\\"
    )
    print("\\midrule")

    # Print data rows
    for i, sport in enumerate(all_sports, 1):
        # Get question count (sample size) from either question or answer results
        q_count = 0
        if sport in question_lookup:
            q_count = question_lookup[sport]["sample_size"]
        elif sport in answer_lookup:
            q_count = answer_lookup[sport]["sample_size"]

        # Question validation data
        if sport in question_lookup:
            q_kappa = question_lookup[sport]["kappa"]
            q_interpretation = get_kappa_interpretation(q_kappa)
            q_cell = f"{q_kappa:.3f} & {q_interpretation}"
        else:
            q_cell = "\\multicolumn{2}{c|}{--}"

        # Answer validation data
        if sport in answer_lookup:
            a_kappa = answer_lookup[sport]["kappa"]
            a_interpretation = get_kappa_interpretation(a_kappa)
            a_cell = f"{a_kappa:.3f} & {a_interpretation}"
        else:
            a_cell = "\\multicolumn{2}{c}{--}"

        print(f"{i} & {sport} & {q_count:,} & {q_cell} & {a_cell} \\\\")

    # Print overall row
    print("\\midrule")
    q_overall_kappa = question_results["overall"]["avg_kappa"]
    q_overall_interpretation = get_kappa_interpretation(q_overall_kappa)
    a_overall_kappa = answer_results["overall"]["avg_kappa"]
    a_overall_interpretation = get_kappa_interpretation(a_overall_kappa)
    total_questions = question_results["overall"]["total_samples"]

    print(
        f"& \\textbf{{Overall}} & {total_questions:,} & {q_overall_kappa:.3f} & {q_overall_interpretation} & {a_overall_kappa:.3f} & {a_overall_interpretation} \\\\"
    )

    print("\\bottomrule")
    print("\\end{tabular}")
    print("\\end{table}")

    # Print additional statistics
    print("\n\\textbf{Additional Statistics:}")
    print(f"\\begin{{itemize}}")
    print(f"\\item Total sports analyzed: {len(all_sports)}")
    print(
        f"\\item Question validation - Total samples: {question_results['overall']['total_samples']:,}"
    )
    print(
        f"\\item Answer validation - Total samples: {answer_results['overall']['total_samples']:,}"
    )
    print(f"\\item Rater groups: {', '.join(question_results['groups'])}")
    print(f"\\end{{itemize}}")

    print("=" * 80)


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

    # Calculate overall metrics for each folder
    overall_metrics = {}
    for folder in folders:
        folder_total_questions = list()
        folder_answer_accuracy = list()
        folder_question_accuracy = list()

        for sport_data in results[folder].values():
            folder_total_questions.append(sport_data["total_questions"])
            folder_answer_accuracy.append(sport_data["answer_accuracy"])
            folder_question_accuracy.append(sport_data["question_accuracy"])

        sum_total_questions = sum(folder_total_questions)
        avg_question_accuracy = sum(folder_question_accuracy) / len(
            folder_question_accuracy
        )
        avg_answer_accuracy = sum(folder_answer_accuracy) / len(folder_answer_accuracy)

        overall_metrics[folder] = {
            "total_questions": sum_total_questions,
            "question_accuracy": avg_question_accuracy,
            "answer_accuracy": avg_answer_accuracy,
        }

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

        row_parts[2] = f"{question_count:,}"

        # Add accuracy data for each folder
        for folder in folders:
            if sport in results[folder]:
                q_acc = results[folder][sport]["question_accuracy"]
                a_acc = results[folder][sport]["answer_accuracy"]
                row_parts.extend([f"{q_acc:.3f}", f"{a_acc:.3f}"])
            else:
                row_parts.extend(["", ""])

        print(" & ".join(row_parts) + " \\\\")

    # Print overall row
    print("\\midrule")
    overall_question_count = overall_metrics[folders[0]]["total_questions"]
    overall_row_parts = [
        "",
        "\\textbf{Overall}",
        f"{overall_question_count:,}",
    ]

    for folder in folders:
        q_acc = overall_metrics[folder]["question_accuracy"]
        a_acc = overall_metrics[folder]["answer_accuracy"]
        overall_row_parts.extend([f"{q_acc:.3f}", f"{a_acc:.3f}"])

    print(" & ".join(overall_row_parts) + " \\\\")

    print("\\bottomrule")
    print("\\end{tabular}")


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

    # Analyze the Inter Agreement
    print("\n" + "=" * 80)
    print("🔍 INTER-RATER RELIABILITY ANALYSIS")
    print("=" * 80)

    # Run Fleiss Kappa analysis for question validation
    question_results = analyze_fleiss_results(
        base_path="output/labeling",
        labeling_group=["mistral", "qwen", "human"],
        labeling_column="is_question_valid",
        print_output=True,
    )

    # Run Fleiss Kappa analysis for answer validation
    answer_results = analyze_fleiss_results(
        base_path="output/labeling",
        labeling_group=["mistral", "qwen", "human"],
        labeling_column="is_answer_correct",
        print_output=True,
    )

    # Generate LaTeX table comparing both analyses
    if question_results and answer_results:
        print_fleiss_latex_table(question_results, answer_results)


if __name__ == "__main__":
    main()
