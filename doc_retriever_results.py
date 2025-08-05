#!/usr/bin/env python3
"""
Script to read and extract results from doc_retriever experiment output files.
Extracts sport subset, model name, and results from the last line of each file.
"""

import os
import re
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List


def extract_sport_and_model_from_filename(filename: str):
    """Extract sport and model from filename pattern qasports-{sport}-{model}.out"""
    parts = filename.replace(".out", "").split("-")
    sport = parts[1]
    model = "-".join(parts[2:])
    return sport, model


def extract_results_from_last_line(content: str) -> Dict:
    """Extract results dictionary from the last non-empty line of the file."""
    lines = [line.strip() for line in content.split("\n") if line.strip()]
    if not lines:
        return {}
    last_line = lines[-1]
    try:
        # Try to evaluate the dictionary string
        results = eval(last_line)
        return results
    except (SyntaxError, NameError):
        # If eval fails, try to parse as JSON
        try:
            results = json.loads(last_line)
            return results
        except json.JSONDecodeError:
            return {"raw_last_line": last_line}


def read_experiment_file(file_path: Path) -> Dict:
    """Read a single experiment file and extract all relevant information."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        sport, model = extract_sport_and_model_from_filename(file_path.name)
        results = extract_results_from_last_line(content)
        return {
            "filename": file_path.name,
            "sport": sport,
            "model": model,
            "results": results,
        }
    except Exception as e:
        return {"filename": file_path.name, "error": str(e)}


def read_all_experiments(
    experiments_dir: str = "output/experiments/doc_retriever",
) -> List[Dict]:
    """Read all experiment files and extract results."""
    experiments_path = Path(experiments_dir)
    if not experiments_path.exists():
        print(f"Error: Directory {experiments_dir} does not exist")
        return []
    results = []
    for file_path in experiments_path.glob("*.out"):
        result = read_experiment_file(file_path)
        results.append(result)
    return results


def print_results_summary(results: List[Dict]):
    """Print a formatted summary of all experiment results."""
    print("=" * 80)
    print("DOC RETRIEVER EXPERIMENT RESULTS SUMMARY")
    print("=" * 80)
    print(
        f"{'Sport':<10} {'Model':<30} {'Recall@K':<12} {'Precision':<12} {'MAP':<12} {'MRR':<12} {'NDCG':<12}"
    )
    print("-" * 80)
    for result in results:
        if "error" in result:
            print(f"Error reading {result['filename']}: {result['error']}")
            continue
        sport = result["sport"]
        model = result["model"]
        retriever_results = result["results"].get("Retriever", {})
        recall = retriever_results.get("recall_multi_hit", "N/A")
        precision = retriever_results.get("precision", "N/A")
        map_ = retriever_results.get("map", "N/A")
        mrr = retriever_results.get("mrr", "N/A")
        ndcg = retriever_results.get("ndcg", "N/A")
        print(
            f"{sport:<10} {model:<30} {recall:<12.4f} {precision:<12.4f} {map_:<12.4f} {mrr:<12.4f} {ndcg:<12.4f}"
            if all(
                isinstance(x, (int, float))
                for x in [recall, precision, map_, mrr, ndcg]
            )
            else f"{sport:<10} {model:<30} {recall:<12} {precision:<12} {map_:<12} {mrr:<12} {ndcg:<12}"
        )
    print("-" * 80)


def print_latex_table(results: List[Dict]):
    """Print results in LaTeX table format."""
    print("\n" + "=" * 80)
    print("LATEX TABLE FORMAT")
    print("=" * 80)
    # Group results by sport
    sport_results = {}
    for result in results:
        if "error" in result:
            continue
        sport = result["sport"]
        model = result["model"]
        recall = result["results"].get("Retriever", {}).get("recall_multi_hit", None)
        if sport not in sport_results:
            sport_results[sport] = {}
        sport_results[sport][model] = recall
    # Print LaTeX table header
    print("\\begin{table}[h]")
    print("\\centering")
    print("\\begin{tabular}{lcccc}")
    print("\\toprule")
    print("& \\textbf{Sport} & \\textbf{Model} & \\textbf{Recall@K} \\\\")
    print("\\midrule")
    row_num = 0
    for sport in sorted(sport_results.keys()):
        for model, recall in sport_results[sport].items():
            recall_str = (
                f"{recall * 100:.2f}\\%"
                if isinstance(recall, (int, float))
                else str(recall)
            )
            print(f"{row_num} & {sport} & {model} & {recall_str} \\\\")
            row_num += 1
    print("\\bottomrule")
    print("\\end{tabular}")
    print("\\caption{Doc Retriever Recall@K by Sport and Model}")
    print("\\label{tab:doc_retriever_results}")
    print("\\end{table}")


def main():
    """Main function to read and display experiment results."""
    print("Reading doc_retriever experiment results...")
    results = read_all_experiments()
    if not results:
        print("No experiment files found!")
        return
    results.sort(key=lambda x: (x.get("model", ""), x.get("sport", "")))
    print_results_summary(results)
    # print_latex_table(results)
    print(f"\nTotal experiments processed: {len(results)}")
    successful = len([r for r in results if "error" not in r])
    print(f"Successful reads: {successful}")
    print(f"Errors: {len(results) - successful}")


if __name__ == "__main__":
    main()
