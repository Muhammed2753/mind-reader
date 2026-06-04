import json

with open("football_characters.json", "r", encoding="utf-8") as f:
    data = json.load(f)
print("✅ Valid JSON!")