#!/usr/bin/env python3
"""
Dataset Analysis Display Script

This script reads JSON files from the output/analysis_results folder and provides
helper functions to analyze and display the results from the dataset analysis.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd


class DatasetAnalysisReader:
    """Class to read and analyze dataset analysis results from JSON files."""

    def __init__(self, results_dir: str = "output/analysis_results"):
        """
        Initialize the reader with the results directory.

        Args:
            results_dir: Path to the directory containing analysis JSON files
        """
        self.results_dir = Path(results_dir)
        self.sport_data = {}
        self.summary_data = None
        self.load_all_data()

    def load_all_data(self):
        """Load all JSON files from the results directory."""
        if not self.results_dir.exists():
            print(f"❌ Results directory not found: {self.results_dir}")
            return

        # Load summary file
        summary_files = list(self.results_dir.glob("analysis_summary_*.json"))
        if summary_files:
            with open(summary_files[0], "r", encoding="utf-8") as f:
                self.summary_data = json.load(f)
            print(f"✅ Loaded summary: {summary_files[0].name}")

        # Load individual sport files
        sport_files = list(self.results_dir.glob("*_analysis.json"))
        sport_files = [
            f for f in sport_files if not f.name.startswith("analysis_summary")
        ]

        for file_path in sport_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                sport_name = data.get("sport", file_path.stem.split("_")[0])
                self.sport_data[sport_name] = data
                print(f"✅ Loaded: {file_path.name}")

            except Exception as e:
                print(f"❌ Failed to load {file_path.name}: {str(e)}")

        print(f"\n📊 Loaded {len(self.sport_data)} sport analysis files")

    def get_sport_names(self) -> List[str]:
        """Get list of all sport names."""
        return list(self.sport_data.keys())

    def get_sport_data(self, sport_name: str) -> Optional[Dict]:
        """Get data for a specific sport."""
        return self.sport_data.get(sport_name)

    def get_overview_statistics(self) -> pd.DataFrame:
        """Get overview statistics for all sports as a DataFrame."""
        overview_data = []

        for sport_name, data in self.sport_data.items():
            if "error" in data:
                continue

            overview = data.get("overview", {})
            overview_data.append(
                {
                    "sport": sport_name,
                    "total_examples": overview.get("total_examples", 0),
                    "unique_contexts": overview.get("unique_contexts", 0),
                    "unique_questions": overview.get("unique_questions", 0),
                    "questions_without_answers": overview.get(
                        "questions_without_answers", 0
                    ),
                    "percentage_without_answers": overview.get(
                        "percentage_without_answers", 0
                    ),
                }
            )

        return pd.DataFrame(overview_data)

    def get_length_statistics(self) -> pd.DataFrame:
        """Get length statistics for all sports as a DataFrame."""
        length_data = []

        for sport_name, data in self.sport_data.items():
            if "error" in data:
                continue

            length_stats = data.get("length_distributions", {})

            # Context lengths
            context = length_stats.get("context", {})
            length_data.append(
                {
                    "sport": sport_name,
                    "type": "context",
                    "mean": context.get("mean", 0),
                    "median": context.get("median", 0),
                    "min": context.get("min", 0),
                    "max": context.get("max", 0),
                    "std": context.get("std", 0),
                }
            )

            # Question lengths
            question = length_stats.get("question", {})
            length_data.append(
                {
                    "sport": sport_name,
                    "type": "question",
                    "mean": question.get("mean", 0),
                    "median": question.get("median", 0),
                    "min": question.get("min", 0),
                    "max": question.get("max", 0),
                    "std": question.get("std", 0),
                }
            )

            # Answer lengths
            answer = length_stats.get("answer", {})
            length_data.append(
                {
                    "sport": sport_name,
                    "type": "answer",
                    "mean": answer.get("mean", 0),
                    "median": answer.get("median", 0),
                    "min": answer.get("min", 0),
                    "max": answer.get("max", 0),
                    "std": answer.get("std", 0),
                }
            )

        return pd.DataFrame(length_data)

    def get_question_type_statistics(self) -> pd.DataFrame:
        """Get question type statistics for all sports as a DataFrame."""
        question_data = []

        for sport_name, data in self.sport_data.items():
            if "error" in data:
                continue

            question_types = data.get("question_types", {})

            for q_type, stats in question_types.items():
                question_data.append(
                    {
                        "sport": sport_name,
                        "question_type": q_type,
                        "count": stats.get("count", 0),
                        "percentage": stats.get("percentage", 0),
                        "empty_answers": stats.get("empty_answers", 0),
                        "empty_percentage": stats.get("empty_percentage", 0),
                    }
                )

        return pd.DataFrame(question_data)

    def get_sports_with_errors(self) -> List[str]:
        """Get list of sports that had errors during analysis."""
        return [sport for sport, data in self.sport_data.items() if "error" in data]


def display_overview_table(reader: DatasetAnalysisReader):
    """Display overview statistics in a formatted table."""
    print("\n" + "=" * 80)
    print("📊 DATASET OVERVIEW STATISTICS")
    print("=" * 80)

    overview_df = reader.get_overview_statistics()

    if overview_df.empty:
        print("❌ No overview data available")
        return

    # Sort by sport name
    overview_df = overview_df.sort_values("sport", ascending=True)

    # Format the display
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", 15)

    print(overview_df.to_string(index=False, float_format="%.1f"))


def display_overview_latex(reader: DatasetAnalysisReader):
    """Display overview statistics as a LaTeX table."""
    print("\n" + "=" * 80)
    print("📊 DATASET OVERVIEW - LATEX TABLE")
    print("=" * 80)

    overview_df = reader.get_overview_statistics()

    if overview_df.empty:
        print("❌ No overview data available")
        return

    # Sort by sport name
    overview_df = overview_df.sort_values("sport", ascending=True)

    # Create LaTeX table
    latex_table = []
    latex_table.append("\\begin{table}[htb]")
    latex_table.append("\\centering\\footnotesize")
    latex_table.append("\\caption{Dataset Overview Statistics by Sport}")
    latex_table.append("\\label{tab:dataset-overview}")
    latex_table.append("\\begin{tabular}{rlrrrrr}")
    latex_table.append("\\toprule")
    latex_table.append(
        "& Sport & Total Examples & Unique Contexts & Unique Questions & Questions w/o Answers & \% w/o Answers \\\\"
    )
    latex_table.append("\\midrule")

    # Add data rows
    for idx, (_, row) in enumerate(overview_df.iterrows(), start=0):
        sport = row["sport"].replace("_", "\\_")  # Escape underscores for LaTeX
        total_examples = f"{row['total_examples']:,}"
        unique_contexts = f"{row['unique_contexts']:,}"
        unique_questions = f"{row['unique_questions']:,}"
        questions_without_answers = f"{row['questions_without_answers']:,}"
        percentage = f"{row['percentage_without_answers']:.1f}"

        latex_table.append(
            f"{idx} & {sport.lower()} & {total_examples} & {unique_contexts} & {unique_questions} & {questions_without_answers} & {percentage}\\% \\\\"
        )

    # Add totals row
    totals = {
        "total_examples": overview_df["total_examples"].sum(),
        "unique_contexts": overview_df["unique_contexts"].sum(),
        "unique_questions": overview_df["unique_questions"].sum(),
        "questions_without_answers": overview_df["questions_without_answers"].sum(),
        "percentage_without_answers": overview_df["percentage_without_answers"].mean(),
    }

    latex_table.append("\\midrule")
    latex_table.append(
        "\\textbf{Total} & "
        + f"\\textbf{{{totals['total_examples']:,}}} & "
        + f"\\textbf{{{totals['unique_contexts']:,}}} & "
        + f"\\textbf{{{totals['unique_questions']:,}}} & "
        + f"\\textbf{{{totals['questions_without_answers']:,}}} & "
        + f"\\textbf{{{totals['percentage_without_answers']:.1f}\\%}} \\\\"
    )

    latex_table.append("\\bottomrule")
    latex_table.append("\\end{tabular}")
    latex_table.append("\\end{table}")

    # Print the LaTeX table
    print("\n".join(latex_table))


def display_question_type_table(reader: DatasetAnalysisReader):
    """Display question type analysis."""
    print("\n" + "=" * 80)
    print("❓ QUESTION TYPE ANALYSIS")
    print("=" * 80)

    question_df = reader.get_question_type_statistics()

    if question_df.empty:
        print("❌ No question type data available")
        return

    # Create a comprehensive table showing all sports with all question types
    print("📊 ALL SPORTS BY QUESTION TYPES:")

    # Pivot the data to create a wide format table
    pivot_df = question_df.pivot(
        index="sport", columns="question_type", values="count"
    ).fillna(0)

    # Add total column
    pivot_df["total"] = pivot_df.sum(axis=1)

    # Sort by sport name
    pivot_df = pivot_df.sort_index(ascending=True)

    # Format the display
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", 10)

    print(pivot_df.to_string(float_format="%.0f"))


def display_question_type_latex(reader: DatasetAnalysisReader):
    """Display question type statistics as a LaTeX table."""
    print("\n" + "=" * 80)
    print("❓ QUESTION TYPE ANALYSIS - LATEX TABLE")
    print("=" * 80)

    question_df = reader.get_question_type_statistics()

    if question_df.empty:
        print("❌ No question type data available")
        return

    # Pivot the data to create a wide format table
    pivot_df = question_df.pivot(
        index="sport", columns="question_type", values="count"
    ).fillna(0)

    # Add total column
    pivot_df["total"] = pivot_df.sum(axis=1)

    # Sort by sport name
    pivot_df = pivot_df.sort_index(ascending=True)

    # Get question types (excluding 'total')
    question_types = [col for col in pivot_df.columns if col != "total"]

    # Create LaTeX table
    latex_table = []
    latex_table.append("\\begin{table}[htb]")
    latex_table.append("\\centering\\footnotesize")
    latex_table.append("\\caption{Question Type Distribution by Sport}")
    latex_table.append("\\label{tab:question-types}")

    # Create column specification - sport + question types + total
    col_spec = "rl" + "r" * len(question_types) + "r"
    latex_table.append(f"\\begin{{tabular}}{{{col_spec}}}")
    latex_table.append("\\toprule")

    # Create header row
    header = (
        ["& Sport"]
        + [qtype.replace("_", "\\_") for qtype in question_types]
        + ["Total"]
    )
    latex_table.append(" & ".join(header) + " \\\\")
    latex_table.append("\\midrule")

    # Add data rows
    for idx, sport_name in enumerate(pivot_df.index, start=0):
        row_data = [
            f"{idx}",
            sport_name.replace("_", "").lower(),
        ]  # Escape underscores for LaTeX

        # Add question type counts
        for qtype in question_types:
            count = int(pivot_df.loc[sport_name, qtype])
            row_data.append(f"{count:,}" if count > 0 else "0")

        # Add total
        total = int(pivot_df.loc[sport_name, "total"])
        row_data.append(f"\\textbf{{{total:,}}}")

        latex_table.append(" & ".join(row_data) + " \\\\")

    # Add totals row
    latex_table.append("\\midrule")
    totals_row = ["\\textbf{Total}"]

    # Calculate column totals
    for qtype in question_types:
        col_total = int(pivot_df[qtype].sum())
        totals_row.append(f"\\textbf{{{col_total:,}}}")

    # Grand total
    grand_total = int(pivot_df["total"].sum())
    totals_row.append(f"\\textbf{{{grand_total:,}}}")

    latex_table.append(" & ".join(totals_row) + " \\\\")

    latex_table.append("\\bottomrule")
    latex_table.append("\\end{tabular}")
    latex_table.append("\\end{table}")

    # Print the LaTeX table
    print("\n".join(latex_table))


def display_sport_comparison(reader: DatasetAnalysisReader, sports: List[str]):
    """Display detailed comparison between specific sports."""
    print("\n" + "=" * 80)
    print("🏆 SPORT COMPARISON")
    print("=" * 80)

    for sport in sports:
        data = reader.get_sport_data(sport)
        if not data or "error" in data:
            print(f"❌ No data available for {sport}")
            continue

        print(f"\n🏀 {sport}:")

        # Overview
        overview = data.get("overview", {})
        print(f"   📊 Overview:")
        print(f"     Total examples: {overview.get('total_examples', 0):,}")
        print(f"     Unique contexts: {overview.get('unique_contexts', 0):,}")
        print(f"     Unique questions: {overview.get('unique_questions', 0):,}")
        print(
            f"     Questions without answers: {overview.get('questions_without_answers', 0):,} ({overview.get('percentage_without_answers', 0):.1f}%)"
        )

        # Lengths
        length_stats = data.get("length_distributions", {})
        print(f"   📏 Average lengths:")
        for content_type in ["context", "question", "answer"]:
            stats = length_stats.get(content_type, {})
            print(f"     {content_type}: {stats.get('mean', 0):.1f} words")

        # Question types
        question_types = data.get("question_types", {})
        if question_types:
            print(f"   ❓ Top question types:")
            sorted_types = sorted(
                question_types.items(), key=lambda x: x[1]["count"], reverse=True
            )
            for q_type, stats in sorted_types[:3]:
                print(f"     {q_type}: {stats['count']:,} ({stats['percentage']:.1f}%)")


def display_error_summary(reader: DatasetAnalysisReader):
    """Display summary of sports with errors."""
    error_sports = reader.get_sports_with_errors()

    if not error_sports:
        print("\n✅ No sports with errors found!")
        return

    print("\n" + "=" * 80)
    print("❌ SPORTS WITH ERRORS")
    print("=" * 80)

    for sport in error_sports:
        data = reader.get_sport_data(sport)
        error_msg = data.get("error", "Unknown error")
        print(f"   {sport}: {error_msg}")


def main():
    """Main function to run the display analysis."""
    import argparse

    parser = argparse.ArgumentParser(description="Display dataset analysis results")
    parser.add_argument(
        "--results-dir",
        type=str,
        default="output/analysis_results",
        help="Directory containing analysis results (default: output/analysis_results)",
    )
    parser.add_argument(
        "--compare-sports",
        type=str,
        nargs="+",
        help="Specific sports to compare in detail",
    )
    parser.add_argument(
        "--show-errors", action="store_true", help="Show only sports with errors"
    )

    args = parser.parse_args()

    # Initialize reader
    reader = DatasetAnalysisReader(args.results_dir)

    if not reader.sport_data:
        print("❌ No analysis data found. Please run the analysis script first.")
        return

    # Display based on arguments
    if args.show_errors:
        display_error_summary(reader)
    elif args.compare_sports:
        display_sport_comparison(reader, args.compare_sports)
    else:
        # Display comprehensive analysis
        display_overview_table(reader)
        display_overview_latex(reader)
        display_question_type_table(reader)
        display_question_type_latex(reader)
        display_error_summary(reader)

    print("\n" + "=" * 80)
    print("✅ Analysis display complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
