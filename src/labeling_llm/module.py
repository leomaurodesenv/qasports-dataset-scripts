#               IMPORTS
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


#               CONFIGURATION
CSV_PATH = "/content/golf-qa-sampling.csv"  # Path to the CSV to evaluate
MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"  # Choose one model:
# MODEL_OPTIONS = [
#     "Qwen/Qwen2.5-3B-Instruct",
#     "Qwen/Qwen2.5-7B-Instruct",
#     "Qwen/Qwen2.5-14B-Instruct",
#     "Qwen/Qwen2.5-72B-Instruct"


#               MODEL LOADING

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)


model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, device_map="auto", trust_remote_code=True
).eval()


#               FUNCTIONS


def is_question_valid(question: str, context: str, answer: str) -> str:
    """
    Evaluates whether a question makes sense within the given context.

    Parameters:
    - question (str): The question to validate.
    - context (str): The context of the question.
    - answer (str): The answer provided for that question.

    Returns:
    - str: "1" if valid, "2" if the subject is not covered in the context.
    """
    prompt = f"""
You are an evaluator. Given a context, a question, and an answer, classify the question by selecting one of the options below.

Context: {context}
Question: {question}
Answer: {answer}

Does the question make sense based on the context?
1 - Yes
2 - No, the subject is not in the context

Respond with only the number (1 or 2). Do not include explanations.
"""

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=10)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return answer.split("explanations.")[-1].strip()


def is_answer_correct(question: str, context: str, answer: str) -> str:
    """
    Evaluates whether the provided answer is correct according to the context.

    Parameters:
    - question (str): The question being asked.
    - context (str): The context in which to evaluate the answer.
    - answer (str): The answer to verify.

    Returns:
    - str: "1" if correct, "2" if incorrect but the answer is found in the context.
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

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=10)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return answer.split("any explanation.")[-1].strip()
