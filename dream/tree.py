import os
import json
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "football_mind_reader_2025"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHARACTERS_PATH = os.path.join(BASE_DIR, "football_characters.json")
QUESTIONS_SCHEMA_PATH = os.path.join(BASE_DIR, "football_questions.json")
KNOW_PATH = os.path.join(BASE_DIR, "knowledge_db.json")

# Ensure static/images exists
os.makedirs(os.path.join(BASE_DIR, "static", "images"), exist_ok=True)
for img in ["default.png", "unknown.png"]:
    path = os.path.join(BASE_DIR, "static", "images", img)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("")


def load_json_file(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default


def save_user_know():
    user_know = load_json_file(KNOW_PATH, {})
    with open(KNOW_PATH, "w", encoding="utf-8") as f:
        json.dump(user_know, f, indent=2, ensure_ascii=False)


def normalize_answer(raw):
    s = raw.strip().lower() if raw else ""
    if s in ("idk", "i don't know", "dont know", "don't know", "unknown"):
        return "i don't know"
    if s in ("yes", "y", "yeah", "yep", "sure"):
        return "yes"
    if s in ("no", "n", "nope", "nah"):
        return "no"
    if s in ("sometimes", "maybe", "occasionally", "not really"):
        return "sometimes"
    return "i don't know"


def get_next_question(answers_list, asked_set, questions_schema):
    answers_dict = dict(answers_list)
    
    # Role
    role = None
    for q in questions_schema.get("role", []):
        if answers_dict.get(q) == "yes":
            role = "player" if "player" in q else "manager" if "manager" in q else "owner"
            break
    if not role:
        for q in questions_schema.get("role", []):
            if q not in asked_set:
                return q
        return None

    # Continent
    continent = None
    for q in questions_schema.get(f"{role}_continent", []):
        if answers_dict.get(q) == "yes":
            continent = q.split("from ")[1].rstrip("?").lower()
            break
    if not continent:
        for q in questions_schema.get(f"{role}_continent", []):
            if q not in asked_set:
                return q
        return None

    # Country
    country_key = f"{role}_country_born_{continent}" if role == "manager" else f"{role}_country_{continent}"
    country_questions = questions_schema.get(country_key, [])
    if not any(answers_dict.get(q) == "yes" for q in country_questions):
        for q in country_questions:
            if q not in asked_set:
                return q

    # League
    league_key = f"{role}_league_{continent}"
    league_questions = questions_schema.get(league_key, [])
    if not any(answers_dict.get(q) == "yes" for q in league_questions):
        for q in league_questions:
            if q not in asked_set:
                return q

    # Club
    league = None
    for q in league_questions:
        if answers_dict.get(q) == "yes":
            if "Premier League" in q:
                club_key = f"{role}_club_premier_league"
            elif "La Liga" in q:
                club_key = f"{role}_club_laliga"
            elif "Serie A" in q:
                club_key = f"{role}_club_serie_a"
            elif "Bundesliga" in q:
                club_key = f"{role}_club_bundesliga"
            elif "Ligue 1" in q:
                club_key = f"{role}_club_ligue_1"
            elif "MLS" in q:
                club_key = f"{role}_club_mls"
            elif "Liga MX" in q:
                club_key = f"{role}_club_liga_mx"
            elif "Ghana Premier League" in q:
                club_key = f"{role}_club_ghana_premier_league"
            elif "Algerian Ligue" in q:
                club_key = f"{role}_club_algerian_ligue_1"
            elif "Botola Pro" in q:
                club_key = f"{role}_club_botola_pro_morocco"
            else:
                club_key = None
            if club_key:
                club_questions = questions_schema.get(club_key, [])
                if not any(answers_dict.get(q2) == "yes" for q2 in club_questions):
                    for q2 in club_questions:
                        if q2 not in asked_set:
                            return q2
            break

    # Final attributes
    final_groups = {
        "player": ["player_position", "player_age", "player_honors"],
        "manager": ["manager_playing_career", "manager_tactics", "manager_honors"],
        "owner": ["owner_profile", "owner_status"]
    }
    for group in final_groups.get(role, []):
        for q in questions_schema.get(group, []):
            if q not in asked_set:
                return q

    return None


def filter_candidates(answers_list, all_characters):
    answers_dict = dict(answers_list)
    candidates = []
    for name, data in all_characters.items():
        if not isinstance(data, dict):
            continue
        match = True
        for q, ans in answers_list:
            if ans == "yes" and data.get("answers", {}).get(q) != "yes":
                match = False
                break
        if match:
            candidates.append((name, data))
    return candidates


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    session.clear()
    session["answers"] = []
    session["wrong_guesses"] = 0
    return redirect(url_for("question"))


@app.route("/question", methods=["GET", "POST"])
def question():
    answers = session.get("answers", [])
    if request.method == "POST":
        raw_ans = request.form.get("answer", "")
        ans = normalize_answer(raw_ans)
        current_q = session.get("current_question")
        if current_q:
            answers.append((current_q, ans))
            session["answers"] = answers

    # Load fresh data on every request (avoids global state issues)
    base_chars = load_json_file(CHARACTERS_PATH, {})
    user_know = load_json_file(KNOW_PATH, {})
    all_chars = {**base_chars, **user_know}
    questions_schema = load_json_file(QUESTIONS_SCHEMA_PATH, {})
    if not questions_schema.get("role"):
        questions_schema["role"] = [
            "Is this person a football player?",
            "Is this person a football manager?",
            "Is this person a football club owner or executive?"
        ]

    asked = set(q for q, _ in answers)
    next_q = get_next_question(answers, asked, questions_schema)

    if not next_q or len(answers) >= 12:
        return redirect(url_for("answer"))

    session["current_question"] = next_q
    progress = min(95, max(0, len([a for a in answers if a[1] == "yes"]) * 10))
    return render_template("question.html", question=next_q, progress=progress)


@app.route("/answer", methods=["GET", "POST"])
def answer():
    answers = session.get("answers", [])
    wrong_guesses = session.get("wrong_guesses", 0)

    if request.method == "POST":
        action = request.form.get("action")
        if action == "correct":
            return redirect(url_for("index"))
        elif action == "wrong":
            wrong_guesses += 1
            session["wrong_guesses"] = wrong_guesses
            if wrong_guesses >= 5:
                return redirect(url_for("learn"))
            else:
                return redirect(url_for("question"))

    base_chars = load_json_file(CHARACTERS_PATH, {})
    user_know = load_json_file(KNOW_PATH, {})
    all_chars = {**base_chars, **user_know}

    candidates = filter_candidates(answers, all_chars)
    if not candidates:
        return render_template("answer.html", guess="I couldn't find anyone matching your answers!")

    best_name, best_data = candidates[0], candidates[0][1]
    if len(candidates) > 1:
        best_score = 0
        for name, data in candidates:
            score = sum(1 for q, a in answers if a == "yes" and data.get("answers", {}).get(q) == "yes")
            if score > best_score:
                best_score = score
                best_name, best_data = name, data

    img = best_data.get("image_url", "/static/images/default.png")
    return render_template("answer.html", guess=best_name, image_url=img)


@app.route("/learn", methods=["GET", "POST"])
def learn():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            user_know = load_json_file(KNOW_PATH, {})
            user_know[name] = {
                "answers": dict(session.get("answers", [])),
                "image_url": "/static/images/default.png"
            }
            with open(KNOW_PATH, "w", encoding="utf-8") as f:
                json.dump(user_know, f, indent=2, ensure_ascii=False)
            return render_template("learn.html", success=True, name=name)
    return render_template("learn.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)