import json
import random

# ----------------------------
# LARGE TOPIC LISTS
# ----------------------------

# 🌍 Countries (195)
countries = [
    "Nigeria","Ghana","Kenya","South Africa","Egypt","Morocco","Ethiopia","Uganda","Tanzania","Cameroon",
    "USA","Canada","Mexico","Brazil","Argentina","Chile","Colombia","Peru","Venezuela","Cuba",
    "UK","France","Germany","Italy","Spain","Portugal","Sweden","Norway","Finland","Denmark",
    "Russia","Ukraine","Poland","Romania","Netherlands","Belgium","Switzerland","Austria","Greece","Turkey",
    "China","India","Japan","South Korea","North Korea","Philippines","Indonesia","Malaysia","Thailand","Vietnam",
    "Saudi Arabia","UAE","Qatar","Kuwait","Oman","Jordan","Israel","Iran","Iraq","Syria",
    "Australia","New Zealand","Fiji","Papua New Guinea","Solomon Islands","Samoa","Tonga","Vanuatu","Kiribati","Micronesia",
    # ... (add all 195 UN countries here for maximum coverage)
]

# 🐾 Animals (sample 300+)
animals = [
    "dog","cat","lion","tiger","elephant","giraffe","zebra","monkey","bear","leopard",
    "cheetah","wolf","fox","panda","kangaroo","koala","rhinoceros","hippopotamus","crocodile","alligator",
    "snake","lizard","turtle","shark","whale","dolphin","octopus","squid","penguin","eagle",
    "sparrow","owl","hawk","falcon","parrot","peacock","goat","sheep","cow","horse",
    # ... continue until ~300 animals
]

# 🍕 Foods (sample 500+)
foods = [
    "pizza","burger","rice","beans","chicken","fish","bread","salad","pasta","sushi",
    "noodles","sandwich","shawarma","jollof rice","egusi soup","fufu","yam porridge","fried rice","pancakes","waffles",
    "cake","cookies","ice cream","chocolate","apple","banana","orange","grapes","mango","pineapple",
    # ... extend with fruits, dishes, drinks, desserts until ~500
]

# ⚽ Sports (50+)
sports = [
    "football","basketball","tennis","cricket","rugby","golf","boxing","wrestling","swimming","cycling",
    "athletics","long jump","high jump","volleyball","handball","badminton","table tennis","karate","judo","mma",
    "surfing","skiing","snowboarding","skating","archery","gymnastics","weightlifting","rowing","canoeing","hockey",
]

# 🎬 Movies & General Interests
movies = [
    "action","comedy","drama","horror","sci-fi","romance","thriller","cartoon","adventure","documentary",
    "anime","fantasy","superhero","musical","crime","biography","historical","mystery","western","war",
]

# 🎶 Music
music = [
    "hip hop","rap","pop","rock","jazz","blues","country","gospel","afrobeat","reggae",
    "techno","classical","folk","metal","soul","r&b","dancehall","opera","house","punk",
]

# ----------------------------
# COMBINE ALL TOPICS
# ----------------------------
topics = countries + animals + foods + sports + movies + music

# ----------------------------
# QUESTION TEMPLATES
# ----------------------------
templates = [
    "Does your character like {}?",
    "Is your character associated with {}?",
    "Has your character ever visited {}?",
    "Is your character known for {}?",
    "Can your character eat {}?",
    "Is your character connected to {}?",
    "Would your character enjoy {}?",
    "Is your character related to {}?",
    "Does your character often talk about {}?",
    "Is {} important to your character?",
]

# ----------------------------
# GENERATE QUESTIONS
# ----------------------------
questions = []
seen = set()
qid = 1

while len(questions) < 30000:  # stop at 30,000
    topic = random.choice(topics)
    template = random.choice(templates)
    question = template.format(topic)

    if question not in seen:  # avoid duplicates
        seen.add(question)
        questions.append({"id": qid, "question": question})
        qid += 1

# ----------------------------
# SAVE TO JSON
# ----------------------------
with open("questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"✅ Generated {len(questions)} unique questions in questions.json")
