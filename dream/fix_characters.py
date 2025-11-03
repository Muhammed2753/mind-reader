# fix_characters.py
import json

# Load your data
with open("football_characters.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Define the EXACT allowed position questions
ALLOWED_POSITION_QUESTIONS = [
    "Does this player play as a goalkeeper?",
    "Does this player play as a center defender?",
    "Does this player play as a left defender?",
    "Does this player play as a right defender?",
    "Does this player play as a right wing back?",
    "Does this player play as a left wing back?",
    "Does this player play as a left midfielder?",
    "Does this player play as a right midfielder?",
    "Does this player play as an center midfielder?",  # ⚠️ typo: "an center" → should be "a center"?
    "Does this player play as an attacking midfielder?",
    "Does this player play as a defensive midfielder?",
    "Does this player play as a striker?",
    "Does this player play as a left winger?",
    "Does this player play as a right winger?",
    "Does this player play as a center forward?"
]

# Map generic -> specific (based on your actual questions)
POSITION_MAP = {
    "goalkeeper": "Does this player play as a goalkeeper?",
    "center defender": "Does this player play as a center defender?",
    "left defender": "Does this player play as a left defender?",
    "right defender": "Does this player play as a right defender?",
    "right wing back": "Does this player play as a right wing back?",
    "left wing back": "Does this player play as a left wing back?",
    "center midfielder": "Does this player play as an center midfielder?",
    "attacking midfielder": "Does this player play as an attacking midfielder?",
    "defensive midfielder": "Does this player play as a defensive midfielder?",
    "striker": "Does this player play as a striker?",
    "left winger": "Does this player play as a left winger?",
    "right winger": "Does this player play as a right winger?",
    "center forward": "Does this player play as a center forward?",
    # Handle common variants
    "midfielder": "Does this player play as an center midfielder?",
    "forward": "Does this player play as a striker?",
    "winger": "Does this player play as a left winger?"
}

# Fix each player
for name, info in data.items():
    answers = info.get("answers", {})
    new_answers = {}
    for q, ans in answers.items():
        # If it's a position-like question but not in allowed list
        if "play as a" in q and q not in ALLOWED_POSITION_QUESTIONS:
            # Extract the role: e.g., "midfielder" from "Does this player play as a midfielder?"
            if "play as a " in q:
                role = q.split("play as a ")[1].rstrip("?").strip().lower()
                if role in POSITION_MAP:
                    new_q = POSITION_MAP[role]
                    new_answers[new_q] = ans
                else:
                    # Keep unknown as-is (or skip)
                    new_answers[q] = ans
            else:
                new_answers[q] = ans
        else:
            new_answers[q] = ans
    info["answers"] = new_answers

# Save fixed data
with open("football_characters_fixed.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Fixed character data saved to football_characters_fixed.json")