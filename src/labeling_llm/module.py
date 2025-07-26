"""Module to labeling the question-answering dataset"""

import re
import ast
import torch
import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM

# Constants
MODEL_SHORT_NAME = "qwen"
MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"
# Sample of models
#   "Qwen/Qwen2.5-3B-Instruct"
#   "Qwen/Qwen2.5-7B-Instruct"
#   "Qwen/Qwen2.5-14B-Instruct"
#   "Qwen/Qwen2.5-72B-Instruct"

# Loading LLM
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, device_map="auto", trust_remote_code=True
).eval()


def is_question_valid(question: str, context: str, answer: str) -> str:
    """
    Evaluates whether a question makes sense within the given context.
    Args:
        question (str): The question to validate.
        context (str): The context of the question.
        answer (str): The answer provided for that question.
    Returns:
        str: "1" if valid, "2" if the subject is not covered in the context.
    """
    prompt = f"""
You are an evaluator. Given a context, a question, and an answer, classify the question by selecting one of the options below.

Context: {context}
Question: {question}
Answer: {answer}

Does the question make sense based on the context?
1 - Yes
2 - No, the subject is not in the context

Respond with only the number (1 or 2). Do not include any explanation.
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=10)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    generated_answer = answer.split("Do not include any explanation.")[-1].strip()
    return re.search("\d+|$", generated_answer).group()


def is_answer_correct(question: str, context: str, answer: str) -> str:
    """
    Evaluates whether the provided answer is correct according to the context.
    Args:
        question (str): The question being asked.
        context (str): The context in which to evaluate the answer.
        answer (str): The answer to verify.
    Returns:
        str: "1" if correct, "2" if incorrect but the answer is found in the context.
    """
    prompt = f"""
You are an evaluator. Given a context, a question, and a provided answer, classify the answer selecting one option.

Context: {context}
Question: {question}
Provided Answer: {answer}

Is the answer correct?
1 - Yes.
2 - No, and the answer is in the context

Return only the number (1 or 2). Do not include any explanation.
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=10)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    generated_answer = answer.split("Do not include any explanation.")[-1].strip()
    return re.search("\d+|$", generated_answer).group()


def labeling(df: pd.DataFrame) -> pd.DataFrame:
    """
    Labeling the question-answering dataset.
    Args:
        df (pd.DataFrame): The dataset to label.
    Returns:
        pd.DataFrame: The labeled dataset.
    """
    labeling_results = []

    for _, row in tqdm(
        df.iterrows(), desc=f"Labeling ({MODEL_SHORT_NAME})", total=len(df)
    ):
        question = row["question"]
        context = row["context"]
        answer_text = (
            ast.literal_eval(row["answer"])
            if isinstance(row["answer"], str)
            else row["answer"]
        )["text"]

        valid_q = is_question_valid(question, context, answer_text)
        correct_a = is_answer_correct(question, context, answer_text)

        labeling_results.append(
            {
                "qa_id": row["qa_id"],
                "question": question,
                "answer": answer_text,
                "context": context,
                "is_question_valid": valid_q,
                "is_answer_correct": correct_a,
            }
        )

    return pd.DataFrame(labeling_results)


def labeling_from_file(input_file: str, output_file: str, test: bool = False):
    """
    Labeling the question-answering dataset.
    Args:
        input_file (str): The input
        output_file (str): The output
        test (bool): testing parameter
    """
    df = pd.read_csv(input_file, sep=",")
    if test:
        df = df.head(5)
    df = labeling(df)
    df.to_csv(output_file, index=False)
    print(df)
    print(f"Saved {len(df)} samples to {output_file}")
