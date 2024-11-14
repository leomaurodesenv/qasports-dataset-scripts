import csv
import logging

import mmh3
import pandas as pd
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import FARMReader, QuestionGenerator
from haystack.pipelines import QuestionAnswerGenerationPipeline
from tqdm.auto import tqdm

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)


def generate_qa(input_file: str, output_file: str, test: bool = False):
    """Generate Questions and Answers"""
    df = pd.read_csv(input_file, sep=",")

    # document Store
    document_store = InMemoryDocumentStore()
    # save documents in Document Store
    docs = [{"content": row["context"], **row} for _, row in df.iterrows()]
    if test:
        docs = docs[:5]
    document_store.write_documents(docs)

    print("total documents:", len(document_store.get_all_documents()))

    # generate questions and answers
    question_generator = QuestionGenerator(num_queries_per_doc=1)
    reader = FARMReader("deepset/roberta-base-squad2", return_no_answer=True)
    qag_pipeline = QuestionAnswerGenerationPipeline(question_generator, reader)

    with open(output_file, "w", newline="") as csvfile:
        fieldnames = [
            "qa_id",
            "question",
            "answer",
            "context",
            "context_id",
            "context_url",
            "context_title",
            "context_categories",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # iterate by the Documents
        for _, document in enumerate(tqdm(document_store)):
            result = qag_pipeline.run(documents=[document])

            # Iterate by the Questions & Answers
            for question, answers in zip(result["queries"], result["answers"]):
                document_str = str(document.content)
                answer_str = str(answers[0].answer)
                offset = document_str.find(answer_str) if len(answer_str) else 0
                offset = [offset, offset+len(answer_str)] if len(answer_str) else [0, 0]
                answer = {
                    "text": answer_str,
                    "offset": offset,
                }
                qa_id = mmh3.hash128(
                    question + answer["text"] + document_str, signed=False
                )
                context_id = mmh3.hash128(document_str, signed=False)
                writer.writerow(
                    {
                        "qa_id": qa_id,
                        "question": question,
                        "answer": answer,
                        "context": document_str,
                        "context_id": context_id,
                        "context_url": document.meta["url"],
                        "context_title": document.meta["title"],
                        "context_categories": document.meta["categories"],
                    }
                )

    print("output:")
    print(pd.read_csv(output_file, sep=","))
