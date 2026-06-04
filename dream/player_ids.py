import json
import os

# -----------------------------
# File Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHARACTERS_PATH = os.path.join(BASE_DIR, "football_characters.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "football_characters_fixed.json")

# -----------------------------
# Load Data
# -----------------------------
with open(CHARACTERS_PATH, "r", encoding="utf-8") as f:
    characters = json.load(f)

# -----------------------------
# Define Mappings: Old Question → New Question
# -----------------------------
# These are the only phrases that need updating based on your data
QUESTION_MAPPINGS = {
    "Does this owner own a club in Europe?": "Is this owner associated with a club in Europe?",
    "Does this owner own a club in England?": "Is this owner associated with a club in England?",
    "Does this owner own a club in Spain?": "Is this owner associated with a club in Spain?",
    "Does this owner own a club in Germany?": "Is this owner associated with a club in Germany?",
    "Does this owner own a club in France?": "Is this owner associated with a club in France?",
    "Does this owner own a club in Italy?": "Is this owner associated with a club in Italy?",
    "Does this owner own a club in Netherlands?": "Is this owner associated with a club in Netherlands?",
    "Does this owner own a club in Portugal?": "Is this owner associated with a club in Portugal?",
    "Does this owner own a club in Belgium?": "Is this owner associated with a club in Belgium?",
    "Does this owner own a club in Turkey?": "Is this owner associated with a club in Turkey?",
    "Does this owner own a club in Russia?": "Is this owner associated with a club in Russia?",
    "Does this owner own a club in Scotland?": "Is this owner associated with a club in Scotland?",
    # Add more if needed — but your data only shows England/Europe
}

# -----------------------------
# Process Each Character
# -----------------------------
updated_count = 0
for name, data in characters.items():
    # Only process owners
    answers = data.get("answers", {})
    is_owner = any("owner" in q.lower() for q in answers.keys())
    if not is_owner:
        continue

    new_answers = {}
    updated = False

    for question, answer in answers.items():
        # Apply mapping if it exists
        if question in QUESTION_MAPPINGS:
            new_question = QUESTION_MAPPINGS[question]
            new_answers[new_question] = answer
            updated = True
        else:
            # Keep all other questions as-is
            new_answers[question] = answer

    if updated:
        data["answers"] = new_answers
        updated_count += 1

# -----------------------------
# Save Updated File
# -----------------------------
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(characters, f, indent=2, ensure_ascii=False)

print(f"✅ Fixed {updated_count} owner(s).")
print(f"📁 Saved to: {OUTPUT_PATH}")
print("👉 Now replace your original football_characters.json with this file.")