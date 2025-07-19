#               IMPORTS
import ast
import json
import pandas as pd
from module import is_answer_correct, is_question_valid, CSV_PATH


#           LOAD DATAFRAME
df = pd.read_csv(CSV_PATH, on_bad_lines="skip")
df["answer_dict"] = df["answer"].apply(ast.literal_eval)


#           EVALUATION LOOP
results = []

for _, row in df.iterrows():  # Use .head(N) to test with a smaller sample
    question = row["question"]
    context = row["context"]
    answer_text = row["answer_dict"]["text"]

    valid_q = is_question_valid(question, context, answer_text)
    correct_a = is_answer_correct(question, context, answer_text)

    results.append(
        {
            "context": context,
            "question": question,
            "answer": answer_text,
            "question_valid": valid_q,
            "answer_correct": correct_a,
        }
    )

print("Evaluation completed:", len(results))

with open("/content/avaliacoes.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print("Results saved to /content/evaluations.json")
