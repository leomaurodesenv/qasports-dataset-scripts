import csv
import json
import os
from pathlib import Path


def extract_contexts(input_folder: str, output_file: str):
    """Extract context from texts"""
    num_contexts = 0
    biggest_context = 0
    with open(output_file, "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["url", "title", "categories", "date_collection", "context"])

        # extracting contexts from cleaned data
        for filename in os.listdir(input_folder):
            file_path = str(Path(input_folder) / filename)
            with open(file_path, "r") as tmp:
                data = json.load(tmp)
                text = data["text"].split(".")
                context = ""
                index = 0

                while index < len(text):
                    context = text[index] + ". "
                    index += 1
                    while len(context) < 255 and index < len(text):
                        context = context + text[index] + ". "
                        index += 1

                    if len(context) > biggest_context:
                        biggest_context = len(context)

                    if (
                        "http" not in context
                        and not context.startswith("Expression error:")
                    ) or index == len(text) - 1:
                        categorias = ""
                        for i in data["categories"]:
                            categorias = categorias + "," + i

                        num_contexts += 1
                        row = [
                            data["url"],
                            data["title"][0],
                            categorias,
                            data["date"],
                            context,
                        ]
                        writer.writerow(row)

    print(f"quantity: {num_contexts}, biggest: {biggest_context}")
