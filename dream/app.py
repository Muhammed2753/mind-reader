import json
import os
import re
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from better_profanity import Profanity
from hints import HintSystem
from achievements import AchievementTracker, ACHIEVEMENTS
from daily_challenge import DailyChallenge
from leaderboard import Leaderboard
from api_routes import api
from game_stats import GameStats

profanity_checker = Profanity()
app = Flask(__name__)
app.secret_key = "Muhfal"
CORS(app)  # Enable CORS for mobile app
app.register_blueprint(api)

# Initialize systems
hint_system = HintSystem()
leaderboard = Leaderboard()
game_stats = GameStats()

# Define Big Teams globally
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
        "Is this player playing for Southampton?"
    ],
    "player_club_laliga": [
        "Is this player playing for Real Madrid?",
        "Is this player playing for Barcelona?",
        "Is this player playing for Atletico Madrid?",
        "Is this player playing for Real Sociedad?",
        "Is this player playing for Villarreal?",
        "Is this player playing for Athletic Club?",
        "Is this player playing for Real Betis?",
        "Is this player playing for Rayo Vallecano?",
        "Is this player playing for Osasuna?",
        "Is this player playing for Girona?",
        "Is this player playing for Sevilla?",
        "Is this player playing for Real Valladolid?",
        "Is this player playing for Las Palmas?",
        "Is this player playing for Celta Vigo?",
        "Is this player playing for Alaves?",
        "Is this player playing for Mallorca?",
        "Is this player playing for Real Oviedo?",
        "Is this player playing for Cadiz?",
        "Is this player playing for Espanol?",
        "Is this player playing for Elche?"
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
        "Is this player playing for Sampdoria?",
        "Is this player playing for Udinese?",
        "Is this player playing for Genoa?",
        "Is this player playing for Empoli?",
        "Is this player playing for Salernitana?",
        "Is this player playing for Sassuolo?",
        "Is this player playing for Cremonese?",
        "Is this player playing for Lecce?",
        "Is this player playing for Monza?",
        "Is this player playing for Verona?",
        "Is this player playing for Spezia?"
    ],
    "player_club_bundesliga": [
        "Is this player playing for Bayern Munich?",
        "Is this player playing for Borussia Dortmund?",
        "Is this player playing for RB Leipzig?",
        "Is this player playing for Bayer Leverkusen?",
        "Is this player playing for Union Berlin?",
        "Is this player playing for Freiburg?",
        "Is this player playing for Wolfsburg?",
        "Is this player playing for Mainz 05?",
        "Is this player playing for Borussia Monchengladbach?",
        "Is this player playing for Eintracht Frankfurt?",
        "Is this player playing for Augsburg?",
        "Is this player playing for VfB Stuttgart?",
        "Is this player playing for Hertha Berlin?",
        "Is this player playing for Cologne?",
        "Is this player playing for Hoffenheim?",
        "Is this player playing for Schalke 04?",
        "Is this player playing for Greuther Furth?",
        "Is this player playing for Bochum?",
        "Is this player playing for RB Salzburg?",
        "Is this player playing for St. Pauli?"
    ],
    "player_club_ligue_1": [
        "Is this player playing for Paris Saint-Germain?",
        "Is this player playing for Monaco?",
        "Is this player playing for Lille?",
        "Is this player playing for Lyon?",
        "Is this player playing for Marseille?",
        "Is this player playing for Lens?",
        "Is this player playing for Rennes?",
        "Is this player playing for Nice?",
        "Is this player playing for Lorient?",
        "Is this player playing for Auxerre?",
        "Is this player playing for Nantes?",
        "Is this player playing for Toulouse?",
        "Is this player playing for Clermont Foot?",
        "Is this player playing for Strasbourg?",
        "Is this player playing for Brest?",
        "Is this player playing for Reims?",
        "Is this player playing for Montpellier?",
        "Is this player playing for Troyes?",
        "Is this player playing for Angers?",
        "Is this player playing for Metz?"
    ]
}

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
# Cache for JSON files
# -----------------------------
_JSON_CACHE = {}
_CACHE_TIMESTAMPS = {}

def load_json_file(path, default):
    if not os.path.exists(path):
        return default
    try:
        mtime = os.path.getmtime(path)
        if path in _JSON_CACHE and _CACHE_TIMESTAMPS.get(path) == mtime:
            return _JSON_CACHE[path]
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        _JSON_CACHE[path] = data
        _CACHE_TIMESTAMPS[path] = mtime
        return data
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return default

def save_json_file(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving {path}: {e}")

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

def normalize_key(q):
    return re.sub(r"[^\w]", "", q.lower().strip())

def normalize_continent_name(continent_str):
    return continent_str.strip().lower().replace(" ", "_").replace("-", "_")
# Global in-memory index (rebuild when KNOW_PATH or CHARACTERS_PATH changes)
QUESTION_TO_NAMES = {}
# -----------------------------
# Profanity Filter
# -----------------------------
PROFANITY_WORDS = {
    "fuck", "shit", "bitch", "asshole", "dick", "piss", "cunt", "slut",
    "whore", "nigga", "nigger", "fag", "faggot", "cock", "twat", "crap",
    "arse", "bollocks", "wanker", "prick", "douche", "motherfucker",
    "bastard", "damn", "hell", "sucker", "retard", "idiot", "mad", "moron"
}

def contains_profanity(text):
    if not text:
        return False
    # Normalize: lowercase + remove punctuation
    clean = re.sub(r"[^\w\s]", "", text.lower())
    words = set(clean.split())
    return bool(words & PROFANITY_WORDS)
def build_question_index(all_characters):
    global QUESTION_TO_NAMES
    QUESTION_TO_NAMES = {}
    for name, data in all_characters.items():
        for q, ans in data.get("answers", {}).items():
            if ans == "yes":
                norm_q = normalize_key(q)
                if norm_q not in QUESTION_TO_NAMES:
                    QUESTION_TO_NAMES[norm_q] = set()
                QUESTION_TO_NAMES[norm_q].add(name)
def extract_age_group(answers_dict):
    if answers_dict.get("Is this player under 18 years old?") == "yes":
        return "under_18"
    elif answers_dict.get("Is this player between 18 and 23 years old?") == "yes":
        return "18_23"
    elif answers_dict.get("Is this player between 23 and 35 years old?") == "yes":
        return "23_35"
    elif answers_dict.get("Is this player over 35 years old?") == "yes":
        return "over_35"
    else:
        return "unknown"

def infer_missing_metadata(answers_dict, questions_schema):
    enriched = answers_dict.copy()
    if answers_dict.get("Is this player under 18 years old?") == "yes":
        enriched["age_group"] = "under_18"
    elif answers_dict.get("Is this player between 18 and 23 years old?") == "yes":
        enriched["age_group"] = "18_23"
    elif answers_dict.get("Is this player between 23 and 35 years old?") == "yes":
        enriched["age_group"] = "23_35"
    elif answers_dict.get("Is this player over 35 years old?") == "yes":
        enriched["age_group"] = "over_35"
    country_to_continent = {
        "england": "europe", "spain": "europe", "italy": "europe",
        "germany": "europe", "france": "europe", "brazil": "south_america",
        "argentina": "south_america", "usa": "north_america", "canada": "north_america",
        "saudi arabia": "asia", "japan": "asia", "south korea": "asia",
        "egypt": "africa", "senegal": "africa", "nigeria": "africa",
        "australia": "oceania"
    }

    role = "player"
    if any("manager" in q.lower() for q in answers_dict if answers_dict[q] == "yes"):
        role = "manager"
    elif any("owner" in q.lower() for q in answers_dict if answers_dict[q] == "yes"):
        role = "owner"

    for q, ans in answers_dict.items():
        if ans == "yes" and "born in" in q:
            match = re.search(r"born in ([a-zA-Z\s]+)\?", q)
            if match:
                country = normalize_continent_name(match.group(1))
                continent = country_to_continent.get(country, "unknown")
                enriched[f"Is this {role} birthplace in {continent.title()}?"] = "yes"
                break

    for q, ans in answers_dict.items():
        if ans == "yes" and "playing in" in q:
            match = re.search(r"playing in ([a-zA-Z\s]+)\?", q)
            if match:
                country = normalize_continent_name(match.group(1))
                continent = country_to_continent.get(country, "unknown")
                enriched[f"Is this {role} playing in {continent.title()}?"] = "yes"
                league_map = {
                    "england": "Is this player playing in the Premier League?",
                    "spain": "Is this player playing in La Liga?",
                    "italy": "Is this player playing in Serie A?",
                    "germany": "Is this player playing in the Bundesliga?",
                    "france": "Is this player playing in Ligue 1?",
                    "saudi arabia": "Is this player playing in the Saudi Pro League?",
                    "usa": "Is this player playing in MLS?"
                }
                if country in league_map:
                    enriched[league_map[country]] = "yes"
                break
    return enriched

def filter_candidates(answers_list, all_characters):
    if not answers_list:
        return [(name, data, 0) for name, data in list(all_characters.items())[:50]]

    user_age_group = None
    if answers_list:
        user_age_group = extract_age_group(dict(answers_list))

    answers_dict = dict(answers_list)
    remaining = list(all_characters.items())
    for name, data in remaining[:]:
        char_answers = data.get("answers", {})
        eliminated = False

        # PLAYER STATUS
        if answers_dict.get("Is this player currently active?") == "yes":
            if char_answers.get("Is this player currently active?") != "yes":
                eliminated = True
        if answers_dict.get("Is this player retired?") == "yes":
            if char_answers.get("Is this player currently active?") == "yes":
                eliminated = True
        if answers_dict.get("Is this player deceased?") == "yes":
            if char_answers.get("Is this player currently active?") == "yes" or char_answers.get("Is this player retired?") == "yes":
                eliminated = True
        if answers_dict.get("Has this player become a pundit or media personality?") == "yes":
            # Pundits are usually retired, but may not be deceased
            if char_answers.get("Is this player currently active?") == "yes":
                eliminated = True

        # MANAGER STATUS
        if answers_dict.get("Is this manager currently active?") == "yes":
            if char_answers.get("Is this manager currently active?") != "yes":
                eliminated = True
        if answers_dict.get("Has this manager retired?") == "yes":
            if char_answers.get("Is this manager currently active?") == "yes":
                eliminated = True
        if answers_dict.get("Is this manager deceased?") == "yes":
            if char_answers.get("Is this manager currently active?") == "yes" or char_answers.get("Has this manager retired?") == "yes":
                eliminated = True
        if answers_dict.get("Has this manager become a pundit or TV analyst?") == "yes":
            if char_answers.get("Is this manager currently active?") == "yes":
                eliminated = True

        # OWNER STATUS
        if answers_dict.get("Is this owner currently active?") == "yes":
            if char_answers.get("Is this owner currently active?") != "yes":
                eliminated = True
        if answers_dict.get("Has this owner stepped down?") == "yes":
            if char_answers.get("Is this owner currently active?") == "yes":
                eliminated = True
        if answers_dict.get("Is this owner deceased?") == "yes":
            if char_answers.get("Is this owner currently active?") == "yes" or char_answers.get("Has this owner stepped down?") == "yes":
                eliminated = True

        if eliminated:
            remaining.remove((name, data))

    for question, user_answer in answers_list:
        norm_q = normalize_key(question)
        new_remaining = []
        for name, data in remaining:
            if user_age_group and user_age_group != "unknown":
                char_age = data.get("age_group", "unknown")
                if char_age != "unknown" and char_age != user_age_group:
                    continue

            char_answers = data.get("answers", {})
            matched = False
            keep = False
            for cq, ca in char_answers.items():
                if normalize_key(cq) == norm_q:
                    matched = True
                    keep = (ca == "yes" and user_answer == "yes") or (ca == "no" and user_answer == "no")
                    break
            if not matched:
                keep = (user_answer != "yes")
            if keep:
                new_remaining.append((name, data))
        remaining = new_remaining
        if not remaining:
            return []

    yes_count = sum(1 for _, a in answers_list if a == "yes")
    scored = []
    for name, data in remaining:
        score = 0
        for q, ua in answers_list:
            if ua == "yes":
                norm_q = normalize_key(q)
                for cq, ca in data.get("answers", {}).items():
                    if normalize_key(cq) == norm_q and ca == "yes":
                        score += 1
                        break
        conf = (score / max(1, yes_count)) * 100 if yes_count > 0 else 50
        scored.append((name, data, round(conf, 1)))
    scored.sort(key=lambda x: x[2], reverse=True)
    return scored[:50]
def get_active_questions(questions_schema, all_characters, answers_list, role, question_group_key):
    base_questions = questions_schema.get(question_group_key, [])
    if not base_questions:
        return []

    candidate_names = {name for name, _, _ in filter_candidates(answers_list, all_characters)}
    if not candidate_names:
        return []

    active_questions = []
    for q in base_questions:
        norm_q = normalize_key(q)
        names_with_q = QUESTION_TO_NAMES.get(norm_q, set())
        if names_with_q & candidate_names:
            active_questions.append(q)

    return active_questions
def get_next_question(answers_list, asked_set, questions_schema, all_characters):
    answers_dict = dict(answers_list)

    # --- 1. ROLE ---
    role = None
    role_questions = questions_schema.get("role", [])
    for q in role_questions:
        if answers_dict.get(q) == "yes":
            if "player" in q.lower(): 
                role = "player"
            elif "manager" in q.lower(): 
                role = "manager"
            elif "owner" in q.lower(): 
                role = "owner"
            break
    
    if not role:
        unasked = [q for q in role_questions if q not in answers_dict]
        if unasked:
            return random.choice(unasked)
        return {"type": "dead_end", "message": "Role unclear."}

    # --- 2. STATUS ---
    status_key = f"{role}_status"
    status_questions = questions_schema.get(status_key, [])
    if status_questions:
        if not any(answers_dict.get(q) == "yes" for q in status_questions):
            unasked = [q for q in status_questions if q not in answers_dict]
            if unasked:
                return random.choice(unasked)
    
    # --- 3. DETERMINE SPECIFIC STATUS (WORKS FOR ALL ROLES) ---
    status = None
    
    # ACTIVE status
    if (answers_dict.get("Is this player currently active?") == "yes" or
        answers_dict.get("Is this manager currently active?") == "yes" or
        answers_dict.get("Is this owner currently active?") == "yes"):
        status = "active"
    
    # RETIRED status
    elif (answers_dict.get("Has this player retired?") == "yes" or
          answers_dict.get("Has this manager retired?") == "yes" or
          answers_dict.get("Has this owner stepped down?") == "yes"):
        status = "retired"
    
    # DECEASED status
    elif (answers_dict.get("Is this player deceased?") == "yes" or
          answers_dict.get("Is this manager deceased?") == "yes" or
          answers_dict.get("Is this owner deceased?") == "yes"):
        status = "deceased"
    
    # PUNDIT status (only for players/managers)
    elif (answers_dict.get("Has this player become a pundit?") == "yes" or
          answers_dict.get("Has this manager become a pundit?") == "yes"):
        status = "pundit"

    # --- 4. BRANCH BASED ON STATUS ---
    if status == "retired":
        # RETIRED PATH: Ask last active context for ANY role
        retired_continent_key = f"{role}_retired_continent"
        retired_continent_qs = get_active_questions(questions_schema, all_characters, answers_list, role, retired_continent_key)
        if not any(answers_dict.get(q) == "yes" for q in retired_continent_qs):
            unasked = [q for q in retired_continent_qs if q not in answers_dict]
            if unasked:
                return random.choice(unasked)

        # Infer retired continent
        retired_continent = None
        for q in retired_continent_qs:
            if answers_dict.get(q) == "yes":
                match = re.search(r"Did this .* last .* in ([a-zA-Z\s]+) before retiring\?", q, re.IGNORECASE)
                if match:
                    retired_continent = normalize_continent_name(match.group(1))
                    break

        if retired_continent:
            # Retired country (continent-specific)
            retired_country_key = f"{role}_retired_country_{retired_continent}"
            retired_country_qs = get_active_questions(questions_schema, all_characters, answers_list, role, retired_country_key)
            if not any(answers_dict.get(q) == "yes" for q in retired_country_qs):
                for q in retired_country_qs:
                    if q not in answers_dict:
                        return q

            # Infer retired country
            retired_country = None
            for q in retired_country_qs:
                if answers_dict.get(q) == "yes":
                    match = re.search(r"Did this .* last .* in ([a-zA-Z\s]+) before retiring\?", q, re.IGNORECASE)
                    if match:
                        retired_country = normalize_continent_name(match.group(1))
                        break

            if retired_country:
                # Retired league & club
                country_to_league = {
                    "england": "premier_league", "spain": "la_liga", "italy": "serie_a",
                    "germany": "bundesliga", "france": "ligue_1", "saudi arabia": "saudi_pro_league",
                    "usa": "mls", "brazil": "brasileirao", "argentina": "liga_profesional",
                    "netherlands": "erdivisie", "portugal": "primeira_liga", "belgium": "belgian_pro_league",
                    "turkey": "turkish_super_lig", "scotland": "scottish_premiership",
                    "egypt": "egyptian_premier_league", "south africa": "south_african_premier_division"
                }
                league_code = country_to_league.get(retired_country)
                if league_code:
                    retired_league_key = f"{role}_retired_league_{league_code}"
                    retired_league_qs = get_active_questions(questions_schema, all_characters, answers_list, role, retired_league_key)
                    if not any(answers_dict.get(q) == "yes" for q in retired_league_qs):
                        unasked = [q for q in retired_league_qs if q not in answers_dict]
                        if unasked:
                            return random.choice(unasked)

        # Retired year
        retired_year_qs = questions_schema.get(f"{role}_retired_year", [])
        if not any(answers_dict.get(q) == "yes" for q in retired_year_qs):
            unasked = [q for q in retired_year_qs if q not in answers_dict]
            if unasked:
                return random.choice(unasked)

        # Fall through to attributes
        pass

    elif status == "deceased":
        # DECEASED PATH: Works for all roles
        deceased_year_qs = questions_schema.get(f"{role}_deceased_year", [])
        if not any(answers_dict.get(q) == "yes" for q in deceased_year_qs):
            unasked = [q for q in deceased_year_qs if q not in answers_dict]
            if unasked:
                return random.choice(unasked)

        deceased_era_qs = questions_schema.get(f"{role}_deceased_era", [])
        if not any(answers_dict.get(q) == "yes" for q in deceased_era_qs):
            unasked = [q for q in deceased_era_qs if q not in answers_dict]
            if unasked:
                return random.choice(unasked)

        # Fall through to attributes
        pass

    elif status == "pundit" and role != "owner":
        # PUNDIT PATH: Only for players and managers
        pundit_network_qs = questions_schema.get(f"{role}_pundit_network", [])
        if not any(answers_dict.get(q) == "yes" for q in pundit_network_qs):
            unasked = [q for q in pundit_network_qs if q not in answers_dict]
            if unasked:
                return random.choice(unasked)

        pundit_bg_qs = questions_schema.get(f"{role}_pundit_background", [])
        if not any(answers_dict.get(q) == "yes" for q in pundit_bg_qs):
            unasked = [q for q in pundit_bg_qs if q not in answers_dict]
            if unasked:
                return random.choice(unasked)

        # Fall through to attributes
        pass

    # --- 5. ACTIVE PATH ---
    if status == "active":
        if role == "manager":
            # === MANAGER-SPECIFIC FLOW ===

            # 1. Birth Continent
            birth_continent = None
            birth_cont_qs = get_active_questions(questions_schema, all_characters, answers_list, role, "manager_birth_continent")
            for q in birth_cont_qs:
                if answers_dict.get(q) == "yes":
                    match = re.search(r"birthplace in ([a-zA-Z\s]+)\?", q, re.IGNORECASE)
                    if match:
                        birth_continent = normalize_continent_name(match.group(1))
                        break
            if not birth_continent:
                unasked = [q for q in birth_cont_qs if q not in answers_dict]
                if unasked:
                    return random.choice(unasked)

            # 2. Birth Country
            if birth_continent:
                birth_country_key = f"manager_birth_country_{birth_continent}"
                birth_country_qs = get_active_questions(questions_schema, all_characters, answers_list, role, birth_country_key)
                for q in birth_country_qs:
                    if answers_dict.get(q) == "yes":
                        break
                else:
                    unasked = [q for q in birth_country_qs if q not in answers_dict]
                    if unasked:
                        return random.choice(unasked)

            # 3. Club vs National Team?
            role_type_qs = questions_schema.get("manager_role_type", [])
            if not any(answers_dict.get(q) == "yes" for q in role_type_qs):
                unasked = [q for q in role_type_qs if q not in answers_dict]
                if unasked:
                    return random.choice(unasked)

            # 4a. National Team Path
            if answers_dict.get("Is this manager currently managing a national team?") == "yes":
                nat_continent = None
                nat_cont_qs = get_active_questions(questions_schema, all_characters, answers_list, role, "manager_national_team_continent")
                for q in nat_cont_qs:
                    if answers_dict.get(q) == "yes":
                        match = re.search(r"managing a national team from ([a-zA-Z\s]+)\?", q, re.IGNORECASE)
                        if match:
                            nat_continent = normalize_continent_name(match.group(1))
                            break
                if not nat_continent:
                    unasked = [q for q in nat_cont_qs if q not in answers_dict]
                    if unasked:
                        return random.choice(unasked)
                
                # National Team Country
                if nat_continent:
                    nat_country_key = f"manager_national_team_country_{nat_continent}"
                    nat_country_qs = get_active_questions(questions_schema, all_characters, answers_list, role, nat_country_key)
                    for q in nat_country_qs:
                        if answers_dict.get(q) == "yes":
                            break
                    else:
                        unasked = [q for q in nat_country_qs if q not in answers_dict]
                        if unasked:
                            return random.choice(unasked)

            # 4b. Club Manager Path
            elif answers_dict.get("Is this manager currently managing a club team?") == "yes":
                # Work continent
                work_continent = None
                work_continent_key = "manager_league_continent"
                active_work_cont_qs = get_active_questions(questions_schema, all_characters, answers_list, role, work_continent_key)
                for q in active_work_cont_qs:
                    if answers_dict.get(q) == "yes":
                        match = re.search(r"is this manager managing in ([a-zA-Z\s]+)\?", q, re.IGNORECASE)
                        if match:
                            work_continent = normalize_continent_name(match.group(1))
                            break
                if not work_continent:
                    unasked = [q for q in active_work_cont_qs if q not in answers_dict]
                    if unasked:
                        return random.choice(unasked)

                # Work country
                if work_continent:
                    work_country_key = f"manager_league_country_{work_continent}"
                    active_work_country_qs = get_active_questions(questions_schema, all_characters, answers_list, role, work_country_key)
                    for q in active_work_country_qs:
                        if answers_dict.get(q) == "yes":
                            match = re.search(r"is this manager managing in ([a-zA-Z\s]+)\?", q, re.IGNORECASE)
                            if match:
                                work_country = normalize_continent_name(match.group(1))
                                break
                    else:
                        unasked = [q for q in active_work_country_qs if q not in answers_dict]
                        if unasked:
                            return random.choice(unasked)

                    # League
                    country_to_league = {
                        "england": "premier_league", "spain": "la_liga", "italy": "serie_a",
                        "germany": "bundesliga", "france": "ligue_1", "saudi arabia": "saudi_pro_league",
                        "usa": "mls", "brazil": "brasileirao", "argentina": "liga_profesional"
                    }
                    league_code = country_to_league.get(work_country)
                    if league_code:
                        league_key = f"manager_league_{league_code}"
                        active_league_qs = get_active_questions(questions_schema, all_characters, answers_list, role, league_key)
                        if not any(answers_dict.get(q) == "yes" for q in active_league_qs):
                            unasked = [q for q in active_league_qs if q not in answers_dict]
                            if unasked:
                                return random.choice(unasked)

                        # Club
                        club_key = f"manager_club_{league_code}"
                        active_club_qs = get_active_questions(questions_schema, all_characters, answers_list, role, club_key)
                        if active_club_qs:
                            if not any(answers_dict.get(q) == "yes" for q in active_club_qs):
                                big_teams = BIG_TEAMS.get(club_key, [])
                                for q in big_teams:
                                    if q in active_club_qs and q not in answers_dict:
                                        return q
                                for q in active_club_qs:
                                    if q not in answers_dict:
                                        return q

        elif role == "player":
            # === PLAYER FLOW (unchanged) ===
            origin_continent = None
            origin_continent_key = "player_continent"
            active_origin_cont_qs = get_active_questions(questions_schema, all_characters, answers_list, role, origin_continent_key)
            for q in active_origin_cont_qs:
                if answers_dict.get(q) == "yes":
                    match = re.search(r"(?:birthplace in|from)\s+([a-zA-Z\s]+)\?", q, re.IGNORECASE)
                    if match:
                        origin_continent = normalize_continent_name(match.group(1))
                        break
            if not origin_continent:
                unasked = [q for q in active_origin_cont_qs if q not in answers_dict]
                if unasked:
                    return random.choice(unasked)
                return {"type": "dead_end", "message": "No valid origin continent."}

            # Origin country
            origin_country_key = f"player_country_{origin_continent}"
            active_origin_country_qs = get_active_questions(questions_schema, all_characters, answers_list, role, origin_country_key)
            if active_origin_country_qs:
                if not any(answers_dict.get(q) == "yes" for q in active_origin_country_qs):
                    for q in active_origin_country_qs:
                        if q not in answers_dict:
                            return q

            # Work continent
            work_continent = None
            work_continent_key = "player_league_continent"
            active_work_cont_qs = get_active_questions(questions_schema, all_characters, answers_list, role, work_continent_key)
            for q in active_work_cont_qs:
                if answers_dict.get(q) == "yes":
                    match = re.search(rf"is this {role} playing in ([a-zA-Z\s]+)\?", q, re.IGNORECASE)
                    if match:
                        work_continent = normalize_continent_name(match.group(1))
                        break
            if not work_continent:
                unasked = [q for q in active_work_cont_qs if q not in answers_dict]
                if unasked:
                    return random.choice(unasked)
                return {"type": "dead_end", "message": "Work continent not found."}

            # Work country
            work_country = None
            work_country_key = f"player_league_country_{work_continent}"
            active_work_country_qs = get_active_questions(questions_schema, all_characters, answers_list, role, work_country_key)
            if active_work_country_qs:
                for q in active_work_country_qs:
                    if answers_dict.get(q) == "yes":
                        match = re.search(rf"is this {role} playing in ([a-zA-Z\s]+)\?", q, re.IGNORECASE)
                        if match:
                            work_country = normalize_continent_name(match.group(1))
                            break
                if not work_country:
                    for q in active_work_country_qs:
                        if q not in answers_dict:
                            return q
                    return {"type": "dead_end", "message": f"No {role} in any country in this continent."}

            # League
            if work_country:
                country_to_league = {
                    "england": "premier_league", "spain": "la_liga", "italy": "serie_a",
                    "germany": "bundesliga", "france": "ligue_1", "saudi arabia": "saudi_pro_league",
                    "usa": "mls", "brazil": "brasileirao", "argentina": "liga_profesional"
                }
                league_code = country_to_league.get(work_country)
                if league_code:
                    league_key = f"player_league_{league_code}"
                    active_league_qs = get_active_questions(questions_schema, all_characters, answers_list, role, league_key)
                    if not any(answers_dict.get(q) == "yes" for q in active_league_qs):
                        unasked = [q for q in active_league_qs if q not in answers_dict]
                        if unasked:
                            return random.choice(unasked)

            # Club
            if league_code:
                club_key = f"player_club_{league_code}"
                active_club_qs = get_active_questions(questions_schema, all_characters, answers_list, role, club_key)
                if active_club_qs:
                    if not any(answers_dict.get(q) == "yes" for q in active_club_qs):
                        big_teams = BIG_TEAMS.get(club_key, [])
                        for q in big_teams:
                            if q in active_club_qs and q not in answers_dict:
                                return q
                        for q in active_club_qs:
                            if q not in answers_dict:
                                return q

        elif role == "owner":
            # === OWNER FLOW (unchanged minimal) ===
            origin_continent = None
            origin_continent_key = "owner_continent"
            active_origin_cont_qs = get_active_questions(questions_schema, all_characters, answers_list, role, origin_continent_key)
            for q in active_origin_cont_qs:
                if answers_dict.get(q) == "yes":
                    match = re.search(r"(?:birthplace in|from)\s+([a-zA-Z\s]+)\?", q, re.IGNORECASE)
                    if match:
                        origin_continent = normalize_continent_name(match.group(1))
                        break
            if not origin_continent:
                unasked = [q for q in active_origin_cont_qs if q not in answers_dict]
                if unasked:
                    return random.choice(unasked)

            origin_country_key = f"owner_country_{origin_continent}"
            active_origin_country_qs = get_active_questions(questions_schema, all_characters, answers_list, role, origin_country_key)
            if active_origin_country_qs:
                if not any(answers_dict.get(q) == "yes" for q in active_origin_country_qs):
                    for q in active_origin_country_qs:
                        if q not in answers_dict:
                            return q

            work_continent_key = "owner_league_continent"
            active_work_cont_qs = get_active_questions(questions_schema, all_characters, answers_list, role, work_continent_key)
            if active_work_cont_qs:
                if not any(answers_dict.get(q) == "yes" for q in active_work_cont_qs):
                    for q in active_work_cont_qs:
                        if q not in answers_dict:
                            return q

    # --- 6. ATTRIBUTES (for all statuses) ---
    if role == "player":
        candidates = filter_candidates(answers_list, all_characters)
        current_positions = set()
        for _, data, _ in candidates:
            for q, ans in data.get("answers", {}).items():
                if ans == "yes":
                    if "goalkeeper" in q.lower() and "position" in q.lower():
                        current_positions.add("goalkeeper")
                    elif "position" in q.lower():
                        match = re.search(r"natural position a ([\w\s]+)\?", q)
                        if match:
                            pos = match.group(1).strip().lower().replace(" ", "_")
                            current_positions.add(pos)

        position_questions = questions_schema.get("player_position", [])
        active_position_qs = []
        for q in position_questions:
            if "goalkeeper" in q.lower():
                if "goalkeeper" in current_positions:
                    active_position_qs.append(q)
            else:
                match = re.search(r"natural position a ([\w\s]+)\?", q)
                if match:
                    pos = match.group(1).strip().lower().replace(" ", "_")
                    if pos in current_positions:
                        active_position_qs.append(q)

        if active_position_qs:
            if not any(answers_dict.get(q) == "yes" for q in active_position_qs):
                unasked = [q for q in active_position_qs if q not in answers_dict]
                if unasked:
                    return random.choice(unasked)

        other_player_groups = []
        is_gk = "goalkeeper" in current_positions
        other_player_groups.extend(["player_status", "player_age"])
        other_player_groups.append("player_honors_goalkeeper" if is_gk else "player_honors_outfield")
        
        for group in other_player_groups:
            active_attr_qs = get_active_questions(questions_schema, all_characters, answers_list, role, group)
            if active_attr_qs:
                if not any(answers_dict.get(q) == "yes" for q in active_attr_qs):
                    unasked = [q for q in active_attr_qs if q not in answers_dict]
                    if unasked:
                        return random.choice(unasked)

    elif role == "manager":
        final_groups = ["manager_status", "manager_era", "manager_playing_career", "manager_tactics", "manager_formation", "manager_honors"]
        for group in final_groups:
            active_attr_qs = get_active_questions(questions_schema, all_characters, answers_list, role, group)
            if active_attr_qs:
                if not any(answers_dict.get(q) == "yes" for q in active_attr_qs):
                    unasked = [q for q in active_attr_qs if q not in answers_dict]
                    if unasked:
                        return random.choice(unasked)

    elif role == "owner":
        final_groups = ["owner_status", "owner_profile"]
        for group in final_groups:
            active_attr_qs = get_active_questions(questions_schema, all_characters, answers_list, role, group)
            if active_attr_qs:
                if not any(answers_dict.get(q) == "yes" for q in active_attr_qs):
                    unasked = [q for q in active_attr_qs if q not in answers_dict]
                    if unasked:
                        return random.choice(unasked)

    return None    # -----------------------------
# Flask Routes
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")
 
@app.route("/start", methods=["POST"])
def start():
    difficulty = request.form.get("difficulty", "medium")
    session.clear()
    session["answers"] = []
    session["wrong_guesses"] = 0
    session["difficulty"] = difficulty
    session["game_start_time"] = str(datetime.now())
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
    
    global QUESTION_TO_NAMES
    if not QUESTION_TO_NAMES:
        build_question_index(all_chars)
    
    questions_schema = load_json_file(QUESTIONS_SCHEMA_PATH, {})
    if "role" not in questions_schema:
        questions_schema["role"] = [
            "Is this person a football player?",
            "Is this person a football manager?",
            "Is this person a football club owner or executive?"
        ]

    candidates = filter_candidates(answers, all_chars)
    next_q = get_next_question(answers, set(), questions_schema, all_chars)

    if not candidates:
        return render_template("answer.html", guess="I don't know this person.", image_url="/static/images/default.png", play_again=True, is_no_match=True)
    if isinstance(next_q, dict) and next_q.get("type") == "dead_end":
        return render_template("answer.html", guess=next_q["message"], image_url="/static/images/default.png", play_again=True, is_no_match=True)

    if (not next_q and len(answers) >= 4) or len(answers) >= 150 or len(candidates) == 1:
        return redirect(url_for("answer"))

    session["current_question"] = next_q
    progress = min(95, len(answers) * 3)
    matches_text = "match" if len(candidates) == 1 else "matches"
    current_thinking_of = candidates[0][0] if candidates else ""

    return render_template(
        "question.html",
        question=next_q,
        progress=progress,
        candidates_count=len(candidates),
        question_number=len(answers) + 1,
        current_thinking_of=current_thinking_of,
        matches_text=matches_text,
        answers=answers
    )

@app.route("/undo", methods=["POST"])
def undo():
    answers = session.get("answers", [])
    if answers:
        answers.pop()
        session["answers"] = answers
        
        # ✅ CORRECT: Only 2 arguments per pop()
        session.pop("auto_jump", None)
        session.pop("final_guess_mode", None)
        session.pop("excluded_names", None)
        session.pop("previous_question", None)
        session.pop("previous_answer", None)
        
        session["wrong_guesses"] = 0  # reset to avoid premature "learn"
    return redirect(url_for("question"))

@app.route("/answer", methods=["GET", "POST"])
def answer():
    answers = session.get("answers", [])
    base_chars = load_json_file(CHARACTERS_PATH, {})
    user_know = load_json_file(KNOW_PATH, {})
    all_chars = {**base_chars, **user_know}
    candidates = filter_candidates(answers, all_chars)
    if not candidates:
        game_stats.record_loss(len(answers))
        return render_template("answer.html", guess="I give up — I don't know!", image_url="/static/images/default.png", play_again=True, is_no_match=True)
    best_name, best_data, confidence = candidates[0]
    img = best_data.get("image_url", "/static/images/default.png")
    if request.method == "POST":
        action = request.form.get("action")
        if action == "correct":
            start_time = datetime.fromisoformat(session.get("game_start_time", str(datetime.now())))
            time_taken = (datetime.now() - start_time).seconds
            game_stats.record_win(len(answers), best_name, time_taken)
            stats = game_stats.get_stats()
            return render_template("answer.html", guess=f"Yes! It's {best_name}!", show_success=True, play_again=True, player_name=best_name, image_url=img, questions_count=len(answers), stats=stats)
        elif action == "wrong":
            session["wrong_guesses"] = session.get("wrong_guesses", 0) + 1
            if session["wrong_guesses"] >= 3:
                return redirect(url_for("learn"))
            return redirect(url_for("question"))
    return render_template(
        "answer.html",
        guess=best_name,
        image_url=img,
        confidence=round(confidence, 1),
        candidates=candidates[:5],
        show_candidates=True,
        play_again=False
    )

@app.route("/learn", methods=["GET", "POST"])
def learn():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        image_url = request.form.get("image_url", "/static/images/default.png").strip()
        description = request.form.get("description", "").strip()
        age_group = request.form.get("age_group", "unknown")

        if not name:
            return render_template("learn.html", error="Name is required.")
        
        if not description:
            return render_template("learn.html", error="Description is required.")
        
        if contains_profanity(name) or contains_profanity(description):
            return render_template("learn.html", error="Invalid input: Please avoid inappropriate language.")

        user_know = load_json_file(KNOW_PATH, {})
        questions_schema = load_json_file(QUESTIONS_SCHEMA_PATH, {})
        raw_answers = dict(session.get("answers", []))
        enriched_answers = infer_missing_metadata(raw_answers, questions_schema)
        auto_age = extract_age_group(raw_answers)
        final_age = auto_age if auto_age != "unknown" else age_group

        user_know[name] = {
            "answers": enriched_answers,
            "age_group": final_age,
            "image_url": image_url,
            "description": description
        }
        save_json_file(KNOW_PATH, user_know)
        return redirect(url_for("index"))

    return render_template("learn.html")
if __name__ == "__main__":
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"✅ Muhfal running on:")
    print(f"   Local: http://localhost:5000")
    print(f"   Network: http://{local_ip}:5000")
    print(f"   Access from phone: http://{local_ip}:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)

@app.route("/stats")
def stats():
    return jsonify(game_stats.get_stats())