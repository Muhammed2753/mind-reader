import os
import json
import random
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "football_mind_reader_2025"

# File paths
CHARACTERS_PATH = "football_characters.json"
QUESTIONS_SCHEMA_PATH = "football_questions.json"
KNOW_PATH = "knowledge_db.json"

# Ensure static/images exists
os.makedirs("static/images", exist_ok=True)
for img in ["default.png", "unknown.png"]:
    path = os.path.join("static", "images", img)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("")


def load_json_file(path, default):
    if not os.path.exists(path):
        print(f"⚠️ Warning: {path} not found. Using default.")
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else default
    except json.JSONDecodeError as e:
        print(f"❌ Error decoding {path}: {e}")
        return default
    except Exception as e:
        print(f"❌ Unexpected error loading {path}: {e}")
        return default


def save_user_know():
    with open(KNOW_PATH, "w", encoding="utf-8") as f:
        json.dump(USER_KNOW, f, indent=2, ensure_ascii=False)


# Load data
BASE_CHARACTERS = load_json_file(CHARACTERS_PATH, {})
USER_KNOW = load_json_file(KNOW_PATH, {})
ALL_CHARACTERS = {**BASE_CHARACTERS, **USER_KNOW}

# Load questions schema once at startup
QUESTIONS_SCHEMA = load_json_file(QUESTIONS_SCHEMA_PATH, {})

# Validate critical schema
if not QUESTIONS_SCHEMA.get("role"):
    print("❗ CRITICAL: 'role' questions missing in football_questions.json!")
    QUESTIONS_SCHEMA["role"] = [
        "Is this person a football player?",
        "Is this person a football manager?",
        "Is this person a football club owner or executive?"
    ]


def normalize_answer(raw):
    if not raw:
        return "i don't know"
    s = raw.strip().lower()
    if s in ("idk", "i don't know", "dont know", "don't know", "unknown"):
        return "i don't know"
    if s in ("yes", "y", "yeah", "yep", "sure"):
        return "yes"
    if s in ("no", "n", "nope", "nah"):
        return "no"
    if s in ("sometimes", "maybe", "occasionally"):
        return "sometimes"
    return "i don't know"


def get_role_from_answers(answers_dict):
    if answers_dict.get("Is this person a football player?") == "yes":
        return "player"
    if answers_dict.get("Is this person a football manager?") == "yes":
        return "manager"
    if answers_dict.get("Is this person a football club owner or executive?") == "yes":
        return "owner"
    return None


def get_continent_from_answers(answers_dict, role="player"):
    prefix = "Is this player from " if role == "player" else "Is this manager from "
    for continent in ["Europe", "South America", "Africa", "Asia", "North America"]:
        if answers_dict.get(f"{prefix}{continent}?") == "yes":
            return continent
    return None


def get_league_from_answers(answers_dict, role="player"):
    prefix = "Is this player playing in " if role == "player" else "Has this manager managed in "
    leagues = [
        "Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1",
        "MLS", "Liga MX", "J-League", "Brasileirão (Brazil)"
    ]
    for league in leagues:
        q = f"{prefix}{league}?"
        if answers_dict.get(q) == "yes":
            return league
    return None


def get_next_question(answers_list, asked_set):
    answers_dict = dict(answers_list)
    role = get_role_from_answers(answers_dict)

    # === STEP 1: ROLE ===
    if not role:
        role_questions = QUESTIONS_SCHEMA.get("role", [])
        for q in role_questions:
            if q not in asked_set:
                return q
        return None  # All roles rejected

    # === STEP 2: CONTINENT ===
    continent = get_continent_from_answers(answers_dict, role)
    if not continent:
        key = f"{role}_continent"
        continent_questions = QUESTIONS_SCHEMA.get(key, [])
        for q in continent_questions:
            if q not in asked_set:
                return q
        return None

    # === STEP 3: COUNTRY ===
    country_key = f"{role}_country_{continent.lower()}"
    country_questions = QUESTIONS_SCHEMA.get(country_key, [])
    for q in country_questions:
        if q not in asked_set:
            return q

    # === STEP 4: LEAGUE ===
    league = get_league_from_answers(answers_dict, role)
    if not league:
        league_key = f"{role}_league_{continent.lower()}"
        league_questions = QUESTIONS_SCHEMA.get(league_key, [])
        for q in league_questions:
            if q not in asked_set:
                return q
        return None

    # === STEP 5: CLUB ===
    league_to_club = {
        "Premier League": "premier_league",
        "La Liga": "laliga",
        "Serie A": "serie_a",
        "Bundesliga": "bundesliga",
        "Ligue 1": "ligue_1",
        "MLS": "mls",
        "Liga MX": "liga_mx",
        "J-League": "j_league",
        "Brasileirão (Brazil)": "brasileirao"
    }
    club_group = league_to_club.get(league)
    if club_group:
        club_key = f"{role}_club_{club_group}"
        club_questions = QUESTIONS_SCHEMA.get(club_key, [])
        for q in club_questions:
            if q not in asked_set:
                return q

    # === STEP 6: FINAL ATTRIBUTES ===
    final_groups = {
        "player": ["player_position", "player_age", "player_status", "player_honors", "player_post_career"],
        "manager": ["manager_playing_career", "manager_tactics", "manager_honors", "manager_status", "manager_era"],
        "owner": ["owner_profile", "owner_status"]
    }
    for group in final_groups.get(role, []):
        for q in QUESTIONS_SCHEMA.get(group, []):
            if q not in asked_set:
                return q

    # Fallback: any unasked question
    all_questions = []
    for v in QUESTIONS_SCHEMA.values():
        if isinstance(v, list):
            all_questions.extend(v)
    for q in all_questions:
        if q not in asked_set:
            return q

    return None


def score_character(user_answers, character_data):
    expected = character_data.get("answers", {})
    score = 0.0
    total_weight = 0

    for q, user_ans in user_answers:
        if q not in expected:
            continue
        char_ans = expected[q]

        if user_ans == "no":
            continue

        weight = 1.0
        total_weight += weight

        if user_ans == char_ans:
            score += weight
        elif user_ans == "i don't know" or char_ans == "i don't know":
            score += weight * 0.5

    if total_weight == 0:
        return 0.0
    return score / total_weight


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

    # 🔥 CRITICAL FIX: Never jump to answer if no questions were asked yet
    if not next_q and len(asked) == 0:
        # Fallback to first role question if somehow schema is broken
        fallback = QUESTIONS_SCHEMA.get("role", ["Is this person a football player?"])
        next_q = fallback[0]

    if not next_q:
        return redirect(url_for("answer"))

    session["current_question"] = next_q
    progress = min(95, max(10, int(len(asked) * 3.8)))
    return render_template("question.html", question=next_q, progress=progress)


@app.route("/answer")
def answer():
    user_answers = session.get("answers", [])
    if not user_answers:
        return redirect(url_for("question"))  # Should not happen, but safe

    scores = {}
    for name, data in ALL_CHARACTERS.items():
        if not isinstance(data, dict):
            continue
        s = score_character(user_answers, data)
        if s > 0.1:
            scores[name] = s

    if scores:
        guess = max(scores, key=scores.get)
        confidence = min(95, max(20, int(scores[guess] * 100)))
        img = ALL_CHARACTERS[guess].get("image_url", "/static/images/default.png")
        return render_template("answer.html", guess=guess, confidence=confidence,
                               image_url=img, ask_confirm=True)
    else:
        return render_template("answer.html", guess="A mysterious football figure...",
                               confidence=0, image_url="/static/images/unknown.png",
                               ask_confirm=False)


@app.route("/learn", methods=["GET", "POST"])
def learn():
    if request.method == "POST":
        name = request.form.get("correct_answer", "").strip()
        if not name:
            return render_template("learn.html", error="Name is required.")
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
    answers = session.get("answers", [])
    if answers:
        session["answers"] = answers[:-1]
        session.modified = True
    return redirect(url_for("question"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)