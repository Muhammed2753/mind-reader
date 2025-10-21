import json
import os
from random import choice

OUT = "knowledge_10000.json"
PLACEHOLDER_IMG = "https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png"

QUESTIONS = [
    "Is it a person?",
    "Is it an animal?",
    "Is it an object?",
    "Is it alive?",
    "Is it famous?",
    "Is it used daily?",
    "Is it fictional?",
    "Is it related to sports?",
    "Is it related to music?",
    "Is it related to politics?"
]

def make_traits(is_person=False, is_animal=False, is_object=False,
                alive=False, famous=False, used_daily=False,
                fictional=False, sport=False, music=False, politics=False):
    return {q: "Yes" if val else "No" for q, val in zip(QUESTIONS, [
        is_person, is_animal, is_object, alive, famous,
        used_daily, fictional, sport, music, politics
    ])}

db = {}

# =============================
# 1️⃣ People (sports + historical + artists)
# =============================
people = [
    # Footballers, NBA, rugby, AFL, cricket stars
    "Cristiano Ronaldo", "Lionel Messi", "Neymar Jr", "LeBron James", "Michael Jordan",
    "Kobe Bryant", "Stephen Curry", "Roger Federer", "Serena Williams", "Virat Kohli",
    "Aaron Finch", "Israel Folau", "Adam Goodes", "Sadio Mané", "Mohamed Salah",
    # Historical figures / leaders / scientists / inventors / artists
    "Albert Einstein", "Isaac Newton", "Nikola Tesla", "Thomas Edison", "Marie Curie",
    "Barack Obama", "Donald Trump", "Nelson Mandela", "Mahatma Gandhi",
    "William Shakespeare", "Vincent van Gogh", "Chinua Achebe", "Frida Kahlo"
]

# Generate placeholder names to reach ~4000 people
firsts = ["Alex", "Sam", "Chris", "Jordan", "Taylor", "Casey", "Morgan", "Riley"]
lasts = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

while len(people) < 4000:
    name = f"{choice(firsts)} {choice(lasts)}"
    if name not in people:
        people.append(name)

for name in people:
    lower = name.lower()
    traits = make_traits(
        is_person=True,
        alive=True,
        famous=any(tok in lower for tok in ["messi","ronaldo","lebron","beyoncé","obama","einstein"]),
        sport=any(tok in lower for tok in ["football","messi","ronaldo","lebron","jordan"]),
        music=any(tok in lower for tok in ["beyoncé","drake","adele","rihanna"]),
        politics=any(tok in lower for tok in ["obama","trump","mandela","gandhi"])
    )
    db[name] = {"traits": traits, "image": PLACEHOLDER_IMG}

# =============================
# 2️⃣ Animals (living + extinct)
# =============================
animals = ["Lion", "Tiger", "Elephant", "Dodo", "Panda", "Koala", "Dragon", "Unicorn"]
species_suffix = ["bird", "fish", "mammal", "reptile", "insect"]

while len(animals) < 3000:
    candidate = f"Species {len(animals)+1}"
    animals.append(candidate)

for name in animals:
    traits = make_traits(
        is_animal=True,
        alive=not any(x in name.lower() for x in ["dodo"]),
        used_daily=name.lower() in ["dog","cat","cow","chicken"],
        fictional=name in ["Dragon", "Unicorn", "Phoenix"]
    )
    db[name] = {"traits": traits, "image": PLACEHOLDER_IMG}

# =============================
# 3️⃣ Objects (modern + historical)
# =============================
objects = ["Chair", "Table", "Phone", "Laptop", "Car", "Chariot", "Sword", "Book", "Pen"]
while len(objects) < 1500:
    objects.append(f"Object {len(objects)+1}")

for name in objects:
    traits = make_traits(is_object=True, alive=False, used_daily=name.lower() in ["phone","laptop","chair","table","book","pen"])
    db[name] = {"traits": traits, "image": PLACEHOLDER_IMG}

# =============================
# 4️⃣ Fictional / Games / Characters
# =============================
fictional = ["Mario", "Link", "Pikachu", "Goku", "Naruto", "Batman", "Superman"]
while len(fictional) < 1500:
    fictional.append(f"Fictional {len(fictional)+1}")

for name in fictional:
    traits = make_traits(is_person=False, fictional=True, alive=True, famous=True)
    db[name] = {"traits": traits, "image": PLACEHOLDER_IMG}

# =============================
# Save JSON
# =============================
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f"✅ Generated {len(db)} entries in {OUT}")
