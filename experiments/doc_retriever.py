"""Document Retriever Experiments"""

import argparse
from haystack.utils import print_documents
from haystack.pipelines import DocumentSearchPipeline

# from haystack.document_stores import ElasticsearchDocumentStore
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever, TfidfRetriever, DensePassageRetriever

from .module import Dataset, DocRetriever, Sports, dataset_switch


# Model setup
# NUM_K = 1  # 1, 3, 5, 10, 20
# DATASET = Dataset.SQuAD
# DOC_RETRIEVER = DocRetriever.BM25
# SPORT = Sports.ALL
parser = argparse.ArgumentParser(description="Run document retriever experiments.")
parser.add_argument(
    "--num_k",
    type=int,
    default=1,
    help="Number of top-k documents to retrieve.",
)
parser.add_argument(
    "--dataset",
    type=str,
    default="QASports",
    choices=[attr.name for attr in Dataset],
    help="Dataset to use for the experiment.",
)
parser.add_argument(
    "--model",
    type=str,
    default="BM25",
    choices=[attr.name for attr in DocRetriever],
    help="Document retriever model to use.",
)
parser.add_argument(
    "--sport",
    type=str,
    default="ALL",
    choices=[attr.name for attr in Sports],
    help="Sport to filter for QASports dataset.",
)

args = parser.parse_args()

NUM_K = args.num_k
DATASET = Dataset[args.dataset]
DOC_RETRIEVER = DocRetriever[args.model]
SPORT = Sports[args.sport].value
print(f"Dataset: {DATASET} // Sport: {SPORT}")
print(f"Model: {DOC_RETRIEVER} // Top-K: {NUM_K}")


# Document Store
# document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")
document_store = InMemoryDocumentStore(use_bm25=True)

# Get the dataset
dataset = dataset_switch(DATASET, SPORT)

# Store documents in the Document Store
docs = dataset.get_documents()
document_store.write_documents(docs)

"""---
## Document Retriever

In this experiment, we explored the BM25, TF-IDF and Dense Passage Retrieval (DPR).

* https://docs.haystack.deepset.ai/docs/retriever
* https://github.com/facebookresearch/DPR
* https://www.elastic.co/pt/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables

### Get the Retriever
"""


def retriever_switch(choice, document_store):
    """Get Retriever object"""

    if choice == DocRetriever.BM25:
        retriever = BM25Retriever(document_store=document_store)
        return retriever
    elif choice == DocRetriever.TFIDF:
        retriever = TfidfRetriever(document_store=document_store)
        return retriever
    elif choice == DocRetriever.DPR:
        retriever = DensePassageRetriever(
            document_store=document_store,
            query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
            passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
            use_fast_tokenizers=True,
        )
        document_store.update_embeddings(retriever)
        return retriever
    else:
        return "Invalid retriever"


# Get the retriever
retriever = retriever_switch(DOC_RETRIEVER, document_store)
print(f"Retriever: {retriever}")


"""### Build the Pipeline"""
pipe = DocumentSearchPipeline(retriever=retriever)

# # Querying documents
# question = "What is your name?"
# prediction = pipe.run(query=question, params={"Retriever": {"top_k": 1}})

# # Print answer
# print_documents(prediction)

"""---
## Evaluation

About the metrics, you can read the [evaluation](https://docs.haystack.deepset.ai/docs/evaluation) web page.
"""

# For testing purposes, running on the first 100 labels
# For real evaluation, you must remove the [0:100]
eval_labels = dataset.get_validation()
eval_result = pipe.eval(labels=eval_labels, params={"Retriever": {"top_k": NUM_K}})

# Get and print the metrics
metrics = eval_result.calculate_metrics()
print(metrics)
