import json
import random

# ----------------------------
# TOPICS (big pool to reach 30,000+)
# ----------------------------
animals = ["dog", "cat", "lion", "tiger", "elephant", "snake", "giraffe", "monkey", "bear", "zebra"]
sports = ["football", "basketball", "tennis", "cricket", "boxing", "swimming", "golf", "rugby", "wrestling", "cycling"]
foods = ["pizza", "burger", "rice", "beans", "chicken", "sushi", "pasta", "bread", "salad", "fish"]
places = ["Africa", "Europe", "Asia", "America", "Australia", "Nigeria", "China", "USA", "Brazil", "India"]
movies = ["action", "comedy", "drama", "horror", "sci-fi", "romance", "thriller", "cartoon", "adventure", "documentary"]

# You can expand with thousands of entries later (e.g. all countries, cities, animals, foods, etc.)
topics = animals + sports + foods + places + movies

# ----------------------------
# QUESTION TEMPLATES
# ----------------------------
templates = [
    "Does your character like {}?",
    "Is your character associated with {}?",
    "Has your character ever visited {}?",
    "Is your character known for {}?",
    "Can your character eat {}?",
    "Is your character connected to {}?",
    "Would your character enjoy {}?",
    "Is your character related to {}?",
    "Does your character often talk about {}?",
    "Is {} important to your character?",
]

# ----------------------------
# GENERATE QUESTIONS
# ----------------------------
questions = []
seen = set()  # to avoid duplicates
qid = 1

while len(questions) < 30000:  # stop at 30,000
    topic = random.choice(topics)
    template = random.choice(templates)
    question = template.format(topic)

    if question not in seen:  # ensure no duplicates
        seen.add(question)
        questions.append({"id": qid, "question": question})
        qid += 1

# ----------------------------
# SAVE TO JSON
# ----------------------------
with open("questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"✅ Generated {len(questions)} unique questions in questions.json")
