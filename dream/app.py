import json
import os
import re
import random
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from better_profanity import Profanity

# ============================================================
#  APP SETUP
# ============================================================

app = Flask(__name__)
app.secret_key = "Muhfal_2025_Secret"
CORS(app)

profanity_checker = Profanity()

# ============================================================
#  FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).parent
CHARACTERS_PATH = BASE_DIR / "football_characters.json"
QUESTIONS_SCHEMA_PATH = BASE_DIR / "football_questions.json"
KNOW_PATH = BASE_DIR / "knowledge_db.json"
STATS_PATH = BASE_DIR / "game_stats.json"

# Ensure static/images directory exists with placeholder files
(BASE_DIR / "static" / "images").mkdir(parents=True, exist_ok=True)
for img_name in ["default.png", "unknown.png"]:
    img_path = BASE_DIR / "static" / "images" / img_name
    if not img_path.exists():
        img_path.write_text("")

# ============================================================
#  JSON HELPERS
# ============================================================

def load_json(path, default):
    """Load a JSON file safely, returning default on failure."""
    path = Path(path)
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[WARN] Could not load {path}: {e}")
        return default

def save_json(path, data):
    """Save data to a JSON file safely."""
    try:
        Path(path).write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    except Exception as e:
        print(f"[WARN] Could not save {path}: {e}")

# ============================================================
#  STARTUP: LOAD DATA ONCE
# ============================================================

BASE_CHARS = load_json(CHARACTERS_PATH, {})
USER_KNOW  = load_json(KNOW_PATH, {})
ALL_CHARS  = {**BASE_CHARS, **USER_KNOW}

# ============================================================
#  NORMALISATION HELPERS
# ============================================================

def normalize_answer(raw: str) -> str:
    s = (raw or "").strip().lower()
    if s in {"idk", "i don't know", "dont know", "unknown", ""}:
        return "i don't know"
    if s in {"yes", "y", "yeah", "yep", "sure"}:
        return "yes"
    if s in {"no", "n", "nope", "nah"}:
        return "no"
    if s in {"sometimes", "maybe", "occasionally", "not really"}:
        return "sometimes"
    return "i don't know"

def normalize_key(text: str) -> str:
    """Strip punctuation/spaces for question matching."""
    return re.sub(r"[^\w]", "", text.lower().strip())

def normalize_continent(text: str) -> str:
    return text.strip().lower().replace(" ", "_").replace("-", "_")

# ============================================================
#  PROFANITY CHECK
# ============================================================

_BAD_WORDS = {
    "fuck", "shit", "bitch", "asshole", "dick", "piss", "cunt", "slut",
    "whore", "nigga", "nigger", "fag", "faggot", "cock", "twat", "crap",
    "arse", "bollocks", "wanker", "prick", "douche", "motherfucker",
    "bastard", "retard", "moron",
}

def has_profanity(text: str) -> bool:
    if not text:
        return False
    words = set(re.sub(r"[^\w\s]", "", text.lower()).split())
    return bool(words & _BAD_WORDS) or profanity_checker.contains_profanity(text)

# ============================================================
#  QUESTION INDEX  (built once at startup)
# ============================================================

QUESTION_TO_NAMES: dict[str, set] = {}

def build_question_index(all_characters: dict):
    global QUESTION_TO_NAMES
    QUESTION_TO_NAMES = {}
    for name, data in all_characters.items():
        for q, ans in data.get("answers", {}).items():
            if ans == "yes":
                key = normalize_key(q)
                QUESTION_TO_NAMES.setdefault(key, set()).add(name)

build_question_index(ALL_CHARS)

# ============================================================
#  GAME STATS
# ============================================================

_EMPTY_STATS = {
    "games_played": 0,
    "games_won": 0,
    "current_streak": 0,
    "best_streak": 0,
    "level": 1,
}

def get_stats() -> dict:
    stats = load_json(STATS_PATH, dict(_EMPTY_STATS))
    stats["level"] = min(1 + stats.get("games_played", 0) // 10, 10)
    return stats

def save_stats(stats: dict):
    save_json(STATS_PATH, stats)

def record_win(questions_asked: int, player_name: str, time_taken: int):
    stats = get_stats()
    stats["games_played"] += 1
    stats["games_won"]    += 1
    stats["current_streak"] += 1
    stats["best_streak"] = max(stats["best_streak"], stats["current_streak"])
    save_stats(stats)
    check_achievements(stats)

def record_loss(questions_asked: int):
    stats = get_stats()
    stats["games_played"]   += 1
    stats["current_streak"]  = 0
    save_stats(stats)

# ============================================================
#  ACHIEVEMENTS
# ============================================================

ALL_ACHIEVEMENTS = {
    "first_win":    {"name": "First Victory",   "description": "Win your first game",        "icon": "🏆"},
    "streak_5":     {"name": "Streak Master",   "description": "Win 5 games in a row",       "icon": "🔥"},
    "streak_10":    {"name": "Unstoppable",      "description": "Win 10 games in a row",      "icon": "⚡"},
    "quick_win":    {"name": "Mind Reader",      "description": "Win in under 10 questions",  "icon": "🧠"},
    "veteran":      {"name": "Veteran Player",   "description": "Play 50 games",              "icon": "🎖️"},
    "perfect_week": {"name": "Perfect Week",     "description": "Win 7 games this week",      "icon": "💎"},
}

ACHIEVEMENTS_PATH = BASE_DIR / "achievements.json"

def get_unlocked() -> list:
    return load_json(ACHIEVEMENTS_PATH, [])

def unlock(achievement_id: str) -> dict | None:
    unlocked = get_unlocked()
    if achievement_id not in unlocked:
        unlocked.append(achievement_id)
        save_json(ACHIEVEMENTS_PATH, unlocked)
        return ALL_ACHIEVEMENTS.get(achievement_id)
    return None

def check_achievements(stats: dict) -> list:
    new = []
    if stats.get("games_won", 0) >= 1:
        a = unlock("first_win");  a and new.append(a)
    if stats.get("current_streak", 0) >= 5:
        a = unlock("streak_5");   a and new.append(a)
    if stats.get("current_streak", 0) >= 10:
        a = unlock("streak_10");  a and new.append(a)
    if stats.get("games_played", 0) >= 50:
        a = unlock("veteran");    a and new.append(a)
    return new

# ============================================================
#  CANDIDATE FILTERING
# ============================================================

def extract_age_group(answers_dict: dict) -> str:
    if answers_dict.get("Is this player under 18 years old?") == "yes":          return "under_18"
    if answers_dict.get("Is this player between 18 and 23 years old?") == "yes": return "18_23"
    if answers_dict.get("Is this player between 23 and 35 years old?") == "yes": return "23_35"
    if answers_dict.get("Is this player over 35 years old?") == "yes":           return "over_35"
    return "unknown"

def filter_candidates(answers_list: list, all_characters: dict) -> list:
    """Return ranked (name, data, confidence%) list of matching characters."""
    if not answers_list:
        return [(n, d, 0) for n, d in list(all_characters.items())[:50]]

    answers_dict  = dict(answers_list)
    user_age      = extract_age_group(answers_dict)
    remaining     = list(all_characters.items())

    # --- Status contradiction check ---
    def status_eliminated(char_ans: dict) -> bool:
        pairs = [
            ("Is this player currently active?",   "Has this player retired?",        "Is this player deceased?"),
            ("Is this manager currently active?",  "Has this manager retired?",       "Is this manager deceased?"),
            ("Is this owner currently active?",    "Has this owner stepped down?",    "Is this owner deceased?"),
        ]
        for active_q, retired_q, deceased_q in pairs:
            if answers_dict.get(active_q) == "yes":
                if char_ans.get(retired_q) == "yes" or char_ans.get(deceased_q) == "yes":
                    return True
            if answers_dict.get(retired_q) == "yes":
                if char_ans.get(active_q) == "yes":
                    return True
            if answers_dict.get(deceased_q) == "yes":
                if char_ans.get(active_q) == "yes" or char_ans.get(retired_q) == "yes":
                    return True
        return False

    remaining = [(n, d) for n, d in remaining if not status_eliminated(d.get("answers", {}))]
    if not remaining:
        return []

    # --- Answer-by-answer hard filtering ---
    for question, user_answer in answers_list:
        norm_q = normalize_key(question)
        new_remaining = []
        for name, data in remaining:
            char_age = data.get("age_group", "unknown")
            if user_age != "unknown" and char_age != "unknown" and char_age != user_age:
                continue
            char_answers = data.get("answers", {})
            matched = keep = False
            for cq, ca in char_answers.items():
                if normalize_key(cq) == norm_q:
                    matched = True
                    keep = (ca == user_answer)
                    break
            if not matched:
                keep = (user_answer != "yes")
            if keep:
                new_remaining.append((name, data))
        remaining = new_remaining
        if not remaining:
            return []

    # --- Score survivors ---
    yes_count = sum(1 for _, a in answers_list if a == "yes")
    scored = []
    for name, data in remaining:
        score = sum(
            1 for q, ua in answers_list if ua == "yes"
            for cq, ca in data.get("answers", {}).items()
            if normalize_key(cq) == normalize_key(q) and ca == "yes"
        )
        conf = (score / max(1, yes_count)) * 100 if yes_count else 50
        scored.append((name, data, round(conf, 1)))

    scored.sort(key=lambda x: x[2], reverse=True)
    return scored[:50]

# ============================================================
#  ACTIVE QUESTION HELPER
# ============================================================

def active_questions(schema: dict, all_chars: dict, answers_list: list, group_key: str) -> list:
    """Return questions from a schema group that are relevant to current candidates."""
    base_qs = schema.get(group_key, [])
    if not base_qs:
        return []
    candidate_names = {n for n, _, _ in filter_candidates(answers_list, all_chars)}
    return [q for q in base_qs if QUESTION_TO_NAMES.get(normalize_key(q), set()) & candidate_names]

# ============================================================
#  CLUB MAPPING
# ============================================================

BIG_TEAMS = {
    "player_club_premier_league": [
        "Is this player playing for Manchester United?",
        "Is this player playing for Manchester City?",
        "Is this player playing for Liverpool?",
        "Is this player playing for Arsenal?",
        "Is this player playing for Chelsea?",
        "Is this player playing for Tottenham Hotspur?",
        "Is this player playing for Newcastle United?",
        "Is this player playing for Brighton & Hove Albion?",
        "Is this player playing for Aston Villa?",
        "Is this player playing for West Ham United?",
        "Is this player playing for Wolverhampton Wanderers?",
        "Is this player playing for Crystal Palace?",
        "Is this player playing for Brentford?",
        "Is this player playing for Fulham?",
        "Is this player playing for Everton?",
        "Is this player playing for Bournemouth?",
        "Is this player playing for Nottingham Forest?",
        "Is this player playing for Leicester City?",
        "Is this player playing for Leeds United?",
        "Is this player playing for Southampton?",
    ],
    "player_club_laliga": [
        "Is this player playing for Real Madrid?",
        "Is this player playing for Barcelona?",
        "Is this player playing for Atletico Madrid?",
        "Is this player playing for Real Sociedad?",
        "Is this player playing for Villarreal?",
        "Is this player playing for Athletic Club?",
        "Is this player playing for Real Betis?",
        "Is this player playing for Sevilla?",
        "Is this player playing for Girona?",
        "Is this player playing for Osasuna?",
        "Is this player playing for Rayo Vallecano?",
        "Is this player playing for Celta Vigo?",
        "Is this player playing for Alaves?",
        "Is this player playing for Mallorca?",
        "Is this player playing for Las Palmas?",
    ],
    "player_club_serie_a": [
        "Is this player playing for Juventus?",
        "Is this player playing for Inter Milan?",
        "Is this player playing for AC Milan?",
        "Is this player playing for Napoli?",
        "Is this player playing for Roma?",
        "Is this player playing for Atalanta?",
        "Is this player playing for Fiorentina?",
        "Is this player playing for Lazio?",
        "Is this player playing for Torino?",
        "Is this player playing for Udinese?",
        "Is this player playing for Genoa?",
        "Is this player playing for Monza?",
        "Is this player playing for Lecce?",
        "Is this player playing for Empoli?",
        "Is this player playing for Verona?",
    ],
    "player_club_bundesliga": [
        "Is this player playing for Bayern Munich?",
        "Is this player playing for Borussia Dortmund?",
        "Is this player playing for RB Leipzig?",
        "Is this player playing for Bayer Leverkusen?",
        "Is this player playing for Eintracht Frankfurt?",
        "Is this player playing for Wolfsburg?",
        "Is this player playing for Union Berlin?",
        "Is this player playing for Freiburg?",
        "Is this player playing for Mainz 05?",
        "Is this player playing for VfB Stuttgart?",
        "Is this player playing for Borussia Monchengladbach?",
        "Is this player playing for Augsburg?",
        "Is this player playing for Hoffenheim?",
        "Is this player playing for Bochum?",
        "Is this player playing for St. Pauli?",
    ],
    "player_club_ligue_1": [
        "Is this player playing for Paris Saint-Germain?",
        "Is this player playing for Monaco?",
        "Is this player playing for Marseille?",
        "Is this player playing for Lyon?",
        "Is this player playing for Lille?",
        "Is this player playing for Lens?",
        "Is this player playing for Rennes?",
        "Is this player playing for Nice?",
        "Is this player playing for Nantes?",
        "Is this player playing for Strasbourg?",
        "Is this player playing for Reims?",
        "Is this player playing for Brest?",
        "Is this player playing for Toulouse?",
        "Is this player playing for Montpellier?",
        "Is this player playing for Auxerre?",
    ],
}

COUNTRY_TO_LEAGUE = {
    "england":      "premier_league",
    "spain":        "la_liga",
    "italy":        "serie_a",
    "germany":      "bundesliga",
    "france":       "ligue_1",
    "saudi arabia": "saudi_pro_league",
    "usa":          "mls",
    "brazil":       "brasileirao",
    "argentina":    "liga_profesional",
    "netherlands":  "eredivisie",
    "portugal":     "primeira_liga",
    "belgium":      "belgian_pro_league",
    "turkey":       "turkish_super_lig",
    "scotland":     "scottish_premiership",
    "egypt":        "egyptian_premier_league",
}

# ============================================================
#  QUESTION FLOW
# ============================================================

def get_next_question(answers_list: list, schema: dict, all_chars: dict):
    """Return the next best question string, a dead-end dict, or None (→ answer)."""
    answers_dict = dict(answers_list)
    asked = set(answers_dict.keys())

    def unasked(qs):
        return [q for q in qs if q not in asked]

    def answered_yes(qs):
        return any(answers_dict.get(q) == "yes" for q in qs)

    def pick(qs):
        """Return a random unasked question from list, or None."""
        pool = unasked(qs)
        return random.choice(pool) if pool else None

    # ── 1. ROLE ──────────────────────────────────────────────
    role_qs = schema.get("role", [
        "Is this person a football player?",
        "Is this person a football manager?",
        "Is this person a football club owner or executive?",
    ])
    role = None
    for q in role_qs:
        if answers_dict.get(q) == "yes":
            if "player"  in q.lower(): role = "player"
            elif "manager" in q.lower(): role = "manager"
            elif "owner"   in q.lower(): role = "owner"
            break

    if not role:
        nxt = pick(role_qs)
        return nxt or {"type": "dead_end", "message": "Could not determine role."}

    # ── 2. STATUS ────────────────────────────────────────────
    status_qs = schema.get(f"{role}_status", [])
    if status_qs and not answered_yes(status_qs):
        nxt = pick(status_qs)
        if nxt:
            return nxt

    # Determine status
    status = None
    active_keys  = {"Is this player currently active?", "Is this manager currently active?", "Is this owner currently active?"}
    retired_keys = {"Has this player retired?", "Has this manager retired?", "Has this owner stepped down?"}
    deceased_keys= {"Is this player deceased?", "Is this manager deceased?", "Is this owner deceased?"}
    pundit_keys  = {"Has this player become a pundit?", "Has this manager become a pundit?"}

    if   any(answers_dict.get(k) == "yes" for k in active_keys):   status = "active"
    elif any(answers_dict.get(k) == "yes" for k in retired_keys):  status = "retired"
    elif any(answers_dict.get(k) == "yes" for k in deceased_keys): status = "deceased"
    elif any(answers_dict.get(k) == "yes" for k in pundit_keys):   status = "pundit"

    # ── 3. NON-ACTIVE PATHS ──────────────────────────────────
    if status == "retired":
        ret_cont_qs = active_questions(schema, all_chars, answers_list, f"{role}_retired_continent")
        if ret_cont_qs and not answered_yes(ret_cont_qs):
            nxt = pick(ret_cont_qs); return nxt if nxt else None

        ret_year_qs = schema.get(f"{role}_retired_year", [])
        if ret_year_qs and not answered_yes(ret_year_qs):
            nxt = pick(ret_year_qs); return nxt if nxt else None

    elif status == "deceased":
        for group in (f"{role}_deceased_year", f"{role}_deceased_era"):
            qs = schema.get(group, [])
            if qs and not answered_yes(qs):
                nxt = pick(qs); return nxt if nxt else None

    elif status == "pundit" and role != "owner":
        for group in (f"{role}_pundit_network", f"{role}_pundit_background"):
            qs = schema.get(group, [])
            if qs and not answered_yes(qs):
                nxt = pick(qs); return nxt if nxt else None

    # ── 4. ACTIVE PATH ───────────────────────────────────────
    if status == "active":
        # Origin continent
        origin_cont_qs = active_questions(schema, all_chars, answers_list, f"{role}_continent")
        origin_continent = None
        for q in origin_cont_qs:
            if answers_dict.get(q) == "yes":
                m = re.search(r"(?:birthplace in|from)\s+([a-zA-Z\s]+)\?", q, re.I)
                if m: origin_continent = normalize_continent(m.group(1)); break
        if not origin_continent:
            nxt = pick(origin_cont_qs)
            return nxt or {"type": "dead_end", "message": "Origin continent unclear."}

        # Origin country
        oc_key = f"{role}_country_born_{origin_continent}" if role == "manager" else f"{role}_country_{origin_continent}"
        oc_qs = active_questions(schema, all_chars, answers_list, oc_key)
        if oc_qs and not answered_yes(oc_qs):
            nxt = pick(oc_qs); return nxt if nxt else None

        # Work continent
        wc_qs = active_questions(schema, all_chars, answers_list, f"{role}_league_continent")
        work_continent = None
        for q in wc_qs:
            if answers_dict.get(q) == "yes":
                m = re.search(rf"is this {role} (?:playing|managing|associated).*?in ([a-zA-Z\s]+)\?", q, re.I)
                if m: work_continent = normalize_continent(m.group(1)); break
        if not work_continent:
            nxt = pick(wc_qs)
            return nxt or {"type": "dead_end", "message": "Work continent unclear."}

        # Work country
        work_country = None
        wco_qs = active_questions(schema, all_chars, answers_list, f"{role}_league_country_{work_continent}")
        for q in wco_qs:
            if answers_dict.get(q) == "yes":
                m = re.search(rf"is this {role} (?:playing|managing|associated) in ([a-zA-Z\s]+)\?", q, re.I)
                if m: work_country = normalize_continent(m.group(1)); break
        if not work_country and wco_qs:
            nxt = pick(wco_qs); return nxt if nxt else None

        # League
        league_code = COUNTRY_TO_LEAGUE.get(work_country) if work_country else None
        if league_code:
            league_qs = active_questions(schema, all_chars, answers_list, f"{role}_league_{league_code}")
            if league_qs and not answered_yes(league_qs):
                nxt = pick(league_qs); return nxt if nxt else None

            # Club
            club_key  = f"{role}_club_{league_code}"
            club_qs   = active_questions(schema, all_chars, answers_list, club_key)
            if club_qs and not answered_yes(club_qs):
                # Ask big teams first
                for q in BIG_TEAMS.get(club_key, []):
                    if q in club_qs and q not in asked:
                        return q
                nxt = pick(club_qs); return nxt if nxt else None

    # ── 5. ATTRIBUTES ────────────────────────────────────────
    if role == "player":
        candidates = filter_candidates(answers_list, all_chars)
        positions = set()
        for _, data, _ in candidates:
            for q, ans in data.get("answers", {}).items():
                if ans == "yes" and "position" in q.lower():
                    if "goalkeeper" in q.lower(): positions.add("goalkeeper")
                    else:
                        m = re.search(r"natural position a ([\w\s]+)\?", q)
                        if m: positions.add(m.group(1).strip().lower().replace(" ", "_"))

        pos_qs = [q for q in schema.get("player_position", [])
                  if any(p in q.lower() for p in positions)]
        if pos_qs and not answered_yes(pos_qs):
            nxt = pick(pos_qs); return nxt if nxt else None

        is_gk = "goalkeeper" in positions
        for group in ["player_age",
                      "player_honors_goalkeeper" if is_gk else "player_honors_outfield",
                      "player_status"]:
            qs = active_questions(schema, all_chars, answers_list, group)
            if qs and not answered_yes(qs):
                nxt = pick(qs); return nxt if nxt else None

    elif role == "manager":
        for group in ["manager_era", "manager_playing_career", "manager_tactics",
                      "manager_formation", "manager_honors", "manager_status"]:
            qs = active_questions(schema, all_chars, answers_list, group)
            if qs and not answered_yes(qs):
                nxt = pick(qs); return nxt if nxt else None

    elif role == "owner":
        for group in ["owner_profile", "owner_status"]:
            qs = active_questions(schema, all_chars, answers_list, group)
            if qs and not answered_yes(qs):
                nxt = pick(qs); return nxt if nxt else None

    return None  # → redirect to answer

# ============================================================
#  METADATA INFERENCE (for learn route)
# ============================================================

def infer_metadata(answers_dict: dict, schema: dict) -> dict:
    enriched = answers_dict.copy()
    country_continent = {
        "england": "europe", "spain": "europe", "italy": "europe",
        "germany": "europe", "france": "europe", "brazil": "south_america",
        "argentina": "south_america", "usa": "north_america",
        "saudi arabia": "asia", "japan": "asia", "south korea": "asia",
        "egypt": "africa", "senegal": "africa", "nigeria": "africa",
        "australia": "oceania",
    }
    role = "player"
    if any("manager" in q.lower() for q, a in answers_dict.items() if a == "yes"):
        role = "manager"
    elif any("owner" in q.lower() for q, a in answers_dict.items() if a == "yes"):
        role = "owner"

    for q, ans in answers_dict.items():
        if ans == "yes" and "born in" in q:
            m = re.search(r"born in ([a-zA-Z\s]+)\?", q)
            if m:
                country = normalize_continent(m.group(1))
                continent = country_continent.get(country, "unknown")
                enriched[f"Is this {role} birthplace in {continent.title()}?"] = "yes"
                break
    return enriched

# ============================================================
#  FLASK ROUTES
# ============================================================

@app.route("/")
def index():
    stats = get_stats()
    return render_template("index.html", stats=stats, streak=stats.get("current_streak", 0))


@app.route("/start", methods=["GET", "POST"])
def start():
    difficulty = request.form.get("difficulty", "medium") if request.method == "POST" else "medium"
    session.clear()
    session.update({
        "answers":         [],
        "wrong_guesses":   0,
        "difficulty":      difficulty,
        "game_start_time": str(datetime.now()),
    })
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

    schema = load_json(QUESTIONS_SCHEMA_PATH, {})
    schema.setdefault("role", [
        "Is this person a football player?",
        "Is this person a football manager?",
        "Is this person a football club owner or executive?",
    ])

    candidates = filter_candidates(answers, ALL_CHARS)

    if not candidates:
        record_loss(len(answers))
        return render_template(
            "answer.html",
            guess="I couldn't guess it! Teach me who you were thinking of.",
            player_name="", image_url="/static/images/default.png",
            play_again=True, is_no_match=True,
        )

    next_q = get_next_question(answers, schema, ALL_CHARS)

    if isinstance(next_q, dict) and next_q.get("type") == "dead_end":
        return render_template(
            "answer.html",
            guess=next_q["message"],
            player_name="", image_url="/static/images/default.png",
            play_again=True, is_no_match=True,
        )

    should_guess = (
        not next_q
        or len(answers) >= 150
        or len(candidates) == 1
        or (len(answers) >= 4 and len(candidates) <= 2)
    )
    if should_guess:
        return redirect(url_for("answer"))

    session["current_question"] = next_q
    progress = min(95, len(answers) * 3)

    return render_template(
        "question.html",
        question=next_q,
        progress=progress,
        candidates_count=len(candidates),
        question_number=len(answers) + 1,
        current_thinking_of=candidates[0][0] if candidates else "",
        matches_text="match" if len(candidates) == 1 else "matches",
        answers=answers,
    )


@app.route("/undo", methods=["POST"])
def undo():
    answers = session.get("answers", [])
    if answers:
        answers.pop()
        session["answers"] = answers
        session["wrong_guesses"] = 0
        for key in ("auto_jump", "final_guess_mode", "excluded_names",
                    "previous_question", "previous_answer"):
            session.pop(key, None)
    return redirect(url_for("question"))


@app.route("/answer", methods=["GET", "POST"])
def answer():
    answers   = session.get("answers", [])
    all_chars = {**load_json(CHARACTERS_PATH, {}), **load_json(KNOW_PATH, {})}
    candidates = filter_candidates(answers, all_chars)

    if not candidates:
        record_loss(len(answers))
        return render_template(
            "answer.html",
            guess="I give up — I don't know who that is!",
            player_name="", image_url="/static/images/default.png",
            play_again=True, is_no_match=True,
        )

    best_name, best_data, confidence = candidates[0]
    img = best_data.get("image_url", "/static/images/default.png")

    if request.method == "POST":
        action = request.form.get("action")

        if action == "correct":
            start_time  = datetime.fromisoformat(session.get("game_start_time", str(datetime.now())))
            time_taken  = (datetime.now() - start_time).seconds
            record_win(len(answers), best_name, time_taken)
            stats = get_stats()
            return render_template(
                "answer.html",
                guess=f"🎉 Yes! It's {best_name}!",
                player_name=best_name, image_url=img,
                show_success=True, play_again=True,
                questions_count=len(answers), stats=stats,
            )

        elif action == "wrong":
            session["wrong_guesses"] = session.get("wrong_guesses", 0) + 1
            if session["wrong_guesses"] >= 3:
                record_loss(len(answers))
                return redirect(url_for("learn"))
            return redirect(url_for("question"))

    return render_template(
        "answer.html",
        guess=best_name, player_name=best_name, image_url=img,
        confidence=round(confidence, 1),
        candidates=candidates[:5],
        show_candidates=True, play_again=False,
    )


@app.route("/learn", methods=["GET", "POST"])
def learn():
    if request.method == "POST":
        name        = request.form.get("name", "").strip()
        image_url   = request.form.get("image_url", "/static/images/default.png").strip()
        description = request.form.get("description", "").strip()
        age_group   = request.form.get("age_group", "unknown")

        if not name:
            return render_template("learn.html", error="⚠️ Name is required.")
        if not description:
            return render_template("learn.html", error="📝 Please provide a brief description.")
        if has_profanity(name) or has_profanity(description):
            return render_template("learn.html", error="🚫 Please avoid inappropriate language.")

        user_know = load_json(KNOW_PATH, {})
        schema    = load_json(QUESTIONS_SCHEMA_PATH, {})
        raw       = dict(session.get("answers", []))
        enriched  = infer_metadata(raw, schema)
        auto_age  = extract_age_group(raw)

        user_know[name] = {
            "answers":     enriched,
            "age_group":   auto_age if auto_age != "unknown" else age_group,
            "image_url":   image_url,
            "description": description,
        }
        save_json(KNOW_PATH, user_know)
        return redirect(url_for("index"))

    return render_template("learn.html")

# ============================================================
#  API ROUTES
# ============================================================

@app.route("/api/stats")
def api_stats():
    return jsonify(get_stats())


@app.route("/api/achievements")
def api_achievements():
    unlocked = get_unlocked()
    return jsonify({
        "unlocked": unlocked,
        "all":      ALL_ACHIEVEMENTS,
    })


@app.route("/api/daily")
def api_daily():
    try:
        from daily_challenge import DailyChallenge
        return jsonify(DailyChallenge().get_challenge_status())
    except Exception as e:
        return jsonify({"error": str(e), "player": "Lionel Messi", "completed": False})


@app.route("/api/analytics")
def api_analytics():
    try:
        from analytics import GameAnalytics
        return jsonify(GameAnalytics().generate_insights_report())
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/api/leaderboard/<board_type>")
def api_leaderboard(board_type):
    try:
        from leaderboard import Leaderboard
        lb = Leaderboard()
        data = lb.get_global() if board_type == "global" else lb.get_weekly() if board_type == "weekly" else None
        if data is None:
            return jsonify({"error": "Invalid type"}), 400
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

# ============================================================
#  PAGE ROUTES
# ============================================================

@app.route("/achievements")
def achievements_page():
    stats    = get_stats()
    unlocked = get_unlocked()
    new_ach  = check_achievements(stats)
    return render_template("achievements.html",
                           achievements=unlocked,
                           all_achievements=ALL_ACHIEVEMENTS,
                           new_achievements=new_ach,
                           stats=stats)


@app.route("/daily")
def daily_challenge():
    try:
        from daily_challenge import DailyChallenge
        challenge = DailyChallenge().get_challenge_status()
    except Exception as e:
        challenge = {"error": str(e)}
    return render_template("daily.html", challenge=challenge)


@app.route("/leaderboard")
def leaderboard_page():
    try:
        from leaderboard import Leaderboard
        lb = Leaderboard()
        global_scores = lb.get_global()
        weekly_scores = lb.get_weekly()
    except Exception as e:
        global_scores = weekly_scores = []
    return render_template("leaderboard.html",
                           global_scores=global_scores,
                           weekly_scores=weekly_scores)


@app.route("/analytics")
def analytics_dashboard():
    try:
        from analytics import GameAnalytics
        report = GameAnalytics().generate_insights_report()
    except Exception as e:
        report = {"error": str(e)}
    return render_template("analytics.html", report=report)

# ============================================================
#  ENTRY POINT
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"✅ Muhfal running → http://0.0.0.0:{port}")
    app.run(debug=False, host="0.0.0.0", port=port)