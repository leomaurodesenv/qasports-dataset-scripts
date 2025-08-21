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
            "sport": sport.lower(),
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


def print_latex_table_advanced(results: List[Dict]):
    """Print results in advanced LaTeX table format with proper column structure."""
    print("\n" + "=" * 80)
    print("ADVANCED LATEX TABLE FORMAT")
    print("=" * 80)

    # Group results by sport and model
    sport_results = {}
    base_models = set()  # BM25, TFIDF, DPR
    k_values = [1, 10, 20]  # Define the K values we want to display

    for result in results:
        if "error" in result:
            continue
        sport = result["sport"]
        model = result["model"]

        # Extract base model name (BM25, TFIDF, DPR) and K value
        if "-k" in model:
            base_model, k_part = model.split("-k", 1)
            try:
                k_value = int(k_part)
                if k_value in k_values:
                    base_models.add(base_model)
                    if sport not in sport_results:
                        sport_results[sport] = {}
                    if base_model not in sport_results[sport]:
                        sport_results[sport][base_model] = {}

                    # Extract recall value
                    retriever_results = result["results"].get("Retriever", {})
                    recall_value = retriever_results.get("recall_multi_hit", 0.0)
                    sport_results[sport][base_model][k_value] = recall_value
            except ValueError:
                continue

    # Sort base models and sports for consistent ordering
    sorted_base_models = ["BM25", "TFIDF", "DPR"]  # sorted(list(base_models))
    sorted_sports = sorted(list(sport_results.keys()))

    # Print LaTeX table
    print("\\begin{table}[htb]")
    print("\\centering\\footnotesize")
    print("\\caption{Document Retriever Recall@K by Sport and Model.}")
    print("\\label{tab:experiment:document-retriever}")
    print("\\begin{tabular}{r l *{9}{c}}")
    print("\\toprule")

    # Print model headers
    model_header = "& \\multicolumn{1}{c}{\\textbf{Sport Subset}}"
    for base_model in sorted_base_models:
        model_header += f" & \\multicolumn{{3}}{{c}}{{\\textbf{{{base_model}}}}}"
    print(model_header + " \\\\")

    # Print cmidrule lines
    cmidrule_line = "\\cmidrule(lr){3-5}"
    col_start = 6
    for i in range(1, len(sorted_base_models)):
        cmidrule_line += f" \\cmidrule(lr){{{col_start}-{col_start + 2}}}"
        col_start += 3
    print(cmidrule_line)

    # Print K value headers
    k_header = "& "
    for base_model in sorted_base_models:
        for k in k_values:
            k_header += f" & \\textbf{{K={k}}}"
    print(k_header + " \\\\")
    print("\\midrule")

    # Print data rows
    for idx, sport in enumerate(sorted_sports):
        row = f"{idx} & {sport}"

        # Find the highest value for each K value across all models
        max_values = {}
        for k in k_values:
            max_value = float("-inf")
            for base_model in sorted_base_models:
                model_data = sport_results[sport].get(base_model, {})
                value = model_data.get(k, 0.0)
                if isinstance(value, (int, float)) and value > max_value:
                    max_value = value
            max_values[k] = max_value

        # Build the row with \hcell for highest values
        for base_model in sorted_base_models:
            model_data = sport_results[sport].get(base_model, {})
            for k in k_values:
                value = model_data.get(k, 0.0)
                if isinstance(value, (int, float)):
                    # Check if this is the highest value for this K
                    if value == max_values[k]:
                        row += f" & \\hcell{{{value:.3f}}}"
                    else:
                        row += f" & {value:.3f}"
                else:
                    row += " & N/A"
        print(row + " \\\\")

    print("\\bottomrule")
    print("\\end{tabular}")
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
    print_latex_table_advanced(results)
    print(f"\nTotal experiments processed: {len(results)}")
    successful = len([r for r in results if "error" not in r])
    print(f"Successful reads: {successful}")
    print(f"Errors: {len(results) - successful}")


if __name__ == "__main__":
    main()
