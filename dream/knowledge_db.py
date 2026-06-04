import json
import os
import re

# -----------------------------
# Configuration
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_SCHEMA_PATH = os.path.join(BASE_DIR, "football_questions.json")
OUTPUT_PATH = QUESTIONS_SCHEMA_PATH

# Continent → Countries (from your data)
COUNTRIES_BY_CONTINENT = {
    "europe": [
        "england", "spain", "germany", "france", "italy", "portugal", "netherlands",
        "belgium", "austria", "denmark", "sweden", "norway", "scotland", "switzerland",
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
            # Europe
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
        "switzerland": "swiss_super_league",
        "ukraine": "ukrainian_premier_league",
        "greece": "greek_super_league",
        "austria": "austrian_bundesliga",
        "denmark": "danish_superliga",
        "sweden": "swedish_allsvenskan",
        "norway": "norwegian_eliteserien",
        "czech republic": "czech_first_league",
        "poland": "polish_ekstraklasa",
        "serbia": "serbian_superliga",
        "croatia": "croatian_first_league",
        "hungary": "hungarian_nb_i",
        "slovakia": "slovakia_super_league",
        "slovenia": "slovenia_prva_liga",
        "romania": "romania_liga_i",
        "belarus": "belarus_vysshaya_liga",
        "finland": "finnish_veikkausliiga",
        "russia": "russian_premier_league",
        "bulgaria": "bulgarian_first_league",
        "cyprus": "cypriot_first_division",
        "israel": "israel_premier_league",

        # South America
        "brazil": "brasileirao",
        "argentina": "liga_profesional",
        "colombia": "categoría_primera_a",
        "chile": "primera_división_chile",
        "peru": "liga_1",
        "uruguay": "primera_división_uruguaya",
        "paraguay": "primera_división_paraguaya",
        "ecuador": "serie_a_ecuador",
        "venezuela": "primera_división_venezolana",
        "bolivia": "división_profesional",
        
        # Africa
        "egypt": "egyptian_premier_league",
        "south africa": "south_african_premier_division",
        "tunisia": "tunisian_ligue_1",
        "algeria": "algerian_ligue_1",
        "morocco": "moroccan_botola_pro",
        "nigeria": "nigerian_npfl",
        "ghana": "ghana_premier_league",
        "cameroon": "cameroonian_première_division",
        "ivory coast": "ivory_coast_ligue_1",
        "senegal": "senegal_ligue_1",
        "angola": "angolan_girabola",
        "congo dr": "congolese_linafoot",
        "tanzania": "tanzanian_premier_league",
        "zambia": "zambian_super_league",
        "uganda": "ugandan_super_league",
        "kenya": "kenyan_premier_league",
        "ethiopia": "ethiopian_premier_league",
        "mozambique": "mozambican_liga_moca",
        "rwanda": "rwandan_premier_league",
        "malawi": "malawian_super_league",
        "burundi": "burundian_premier_league",
        "zimbabwe": "zimbabwe_premier_league",
        "libya": "libyan_premier_league",
        "sudan": "sudanese_premier_league",
        
        # Asia
        "saudi arabia": "saudi_pro_league",
        "japan": "j1_league",
        "south korea": "k_league",
        "china": "chinese_super_league",
        "iran": "iran_pro_league",
        "uae": "uae_pro_league",
        "qatar": "qatar_stars_league",
        "india": "indian_super_league",
        "thailand": "thai_league_1",
        "uzbekistan": "uzbekistan_super_league",
        "iraq": "iraq_premier_league",
        "jordan": "jordanian_pro_league",
        "kazakhstan": "kazakhstan_premier_league",
        "malaysia": "malaysian_super_league",
        "vietnam": "vietnamese_v_league_1",
        "indonesia": "indonesia_super_league",
        "philippines": "philippines_united_football_league",
        "singapore": "singapore_premier_league",
        "australia": "a_league",
        
        # North America
        "united states": "mls",
        "mexico": "liga_mx",
        "canada": "canadian_premier_league",
        "costa rica": "costa_rican_primera_division",
        "jamaica": "jamaican_premier_league",
        "haiti": "haitian_premier_league",
        "dominican republic": "dominican_republic_liga_dominicana_de_futbol",
        
        # Oceania
        "new zealand": "new_zealand_premier_league"
}

def normalize_key(s):
    return re.sub(r"[^\w]", "", s.lower())

def generate_retired_questions(role, questions_schema):
    new_questions = {}

    # Year
    new_questions[f"{role}_retired_year"] = [
        f"Did this {role} retire before 2000?",
        f"Did this {role} retire between 2000 and 2010?",
        f"Did this {role} retire between 2011 and 2020?",
        f"Did this {role} retire after 2020?"
    ]

    # Continent
    new_questions[f"{role}_retired_continent"] = [
        f"Did this {role} last {'play' if role == 'player' else 'manage' if role == 'manager' else 'associate'} in Europe before retiring?",
        f"Did this {role} last {'play' if role == 'player' else 'manage' if role == 'manager' else 'associate'} in South America before retiring?",
        f"Did this {role} last {'play' if role == 'player' else 'manage' if role == 'manager' else 'associate'} in Africa before retiring?",
        f"Did this {role} last {'play' if role == 'player' else 'manage' if role == 'manager' else 'associate'} in Asia before retiring?",
        f"Did this {role} last {'play' if role == 'player' else 'manage' if role == 'manager' else 'associate'} in North America before retiring?",
        f"Did this {role} last {'play' if role == 'player' else 'manage' if role == 'manager' else 'associate'} in Oceania before retiring?"
    ]

    # Country — ONE GROUP PER CONTINENT
    for continent, countries in COUNTRIES_BY_CONTINENT.items():
        country_questions = []
        for country in countries:
            action = "play" if role == "player" else "manage" if role == "manager" else "associate"
            country_questions.append(f"Did this {role} last {action} in {country.title()} before retiring?")
        new_questions[f"{role}_retired_country_{continent}"] = country_questions

    # League & Club (only for mapped countries)
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
# Main
# -----------------------------
def main():
    if not os.path.exists(QUESTIONS_SCHEMA_PATH):
        print(f"Error: {QUESTIONS_SCHEMA_PATH} not found!")
        return

    with open(QUESTIONS_SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)

    print("Generating status questions...")

    for role in ["player", "manager", "owner"]:
        schema.update(generate_retired_questions(role, schema))
        schema.update(generate_deceased_questions(role))
        if role != "owner":
            schema.update(generate_pundit_questions(role))

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)

    print(f"✅ Updated {QUESTIONS_SCHEMA_PATH}!")

if __name__ == "__main__":
    main()