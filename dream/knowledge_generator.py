# app.py
import os
import json
import random
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "football_mind_reader_2025"

CHARACTERS_PATH = "football_characters.json"
QUESTIONS_SCHEMA_PATH = "football_questions.json"
KNOW_PATH = "knowledge_db.json"

# ----------------------------
# CONFIDENCE WEIGHTS
# ----------------------------
CONFIDENCE_WEIGHTS = {
    "yes": 1.0,
    "sometimes": 0.1,
    "i don't know": 0.02,
    "no": 0.0
}

# ----------------------------
# LOAD QUESTIONS SCHEMA
# ----------------------------
if os.path.exists(QUESTIONS_SCHEMA_PATH):
    try:
        with open(QUESTIONS_SCHEMA_PATH, "r", encoding="utf-8") as f:
            QUESTIONS_SCHEMA = json.load(f)
    except:
        QUESTIONS_SCHEMA = {"global": [], "player": [], "manager": [], "owner": []}
else:
    QUESTIONS_SCHEMA = {"global": [], "player": [], "manager": [], "owner": []}

# ----------------------------
# SETUP IMAGES
# ----------------------------
os.makedirs("static/images", exist_ok=True)
for img in ["default.png", "unknown.png"]:
    path = os.path.join("static", "images", img)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("")

# ----------------------------
# LOAD CHARACTERS
# ----------------------------
def load_json_file(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else default
    except:
        return default

BASE_CHARACTERS = load_json_file(CHARACTERS_PATH, {})
USER_KNOW = load_json_file(KNOW_PATH, {})
ALL_CHARACTERS = {**BASE_CHARACTERS, **USER_KNOW}

def save_user_know():
    with open(KNOW_PATH, "w", encoding="utf-8") as f:
        json.dump(USER_KNOW, f, indent=2, ensure_ascii=False)

def normalize_answer(raw):
    if not raw: return "i don't know"
    s = raw.strip().lower()
    if s in ("idk", "i don't know", "dont know"): return "i don't know"
    if s in ("yes", "y", "yeah"): return "yes"
    if s in ("no", "n", "nope"): return "no"
    if s in ("sometimes", "maybe"): return "sometimes"
    return s

def determine_category(answers_dict):
    if answers_dict.get("Is this person a football player?") == "yes":
        return ("player",)
    elif answers_dict.get("Is this person a football manager?") == "yes":
        return ("manager",)
    elif answers_dict.get("Is this person a football club owner?") == "yes":
        return ("owner",)
    return ("unknown",)

def get_next_question(session_answers, asked_set):
    answers_dict = dict(session_answers)
    
    # Ask global questions first
    for q in QUESTIONS_SCHEMA.get("global", []):
        if q not in asked_set:
            return q

    # Then role-specific
    cat = determine_category(answers_dict)
    if cat[0] in QUESTIONS_SCHEMA:
        pool = [q for q in QUESTIONS_SCHEMA[cat[0]] if q not in asked_set]
        if pool:
            return random.choice(pool)
    
    # Fallback: any unasked question
    all_q = []
    for v in QUESTIONS_SCHEMA.values():
        if isinstance(v, list):
            all_q.extend(v)
    available = [q for q in all_q if q not in asked_set]
    return random.choice(available) if available else None

# ----------------------------
# ROUTES
# ----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    session.clear()
    session["answers"] = []
    session["weighted_confidence"] = 0.0
    return redirect(url_for("question"))

@app.route("/question", methods=["GET", "POST"])
def question():
    if request.method == "POST":
        raw_ans = request.form.get("answer", "")
        ans = normalize_answer(raw_ans)
        q = session.get("current_question")
        if q:
            session["answers"].append((q, ans))
            weight = CONFIDENCE_WEIGHTS.get(ans, 0.0)
            session["weighted_confidence"] = session.get("weighted_confidence", 0.0) + weight
            session.modified = True

    asked = set(q for q, _ in session.get("answers", []))
    next_q = get_next_question(session.get("answers", []), asked)
    if not next_q:
        return redirect(url_for("answer"))

    session["current_question"] = next_q
    progress = min(100, int(session.get("weighted_confidence", 0.0) * 12.5))
    return render_template("question.html", question=next_q, progress=progress)

@app.route("/answer", methods=["GET", "POST"])
def answer():
    if request.method == "POST":
        if request.form.get("feedback") == "yes":
            return render_template("answer.html", done=True, message="I read your mind! ⚽🧠")
        else:
            return redirect(url_for("learn"))

    # Score characters
    scores = {}
    for name, data in ALL_CHARACTERS.items():
        if not isinstance(data, dict):
            continue
        s = 0
        expected = data.get("answers", {})
        for q, user_ans in session.get("answers", []):
            if q in expected and expected[q] == user_ans:
                s += 1
        if s > 0:
            scores[name] = s

    if scores:
        guess = max(scores, key=scores.get)
        img = ALL_CHARACTERS[guess].get("image_url", "/static/images/default.png")
        conf = min(95, 30 + scores[guess] * 10)
    else:
        return render_template("answer.html", 
            guess="A football legend!",
            confidence=0,
            image_url="/static/images/unknown.png",
            ask_confirm=False
        )

    return render_template("answer.html", guess=guess, confidence=conf, image_url=img, ask_confirm=True)

@app.route("/learn", methods=["GET", "POST"])
def learn():
    if request.method == "POST":
        name = request.form.get("correct_answer", "").strip()
        if not name:
            return render_template("learn.html", error="Name required.")
        USER_KNOW[name] = {
            "answers": dict(session.get("answers", [])),
            "image_url": "/static/images/default.png"
        }
        save_user_know()
        return render_template("answer.html", done=True, message=f"Thanks! I learned about {name}.")
    return render_template("learn.html")

@app.route("/undo", methods=["POST"])
def undo():
    if session.get("answers"):
        last_q, last_ans = session["answers"].pop()
        weight = CONFIDENCE_WEIGHTS.get(last_ans, 0.0)
        current = session.get("weighted_confidence", 0.0)
        session["weighted_confidence"] = max(0.0, current - weight)
        session.modified = True
    return redirect(url_for("question"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000) 