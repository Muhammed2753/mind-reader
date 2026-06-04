import json
import os
import re

# -----------------------------
# Configuration
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_SCHEMA_PATH = os.path.join(BASE_DIR, "football_questions.json")
OUTPUT_PATH = QUESTIONS_SCHEMA_PATH  # Overwrite safely

# Continent-specific country groupings (FIXED)
COUNTRIES_BY_CONTINENT = {
    "europe": [
        "england", "spain", "germany", "france", "italy",
        "portugal", "netherlands", "belgium", "austria",
        "denmark", "sweden", "norway", "scotland", "switzerland",
        "czech republic", "croatia", "hungary", "republic of ireland", "wales",
        "russia", "ukraine", "greece", "poland", "serbia", "romania", "bulgaria",
        "finland", "iceland", "bosnia and herzegovina", "albania", "north macedonia",
        "montenegro", "kosovo", "luxembourg", "malta", "estonia", "latvia", "lithuania",
        "slovakia", "slovenia", "belarus", "cyprus", "israel"
    ],
    "south_america": [
        "brazil", "argentina", "colombia", "chile", "peru", "uruguay", "paraguay",
        "ecuador", "venezuela", "bolivia"
    ],
    "africa": [
        "nigeria", "egypt", "south africa", "algeria", "morocco", "ghana", "cameroon",
        "ivory coast", "senegal", "tunisia", "congo dr", "mali", "liberia", "gabon",
        "angola", "tanzania", "zambia", "uganda", "kenya", "ethiopia", "mozambique",
        "rwanda", "malawi", "burundi", "zimbabwe", "libya", "sudan"
    ],
    "asia": [
        "japan", "south korea", "china", "saudi arabia", "uae", "qatar", "india",
        "thailand", "uzbekistan", "iraq", "jordan", "kazakhstan", "malaysia", "vietnam",
        "indonesia", "philippines", "singapore", "iran", "kuwait", "bahrain", "oman",
        "yemen", "turkmenistan", "tajikistan", "kyrgyzstan", "north korea", "pakistan",
        "lebanon", "syria", "palestine", "nepal", "sri lanka", "bhutan", "maldives"
    ],
    "north_america": [
        "united states", "mexico", "canada", "costa rica", "jamaica", "honduras",
        "guatemala", "el salvador", "panama", "trinidad and tobago", "haiti", "cuba",
        "dominican republic", "nicaragua", "grenada", "saint vincent and the grenadines",
        "guyana", "suriname", "bermuda", "greenland", "aruba", "curaçao", "sint maarten", "bonaire"
    ],
    "oceania": [
        "australia", "new zealand", "papua new guinea", "fiji", "solomon islands",
        "vanuatu", "samoa", "tonga", "new caledonia", "french polynesia", "tokelau",
        "wallis and futuna", "american samoa", "guam", "northern mariana islands"
    ]
}

# League mapping (for club questions)
COUNTRY_TO_LEAGUE = {
    "england": "premier_league",
    "spain": "la_liga",
    "italy": "serie_a",
    "germany": "bundesliga",
    "france": "ligue_1",
    "netherlands": "erdivisie",
    "portugal": "primeira_liga",
    "belgium": "belgian_pro_league",
    "turkey": "turkish_super_lig",
    "scotland": "scottish_premiership",
    "brazil": "brasileirao",
    "argentina": "liga_profesional",
    "egypt": "egyptian_premier_league",
    "south africa": "south_african_premier_division",
    "saudi arabia": "saudi_pro_league",
    "japan": "j1_league",
    "united states": "mls",
    "australia": "a_league"
}

def normalize_key(s):
    return re.sub(r"[^\w]", "", s.lower())

def generate_retired_questions(role, questions_schema):
    new_questions = {}

    # Year questions
    new_questions[f"{role}_retired_year"] = [
        f"Did this {role} retire before 2000?",
        f"Did this {role} retire between 2000 and 2010?",
        f"Did this {role} retire between 2011 and 2020?",
        f"Did this {role} retire after 2020?"
    ]

    # Continent questions
    new_questions[f"{role}_retired_continent"] = [
        f"Did this {role} last {'play' if role == 'player' else 'manage' if role == 'manager' else 'associate'} in Europe before retiring?",
        f"Did this {role} last {'play' if role == 'player' else 'manage' if role == 'manager' else 'associate'} in South America before retiring?",
        f"Did this {role} last {'play' if role == 'player' else 'manage' if role == 'manager' else 'associate'} in Africa before retiring?",
        f"Did this {role} last {'play' if role == 'player' else 'manage' if role == 'manager' else 'associate'} in Asia before retiring?",
        f"Did this {role} last {'play' if role == 'player' else 'manage' if role == 'manager' else 'associate'} in North America before retiring?",
        f"Did this {role} last {'play' if role == 'player' else 'manage' if role == 'manager' else 'associate'} in Oceania before retiring?"
    ]

    # Country questions - ONE GROUP PER CONTINENT (FIXED)
    for continent, countries in COUNTRIES_BY_CONTINENT.items():
        country_questions = []
        for country in countries:
            action = "play" if role == "player" else "manage" if role == "manager" else "associate"
            country_questions.append(f"Did this {role} last {action} in {country.title()} before retiring?")
        new_questions[f"{role}_retired_country_{continent}"] = country_questions

    # League & Club questions
    for country, league_code in COUNTRY_TO_LEAGUE.items():
        league_name = " ".join(w.capitalize() for w in league_code.split("_"))
        new_questions[f"{role}_retired_league_{league_code}"] = [
            f"Did this {role} last {'play' if role == 'player' else 'manage' if role == 'manager' else 'associate'} in the {league_name} before retiring?"
        ]
        
        # Add club questions (reuse existing)
        club_key = f"{role}_club_{league_code}"
        if club_key in questions_schema:
            clubs = questions_schema[club_key]
            retired_clubs = []
            for q in clubs:
                if role == "player":
                    new_q = q.replace("Is this player playing for ", "Did this player last play for ").replace("?", " before retiring?")
                elif role == "manager":
                    new_q = q.replace("Is this manager managing at ", "Did this manager last manage at ").replace("?", " before retiring?")
                else:  # owner
                    new_q = q.replace("Is this owner associated with ", "Was this owner last associated with ").replace("?", " before stepping down?")
                retired_clubs.append(new_q)
            new_questions[f"{role}_retired_league_{league_code}"].extend(retired_clubs)

    return new_questions

def generate_deceased_questions(role):
    return {
        f"{role}_deceased_year": [
            f"Did this {role} pass away before 1980?",
            f"Did this {role} pass away between 1980 and 2000?",
            f"Did this {role} pass away after 2000?"
        ],
        f"{role}_deceased_era": [
            f"Was this {role} active in the 1950s or earlier?",
            f"Was this {role} active in the 1960s–1970s?",
            f"Was this {role} active in the 1980s–1990s?",
            f"Was this {role} active in the 2000s?"
        ]
    }

def generate_pundit_questions(role):
    if role == "owner":
        return {}
    return {
        f"{role}_pundit_network": [
            f"Is this pundit associated with BBC?",
            f"Is this pundit associated with Sky Sports?",
            f"Is this pundit associated with ESPN?",
            f"Is this pundit on beIN Sports?",
            f"Is this pundit on CBS Sports?"
        ],
        f"{role}_pundit_background": [
            f"Was this pundit a former international {role}?",
            f"Was this pundit a former top-flight {role}?"
        ]
    }

# -----------------------------
# Main Logic
# -----------------------------
def main():
    if not os.path.exists(QUESTIONS_SCHEMA_PATH):
        print(f"Error: {QUESTIONS_SCHEMA_PATH} not found!")
        return

    with open(QUESTIONS_SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)

    print("Generating status questions...")

    for role in ["player", "manager", "owner"]:
        # Add retired questions with proper continent grouping
        schema.update(generate_retired_questions(role, schema))
        # Add deceased questions
        schema.update(generate_deceased_questions(role))
        # Add pundit questions (skip for owners)
        if role != "owner":
            schema.update(generate_pundit_questions(role))

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)

    print(f"✅ Updated {QUESTIONS_SCHEMA_PATH} with proper continent-grouped status questions!")

if __name__ == "__main__":
    main()