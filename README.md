# 📄 QASports: Question Answering Dataset about Sports

This repository presents a collection of codes to elaborate the dataset named "QASports", the first large sports question answering dataset for open questions. QASports contains real data of players, teams and matches from the sports soccer, basketball and American football. It counts over 1.5 million questions and answers about 54k preprocessed, cleaned and organized documents from Wikipedia-like sources.

- **Paper**: Pedro Calciolari Jardim, Leonardo Mauro Pereira Moraes, and Cristina Dutra Aguiar. [QASports: A Question Answering Dataset about Sports](https://doi.org/10.5753/dsw.2023.233602). In Proceedings of the Brazilian Symposium on Databases: Dataset Showcase Workshop, pages 1-12, Belo Horizonte, Minas Gerais, Brazil, 2023.

> **Abstract**: Sport is one of the most popular and revenue-generating forms of entertainment. Therefore, analyzing data related to this domain introduces several opportunities for Question Answering (QA) systems, such as supporting tactical decision-making. But, to develop and evaluate QA systems, researchers and developers need datasets that contain questions and their corresponding answers. In this paper, we focus on this issue. We propose QASports, the first large sports question answering dataset for extractive answer questions. QASports contains more than 1.5 million triples of questions, answers, and context about three popular sports: soccer, American football, and basketball. We describe the QASports processes of data collection and questions and answers generation. We also describe the characteristics of the QASports data. Furthermore, we analyze the sources used to obtain raw data and investigate the usability of QASports by issuing "wh-queries". Moreover, we describe scenarios for using QASports, highlighting its importance for training and evaluating QA systems.

---
## Download

- 🎲 Dataset: https://osf.io/n7r23/
- 🎲 Dataset: https://huggingface.co/datasets/PedroCJardim/QASports/

---
## Dataset Elaboration

We have sorted the resources into five separate folders.
- 🔧 [Crawlers/](Crawlers/) - Gathering wiki links.
- 🔧 [Fetching/](Fetching/) - Fetching raw HTML from links.
- 🔧 [Processing/](Processing/) - Process and clean textual data.
- 🔧 [ExtractingContexts/](ExtractingContexts/) - Extract contexts from data.
- 🔧 [QuestionAnswer/](QuestionAnswer/) - Generate questions and answers.

```sh
# Creating a virtual environment
$ python -m venv .venv
$ source .venv/bin/activate
# Installing packages
$ pip install -r requirements.txt
# Setup pre-commit
$ pre-commit install

# 1. Gathering links (run: ~35 seconds)
$ python -m Crawlers.CrawlerRun
# 2. Fetching wiki pages (run: ~40h)
$ python -m Fetching.FetchRun
# 3. Processing, clean text (run: ~50 minutes)
$ python -m Processing.ProcRun
# 4. Extracting context (run: ~35 seconds)
$ python -m ExtractingContexts.ContextRun
# 5. Questions and answers generation (run: ~36 days)
$ python -m QuestionAnswer.QARun
```

---
## Citation

```tex
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
