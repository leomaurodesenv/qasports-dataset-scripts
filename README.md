# 📄 QASports: Question Answering Dataset about Sports

This repository presents a collection of codes to elaborate the dataset named "QASports", the first large sports question answering dataset for open questions. QASports contains real data of players, teams and matches from the sports soccer, basketball and American football. It counts over one million questions and answers about 54k preprocessed, cleaned and organized documents from Wikipedia-like sources.

**Paper**: _under submission review_.

> **Abstract**: writing.

---
## Download

🎲 _dataset link_

---
## Dataset Elaboration

We have sorted the resources into five separate folders.
- 🔧 [Crawlers/](Crawlers/) - Gathering wiki links.
- 🔧 [Fetching/](Fetching/) - Fetching raw HTML from links.
- 🔧 [Processing/](Processing/) - Process and clean textual data.
- 🔧 [ExtractingContexts/](ExtractingContexts/) - Extract contexts from data.
- 🔧 [QuestionAnswering/](QuestionAnswering/) - Generate question and answers.

```sh
# Creating a virtual environment
$ python -m venv .venv
$ source .venv/bin/activate
# Installing packages
$ pip install -r requirements.txt

# 1. Gathering links (run: ~35 seconds)
$ python -m Crawlers.CrawlerRun
# 2. Fetching wiki pages (run: ~97h)
$ python -m Fetching.FetchRun
# 3. Processing, clean text (run: ~50 minutes)
$ python -m Processing.ProcRun
# 4. Extracting context (run: ~35 seconds)
$ python -m ExtractingContexts.ContextRun
# 5. Question and answer generation (run: ~39 days)
$ python -m 
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
