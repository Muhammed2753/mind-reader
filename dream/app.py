import json
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "football_mind_reader_2025"

# -----------------------------
# File Paths
# -----------------------------
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


# -----------------------------
# Utility functions
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
    if s in ("sometimes", "maybe", "occasionally", "not really"):
        return "sometimes"
    return "i don't know"


def normalize_continent_name(continent_str):
    return continent_str.strip().lower().replace(" ", "_").replace("-", "_")


def normalize_key(text):
    """Normalize question keys for matching"""
    return text.strip().lower().replace(" ", "_").replace("?", "")


# -----------------------------
# Question Flow Logic
# -----------------------------
def get_next_question(answers_list, asked_set, questions_schema):
    answers_dict = dict(answers_list)

    # --- ROLE ---
    role = None
    for q in questions_schema.get("role", []):
        if answers_dict.get(q) == "yes":
            if "player" in q.lower():
                role = "player"
            elif "manager" in q.lower():
                role = "manager"
            elif "owner" in q.lower():
                role = "owner"
            break

    # ✅ Immediate role lock-in
    if not role:
        for q in questions_schema.get("role", []):
            if q not in asked_set:
                return q
        return None
    else:
        asked_set.update(questions_schema.get("role", []))

    # --- CONTINENT ---
    continent = None
    for q in questions_schema.get(f"{role}_continent", []):
        if answers_dict.get(q) == "yes" and "from " in q:
            raw = q.split("from ", 1)[1].rstrip("?")
            continent = normalize_continent_name(raw)
            break

    if not continent:
        for q in questions_schema.get(f"{role}_continent", []):
            if q not in asked_set:
                return q
        return None

    # --- COUNTRY ---
    country_key = f"{role}_country_born_{continent}" if role == "manager" else f"{role}_country_{continent}"
    country_questions = questions_schema.get(country_key, [])
    if country_questions:
        if any(answers_dict.get(q) == "yes" for q in country_questions):
            asked_set.update(country_questions)
        else:
            for q in country_questions:
                if q not in asked_set:
                    return q

    # --- LEAGUE (auto-skip on yes) ---
    league_keys = [k for k in questions_schema if k.startswith(f"{role}_league_")]
    league_keys.sort(key=lambda x: 0 if x.endswith(continent) else 1)

    league_found = False
    for league_key in league_keys:
        league_questions = questions_schema.get(league_key, [])
        if not league_questions:
            continue
        if any(answers_dict.get(q) == "yes" for q in league_questions):
            league_found = True
            break
        for q in league_questions:
            if q not in asked_set:
                return q

    if league_found:
        for league_key in league_keys:
            asked_set.update(questions_schema.get(league_key, []))

    # --- CLUB (auto-skip on yes) ---
    # --- CLUB (cross-continent & full mapping support) ---
    club_key = None
    chosen_league = None

    # Search through all leagues, not just continent-based ones
    all_league_groups = [k for k in questions_schema if k.startswith(f"{role}_league_")]
    for league_group in all_league_groups:
        for q in questions_schema.get(league_group, []):
            if answers_dict.get(q) == "yes":
                chosen_league = q.lower()
                break
        if chosen_league:
            break

    if chosen_league:
        mapping = {
            # --- EUROPE ---
            "premier league": "premier_league",
            "championship": "championship",
            "la liga": "laliga",
            "serie a": "serie_a",
            "bundesliga": "bundesliga",
            "ligue 1": "ligue_1",
            "eredivisie": "eredivisie",
            "primeira liga": "primeira_liga",
            "belgian pro league": "belgian_pro_league",
            "super lig": "turkish_super_lig",
            "russian premier league": "russian_premier_league",
            "scottish premiership": "scottish_premiership",
            "swiss super league": "swiss_super_league",
            "ukrainian premier league": "ukrainian_premier_league",
            "greek super league": "greek_super_league",
            "cypriot first division": "cypriot_first_division",
            "norwegian eliteserien": "eliteserien",
            "swedish allsvenskan": "allsvenskan",
            "danish superliga": "danish_superliga",
            "romanian liga i": "liga_i",
            "polish ekstraklasa": "ekstraklasa",
            "czech first league": "czech_first_league",

            # --- AFRICA ---
            "egyptian premier league": "egyptian_premier_league",
            "npfl": "npfl",
            "south african premier division": "psl",
            "botola pro": "botola_pro",
            "tunisian ligue 1": "tunisian_ligue_1",
            "ghana premier league": "ghana_premier_league",
            "caf champions league": "caf_champions_league",
            "caf confederation cup": "caf_confederation_cup",

            # --- ASIA / MIDDLE EAST ---
            "saudi pro league": "saudi_pro_league",
            "qatar stars league": "qatar_stars_league",
            "uae pro league": "uae_pro_league",
            "j1 league": "j1_league",
            "k league": "k_league",
            "indian super league": "indian_super_league",
            "chinese super league": "chinese_super_league",
            "iran pro league": "iran_pro_league",

            # --- AMERICA ---
            "mls": "mls",
            "liga mx": "liga_mx",
            "brasileirão": "brasileirao",
            "argentine primera division": "argentine_primera_division",
            "uruguayan primera division": "uruguayan_primera_division",
            "chilean primera division": "chilean_primera_division",
            "colombian primera a": "colombian_primera_a",

            # --- OCEANIA / OTHER ---
            "a-league": "a_league",
        }

        for key, val in mapping.items():
            if key in chosen_league:
                club_key = f"{role}_club_{val}"
                break

    if club_key:
        club_questions = questions_schema.get(club_key, [])
        if club_questions:
            confirmed = any(answers_dict.get(q) == "yes" for q in club_questions)
            all_asked = all(q in asked_set for q in club_questions)
            if not (confirmed or all_asked):
                for q in club_questions:
                    if q not in asked_set:
                        return q

    if club_key:
        club_questions = questions_schema.get(club_key, [])
        if club_questions:
            if any(answers_dict.get(q) == "yes" for q in club_questions):
                asked_set.update(club_questions)
            else:
                for q in club_questions:
                    if q not in asked_set:
                        return q

    # --- FINAL PHASE: Always ask critical questions ---
    is_goalkeeper = any(
        answers_dict.get(q) == "yes"
        for q in questions_schema.get("player_position", [])
        if "goalkeeper" in q.lower() or "gk" in q.lower()
    )

    # Critical groups that MUST be asked (even if club is known)
    critical_groups = ["player_position", "player_age", "player_status"]
    if role == "player":
        honors_group = "player_honors_goalkeeper" if is_goalkeeper else "player_honors_outfield"
        critical_groups.append(honors_group)

    for group in critical_groups:
        group_questions = questions_schema.get(group, [])
        for q in group_questions:
            if q not in asked_set:
                return q

    # Other groups (non-critical)
    other_groups = {
        "player": ["player_post_career"],
        "manager": ["manager_playing_career", "manager_tactics", "manager_honors", "manager_status", "manager_era"],
        "owner": ["owner_profile", "owner_status"],
    }
    for group in other_groups.get(role, []):
        group_questions = questions_schema.get(group, [])
        for q in group_questions:
            if q not in asked_set:
                return q

    return None


# -----------------------------
# Candidate Filtering
# -----------------------------
def filter_candidates(answers_list, all_characters):
    """
    Implements Akinator-like logic:
    1. HARD ELIMINATION: Remove anyone contradicting a 'yes'/'no' answer
    2. SCORE survivors: How many answers they matched
    3. RETURN top 10 by score
    """
    if not answers_list:
        # No answers yet → return top 10
        return [(name, data, 0) for name, data in list(all_characters.items())[:10]]

    # Normalize user answers for comparison
    user_answers_norm = {
        normalize_key(q): ans
        for q, ans in answers_list
        if ans in ("yes", "no")
    }

    survivors = []
    for name, data in all_characters.items():
        if not isinstance(data, dict):
            continue
        char_answers = data.get("answers", {})
        
        valid = True
        # Check each user answer against character's answers
        for norm_q, user_ans in user_answers_norm.items():
            # Find matching question in character's answers
            matched = False
            for char_q, char_ans in char_answers.items():
                if normalize_key(char_q) == norm_q:
                    if char_ans != user_ans:
                        valid = False  # Contradiction found
                        matched = True
                        break
                    matched = True
                    break
            if not valid:
                break
            # If no matching question found, that's okay (neutral)
        
        if valid:
            survivors.append((name, data))

    if not survivors:
        print("--- NO SURVIVORS AFTER ELIMINATION ---")
        # Fallback: return top 10 with 0% confidence
        return [(name, data, 0) for name, data in list(all_characters.items())[:10]]

    # Score survivors based on how many answers they matched
    scored = []
    total_yes_no = len([1 for q, a in answers_list if a in ("yes", "no")])
    for name, data in survivors:
        char_answers = data.get("answers", {})
        matches = 0
        for q, user_ans in answers_list:
            if user_ans in ("yes", "no"):
                norm_q = normalize_key(q)
                # Find matching question in character's answers
                for char_q, char_ans in char_answers.items():
                    if normalize_key(char_q) == norm_q:
                        if char_ans == user_ans:
                            matches += 1
                        break
        
        confidence = (matches / total_yes_no * 100) if total_yes_no > 0 else 0
        scored.append((name, data, round(confidence, 2)))

    # Sort by confidence descending
    scored.sort(key=lambda x: x[2], reverse=True)
    return scored[:10]


# -----------------------------
# Flask Routes
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

    asked = {q for q, _ in answers}
    next_q = get_next_question(answers, asked, questions_schema)
    if not next_q:
        return redirect(url_for("answer"))

    session["current_question"] = next_q
    progress = min(95, len([a for a in answers if a[1] == "yes"]) * 10)
    return render_template("question.html", question=next_q, progress=progress)


@app.route("/undo", methods=["POST"])
def undo():
    answers = session.get("answers", [])
    if answers:
        answers.pop()
        session["answers"] = answers
    return redirect(url_for("question"))


@app.route("/answer", methods=["GET", "POST"])
def answer():
    answers = session.get("answers", [])
    wrong_guesses = session.get("wrong_guesses", 0)
    base_chars = load_json_file(CHARACTERS_PATH, {})
    user_know = load_json_file(KNOW_PATH, {})
    all_chars = {**base_chars, **user_know}
    
    print("\n🔍 USER ANSWERS:")
    for q, ans in answers:
        print(f"  • {q} → {ans}")

    candidates = filter_candidates(answers, all_chars)
    print("\n--- CANDIDATE SCORES ---")
    for n, _, c in candidates:
        print(f"{n}: {c:.2f}%")
        print("--------------------------")

    if not candidates:
        return render_template("answer.html", guess="😅 I couldn't find anyone matching your answers!",
                               image_url="/static/images/unknown.png", play_again=True)

    best_name, best_data, confidence = candidates[0]
    img = best_data.get("image_url", "/static/images/default.png")

    # Lowered threshold to 10
    if confidence < 10:
        return render_template("answer.html", guess="🤔 I'm not confident enough to guess.",
                               image_url="/static/images/unknown.png", low_confidence=True, play_again=True)

    if request.method == "POST":
        if request.form.get("action") == "correct":
            return render_template("answer.html", guess=f"🎉 Yes! It was {best_name}!",
                                   show_success=True, play_again=True)
        elif request.form.get("action") == "wrong":
            wrong_guesses += 1
            session["wrong_guesses"] = wrong_guesses
            if wrong_guesses >= 5:
                return redirect(url_for("learn"))
            return redirect(url_for("question"))

    return render_template("answer.html", guess=best_name, image_url=img, play_again=True, confidence=confidence)


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
            save_json_file(KNOW_PATH, user_know)
            return redirect(url_for("index"))
    return render_template("learn.html")


if __name__ == "__main__":
    print("✅ Football Mind Reader running on http://127.0.0.1:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)