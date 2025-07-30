"""Document Reader Experiments"""

from haystack import Pipeline
from haystack.nodes import FARMReader
from haystack.utils import print_answers

from .module import Dataset, DocReader, Sports
from .module import (
    SQuadDataset,
    AdversarialQADataset,
    DuoRCDataset,
    QASportsDataset,
)


# Model setup
NUM_K = 1  # always = 1
DATASET = Dataset.QASports
DOC_READER = DocReader.BERT
SPORT = Sports.SKIING


# Download the dataset
def dataset_switch(choice):
    """Get dataset class"""

    if choice == Dataset.SQuAD:
        return SQuadDataset()
    elif choice == Dataset.AdvQA:
        return AdversarialQADataset()
    elif choice == Dataset.DuoRC:
        return DuoRCDataset()
    elif choice == Dataset.QASports:
        return QASportsDataset(SPORT)
    else:
        return "Invalid dataset"


# Get the dataset
dataset = dataset_switch(DATASET)
docs = dataset.get_documents()

"""---
## Document Reader

In this experiment, we explored three Transformer based models for extractive Question Answering using the [FARM framework](https://github.com/deepset-ai/FARM).
* [BERT paper](https://arxiv.org/abs/1810.04805), [implementation](https://huggingface.co/deepset/bert-base-uncased-squad2)
* [RoBERTa paper](https://arxiv.org/abs/1907.11692), [implementation](https://huggingface.co/deepset/roberta-base-squad2)
* [MiniLM paper](https://arxiv.org/abs/2002.10957), [implementation](https://huggingface.co/deepset/minilm-uncased-squad2)

"""

# Get the reader
reader = FARMReader(DOC_READER, use_gpu=True)

# Build the pipeline
pipe = Pipeline()
pipe.add_node(component=reader, name="Reader", inputs=["Query"])

# Querying documents
question = "Who did the Raptors face in the first round of the 2015 Playoffs?"
prediction = pipe.run(
    query=question, documents=docs[0:10], params={"Reader": {"top_k": 3}}
)

# Print answer
print_answers(prediction)

"""---
## Evaluation

About the metrics, you can read the [evaluation](https://docs.haystack.deepset.ai/docs/evaluation) web page.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
#
# For testing purposes, running on the first 100 labels
# For real evaluation, you must remove the [0:100]
eval_labels = dataset.get_validation()
eval_docs = [
    [label.document for label in multi_label.labels] for multi_label in eval_labels
][0:10]

eval_result = pipe.eval(
    labels=eval_labels, documents=eval_docs, params={"Reader": {"top_k": NUM_K}}
)

from pprint import pprint

# Get and print the metrics
metrics = eval_result.calculate_metrics()
pprint(metrics)

# Print a detailed report
# pipe.print_eval_report(eval_result)
