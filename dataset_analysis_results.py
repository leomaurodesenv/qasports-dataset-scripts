"""
Dataset Analysis Results Script

This script iterates through all sports in the Sports enum and uses the analysis methods
from experiments/dataset_analysis.py to generate a comprehensive JSON file with all results.
"""

import json
from datetime import datetime

from experiments.module import Dataset, Sports, DatasetSplit, dataset_switch
from experiments.dataset_analysis import (
    analyze_length_distributions,
    analyze_question_types,
    analyze_dataset_overview,
)


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
    output_file: str = "dataset_analysis_results.json",
    split: DatasetSplit = DatasetSplit.TRAIN,
    include_all_sport: bool = True,
):
    """
    Generate comprehensive analysis for all sports and save to JSON file.

    Args:
        output_file: Path to the output JSON file
        split: The dataset split to analyze
        include_all_sport: Whether to include the "ALL" sport category
    """
    print("🚀 Starting comprehensive dataset analysis...")
    print(f"📊 Analyzing split: {split.value}")
    print(f"📁 Output file: {output_file}")

    # Get all sports from the enum
    sports_to_analyze = list(Sports)

    # Optionally exclude the "ALL" sport
    if not include_all_sport:
        sports_to_analyze = [
            sport for sport in sports_to_analyze if sport != Sports.ALL
        ]

    print(f"🏃‍♂️ Analyzing {len(sports_to_analyze)} sports...")

    # Analyze each sport
    all_results = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_sports": len(sports_to_analyze),
            "split_analyzed": split.value,
            "include_all_sport": include_all_sport,
        },
        "sports": [],
    }

    for i, sport in enumerate(sports_to_analyze, 1):
        print(f"\n📈 Progress: {i}/{len(sports_to_analyze)}")
        sport_results = analyze_sport_dataset(sport, split)
        all_results["sports"].append(sport_results)

    # Calculate summary statistics across all sports
    print("\n📊 Calculating summary statistics...")
    all_results["summary"] = calculate_summary_statistics(all_results["sports"])

    # Save results to JSON file
    print(f"\n💾 Saving results to {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"✅ Analysis complete! Results saved to {output_file}")

    # Print summary
    print_summary(all_results)


def calculate_summary_statistics(sports_results):
    """
    Calculate summary statistics across all sports.

    Args:
        sports_results: List of analysis results for each sport

    Returns:
        dict: Summary statistics
    """
    summary = {
        "total_examples_across_sports": 0,
        "total_unique_contexts": 0,
        "total_unique_questions": 0,
        "total_questions_without_answers": 0,
        "sports_with_data": 0,
        "sports_with_errors": 0,
        "average_context_length": 0,
        "average_question_length": 0,
        "average_answer_length": 0,
        "most_common_question_types": {},
    }

    # Aggregate statistics
    context_lengths = []
    question_lengths = []
    answer_lengths = []
    question_type_counts = {}

    for sport_result in sports_results:
        if "error" in sport_result:
            summary["sports_with_errors"] += 1
            continue

        summary["sports_with_data"] += 1

        # Overview statistics
        overview = sport_result.get("overview", {})
        summary["total_examples_across_sports"] += overview.get("total_examples", 0)
        summary["total_unique_contexts"] += overview.get("unique_contexts", 0)
        summary["total_unique_questions"] += overview.get("unique_questions", 0)
        summary["total_questions_without_answers"] += overview.get(
            "questions_without_answers", 0
        )

        # Length statistics
        length_stats = sport_result.get("length_distributions", {})
        if "context" in length_stats:
            context_lengths.extend(
                [length_stats["context"]["mean"]] * overview.get("total_examples", 0)
            )
        if "question" in length_stats:
            question_lengths.extend(
                [length_stats["question"]["mean"]] * overview.get("total_examples", 0)
            )
        if "answer" in length_stats:
            answer_lengths.extend(
                [length_stats["answer"]["mean"]] * overview.get("total_examples", 0)
            )

        # Question type statistics
        question_types = sport_result.get("question_types", {})
        for q_type, stats in question_types.items():
            if q_type not in question_type_counts:
                question_type_counts[q_type] = 0
            question_type_counts[q_type] += stats.get("count", 0)

    # Calculate averages
    if context_lengths:
        summary["average_context_length"] = sum(context_lengths) / len(context_lengths)
    if question_lengths:
        summary["average_question_length"] = sum(question_lengths) / len(
            question_lengths
        )
    if answer_lengths:
        summary["average_answer_length"] = sum(answer_lengths) / len(answer_lengths)

    # Sort question types by count
    summary["most_common_question_types"] = dict(
        sorted(question_type_counts.items(), key=lambda x: x[1], reverse=True)
    )

    return summary


def print_summary(all_results):
    """
    Print a summary of the analysis results.

    Args:
        all_results: Complete analysis results
    """
    print("\n" + "=" * 60)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 60)

    metadata = all_results["metadata"]
    summary = all_results["summary"]

    print(f"📅 Generated at: {metadata['generated_at']}")
    print(f"🏃‍♂️ Sports analyzed: {metadata['total_sports']}")
    print(f"📊 Split analyzed: {metadata['split_analyzed']}")
    print(f"✅ Sports with data: {summary['sports_with_data']}")
    print(f"❌ Sports with errors: {summary['sports_with_errors']}")

    print(f"\n📈 OVERALL STATISTICS:")
    print(f"   Total examples: {summary['total_examples_across_sports']:,}")
    print(f"   Unique contexts: {summary['total_unique_contexts']:,}")
    print(f"   Unique questions: {summary['total_unique_questions']:,}")
    print(
        f"   Questions without answers: {summary['total_questions_without_answers']:,}"
    )

    print(f"\n📏 AVERAGE LENGTHS:")
    print(f"   Context: {summary['average_context_length']:.1f} words")
    print(f"   Question: {summary['average_question_length']:.1f} words")
    print(f"   Answer: {summary['average_answer_length']:.1f} words")

    print(f"\n❓ MOST COMMON QUESTION TYPES:")
    for q_type, count in list(summary["most_common_question_types"].items())[:5]:
        print(f"   {q_type}: {count:,}")

    print("=" * 60)


# Run the analysis
generate_comprehensive_analysis(
    output_file="dataset_analysis_results.json", split=DatasetSplit.TRAIN
)
