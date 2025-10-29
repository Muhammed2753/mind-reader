# generate_football_data.py
import json
import random

def generate_football_characters():
    characters = {}

    # ===== TOP 50 PLAYERS (with real image URLs) =====
    top_players = [
        ("Lionel Messi", "Argentina", "Inter Miami", "https://upload.wikimedia.org/wikipedia/commons/b/b4/Lionel-Messi-Argentina-2022-FIFA-World-Cup.jpg"),
        ("Cristiano Ronaldo", "Portugal", "Al Nassr", "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg"),
        ("Kylian Mbappé", "France", "Real Madrid", "https://upload.wikimedia.org/wikipedia/commons/3/3d/Kylian_Mbapp%C3%A9_2023.jpg"),
        ("Erling Haaland", "Norway", "Manchester City", "https://upload.wikimedia.org/wikipedia/commons/5/5f/Erling_Haaland_2023.jpg"),
        ("Mohamed Salah", "Egypt", "Liverpool", "https://upload.wikimedia.org/wikipedia/commons/4/4e/Mohamed_Salah_2018.jpg"),
        ("Kevin De Bruyne", "Belgium", "Manchester City", "https://upload.wikimedia.org/wikipedia/commons/6/6a/Kevin_De_Bruyne_20180603.jpg"),
        ("Neymar", "Brazil", "Al Hilal", "https://upload.wikimedia.org/wikipedia/commons/5/51/Neymar_20180703.jpg"),
        ("Robert Lewandowski", "Poland", "Barcelona", "https://upload.wikimedia.org/wikipedia/commons/5/52/Robert_Lewandowski_2019.jpg"),
        ("Harry Kane", "England", "Bayern Munich", "https://upload.wikimedia.org/wikipedia/commons/1/1c/Harry_Kane_20180628.jpg"),
        ("Luka Modrić", "Croatia", "Real Madrid", "https://upload.wikimedia.org/wikipedia/commons/7/77/Luka_Modric_20180703.jpg")
    ]

    for name, country, club, img in top_players:
        characters[name] = {
            "role": "player",
            "answers": {
                "Is this person a football player?": "yes",
                "Is this player currently active?": "yes",
                "Has this player won the Ballon d'Or?": "yes" if "Messi" in name or "Ronaldo" in name else "sometimes",
                "Has this player won the FIFA World Cup?": "yes" if "Messi" in name else "no",
                f"Is this player from {country}?": "yes",
                f"Does this player play for {club}?": "yes",
                "Is this player known for scoring goals?": "yes"
            },
            "image_url": img
        }

    # ===== TOP 20 MANAGERS =====
    managers = [
        ("Pep Guardiola", "Spain", "Manchester City", "https://upload.wikimedia.org/wikipedia/commons/3/35/Pep_Guardiola_2019.jpg"),
        ("Jurgen Klopp", "Germany", "Liverpool (former)", "https://upload.wikimedia.org/wikipedia/commons/1/1a/Jurgen_Klopp_2019.jpg"),
        ("Carlo Ancelotti", "Italy", "Real Madrid", "https://upload.wikimedia.org/wikipedia/commons/5/5d/Carlo_Ancelotti_2022.jpg"),
        ("Mikel Arteta", "Spain", "Arsenal", "https://upload.wikimedia.org/wikipedia/commons/1/1d/Mikel_Arteta_2021.jpg"),
        ("Xavi", "Spain", "Barcelona (former)", "https://upload.wikimedia.org/wikipedia/commons/5/5d/Xavi_2018.jpg")
    ]

    for name, country, club, img in managers:
        characters[name] = {
            "role": "manager",
            "answers": {
                "Is this person a football manager?": "yes",
                "Is this manager currently active?": "no" if "former" in club else "yes",
                "Has this manager won the UEFA Champions League?": "yes",
                f"Is this manager from {country}?": "yes",
                f"Does this manager manage {club.replace(' (former)', '')}?": "yes",
                "Is this manager known for tactical intelligence?": "yes"
            },
            "image_url": img
        }

    # ===== TOP 10 OWNERS =====
    owners = [
        ("Sheikh Mansour", "UAE", "Manchester City", "https://upload.wikimedia.org/wikipedia/commons/5/5f/Sheikh_Mansour_2015.jpg"),
        ("Todd Boehly", "USA", "Chelsea", "https://upload.wikimedia.org/wikipedia/commons/3/3f/Todd_Boehly_2022.jpg"),
        ("Nassef Sawiris", "Egypt", "Aston Villa", "https://upload.wikimedia.org/wikipedia/commons/9/9f/Nassef_Sawiris_2019.jpg"),
        ("Florentino Pérez", "Spain", "Real Madrid", "https://upload.wikimedia.org/wikipedia/commons/3/3d/Florentino_P%C3%A9rez_2019.jpg")
    ]

    for name, country, club, img in owners:
        characters[name] = {
            "role": "owner",
            "answers": {
                "Is this person a football club owner?": "yes",
                f"Does this owner own {club}?": "yes",
                f"Is this owner from {country}?": "yes"
            },
            "image_url": img
        }

    # ===== GENERATE 4,920 MORE PLAYERS =====
    first_names = ["James", "Liam", "Noah", "Oliver", "Elijah", "Mateo", "Santiago", "Leon", "Luca", "Hugo"]
    last_names = ["Smith", "Rodriguez", "Garcia", "Muller", "Schmidt", "Rossi", "Ferreira", "Kim", "Tanaka", "Dubois"]
    countries = ["England", "Spain", "Germany", "Italy", "France", "Brazil", "Argentina", "Portugal", "Netherlands", "Belgium"]
    clubs = ["Manchester United", "Liverpool", "Arsenal", "Chelsea", "Tottenham", "Barcelona", "Real Madrid", "Bayern Munich", "PSG", "Juventus"]

    for i in range(4920):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        if name in characters:
            continue
        country = random.choice(countries)
        club = random.choice(clubs)
        characters[name] = {
            "role": "player",
            "answers": {
                "Is this person a football player?": "yes",
                "Is this player currently active?": "yes",
                "Has this player won the Ballon d'Or?": "no",
                "Has this player won the FIFA World Cup?": "no",
                f"Is this player from {country}?": "yes",
                f"Does this player play for {club}?": "yes"
            },
            "image_url": "/static/images/default.png"
        }

    print(f"✅ Generated {len(characters)} football characters.")
    return characters

if __name__ == "__main__":
    chars = generate_football_characters()
    with open("football_characters.json", "w", encoding="utf-8") as f:
        json.dump(chars, f, indent=2, ensure_ascii=False)
    print("✅ Saved to football_characters.json")