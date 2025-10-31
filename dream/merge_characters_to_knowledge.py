import json
import os

# Load both files
with open("football_characters.json", "r", encoding="utf-8") as f:
    characters = json.load(f)

# Load existing knowledge (if any)
if os.path.exists("knowledge_db.json"):
    with open("knowledge_db.json", "r", encoding="utf-8") as f:
        knowledge = json.load(f)
else:
    knowledge = {}

# Merge all characters into knowledge (overwrite if exists)
for name, data in characters.items():
    knowledge[name] = data

# Save back to knowledge_db.json
with open("knowledge_db.json", "w", encoding="utf-8") as f:
    json.dump(knowledge, f, indent=2, ensure_ascii=False)

print(f"✅ Merged {len(characters)} players into knowledge_db.json")