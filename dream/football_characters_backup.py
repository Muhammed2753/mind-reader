import json
import os

# -----------------------------
# File Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHARACTERS_PATH = os.path.join(BASE_DIR, "football_characters.json")

def main():
    # Load data
    with open(CHARACTERS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    modified_count = 0

    for name, entry in data.items():
        answers = entry.get("answers", {})
        
        # Check if it's a manager
        if answers.get("Is this person a football manager?") == "yes":
            # Only add if not already present
            if "Is this manager currently managing a club team?" not in answers:
                answers["Is this manager currently managing a club team?"] = "yes"
                modified_count += 1

    # Save back
    with open(CHARACTERS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully added 'Is this manager currently managing a club team?' to {modified_count} manager(s).")

if __name__ == "__main__":
    main()