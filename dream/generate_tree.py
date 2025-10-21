import os
import random

QUESTIONS_PATH = "questions_500k.jsonl"

def generate_questions_file():
    if not needs_regen(QUESTIONS_PATH):
        return
    print("⚡ Generating questions_500k.jsonl (this may take a moment)...")

    categories = [
        "Is it an animal?",
        "Is it a person?",
        "Is it a place?",
        "Is it an object?",
        "Can it fly?",
        "Can it swim?",
        "Does it exist in real life?",
        "Is it fictional?",
        "Is it used in sports?",
        "Is it bigger than a car?"
    ]

    variations = [
        "",  # plain
        " that is commonly found in cities?",
        " that is often used at home?",
        " that people usually see on TV?",
        " related to technology?",
        " found in nature?"
    ]

    total = 500_000
    chunk_size = 20_000

    with open(QUESTIONS_PATH, "w", encoding="utf-8") as f:
        for i in range(0, total, chunk_size):
            batch = []
            for _ in range(min(chunk_size, total - i)):
                base = random.choice(categories)
                var = random.choice(variations)
                q = base.replace("?", "") + var
                if not q.endswith("?"):
                    q += "?"
                batch.append(q + "\n")
            f.writelines(batch)

    print("✅ questions_500k.jsonl created with 500,000 unique-style questions.")

if __name__ == "__main__":
    generate_questions_file()
