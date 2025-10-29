# generate_data.py
import json
import random

# ===== REAL PEOPLE (500) =====
real_people = [
    ("Cristiano Ronaldo", "athlete", "football_soccer", "Portuguese"),
    ("Lionel Messi", "athlete", "football_soccer", "Argentinian"),
    ("Serena Williams", "athlete", "tennis", "American"),
    ("LeBron James", "athlete", "basketball", "American"),
    ("Taylor Swift", "celebrity", "musician", "American"),
    ("Beyoncé", "celebrity", "musician", "American"),
    ("Leonardo DiCaprio", "celebrity", "actor", "American"),
    ("Scarlett Johansson", "celebrity", "actor", "American"),
    ("Elon Musk", "celebrity", "influencer", "American"),
    ("Marie Curie", "historical", None, "Polish"),
    ("Albert Einstein", "historical", None, "German"),
    ("Nelson Mandela", "historical", None, "South African"),
    ("Malala Yousafzai", "historical", None, "Pakistani"),
]

# Add more via patterns
first_names_male = ["James", "John", "Robert", "Michael", "David", "William", "Richard", "Joseph", "Thomas", "Charles"]
first_names_female = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

# Generate 400 more athletes
for _ in range(400):
    gender = random.choice(["male", "female"])
    first = random.choice(first_names_male if gender == "male" else first_names_female)
    last = random.choice(last_names)
    sport = random.choice(["football_soccer", "basketball", "tennis"])
    country = random.choice(["American", "Brazilian", "German", "Japanese", "Nigerian", "Australian"])
    real_people.append((f"{first} {last}", "athlete", sport, country))

# ===== FICTIONAL CHARACTERS (500) =====
fictional = [
    ("Sherlock Holmes", "book", "British"),
    ("Harry Potter", "book", "British"),
    ("Frodo Baggins", "book", "British"),
    ("Spider-Man", "superhero", "American"),
    ("Wonder Woman", "superhero", "American"),
    ("Batman", "superhero", "American"),
    ("Tony Stark", "superhero", "American"),
    ("Homer Simpson", "movie_tv", "American"),
    ("Bender", "movie_tv", "American"),
    ("Arya Stark", "movie_tv", "British"),
    ("Darth Vader", "movie_tv", "American"),
    ("Nezuko Kamado", "movie_tv", "Japanese"),
    ("Goku", "movie_tv", "Japanese"),
]

# Generate 400 more
for _ in range(400):
    first = random.choice(["Alex", "Zara", "Kai", "Luna", "Rex", "Mira"])
    last = random.choice(["Storm", "Blaze", "Night", "Sky", "Wolf", "Raven"])
    origin = random.choice(["book", "movie_tv", "superhero"])
    nationality = random.choice(["American", "British", "Japanese", "French"])
    fictional.append((f"{first} {last}", origin, nationality))

# ===== BUILD CHARACTERS DICT =====
characters = {}

# Add real people
for name, cat, subcat, nationality in real_people:
    answers = {"Is this person real or fictional?": "real"}
    if cat == "athlete":
        answers["Is this person an athlete?"] = "yes"
        if subcat == "football_soccer":
            answers["Does this person play soccer (football)?"] = "yes"
        elif subcat == "basketball":
            answers["Does this person play basketball?"] = "yes"
        elif subcat == "tennis":
            answers["Does this person play tennis?"] = "yes"
        answers[f"Is this person {nationality}?"] = "yes"
    elif cat == "celebrity":
        answers["Is this person a singer or musician?"] = "yes" if subcat == "musician" else "no"
        answers["Is this person primarily an actor?"] = "yes" if subcat == "actor" else "no"
        answers[f"Is this person {nationality}?"] = "yes"
    elif cat == "historical":
        answers["Did this person live before 1900?"] = "yes" if "Curie" in name or "Einstein" in name else "sometimes"
        answers[f"Is this person {nationality}?"] = "yes"
    
    characters[name] = {
        "type": "real",
        "category": cat,
        "subcategory": subcat,
        "answers": answers,
        "image_url": "/static/images/default_real.png"
    }

# Add fictional
for name, origin, nationality in fictional:
    answers = {
        "Is this person real or fictional?": "fictional",
        "Is this character from a novel?": "yes" if origin == "book" else "no",
        "Does this character have superpowers?": "yes" if origin == "superhero" else "no",
        "Is this character from a movie?": "yes" if origin == "movie_tv" else "no",
        f"Is this character {nationality}?": "yes"
    }
    characters[name] = {
        "type": "fictional",
        "category": origin,
        "answers": answers,
        "image_url": "/static/images/default_fictional.png"
    }

# Add self & family
characters.update({
    "User (Self)": {
        "type": "real",
        "category": "self",
        "answers": {"Are you thinking of yourself?": "yes"},
        "image_url": "/static/images/default_user.png"
    },
    "Mom": {
        "type": "real",
        "category": "family_or_self",
        "answers": {
            "Are you thinking of a family member (parent, sibling, child, etc.)?": "yes",
            "Is this person your mother or father?": "yes"
        },
        "image_url": "/static/images/family_default.png"
    }
})

# Save
with open("characters.json", "w", encoding="utf-8") as f:
    json.dump(characters, f, indent=2, ensure_ascii=False)

print(f"✅ Generated {len(characters)} characters in characters.json")