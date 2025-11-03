import json
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "football_mind_reader_2025"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHARACTERS_PATH = os.path.join(BASE_DIR, "football_characters.json")
QUESTIONS_SCHEMA_PATH = os.path.join(BASE_DIR, "football_questions.json")
KNOW_PATH = os.path.join(BASE_DIR, "knowledge_db.json")

# Ensure image folder exists
os.makedirs(os.path.join(BASE_DIR, "static", "images"), exist_ok=True)
for img in ["default.png", "unknown.png"]:
    img_path = os.path.join(BASE_DIR, "static", "images", img)
    if not os.path.exists(img_path):
        with open(img_path, "w") as f:
            f.write("")


# -----------------------------
# Utility Functions
# -----------------------------
def load_json_file(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default


def save_json_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def normalize_answer(raw):
    s = raw.strip().lower() if raw else ""
    if s in ("idk", "i don't know", "dont know", "unknown"):
        return "i don't know"
    if s in ("yes", "y", "yeah", "yep", "sure"):
        return "yes"
    if s in ("no", "n", "nope", "nah"):
        return "no"
    if s in ("maybe", "sometimes", "not sure"):
        return "sometimes"
    return "i don't know"


def normalize_continent_name(continent_str):
    return continent_str.strip().lower().replace(" ", "_").replace("-", "_")


# -----------------------------
# SMART QUESTION LOGIC
# -----------------------------
def get_next_question(answers_list, asked_set, schema):
    answers = dict(answers_list)

    # ---------- ROLE ----------
    role = None
    if answers.get("Is this person a football player?") == "yes":
        role = "player"
    elif answers.get("Is this person a football manager?") == "yes":
        role = "manager"
    elif answers.get("Is this person a football club owner or executive?") == "yes":
        role = "owner"

    if not role:
        for q in schema.get("role", []):
            if q not in asked_set:
                return q
        return None

    # ---------- CONTINENT ----------
    continent = None
    for q in schema.get(f"{role}_continent", []):
        if answers.get(q) == "yes":
            raw_cont = q.split("from ", 1)[1].rstrip("?")
            continent = normalize_continent_name(raw_cont)
            break

    if not continent:
        for q in schema.get(f"{role}_continent", []):
            if q not in asked_set:
                return q
        return None

    # ---------- LEAGUE (CONTINENT BY CONTINENT ORDER) ----------
    continents_order = [
        "europe", "africa", "south_america", "north_america", "asia", "oceania"
    ]

    # If user said yes in any league, skip remaining leagues and move on
    league_yes = any(
        answers.get(q) == "yes"
        for cont in continents_order
        for q in schema.get(f"{role}_league_{cont}", [])
    )

    if not league_yes:
        for cont in continents_order:
            league_key = f"{role}_league_{cont}"
            for q in schema.get(league_key, []):
                if q not in asked_set:
                    return q
    # If any league got a "yes", move straight to clubs.

    # ---------- CLUB ----------
    club_key = None
    for cont in continents_order:
        for q in schema.get(f"{role}_league_{cont}", []):
            if answers.get(q) == "yes":
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
                elif "Eredivisie" in q:
                    club_key = f"{role}_club_eredivisie"
                elif "MLS" in q:
                    club_key = f"{role}_club_mls"
                elif "Liga MX" in q:
                    club_key = f"{role}_club_liga_mx"
                elif "Brazil" in q or "Brasileirão" in q:
                    club_key = f"{role}_club_brasileirao"
                elif "Ghana" in q:
                    club_key = f"{role}_club_ghana_premier_league"
                elif "Algeria" in q:
                    club_key = f"{role}_club_algerian_ligue_1"
                elif "Morocco" in q or "Botola" in q:
                    club_key = f"{role}_club_botola_pro_morocco"
                elif "Kenya" in q:
                    club_key = f"{role}_club_kenyan_premier_league"
                break
        if club_key:
            break

    if club_key:
        for q in schema.get(club_key, []):
            if q not in asked_set:
                return q

    # ---------- POSITION / TRAITS ----------
    final_groups = {
        "player": ["player_position", "player_age", "player_status", "player_honors", "player_post_career"],
        "manager": ["manager_playing_career", "manager_tactics", "manager_honors", "manager_status", "manager_era"],
        "owner": ["owner_profile", "owner_status"]
    }

    for group in final_groups.get(role, []):
        for q in schema.get(group, []):
            if q not in asked_set:
                return q

    return None


# -----------------------------
# CANDIDATE FILTER
# -----------------------------
def filter_candidates(answers_list, all_chars):
    candidates = []
    for name, data in all_chars.items():
        if not isinstance(data, dict):
            continue
        char_ans = data.get("answers", {})
        match = True
        for q, a in answers_list:
            if a == "yes" and char_ans.get(q) != "yes":
                match = False
                break
            elif a == "no" and char_ans.get(q) == "yes":
                match = False
                break
        if match:
            candidates.append((name, data))
    return candidates


# -----------------------------
# ROUTES
# -----------------------------
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
        ans = normalize_answer(request.form.get("answer", ""))
        current_q = session.get("current_question")
        if current_q:
            answers.append((current_q, ans))
            session["answers"] = answers

    schema = load_json_file(QUESTIONS_SCHEMA_PATH, {})
    base_chars = load_json_file(CHARACTERS_PATH, {})
    user_chars = load_json_file(KNOW_PATH, {})
    all_chars = {**base_chars, **user_chars}

    if "role" not in schema:
        schema["role"] = [
            "Is this person a football player?",
            "Is this person a football manager?",
            "Is this person a football club owner or executive?"
        ]

    asked = {q for q, _ in answers}
    next_q = get_next_question(answers, asked, schema)

    if not next_q or len(answers) >= 20:
        return redirect(url_for("answer"))

    session["current_question"] = next_q
    yes_count = len([a for _, a in answers if a == "yes"])
    progress = min(95, yes_count * 10)
    return render_template("question.html", question=next_q, progress=progress)


@app.route("/undo", methods=["POST"])
def undo():
    answers = session.get("answers", [])
    if answers:
        answers.pop()
        session["answers"] = answers
        session.modified = True
    return redirect(url_for("question"))


@app.route("/answer", methods=["GET", "POST"])
def answer():
    answers = session.get("answers", [])
    wrong = session.get("wrong_guesses", 0)

    base_chars = load_json_file(CHARACTERS_PATH, {})
    user_chars = load_json_file(KNOW_PATH, {})
    all_chars = {**base_chars, **user_chars}
    candidates = filter_candidates(answers, all_chars)
    has_yes = any(a == "yes" for _, a in answers)

    if request.method == "POST":
        action = request.form.get("action")
        if action == "correct":
            return render_template("answer.html", guess="🎉 Correct! I read your mind!", show_success=True, play_again=True)
        elif action == "wrong":
            wrong += 1
            session["wrong_guesses"] = wrong
            schema = load_json_file(QUESTIONS_SCHEMA_PATH, {})
            asked = {q for q, _ in answers}
            next_q = get_next_question(answers, asked, schema)
            if wrong >= 5 or not next_q:
                return redirect(url_for("learn"))
            else:
                return redirect(url_for("question"))

    if not has_yes or not candidates:
        return render_template(
            "answer.html",
            guess="😅 I couldn't find anyone matching your answers!",
            image_url="/static/images/unknown.png",
            show_final=True,
            play_again=True
        )

    name, data = candidates[0]
    img = data.get("image_url", "/static/images/default.png")
    return render_template("answer.html", guess=name, image_url=img, play_again=True)


@app.route("/learn", methods=["GET", "POST"])
def learn():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            user_chars = load_json_file(KNOW_PATH, {})
            user_chars[name] = {
                "answers": dict(session.get("answers", [])),
                "image_url": "/static/images/default.png"
            }
            save_json_file(KNOW_PATH, user_chars)
            return redirect(url_for("index"))
    return render_template("learn.html")

#gdrf g v
# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("✅ Football Mind Reader running on http://127.0.0.1:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
