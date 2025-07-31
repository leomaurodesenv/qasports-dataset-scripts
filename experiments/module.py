"""Module to support model experiments.

This module provides classes and functionalities for conducting experiments
related to document reading and question answering using various datasets
and models. It integrates with the Haystack framework for building and
evaluating NLP pipelines.
"""

import enum
import mmh3
from abc import ABCMeta, abstractmethod

import pandas as pd
from datasets import load_dataset
from haystack.schema import Label, Document, Answer, MultiLabel


class Dataset(enum.Enum):
    """Dataset options"""

    SQuAD = 1
    AdvQA = 2
    DuoRC = 3
    QASports = 4


class DocRetriever(enum.Enum):
    """Document Retriever options"""

    BM25 = 1
    TFIDF = 2
    DPR = 3


class DocReader(str, enum.Enum):
    """Document Reader options"""

    BERT = "deepset/bert-base-uncased-squad2"
    RoBERTa = "deepset/roberta-base-squad2"
    MiniLM = "deepset/minilm-uncased-squad2"
    DistilBERT = "distilbert-base-uncased-distilled-squad"
    ELECTRA = "deepset/electra-base-squad2"


class Sports(str, enum.Enum):
    BASKETBALL = "basketball"
    FOOTBALL = "football"
    AMERICANFOOTBALL = "americanfootball"
    HOCKEY = "hockey"
    CRICKET = "cricket"
    GOLF = "golf"
    RUGBYUNION = "rugbyunion"
    RUGBY = "rugby"
    BASEBALL = "baseball"
    MARTIALARTS = "martialarts"
    BOXING = "boxing"
    MIXEDMARTIALARTS = "mixedmartialarts"
    FITNESS = "fitness"
    CYCLING = "cycling"
    BADMINTON = "badminton"
    GYMNASTICS = "gymnastics"
    HANDBALL = "handball"
    SKIING = "skiing"
    HORSE_RACING = "horse_racing"
    F1 = "f1"
    ALL = "all"


"""---
## Dataset

Importing and download the respective dataset.

### Abstract Dataset
"""


class AbstactDataset(metaclass=ABCMeta):
    """Abstract dataset class"""

    def __init__(self):
        self.raw_dataset = self.download()
        self.df_dataset = self._transform_df()
        print(f"## {self.name} ##")
        print(self.raw_dataset)

    def _transform_df(self):
        """Transform dataset in a pd.DataFrame"""
        return pd.DataFrame(self.raw_dataset)

    @property
    @abstractmethod
    def name(self):
        """Dataset name"""
        pass

    @abstractmethod
    def download(self):
        """Download the dataset"""
        pass

    @abstractmethod
    def get_documents(self):
        """Get the unique documents to store in the Document Store"""
        pass

    @abstractmethod
    def get_validation(self):
        """Get the validation set"""
        pass


class SQuadDataset(AbstactDataset):
    """
    SQuaD Dataset
    A dataset for question answering from open-domain Wikipedia articles.
    Source: https://huggingface.co/datasets/rajpurkar/squad
    """

    name = "SQuaD Dataset"
    _columns = {
        "title": "title",
        "document": "context",
        "question": "question",
    }
    _metadata = {"dataset_id": "id"}

    def download(self):
        dataset = load_dataset("squad", split="validation")
        return dataset

    def get_documents(self):
        # Remove duplicated contents
        cc = self._columns
        dataset_name = f"{self.name}"
        df = self.df_dataset
        df = df.drop_duplicates(subset=[cc["title"], cc["document"]], keep="first")

        # Create Haystack Document objects
        list_docs = []
        for _, row in df.iterrows():
            document_id = mmh3.hash128(row[cc["document"]], signed=False)
            doc_metadata = {k: row[v] for k, v in self._metadata.items()}
            doc_metadata["title"] = row[cc["title"]]
            doc_metadata["dataset_name"] = dataset_name
            doc = Document(
                id=document_id,
                content_type="text",
                content=row[cc["document"]],
                meta=doc_metadata,
            )
            list_docs.append(doc)
        return list_docs

    def _get_answers(self, data):
        # Get question answer
        return data["answers"]["text"]

    def get_validation(self):
        # Get dataset info
        cc = self._columns
        df = self.df_dataset
        _self = self

        # Create Haystack labels
        eval_labels = []
        for _, row in df.iterrows():
            document_id = mmh3.hash128(row[cc["document"]], signed=False)
            doc_label = MultiLabel(
                labels=[
                    Label(
                        query=row[cc["question"]],
                        answer=Answer(answer=answer, type="extractive"),
                        document=Document(
                            id=document_id,
                            content_type="text",
                            content=row[cc["document"]],
                        ),
                        is_correct_answer=True,
                        is_correct_document=True,
                        origin="gold-label",
                    )
                    for answer in _self._get_answers(row)
                ]
            )
            eval_labels.append(doc_label)
        return eval_labels


class AdversarialQADataset(SQuadDataset):
    """AdversarialQA Dataset
    A dataset for complex and adversarial questions.
    Source: https://huggingface.co/datasets/UCLNLP/adversarial_qa
    """

    name = "AdversarialQA Dataset"

    def download(self):
        dataset = load_dataset(
            "UCLNLP/adversarial_qa", "adversarialQA", split="validation"
        )
        return dataset


class DuoRCDataset(SQuadDataset):
    """DuoRC  Dataset
    A dataset for question answering from movie plots.
    Source: https://huggingface.co/datasets/ibm-research/duorc
    """

    name = "DuoRC Dataset"
    _columns = {
        "title": "title",
        "document": "plot",
        "question": "question",
    }
    _metadata = {"dataset_id": "question_id"}

    def download(self):
        dataset = load_dataset("duorc", "SelfRC", split="validation")
        return dataset

    def _transform_df(self):
        """Transform dataset in a pd.DataFrame"""
        df = pd.DataFrame(self.raw_dataset)
        # Get questions with answer
        return df[~df["no_answer"]]

    def _get_answers(self, data):
        # Get question answer
        return data["answers"]


class QASportsDataset(SQuadDataset):
    """QASports2  Dataset
    A dataset for sports-related Question Answering, available on Hugging Face.
    Source: https://huggingface.co/datasets/leomaurodesenv/QASports2
    """

    name = "QASports Dataset"
    _columns = {
        "title": "context_title",
        "document": "context",
        "question": "question",
    }
    _metadata = {"dataset_id": "qa_id"}

    def __init__(self, sport=None):
        self.sport = sport
        super().__init__()

    def download(self):
        dataset = load_dataset(
            "leomaurodesenv/QASports2", self.sport, split="validation"
        )
        return dataset

    def _transform_df(self):
        """Transform dataset in a pd.DataFrame"""
        df = pd.DataFrame(self.raw_dataset)
        # Get questions with answer
        df["answer"] = df["answer"].apply(eval)
        mask = df["answer"].apply(lambda x: True if x["text"] != "" else False)
        return df[mask]

    def _get_answers(self, data):
        # Get question answer
        return [data["answer"]["text"]]
