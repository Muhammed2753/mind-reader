import json

# Path to your file
FILE_PATH = "football_characters.json"

# Load the data
with open(FILE_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

fixed_count = 0
total_players = len(data)

# Traverse each player
for name, info in data.items():
    if not isinstance(info, dict) or "answers" not in info:
        continue

    answers = info["answers"]

    # Check if both keys exist
    double_key = "Is this player currently active??"
    single_key = "Is this player currently active?"

    if double_key in answers:
        # If both exist, remove the double-key version
        if single_key in answers:
            del answers[double_key]
            fixed_count += 1
        else:
            # If only double-key exists, rename it to single-key
            answers[single_key] = answers.pop(double_key)
            fixed_count += 1

    # Optional: Ensure single_key exists and is either "yes" or "no"
    if single_key in answers:
        if answers[single_key] not in ("yes", "no"):
            # Optional cleanup: set to "yes" if invalid
            answers[single_key] = "yes"

print(f"✅ Fixed {fixed_count}/{total_players} players")
print(f"✔️ Removed all 'Is this player currently active??' entries")
print(f"✔️ Ensured 'Is this player currently active?' is present and valid")

# Save back to file
with open(FILE_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"💾 Saved cleaned data to {FILE_PATH}")