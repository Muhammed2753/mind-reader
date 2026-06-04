import json
import re

CHARACTERS_FILE = "football_characters.json"

# Canonical defender questions
CENTER_DEF = "Is this player natural position a center defender?"
LEFT_DEF = "Is this player natural position a left defender?"
RIGHT_DEF = "Is this player natural position a right defender?"

# Keywords mapping to canonical question
DEFENDER_MAP = {
    "center": CENTER_DEF,
    "centre": CENTER_DEF,
    "central": CENTER_DEF,
    "cb": CENTER_DEF,
    "left back": LEFT_DEF,
    "left": LEFT_DEF,
    "lb": LEFT_DEF,
    "right back": RIGHT_DEF,
    "right": RIGHT_DEF,
    "rb": RIGHT_DEF,
    "defender": CENTER_DEF,  # default to center if ambiguous
}

def get_canonical_defender_question(position_text):
    """Convert raw position text to one of the 3 official defender questions."""
    if not isinstance(position_text, str):
        return None
    text = position_text.lower()
    # Check for left/right first (more specific)
    if "left" in text or "lb" in text:
        return LEFT_DEF
    if "right" in text or "rb" in text:
        return RIGHT_DEF
    # Then check for center/central
    if any(kw in text for kw in ["center", "centre", "central", "cb", "defender"]):
        return CENTER_DEF
    return None

def main():
    with open(CHARACTERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    fixed = 0
    for name, info in data.items():
        answers = info.get("answers", {})
        # Skip if not a player
        if answers.get("Is this person a football player?") != "yes":
            continue

        # Check if any existing answer matches a defender question (old or new)
        position_text = ""
        keys_to_remove = []
        for q, val in list(answers.items()):
            if val == "yes" and ("defender" in q.lower() or "back" in q.lower()):
                # Extract position from question
                match = re.search(r"natural position a (.+?)\?", q)
                if match:
                    position_text = match.group(1)
                else:
                    position_text = q
                keys_to_remove.append(q)
        
        if not keys_to_remove and "Does this player play as a defender?" in answers:
            # Handle legacy "Does this player play as a defender?" case
            keys_to_remove.append("Does this player play as a defender?")
            position_text = "defender"

        if not position_text:
            continue

        # Determine canonical defender question
        new_q = get_canonical_defender_question(position_text)
        if not new_q:
            continue

        # Remove old defender questions
        for k in keys_to_remove:
            answers.pop(k, None)
        
        # Add the official one
        answers[new_q] = "yes"
        fixed += 1
        print(f"✅ Fixed {name}: '{position_text}' → '{new_q}'")

    # Save back
    with open(CHARACTERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Done! Fixed {fixed} defender positions.")

if __name__ == "__main__":
    main()