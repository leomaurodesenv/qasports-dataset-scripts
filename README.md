# 📄 QASports2: Question Answering Dataset about Sports

[![GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=blue&style=flat-square)](https://github.com/leomaurodesenv/qasports-dataset-scripts)
[![MIT license](https://img.shields.io/static/v1?label=License&message=MIT&color=blue&style=flat-square)](LICENSE)
[![Python](https://img.shields.io/static/v1?label=Python&message=3.9&color=blue&style=flat-square)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/static/v1?label=Package&message=uv&color=orange&style=flat-square)](https://github.com/astral-sh/uv)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/leomaurodesenv/qasports-dataset-scripts/continuous-integration.yml?label=Build&style=flat-square)](https://github.com/leomaurodesenv/qasports-dataset-scripts/actions/workflows/continuous-integration.yml)

> **The first large-scale, open-domain sports question answering dataset**

QASports is a comprehensive dataset featuring over **1 million question-answer-context tuples** derived from more than **400,000 thoroughly preprocessed, cleaned, and organized documents** about players, teams, and matches from multiple sports. The data is sourced from Wikipedia-like resources to ensure quality and relevance.

## 📚 Research Paper

**Pedro Calciolari Jardim, Leonardo Mauro Pereira Moraes, and Cristina Dutra Aguiar.** [QASports: A Question Answering Dataset about Sports](https://doi.org/10.5753/dsw.2023.233602). In Proceedings of the Brazilian Symposium on Databases: Dataset Showcase Workshop, pages 1-12, Belo Horizonte, Minas Gerais, Brazil, 2023.

### Abstract

Sport is one of the most popular and revenue-generating forms of entertainment. Therefore, analyzing data related to this domain introduces several opportunities for Question Answering (QA) systems, such as supporting tactical decision-making. But, to develop and evaluate QA systems, researchers and developers need datasets that contain questions and their corresponding answers. In this paper, we focus on this issue. We propose QASports, the first large sports question answering dataset for extractive answer questions. QASports contains more than 1.5 million triples of questions, answers, and context about three popular sports: soccer, American football, and basketball. We describe the QASports processes of data collection and questions and answers generation. We also describe the characteristics of the QASports data. Furthermore, we analyze the sources used to obtain raw data and investigate the usability of QASports by issuing "wh-queries". Moreover, we describe scenarios for using QASports, highlighting its importance for training and evaluating QA systems.

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **uv** package manager ([Installation Guide](https://github.com/astral-sh/uv))

### Installation

```bash
# Clone the repository
git clone https://github.com/leomaurodesenv/qasports-dataset-scripts.git
cd qasports-dataset-scripts

# Install dependencies
uv sync

# Verify installation
uv run pre-commit run --all-files
```

## 📥 Download the Dataset

- **🎲 Full Dataset**: [OSF Repository](https://osf.io/n7r23/)
- **🎲 Formatted Dataset**: [Hugging Face Hub](https://huggingface.co/datasets/leomaurodesenv/QASports2)
- **🛠 Dataset v1**: [GitHub Release v1.1.0](https://github.com/leomaurodesenv/qasports-dataset-scripts/tree/v1.1.0)

## 🏗️ Dataset Generation Pipeline

The dataset generation process is organized into seven main stages, each contained in separate modules:

### 📁 Project Structure

```
src/
├── crawler/            # 🔍 Gather wiki links
├── fetching/           # 📥 Fetch raw HTML from links
├── processing/         # 🧹 Process and clean textual data
├── extracting_context/ # 📄 Extract contexts from data
├── question_answer/    # ❓ Generate questions and answers
├── sampling/           # 🎯 Sample representative questions
└── labeling_llm/       # 🏷️ Label samples using LLMs
```

### 🔄 Generation Steps

```bash
# 1. Crawler: Gather wiki links (~2 minutes)
uv run -m src.crawler.run

# 2. Fetching: Download wiki pages (~20 hours)
uv run -m src.fetching.run

# 3. Processing: Clean and process text (~50 minutes)
uv run -m src.processing.run

# 4. Context Extraction: Extract relevant contexts (~35 seconds)
uv run -m src.extracting_context.run

# 5. Q&A Generation: Create questions and answers (~5 days)
uv run -m src.question_answer.run
uv run -m src.question_answer.run_huggingface  # Optional

# 6. Sampling: Select representative questions
uv run -m src.sampling.run

# 7. LLM Labeling: Label samples using LLMs (~1h 30 minutes)
uv run -m src.labeling_llm.run
```

## 🧪 Experiments

This repository includes experimental frameworks for evaluating QA systems using the QASports dataset.

### Document Retriever Experiments

```bash
# Run document retriever experiments
uv run -m experiments.doc_retriever --help

# Example usage
uv run -m experiments.doc_retriever --model BM25 --num_k 3
```

### Document Reader Experiments

```bash
# Run document reader experiments
uv run -m experiments.doc_reader --help

# Example usage
uv run -m experiments.doc_reader --model RoBERTa --dataset SQuAD
```

## 📊 Dataset Statistics

- **Total Questions**: 1,000,000+
- **Source Documents**: 400,000+ preprocessed documents
- **Data Sources**: Wikipedia-like resources
- **Question Types**: Extractive QA, Wh-questions
- **Sports Covered**: Football, American Football, Basketball, Cricket, +15 Sports

```bash
# Run dataset general analysis
uv run -m experiments.dataset_analysis --help

# Example usage
uv run -m experiments.dataset_analysis --dataset QASports --sport RUGBY
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Brazilian Computer Society for hosting the Dataset Showcase Workshop
- The research community for feedback and contributions
- All contributors to the QASports dataset

## 📖 Citation

If you use QASports in your research, please cite our paper:

```bibtex
@inproceedings{jardim:2023:qasports-dataset,
    author={Pedro Calciolari Jardim and Leonardo Mauro Pereira Moraes and Cristina Dutra Aguiar},
    title = {{QASports}: A Question Answering Dataset about Sports},
    booktitle = {Proceedings of the Brazilian Symposium on Databases: Dataset Showcase Workshop},
    address = {Belo Horizonte, MG, Brazil},
    url = {https://github.com/leomaurodesenv/qasports-dataset-scripts},
    publisher = {Brazilian Computer Society},
    pages = {1-12},
    year = {2023}
}
```
