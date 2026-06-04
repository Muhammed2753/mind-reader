import json
import re

# Official position questions (from your schema)
OFFICIAL_POSITIONS = [
    "Is this player natural position a goalkeeper?",
    "Is this player natural position a center defender?",
    "Is this player natural position a left defender?",
    "Is this player natural position a right defender?",
    "Is this player natural position a left wing back?",
    "Is this player natural position a right wing back?",
    "Is this player natural position a left midfielder?",
    "Is this player natural position a right midfielder?",
    "Is this player natural position a center midfielder?",
    "Is this player natural position an attacking midfielder?",
    "Is this player natural position a defensive midfielder?",
    "Is this player natural position a striker?",
    "Is this player natural position a center forward?",
    "Is this player natural position a left winger?",
    "Is this player natural position a right winger?"
]

# Create a reverse mapping from keywords to official question
POSITION_MAP = {}

# Helper: add mappings
def add_mapping(keywords, official_question):
    for k in keywords:
        POSITION_MAP[k.lower()] = official_question

add_mapping(["goalkeeper", "gk"], OFFICIAL_POSITIONS[0])
add_mapping(["center defender", "centre back", "central defender", "center back", "cb"], OFFICIAL_POSITIONS[1])
add_mapping(["left defender", "left back", "lb"], OFFICIAL_POSITIONS[2])
add_mapping(["right defender", "right back", "rb"], OFFICIAL_POSITIONS[3])
add_mapping(["left wing back", "left wingback", "lwb"], OFFICIAL_POSITIONS[4])
add_mapping(["right wing back", "right wingback", "rwb"], OFFICIAL_POSITIONS[5])
add_mapping(["left midfielder", "lm"], OFFICIAL_POSITIONS[6])
add_mapping(["right midfielder", "rm"], OFFICIAL_POSITIONS[7])
add_mapping(["center midfielder", "central midfielder", "midfielder", "cm"], OFFICIAL_POSITIONS[8])
add_mapping(["attacking midfielder", "number 10", "playmaker", "am"], OFFICIAL_POSITIONS[9])
add_mapping(["defensive midfielder", "holding midfielder", "cdm", "dm"], OFFICIAL_POSITIONS[10])
add_mapping(["striker", "forward"], OFFICIAL_POSITIONS[11])
add_mapping(["center forward", "cf"], OFFICIAL_POSITIONS[12])
add_mapping(["left winger", "left wing", "lw"], OFFICIAL_POSITIONS[13])
add_mapping(["right winger", "right wing", "rw"], OFFICIAL_POSITIONS[14])

def normalize_position_answer(position_str):
    """Convert raw position string to official question"""
    if not isinstance(position_str, str):
        return None
    key = position_str.lower().strip()
    # Try exact match first
    if key in POSITION_MAP:
        return POSITION_MAP[key]
    # Try partial match (e.g., "center back" in "center back left")
    for phrase in sorted(POSITION_MAP.keys(), key=len, reverse=True):
        if phrase in key:
            return POSITION_MAP[phrase]
    return None

def main():
    CHARACTERS_FILE = "football_characters.json"
    
    with open(CHARACTERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    fixed = 0
    for name, info in data.items():
        answers = info.get("answers", {})
        # Skip if not a player
        if answers.get("Is this person a football player?") != "yes":
            continue

        # Find existing position answer
        old_position_q = None
        old_position_val = None
        for q, val in answers.items():
            if "natural position" in q and val == "yes":
                old_position_q = q
                old_position_val = val
                break
        
        # Extract position from question or value
        position_text = ""
        if old_position_q:
            # Extract from question: "Is this player natural position a center midfielder?"
            match = re.search(r"natural position a (.+?)\?", old_position_q)
            if match:
                position_text = match.group(1)
            else:
                position_text = old_position_q
        
        # Normalize to official question
        new_position_q = normalize_position_answer(position_text)
        
        if new_position_q:
            # Remove old position question(s)
            keys_to_remove = [q for q in answers.keys() if "natural position" in q]
            for k in keys_to_remove:
                answers.pop(k, None)
            # Add new official question
            answers[new_position_q] = "yes"
            fixed += 1
            print(f"✅ Fixed {name}: '{position_text}' → '{new_position_q}'")
        else:
            print(f"⚠️ Could not map position for {name}: '{position_text}'")

    # Save back
    with open(CHARACTERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Done! Fixed positions for {fixed} players.")

if __name__ == "__main__":
    main()