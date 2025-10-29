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

# Setup images
os.makedirs("static/images", exist_ok=True)
for img in ["default.png", "unknown.png"]:
    path = os.path.join("static", "images", img)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("")

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
    if not raw: 
        return "i don't know"
    s = raw.strip().lower()
    if s in ("idk", "i don't know", "dont know", "don't know"): 
        return "i don't know"
    if s in ("yes", "y", "yeah", "yep"): 
        return "yes"
    if s in ("no", "n", "nope"): 
        return "no"
    if s in ("sometimes", "maybe", "occasionally"): 
        return "sometimes"
    return "i don't know"

def get_next_question(session_answers, asked_set):
    answers_dict = dict(session_answers)

    # Load questions safely
    QUESTIONS_SCHEMA = {}
    if os.path.exists("football_questions.json"):
        try:
            with open("football_questions.json", "r", encoding="utf-8") as f:
                QUESTIONS_SCHEMA = json.load(f)
        except:
            pass

    role_questions = QUESTIONS_SCHEMA.get("role", [
        "Is this person a football player?",
        "Is this person a football manager?",
        "Is this person a football club owner or executive?"
    ])

    # Check if any role is confirmed with "yes"
    is_player = answers_dict.get("Is this person a football player?") == "yes"
    is_manager = answers_dict.get("Is this person a football manager?") == "yes"
    is_owner = answers_dict.get("Is this person a football club owner or executive?") == "yes"

    # If a role is confirmed, skip ALL role questions
    if is_player or is_manager or is_owner:
        pass
    else:
        # Only offer role questions that haven't been asked AND weren't answered "no"
        available = []
        for q in role_questions:
            if q in asked_set:
                continue
            # Skip if user already said "no" (even if not in asked_set due to edge case)
            if answers_dict.get(q) == "no":
                continue
            available.append(q)
        
        if available:
            return random.choice(available)
        else:
            return None  # All roles rejected

    # === PLAYER FLOW ===
    if is_player:
        # Continent
        for q in QUESTIONS_SCHEMA.get("player_continent", []):
            if q not in asked_set:
                return q

        # Country (only if continent = yes)
        if answers_dict.get("Is this player from Europe?") == "yes":
            for q in QUESTIONS_SCHEMA.get("player_country_europe", []):
                if q not in asked_set:
                    return q
        elif answers_dict.get("Is this player from South America?") == "yes":
            for q in QUESTIONS_SCHEMA.get("player_country_south_america", []):
                if q not in asked_set:
                    return q
        elif answers_dict.get("Is this player from Africa?") == "yes":
            for q in QUESTIONS_SCHEMA.get("player_country_africa", []):
                if q not in asked_set:
                    return q

        # League (only if continent = yes)
        if answers_dict.get("Is this player from Europe?") == "yes":
            for q in QUESTIONS_SCHEMA.get("player_league_europe", []):
                if q not in asked_set:
                    return q
        elif (answers_dict.get("Is this player from North America?") == "yes" or
              answers_dict.get("Is this player from South America?") == "yes"):
            for q in QUESTIONS_SCHEMA.get("player_league_america", []):
                if q not in asked_set:
                    return q
        elif answers_dict.get("Is this player from Asia?") == "yes":
            for q in QUESTIONS_SCHEMA.get("player_league_asia", []):
                if q not in asked_set:
                    return q

        # Club (only if league = yes)
        if answers_dict.get("Has this player played in the Premier League?") == "yes":
            for q in QUESTIONS_SCHEMA.get("player_club_premier", []):
                if q not in asked_set:
                    return q
        elif answers_dict.get("Has this player played in La Liga?") == "yes":
            for q in QUESTIONS_SCHEMA.get("player_club_laliga", []):
                if q not in asked_set:
                    return q

        # Final attributes
        for group in ["player_position", "player_age", "player_status", "player_honors", "player_post_career"]:
            for q in QUESTIONS_SCHEMA.get(group, []):
                if q not in asked_set:
                    return q

    # === MANAGER FLOW ===
    elif is_manager:
        for q in QUESTIONS_SCHEMA.get("manager_continent", []):
            if q not in asked_set:
                return q
        if answers_dict.get("Is this manager from Europe?") == "yes":
            for q in QUESTIONS_SCHEMA.get("manager_country_europe", []):
                if q not in asked_set:
                    return q
        for q in QUESTIONS_SCHEMA.get("manager_league", []):
            if q not in asked_set:
                return q
        for q in QUESTIONS_SCHEMA.get("manager_club", []):
            if q not in asked_set:
                return q
        for group in ["manager_playing_career", "manager_tactics", "manager_honors", "manager_status"]:
            for q in QUESTIONS_SCHEMA.get(group, []):
                if q not in asked_set:
                    return q

    # === OWNER FLOW ===
    elif is_owner:
        for q in QUESTIONS_SCHEMA.get("owner_region", []):
            if q not in asked_set:
                return q
        for q in QUESTIONS_SCHEMA.get("owner_club", []):
            if q not in asked_set:
                return q
        for q in QUESTIONS_SCHEMA.get("owner_profile", []):
            if q not in asked_set:
                return q

    # Final fallback: any unasked question
    all_questions = []
    for group in QUESTIONS_SCHEMA.values():
        if isinstance(group, list):
            all_questions.extend(group)
    for q in all_questions:
        if q not in asked_set:
            return q

    return None

def score_character(user_answers, character_data):
    expected = character_data.get("answers", {})
    score = 0.0
    total = 0
    for q, user_ans in user_answers:
        if q not in expected:
            continue
        char_ans = expected[q]
        total += 1
        if user_ans == char_ans:
            score += 1.0
        elif user_ans == "i don't know" or char_ans == "i don't know":
            score += 0.5
        else:
            score -= 0.3
    return score / max(total, 1)

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    session.clear()
    session["answers"] = []
    return redirect(url_for("question"))

@app.route("/question", methods=["GET", "POST"])
def question():
    if request.method == "POST":
        raw_ans = request.form.get("answer", "")
        ans = normalize_answer(raw_ans)
        q = session.get("current_question")
        if q:
            session["answers"].append((q, ans))
            session.modified = True

    asked = set(q for q, _ in session.get("answers", []))
    next_q = get_next_question(session.get("answers", []), asked)
    if not next_q:
        return redirect(url_for("answer"))

    session["current_question"] = next_q
    progress = min(95, int(len(asked) * 3.5))
    return render_template("question.html", question=next_q, progress=progress)

@app.route("/answer", methods=["GET", "POST"])
def answer():
    if request.method == "POST":
        if request.form.get("feedback") == "yes":
            return render_template("answer.html", done=True, message="I read your mind! ⚽🧠")
        else:
            return redirect(url_for("learn"))

    user_answers = session.get("answers", [])
    if not user_answers:
        return render_template("answer.html", 
            guess="No questions answered!",
            confidence=0,
            image_url="/static/images/unknown.png",
            ask_confirm=False
        )

    scores = {}
    for name, data in ALL_CHARACTERS.items():
        if not isinstance(data, dict):
            continue
        s = score_character(user_answers, data)
        if s > -0.5:
            scores[name] = s

    if scores:
        guess = max(scores, key=scores.get)
        conf = min(95, max(20, int((scores[guess] + 0.5) * 60)))
        img = ALL_CHARACTERS[guess].get("image_url", "/static/images/default.png")
        return render_template("answer.html", guess=guess, confidence=conf, image_url=img, ask_confirm=True)
    else:
        return render_template("answer.html", 
            guess="A mysterious football figure...",
            confidence=0,
            image_url="/static/images/unknown.png",
            ask_confirm=False
        )

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
        ALL_CHARACTERS[name] = USER_KNOW[name]
        return render_template("answer.html", done=True, message=f"Thanks! I learned about {name}.")
    return render_template("learn.html")

@app.route("/undo", methods=["POST"])
def undo():
    if session.get("answers"):
        session["answers"].pop()
        session.modified = True
    return redirect(url_for("question"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)