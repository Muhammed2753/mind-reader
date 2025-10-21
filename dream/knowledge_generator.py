import requests
import json
import random

def fetch_wikipedia_entities(category, limit=200):
    """
    Fetch entities from Wikipedia category (using Wikidata).
    Example categories:
    - Q5 = human
    - Q729 = animal
    - Q488383 = object
    """
    url = f"https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbgetentities",
        "sites": "enwiki",
        "format": "json",
        "titles": category
    }
    res = requests.get(url, params=params)
    data = res.json()
    return data

def build_knowledge_base():
    knowledge = []

    # Example sources (you can expand with many categories)
    people = [
        "Cristiano Ronaldo", "Lionel Messi", "Ruben Amorim", "Elon Musk",
        "Taylor Swift", "Barack Obama", "MrBeast", "PewDiePie",
        "KSI", "Lebron James", "Roger Federer", "Oprah Winfrey",
        "Bill Gates", "Albert Einstein", "Cleopatra", "Ariana Grande",
    ]
    animals = [
        "Lion", "Elephant", "Cat", "Dog", "Horse", "Eagle",
        "Shark", "Dolphin", "Snake", "Kangaroo", "Panda"
    ]
    objects = [
        "Phone", "Laptop", "Car", "Bicycle", "Television",
        "Football", "Drone", "Airplane", "Camera", "Guitar"
    ]

    # Turn each entry into dictionary
    for name in people:
        knowledge.append({
            "name": name,
            "type": "person",
            "traits": {
                "category": "human",
                "profession": random.choice(["footballer", "singer", "youtuber", "president", "scientist", "coach"]),
                "alive": random.choice([True, False]),
                "country": random.choice(["Portugal", "USA", "UK", "Nigeria", "Brazil", "Argentina", "France"]),
                "legend": random.choice([True, False])
            },
            "image": f"https://source.unsplash.com/400x400/?{name.replace(' ', '%20')}"
        })

    for name in animals:
        knowledge.append({
            "name": name,
            "type": "animal",
            "traits": {
                "domestic": name in ["Cat", "Dog", "Horse"],
                "wild": name not in ["Cat", "Dog", "Horse"],
                "moves": random.choice(["land", "sea", "air"]),
                "size": random.choice(["small", "medium", "large"])
            },
            "image": f"https://source.unsplash.com/400x400/?{name}"
        })

    for name in objects:
        knowledge.append({
            "name": name,
            "type": "object",
            "traits": {
                "electronic": name in ["Phone", "Laptop", "Television", "Drone", "Camera"],
                "transport": name in ["Car", "Bicycle", "Airplane"],
                "entertainment": name in ["Football", "Guitar"],
                "daily_use": name in ["Phone", "Laptop", "Car", "Television"]
            },
            "image": f"https://source.unsplash.com/400x400/?{name}"
        })

    # Expand dataset by random duplication until ~10,000 entries
    while len(knowledge) < 10000:
        knowledge.append(random.choice(knowledge))

    with open("knowledge_10000.json", "w", encoding="utf-8") as f:
        json.dump(knowledge, f, indent=2)

    print("✅ knowledge_10000.json created with", len(knowledge), "entries")

if __name__ == "__main__":
    build_knowledge_base()
