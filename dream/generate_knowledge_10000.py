import json
import random

# Sample lists of names & categories
people_names = [
    "Lionel Messi", "Cristiano Ronaldo", "Elon Musk", "Taylor Swift",
    "Bill Gates", "Michael Jackson", "Albert Einstein", "Ariana Grande",
    "Beyoncé", "Dwayne Johnson", "Oprah Winfrey", "Neymar Jr", "LeBron James",
    "Selena Gomez", "Drake", "Robert Downey Jr", "Will Smith", "Rihanna",
    "Tom Holland", "Zendaya", "Shakira", "Kim Kardashian", "Kylie Jenner",
    "Justin Bieber", "Emma Watson", "Post Malone", "Nicki Minaj"
]

animals = ["Dog", "Cat", "Elephant", "Lion", "Tiger", "Horse", "Giraffe", "Kangaroo", "Panda", "Dolphin"]
objects = ["Car", "Phone", "Laptop", "Chair", "Table", "Watch", "Bicycle", "Airplane", "Book", "Camera"]

def make_entry(name, category):
    return {
        "name": name,
        "category": category,
        "traits": {
            "human": category == "person",
            "animal": category == "animal",
            "object": category == "object",
        },
        "image": f"https://via.placeholder.com/150?text={name.replace(' ', '+')}"
    }

knowledge = []

# Target distribution: 70% people, 30% animals/objects
n_people = 7000
n_others = 3000

# Generate people
for _ in range(n_people):
    name = random.choice(people_names)
    knowledge.append(make_entry(name, "person"))

# Generate animals and objects
for _ in range(n_others // 2):
    knowledge.append(make_entry(random.choice(animals), "animal"))
for _ in range(n_others // 2):
    knowledge.append(make_entry(random.choice(objects), "object"))

# Shuffle
random.shuffle(knowledge)

# Save to file
with open("knowledge_10000.json", "w", encoding="utf-8") as f:
    json.dump(knowledge, f, ensure_ascii=False, indent=2)

print("✅ knowledge_10000.json generated with", len(knowledge), "entries.")
