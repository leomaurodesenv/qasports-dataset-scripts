"""Module to generate Questions and Answers from a given dataset"""

import logging

import mmh3
import pandas as pd
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import FARMReader, QuestionGenerator
from haystack.pipelines import QuestionAnswerGenerationPipeline
from tqdm.auto import tqdm

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)


def generate_qa(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate Questions and Answers
    Args:
        df (pd.DataFrame): The dataset to generate questions and answers
    Returns:
        pd.DataFrame: The dataset with the generated questions and answers
    """
    # document Store
    document_store = InMemoryDocumentStore()
    # save documents in Document Store
    docs = [{"content": row["context"], **row} for _, row in df.iterrows()]
    document_store.write_documents(docs)

    # generate questions and answers
    question_generator = QuestionGenerator(num_queries_per_doc=1)
    reader = FARMReader("deepset/roberta-base-squad2", return_no_answer=True)
    qag_pipeline = QuestionAnswerGenerationPipeline(question_generator, reader)

    # iterate by the Documents
    generated_questions = list()
    number_of_documents = len(document_store.get_all_documents())
    print("Generating Questions and Answers")
    for _, document in enumerate(
        tqdm(document_store, total=number_of_documents, desc="Documents")
    ):
        result = qag_pipeline.run(documents=[document])

        # Iterate by the Questions & Answers
        for question, answers in zip(result["queries"], result["answers"]):
            document_str = str(document.content)
            answer_str = str(answers[0].answer)
            offset = document_str.find(answer_str) if len(answer_str) else 0
            offset = [offset, offset + len(answer_str)] if len(answer_str) else [0, 0]
            answer = {
                "text": answer_str,
                "offset": offset,
            }
            qa_id = mmh3.hash128(question + answer["text"] + document_str, signed=False)
            context_id = mmh3.hash128(document_str, signed=False)
            generated_questions.append(
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

    return pd.DataFrame(generated_questions)


def generate_qa_from_file(input_file: str, output_file: str, test: bool = False):
    """
    Generate Questions and Answers from File
    Args:
        input_file (str): The input CSV file containing the dataset
        output_file (str): The output CSV file to save the generated questions and answers
        test (bool): If True, only process the first 5 rows of the dataset
    """
    df = pd.read_csv(input_file, sep=",")
    if test:
        df = df.head(5)
    df = generate_qa(df)

    # save the generated questions and answers
    df.to_csv(output_file, sep=",", index=False, encoding="utf-8")
    print(df.head())
    print(f"Saved {len(df)} samples to {output_file}")
