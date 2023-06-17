# 📄 QASports: Question Answering Dataset about Sports

This repository presents a collection of codes to elaborate the dataset named "QASports", the first large sports question answering dataset for open questions. QASports contains real data of players, teams and matches from the sports soccer, basketball and American football. It counts over one million questions and answers about 54k preprocessed, cleaned and organized documents from Wikipedia-like sources.

**Paper**: _under submission review_.

> **Abstract**: doing

---
## Download

🎲 _dataset link_

---
## Dataset Elaboration

We have sorted the resources into five separate folders.
- 🔧 [Crawlers/](Crawlers/) - Gathering wiki links.
- 🔧 [Fetching/](Fetching/) - Fetching raw data from links.
- 🔧 [Processing/](Processing/) - 
- 🔧 [ExtractingContexts/](ExtractingContexts/) - 
- 🔧 [QuestionAnswering/](QuestionAnswering/) - .

```sh
# Creating a virtual environment
$ python -m venv .venv
$ source .venv/bin/activate
# Installing packages
$ pip install -r requirements.txt

# 1. Gathering links (run: ~35 seconds)
$ python -m Crawlers.CrawlerRun
# 2. Fetching wiki pages (run: )
$ python -m Fetching.FetchRun

# ..doing..
```

---
## Citation

The citation will be updated when accepted, _paper is under submission review_.

```tex
@misc{jardim:2023:qasports-dataset,
    author={Pedro Calciolari Jardim and Leonardo Mauro Pereira Moraes and Cristina Dutra Aguiar},
    title={QASports: Question Answering Dataset about Sports},
    year={2023},
    url={https://github.com/leomaurodesenv/qasports-dataset-scripts},
}
```
