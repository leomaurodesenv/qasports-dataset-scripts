# 📄 QASports: Question Answering Dataset about Sports

[![GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=blue&style=flat-square)](https://github.com/leomaurodesenv/qasports-dataset-scripts)
[![MIT license](https://img.shields.io/static/v1?label=License&message=MIT&color=blue&style=flat-square)](LICENSE)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/leomaurodesenv/qasports-dataset-scripts/continuous-integration.yml?label=Build&style=flat-square)](https://github.com/leomaurodesenv/qasports-dataset-scripts/actions/workflows/continuous-integration.yml)


This repository presents a collection of codes to elaborate the dataset named "QASports", the first large sports question answering dataset for open questions. QASports contains real data of players, teams and matches from the sports soccer, basketball and American football. It counts over 1.5 million questions and answers about 54k preprocessed, cleaned and organized documents from Wikipedia-like sources.

- **Paper**: Pedro Calciolari Jardim, Leonardo Mauro Pereira Moraes, and Cristina Dutra Aguiar. [QASports: A Question Answering Dataset about Sports](https://doi.org/10.5753/dsw.2023.233602). In Proceedings of the Brazilian Symposium on Databases: Dataset Showcase Workshop, pages 1-12, Belo Horizonte, Minas Gerais, Brazil, 2023.

> **Abstract**: Sport is one of the most popular and revenue-generating forms of entertainment. Therefore, analyzing data related to this domain introduces several opportunities for Question Answering (QA) systems, such as supporting tactical decision-making. But, to develop and evaluate QA systems, researchers and developers need datasets that contain questions and their corresponding answers. In this paper, we focus on this issue. We propose QASports, the first large sports question answering dataset for extractive answer questions. QASports contains more than 1.5 million triples of questions, answers, and context about three popular sports: soccer, American football, and basketball. We describe the QASports processes of data collection and questions and answers generation. We also describe the characteristics of the QASports data. Furthermore, we analyze the sources used to obtain raw data and investigate the usability of QASports by issuing "wh-queries". Moreover, we describe scenarios for using QASports, highlighting its importance for training and evaluating QA systems.

---
## Download

- 🎲 Full Dataset: https://osf.io/n7r23/
- 🎲 Preprocessed Dataset v1: https://huggingface.co/datasets/PedroCJardim/QASports
- 🎲 Preprocessed Dataset v2: https://huggingface.co/datasets/leomaurodesenv/QASports2

---
## Dataset Elaboration

We have sorted the resources into five separate folders.
- 🔧 [src/crawler/](src/crawler/) - Gather wiki links.
- 🔧 [src/fetching/](src/fetching/) - Fetch raw HTML from links.
- 🔧 [src/processing/](src/processing/) - Process and clean textual data.
- 🔧 [src/extracting_context/](src/extracting_context/) - Extract contexts from data.
- 🔧 [src/question_answer/](src/question_answer/) - Generate questions and answers.
- 🔧 [src/sampling/](src/sampling/) - Sample representative questions and answers.

```sh
# Setup `uv` in your machine
# https://github.com/astral-sh/uv
# Installing packages
$ uv sync
# Testing pre-commit
$ uv run pre-commit run --all-files

# 1. Crawler links (run: ~35 seconds)
$ uv run -m src.crawler.run
# 2. Fetching wiki pages (run: ~40h)
$ uv run -m src.fetching.run
# 3. Processing, clean text (run: ~50 minutes)
$ uv run -m src.processing.run
# 4. Extracting context (run: ~35 seconds)
$ uv run -m src.extracting_context.run
# 5. Questions and answers generation (run: ~36 days)
$ uv run -m src.question_answer.run
$ uv run -m src.question_answer.run_huggingface # optional
# 6. Sampling representative questions (run: )
$ uv run -m src.sampling.run
```

---
## Citation

```tex
# QASports: A Question Answering Dataset about Sports
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
