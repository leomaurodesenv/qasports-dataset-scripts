"""
Dataset Analysis Results Script

This script iterates through all sports in the Sports enum and uses the analysis methods
from experiments/dataset_analysis.py to generate a comprehensive JSON file with all results.
"""

import json
import numpy as np
from datetime import datetime

from experiments.module import Dataset, Sports, DatasetSplit, dataset_switch
from experiments.dataset_analysis import (
    analyze_length_distributions,
    analyze_question_types,
    analyze_dataset_overview,
)


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle NumPy data types."""

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def analyze_general_dataset(
    dataset_type: Dataset, split: DatasetSplit = DatasetSplit.TRAIN
):
    """
    Analyze a specific general dataset (SQuAD2, DuoRC, AdvQA) and return comprehensive results.

    Args:
        dataset_type: The dataset type to analyze
        split: The dataset split to analyze (default: TRAIN)

    Returns:
        dict: Analysis results for the dataset
    """
    print(f"🔍 Analyzing {dataset_type.name} dataset...")

    try:
        # Get the dataset - general datasets don't need sport parameter but it's required
        # Use a dummy sport value since it's not used for these datasets
        dataset = dataset_switch(
            choice=dataset_type,
            sport=Sports.BASKETBALL,  # Dummy value, not used for general datasets
            split=split,
            remove_empty_answers=False,
        )

        # Perform comprehensive analysis
        results = {
            "dataset": dataset_type.name,
            "dataset_value": dataset_type.value,
            "split": split.value,
            "analysis_timestamp": datetime.now().isoformat(),
            "overview": analyze_dataset_overview(dataset),
            "length_distributions": analyze_length_distributions(dataset),
            "question_types": analyze_question_types(dataset),
        }

        print(f"✅ Completed analysis for {dataset_type.name}")
        return results

    except Exception as e:
        print(f"❌ Error analyzing {dataset_type.name}: {str(e)}")
        return {
            "dataset": dataset_type.name,
            "dataset_value": dataset_type.value,
            "split": split.value,
            "analysis_timestamp": datetime.now().isoformat(),
            "error": str(e),
            "overview": {},
            "length_distributions": {},
            "question_types": {},
        }


def generate_comprehensive_analysis_general_datasets(
    output_dir: str = "analysis_results_general",
    split: DatasetSplit = DatasetSplit.TRAIN,
    datasets_to_analyze: list = None,
):
    """
    Generate comprehensive analysis for general datasets (SQuAD2, DuoRC, AdvQA) and save individual JSON files.

    Args:
        output_dir: Directory to save individual dataset analysis files
        split: The dataset split to analyze
        datasets_to_analyze: List of datasets to analyze (default: [SQuAD2, DuoRC, AdvQA])
    """
    print("🚀 Starting comprehensive general datasets analysis...")
    print(f"📊 Analyzing split: {split.value}")
    print(f"📁 Output directory: {output_dir}")

    # Create output directory if it doesn't exist
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Default datasets to analyze
    if datasets_to_analyze is None:
        datasets_to_analyze = [Dataset.SQuAD2, Dataset.DuoRC, Dataset.AdvQA]

    print(f"🏃‍♂️ Analyzing {len(datasets_to_analyze)} datasets...")

    # Track overall statistics
    successful_analyses = 0
    failed_analyses = 0

    for i, dataset_type in enumerate(datasets_to_analyze, 1):
        print(f"\n📈 Progress: {i}/{len(datasets_to_analyze)}")

        # Analyze individual dataset
        dataset_results = analyze_general_dataset(dataset_type, split)

        # Save individual dataset results
        dataset_filename = f"{dataset_type.name.lower()}_{split.value}_analysis.json"
        dataset_filepath = os.path.join(output_dir, dataset_filename)

        try:
            with open(dataset_filepath, "w", encoding="utf-8") as f:
                json.dump(
                    dataset_results, f, indent=2, ensure_ascii=False, cls=NumpyEncoder
                )
            print(f"💾 Saved {dataset_type.name} results to {dataset_filepath}")
            successful_analyses += 1
        except Exception as e:
            print(f"❌ Failed to save {dataset_type.name} results: {str(e)}")
            failed_analyses += 1

    # Create a summary file with metadata
    summary_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_datasets": len(datasets_to_analyze),
            "split_analyzed": split.value,
            "successful_analyses": successful_analyses,
            "failed_analyses": failed_analyses,
            "output_directory": output_dir,
            "datasets_analyzed": [dataset.name for dataset in datasets_to_analyze],
        },
        "files_generated": [
            f"{dataset.name.lower()}_{split.value}_analysis.json"
            for dataset in datasets_to_analyze
        ],
    }

    summary_filepath = os.path.join(
        output_dir, f"analysis_summary_general_{split.value}.json"
    )
    with open(summary_filepath, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)

    print(f"\n✅ General datasets analysis complete!")
    print(f"📊 Successful analyses: {successful_analyses}")
    print(f"❌ Failed analyses: {failed_analyses}")
    print(f"📁 Results saved to: {output_dir}")
    print(f"📋 Summary saved to: {summary_filepath}")

    # Print summary
    print_general_analysis_summary(summary_data)


def print_general_analysis_summary(summary_data):
    """
    Print a summary of the general datasets analysis results.

    Args:
        summary_data: Summary data with metadata and file information
    """
    print("\n" + "=" * 60)
    print("📊 GENERAL DATASETS ANALYSIS SUMMARY")
    print("=" * 60)

    metadata = summary_data["metadata"]

    print(f"📅 Generated at: {metadata['generated_at']}")
    print(f"🗃️ Datasets analyzed: {metadata['total_datasets']}")
    print(f"📊 Split analyzed: {metadata['split_analyzed']}")
    print(f"✅ Successful analyses: {metadata['successful_analyses']}")
    print(f"❌ Failed analyses: {metadata['failed_analyses']}")
    print(f"📁 Output directory: {metadata['output_directory']}")

    print(f"\n🗃️ DATASETS ANALYZED:")
    for dataset_name in metadata["datasets_analyzed"]:
        print(f"   📖 {dataset_name}")

    print(f"\n📄 FILES GENERATED:")
    for filename in summary_data["files_generated"]:
        print(f"   📄 {filename}")

    print("\n💡 Each dataset analysis file contains:")
    print("   - Overview statistics (total examples, unique contexts/questions)")
    print("   - Length distributions (context, question, answer)")
    print("   - Question type analysis (WH-words distribution)")
    print("   - Error information (if any)")

    print("=" * 60)


def analyze_sport_dataset(sport: Sports, split: DatasetSplit = DatasetSplit.TRAIN):
    """
    Analyze a specific sport dataset and return comprehensive results.

    Args:
        sport: The sport to analyze
        split: The dataset split to analyze (default: TRAIN)

    Returns:
        dict: Analysis results for the sport
    """
    print(f"🔍 Analyzing {sport.name} ({sport.value})...")

    try:
        # Get the dataset for this sport
        dataset = dataset_switch(
            choice=Dataset.QASports,
            sport=sport,
            split=split,
            remove_empty_answers=False,
        )

        # Perform comprehensive analysis
        results = {
            "sport": sport.name,
            "sport_value": sport.value,
            "split": split.value,
            "analysis_timestamp": datetime.now().isoformat(),
            "overview": analyze_dataset_overview(dataset),
            "length_distributions": analyze_length_distributions(dataset),
            "question_types": analyze_question_types(dataset),
        }

        print(f"✅ Completed analysis for {sport.name}")
        return results

    except Exception as e:
        print(f"❌ Error analyzing {sport.name}: {str(e)}")
        return {
            "sport": sport.name,
            "sport_value": sport.value,
            "split": split.value,
            "analysis_timestamp": datetime.now().isoformat(),
            "error": str(e),
            "overview": {},
            "length_distributions": {},
            "question_types": {},
        }


def generate_comprehensive_analysis(
    output_dir: str = "analysis_results",
    split: DatasetSplit = DatasetSplit.TRAIN,
    include_all_sport: bool = True,
):
    """
    Generate comprehensive analysis for all sports and save individual JSON files.

    Args:
        output_dir: Directory to save individual sport analysis files
        split: The dataset split to analyze
        include_all_sport: Whether to include the "ALL" sport category
    """
    print("🚀 Starting comprehensive dataset analysis...")
    print(f"📊 Analyzing split: {split.value}")
    print(f"📁 Output directory: {output_dir}")

    # Create output directory if it doesn't exist
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Get all sports from the enum
    sports_to_analyze = list(Sports)

    # Optionally exclude the "ALL" sport
    if not include_all_sport:
        sports_to_analyze = [
            sport for sport in sports_to_analyze if sport != Sports.ALL
        ]

    print(f"🏃‍♂️ Analyzing {len(sports_to_analyze)} sports...")

    # Track overall statistics
    successful_analyses = 0
    failed_analyses = 0

    for i, sport in enumerate(sports_to_analyze, 1):
        print(f"\n📈 Progress: {i}/{len(sports_to_analyze)}")

        # Analyze individual sport
        sport_results = analyze_sport_dataset(sport, split)

        # Save individual sport results
        sport_filename = f"{sport.value}_{split.value}_analysis.json"
        sport_filepath = os.path.join(output_dir, sport_filename)

        try:
            with open(sport_filepath, "w", encoding="utf-8") as f:
                json.dump(
                    sport_results, f, indent=2, ensure_ascii=False, cls=NumpyEncoder
                )
            print(f"💾 Saved {sport.name} results to {sport_filepath}")
            successful_analyses += 1
        except Exception as e:
            print(f"❌ Failed to save {sport.name} results: {str(e)}")
            failed_analyses += 1

    # Create a summary file with metadata
    summary_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_sports": len(sports_to_analyze),
            "split_analyzed": split.value,
            "include_all_sport": include_all_sport,
            "successful_analyses": successful_analyses,
            "failed_analyses": failed_analyses,
            "output_directory": output_dir,
        },
        "files_generated": [
            f"{sport.value}_{split.value}_analysis.json" for sport in sports_to_analyze
        ],
    }

    summary_filepath = os.path.join(output_dir, f"analysis_summary_{split.value}.json")
    with open(summary_filepath, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)

    print(f"\n✅ Analysis complete!")
    print(f"📊 Successful analyses: {successful_analyses}")
    print(f"❌ Failed analyses: {failed_analyses}")
    print(f"📁 Results saved to: {output_dir}")
    print(f"📋 Summary saved to: {summary_filepath}")

    # Print summary
    print_analysis_summary(summary_data)


def print_analysis_summary(summary_data):
    """
    Print a summary of the analysis results.

    Args:
        summary_data: Summary data with metadata and file information
    """
    print("\n" + "=" * 60)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 60)

    metadata = summary_data["metadata"]

    print(f"📅 Generated at: {metadata['generated_at']}")
    print(f"🏃‍♂️ Sports analyzed: {metadata['total_sports']}")
    print(f"📊 Split analyzed: {metadata['split_analyzed']}")
    print(f"✅ Successful analyses: {metadata['successful_analyses']}")
    print(f"❌ Failed analyses: {metadata['failed_analyses']}")
    print(f"📁 Output directory: {metadata['output_directory']}")

    print(f"\n📄 FILES GENERATED:")
    for filename in summary_data["files_generated"][:10]:  # Show first 10 files
        print(f"   📄 {filename}")

    if len(summary_data["files_generated"]) > 10:
        print(f"   ... and {len(summary_data['files_generated']) - 10} more files")

    print("\n💡 Each sport analysis file contains:")
    print("   - Overview statistics (total examples, unique contexts/questions)")
    print("   - Length distributions (context, question, answer)")
    print("   - Question type analysis (WH-words distribution)")
    print("   - Error information (if any)")

    print("=" * 60)


# Run the analysis
# generate_comprehensive_analysis(
#    output_dir="output/analysis_results", split=DatasetSplit.TRAIN
# )

# Run the general datasets analysis
# Uncomment the line below to analyze SQuAD2, DuoRC, and AdvQA datasets
generate_comprehensive_analysis_general_datasets(
    output_dir="output/analysis_results",
    split=DatasetSplit.TRAIN,
    datasets_to_analyze=[Dataset.SQuAD2, Dataset.DuoRC, Dataset.AdvQA],
)
