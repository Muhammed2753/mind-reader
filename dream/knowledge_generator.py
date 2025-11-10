import json
import os
import math
import re
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


def extract_entity_from_question(q_text):
    """
    Try to extract an entity (club/league/country) from a question string.
    Examples:
      "Is this player playing for Al Ahly?" -> "al ahly"
      "Is he from Argentina?" -> "argentina"
    Returns the lowercased entity or None.
    """
    if not q_text:
        return None
    q = q_text.lower().strip()
    # common prepositions that precede entity names
    # order matters: longer phrases first
    patterns = [
        r"playing for (.+)\??$",
        r"plays for (.+)\??$",
        r"is playing for (.+)\??$",
        r"is he playing for (.+)\??$",
        r"from (.+)\??$",
        r"is from (.+)\??$",
        r"born in (.+)\??$",
        r"playing at (.+)\??$",
        r"at (.+)\??$",
        r"for (.+)\??$",
        r"which club (?:does|do).*? (.+)\??$",
    ]
    for pat in patterns:
        m = re.search(pat, q)
        if m:
            ent = m.group(1).strip()
            # remove trailing punctuation
            ent = re.sub(r"[^\w\s&\-\.']", "", ent)
            ent = re.sub(r"\s+", " ", ent).strip()
            return ent.lower()
    # fallback: if question is like "Is this player at Manchester City?" -> catch last two words
    words = q.split()
    if len(words) >= 2 and words[-1].endswith("?"):
        ent = words[-1][:-1]
        return ent.lower()
    return None


# -----------------------------
# Question Flow Logic
# (kept as you supplied, small improvements retained)
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
            # (mapping shortened for brevity — keep your full mapping when using)
            "premier league": "premier_league",
            "la liga": "laliga",
            "serie a": "serie_a",
            "bundesliga": "bundesliga",
            "ligue 1": "ligue_1",
            "egyptian premier league": "egyptian_premier_league",
            "saudi pro league": "saudi_pro_league",
            "mls": "mls",
            "brasileirão": "brasileirao",
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

    # --- FINAL PHASE (auto-skip logic) ---
    is_goalkeeper = any(
        answers_dict.get(q) == "yes"
        for q in questions_schema.get("player_position", [])
        if "goalkeeper" in q.lower() or "gk" in q.lower()
    )

    final_groups = {
        "player": ["player_position", "player_age", "player_status", "player_post_career"],
        "manager": ["manager_playing_career", "manager_tactics", "manager_honors", "manager_status", "manager_era"],
        "owner": ["owner_profile", "owner_status"],
    }

    if role == "player":
        honors_group = "player_honors_goalkeeper" if is_goalkeeper else "player_honors_outfield"
        final_groups["player"].insert(3, honors_group)

    for group in final_groups.get(role, []):
        group_questions = questions_schema.get(group, [])
        if not group_questions:
            continue

        # ✅ Skip group if already confirmed
        if any(answers_dict.get(q) == "yes" for q in group_questions):
            asked_set.update(group_questions)
            continue

        for q in group_questions:
            if q not in asked_set:
                return q

    return None


# -----------------------------
# Candidate Filtering
# -----------------------------
def filter_candidates(answers_list, all_characters):
    """
    HARD ELIMINATION + SOFT SCORING
    Filters candidates using answers, positions, age, status, honors,
    club/league/country entities and then ranks them by confidence.
    """
    if not answers_list:
        # No answers yet → return top 10 with 0% confidence
        return [(name, data, 0) for name, data in list(all_characters.items())[:10]]

    survivors = []

    # Pre-extract confirmed entities for bonuses
    confirmed_entities = {"club": [], "league": [], "country": []}
    for q, ans in answers_list:
        if ans != "yes":
            continue
        ent = extract_entity_from_question(q)
        if not ent:
            continue
        if any(k in q.lower() for k in ("club", "playing for", "plays for", "playing at")):
            confirmed_entities["club"].append(ent)
        elif any(k in q.lower() for k in ("league", "premier", "liga", "serie", "mls")):
            confirmed_entities["league"].append(ent)
        elif any(k in q.lower() for k in ("from ", "born", "country", "nationality")):
            confirmed_entities["country"].append(ent)

    # --- HARD ELIMINATION ---
    for name, data in all_characters.items():
        if not isinstance(data, dict):
            continue
        char_answers = data.get("answers", {})

        valid = True

        # 1️⃣ Compare yes/no answers
        for q, user_ans in answers_list:
            if user_ans not in ("yes", "no"):
                continue
            char_ans = char_answers.get(q, "i don't know")
            if char_ans in ("yes", "no") and user_ans != char_ans:
                valid = False
                break
        if not valid:
            continue

        # 2️⃣ Position
        pos_questions = [q for q, a in answers_list if a == "yes" and "position" in q.lower()]
        position_val = normalize_field(data.get("position"))
        for pq in pos_questions:
            ent = pq.lower().split("is a")[-1].strip().replace("?", "")
            if ent and ent not in position_val:
                valid = False
                break
        if not valid:
            continue

        # 3️⃣ Age
        age_questions = [q for q, a in answers_list if a == "yes" and "age" in q.lower()]
        age_val = str(data.get("age", "")).lower()
        for aq in age_questions:
            nums = re.findall(r"\d+", aq)
            if nums and nums[0] not in age_val:
                valid = False
                break
        if not valid:
            continue

        # 4️⃣ Status
        status_questions = [q for q, a in answers_list if a == "yes" and "status" in q.lower()]
        status_val = normalize_field(data.get("status"))
        for sq in status_questions:
            if "retired" in sq.lower() and "retired" not in status_val:
                valid = False
                break
            if "active" in sq.lower() and "active" not in status_val:
                valid = False
                break
        if not valid:
            continue

        # 5️⃣ Honors
        honors_questions = [q for q, a in answers_list if a == "yes" and "honor" in q.lower()]
        honors_val = normalize_field(data.get("honors"))
        for hq in honors_questions:
            ent = extract_entity_from_question(hq)
            if ent and isinstance(honors_val, list) and not any(ent in hv for hv in honors_val):
                valid = False
                break
        if not valid:
            continue

        survivors.append((name, data))

    if not survivors:
        # Fallback: return top 10 with 0% confidence
        return [(name, data, 0) for name, data in list(all_characters.items())[:10]]

    # --- SOFT SCORING ---
    scored = []
    total_yes_no = len([1 for q, a in answers_list if a in ("yes", "no")])

    for name, data in survivors:
        char_answers = data.get("answers", {})
        score = 0

        # ✅ Match yes/no answers
        for q, user_ans in answers_list:
            if user_ans in ("yes", "no"):
                char_ans = char_answers.get(q, "i don't know")
                if char_ans == user_ans:
                    score += 5
                elif user_ans in ("i don't know", "sometimes") or char_ans == "i don't know":
                    score += 2
                elif user_ans == "no" and char_ans == "no":
                    score += 4
                else:
                    score -= 1

        # ✅ Bonus: match club/country/league
        club_fields = []
        for key in ("current_club", "club", "clubs", "team", "teams"):
            val = data.get(key)
            if val:
                if isinstance(val, list):
                    club_fields.extend([v.lower() for v in val])
                else:
                    club_fields.append(str(val).lower())
        for c in confirmed_entities["club"]:
            if any(c in cf for cf in club_fields):
                score += 15
        for c in confirmed_entities["country"]:
            country_fields = [str(data.get(k, "")).lower() for k in ("country", "nationality", "born_in")]
            if any(c in cf for cf in country_fields if cf):
                score += 12
        for c in confirmed_entities["league"]:
            if any(c in cf for cf in club_fields):
                score += 8

        # ✅ Bonus: position
        for pq in pos_questions:
            ent = pq.lower().split("is a")[-1].strip().replace("?", "")
            if ent and ent in position_val:
                score += 10

        # ✅ Bonus: age
        for aq in age_questions:
            nums = re.findall(r"\d+", aq)
            if nums and nums[0] in age_val:
                score += 8

        # ✅ Bonus: status
        for sq in status_questions:
            if "retired" in sq.lower() and "retired" in status_val:
                score += 8
            if "active" in sq.lower() and "active" in status_val:
                score += 8

        # ✅ Bonus: honors
        for hq in honors_questions:
            ent = extract_entity_from_question(hq)
            if ent and isinstance(honors_val, list) and any(ent in hv for hv in honors_val):
                score += 12

        confidence = ((score) / (total_yes_no * 5 + 100) * 100) if total_yes_no > 0 else 0
        scored.append((name, data, round(confidence, 2)))

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

    if confidence < 20:  # Lowered threshold
        return render_template("answer.html", guess="🤔 I'm not confident enough to guess.",
                               image_url="/static/images/unknown.png", low_confidence=True, play_again=True)

    if request.method == "POST":
        if request.form.get("action") == "correct":
            return render_template("answer.html", guess=f"🎉 Yes! It was {best_name}!",
                                   show_success=True, play_again=True)
        elif request.form.get("action") == "wrong":
            wrong_guesses += 1  # Fixed: was += 3 earlier
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
