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
    print(df)

    # Document Store
    document_store = InMemoryDocumentStore()
    # Save documents in Document Store
    docs = [{"content": row["context"], **row} for _, row in df.iterrows()]
    if test: docs = docs[:5]
    document_store.write_documents(docs)

    print("total documents", len(document_store.get_all_documents()))

    # Generate Questions and Answers
    question_generator = QuestionGenerator(num_queries_per_doc=1)
    reader = FARMReader("deepset/roberta-base-squad2", return_no_answer=True)
    qag_pipeline = QuestionAnswerGenerationPipeline(question_generator, reader)

    with open(output_file, "w", newline="") as csvfile:
        fieldnames = [
            "id_qa",
            "context_id",
            "context",
            "question",
            "answer",
            "context_title",
            "context_categories",
            "url",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Iterate by the Documents
        for _, document in enumerate(tqdm(document_store)):
            result = qag_pipeline.run(documents=[document])

            # Iterate by the Questions & Answers
            for question, answers in zip(result["queries"], result["answers"]):
                offset = answers[0].offsets_in_context[0]
                answer = {
                    "text": answers[0].answer,
                    "offset": [offset.start, offset.end],
                }
                id_qa = mmh3.hash128(
                    question + answer["text"] + document.content, signed=False
                )
                context_id = mmh3.hash128(document.content, signed=False)
                writer.writerow(
                    {
                        "id_qa": id_qa,
                        "context_id": context_id,
                        "context": document.content,
                        "question": question,
                        "answer": answer,
                        "context_title": document.meta["title"],
                        "context_categories": document.meta["categories"],
                        "url": document.meta["url"],
                    }
                )

    print("Output:")
    print(pd.read_csv(output_file, sep=","))
