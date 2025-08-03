#!/usr/bin/env python3
"""
Script to read and extract results from doc_reader experiment output files.
Extracts sport subset, model name, and results from the last line of each file.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple


def extract_sport_and_model_from_filename(filename: str) -> str:
    """Extract sport name from filename pattern qasports-{sport}-{model}.out"""
    return filename.split("-")[1], filename.split("-")[2]


def extract_model_from_content(content: str) -> str:
    """Extract model name from the 'Model:' line in the file content."""
    for line in content.split("\n"):
        if line.startswith("Model:"):
            return line.replace("Model:", "").strip()
    return "unknown"


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
    experiments_dir: str = "output/experiments/doc_reader",
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
    print("DOC READER EXPERIMENT RESULTS SUMMARY")
    print("=" * 80)
    print(
        f"{'Sport':<20} {'Model':<35} {'Exact Match':<12} {'F1 Score':<12} {'Num Examples':<12}"
    )
    print("-" * 80)

    for result in results:
        if "error" in result:
            print(f"Error reading {result['filename']}: {result['error']}")
            continue

        sport = result["sport"]
        model = result["model"]

        # Extract metrics from results
        reader_results = result["results"].get("Reader", {})
        exact_match = reader_results.get("exact_match", "N/A")
        f1_score = reader_results.get("f1", "N/A")
        num_examples = reader_results.get("num_examples_for_eval", "N/A")

        # Format the values
        exact_match_str = (
            f"{exact_match:.4f}"
            if isinstance(exact_match, (int, float))
            else str(exact_match)
        )
        f1_score_str = (
            f"{f1_score:.4f}" if isinstance(f1_score, (int, float)) else str(f1_score)
        )
        num_examples_str = (
            f"{int(num_examples)}"
            if isinstance(num_examples, (int, float))
            else str(num_examples)
        )

        print(
            f"{sport:<20} {model:<35} {exact_match_str:<12} {f1_score_str:<12} {num_examples_str:<12}"
        )

    print("-" * 80)


def print_detailed_results(results: List[Dict]):
    """Print detailed results for each experiment."""
    print("\n" + "=" * 80)
    print("DETAILED RESULTS")
    print("=" * 80)

    for result in results:
        if "error" in result:
            print(f"\nError reading {result['filename']}: {result['error']}")
            continue

        print(f"\nFile: {result['filename']}")
        print(f"Sport: {result['sport']}")
        print(f"Model: {result['model']}")
        print(f"Results: {result['results']}")


def main():
    """Main function to read and display experiment results."""
    print("Reading doc_reader experiment results...")

    # Read all experiment files
    results = read_all_experiments()

    if not results:
        print("No experiment files found!")
        return

    # Sort results by sport and model for better readability
    results.sort(key=lambda x: (x.get("sport", ""), x.get("model", "")))

    # Print summary
    print_results_summary(results)

    # Print detailed results
    print_detailed_results(results)

    # Print statistics
    print(f"\nTotal experiments processed: {len(results)}")
    successful = len([r for r in results if "error" not in r])
    print(f"Successful reads: {successful}")
    print(f"Errors: {len(results) - successful}")


if __name__ == "__main__":
    main()
