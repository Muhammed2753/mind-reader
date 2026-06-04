import json
import os

PREMIER_LEAGUE_PLAYERS = {
    "Erling Haaland": {
        "answers": {
            "Is this person a football player?": "yes",
            "Is this player currently active?": "yes",
            "Was this player born in Norway?": "yes",
            "Is this player playing in England?": "yes",
            "Is this player playing in the Premier League?": "yes",
            "Is this player playing for Manchester City?": "yes",
            "Is this player's natural position a Striker?": "yes",
            "Is this player between 23 and 35 years old?": "yes",
            "Has this player won the Premier League?": "yes",
            "Has this player won the UEFA Champions League?": "yes"
        },
        "image_url": "https://media.api-sports.io/football/players/1100.png"
    },
    "Mohamed Salah": {
        "answers": {
            "Is this person a football player?": "yes",
            "Is this player currently active?": "yes",
            "Was this player born in Egypt?": "yes",
            "Is this player playing in England?": "yes",
            "Is this player playing in the Premier League?": "yes",
            "Is this player playing for Liverpool?": "yes",
            "Is this player's natural position a Right Winger?": "yes",
            "Is this player between 23 and 35 years old?": "yes",
            "Has this player won the Premier League?": "yes",
            "Has this player won the UEFA Champions League?": "yes"
        },
        "image_url": "https://media.api-sports.io/football/players/306.png"
    },
    "Kevin De Bruyne": {
        "answers": {
            "Is this person a football player?": "yes",
            "Is this player currently active?": "yes",
            "Was this player born in Belgium?": "yes",
            "Is this player playing in England?": "yes",
            "Is this player playing in the Premier League?": "yes",
            "Is this player playing for Manchester City?": "yes",
            "Is this player's natural position a Attacking Midfielder?": "yes",
            "Is this player between 23 and 35 years old?": "yes",
            "Has this player won the Premier League?": "yes",
            "Has this player won the UEFA Champions League?": "yes"
        },
        "image_url": "https://media.api-sports.io/football/players/629.png"
    },
    "Bukayo Saka": {
        "answers": {
            "Is this person a football player?": "yes",
            "Is this player currently active?": "yes",
            "Was this player born in England?": "yes",
            "Is this player playing in England?": "yes",
            "Is this player playing in the Premier League?": "yes",
            "Is this player playing for Arsenal?": "yes",
            "Is this player's natural position a Right Winger?": "yes",
            "Is this player between 18 and 23 years old?": "yes"
        },
        "image_url": "https://media.api-sports.io/football/players/18936.png"
    },
    "Son Heung-min": {
        "answers": {
            "Is this person a football player?": "yes",
            "Is this player currently active?": "yes",
            "Was this player born in South Korea?": "yes",
            "Is this player playing in England?": "yes",
            "Is this player playing in the Premier League?": "yes",
            "Is this player playing for Tottenham Hotspur?": "yes",
            "Is this player's natural position a Left Winger?": "yes",
            "Is this player between 23 and 35 years old?": "yes"
        },
        "image_url": "https://media.api-sports.io/football/players/832.png"
    }
}

def add_players(file_path="football_characters.json"):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(BASE_DIR, file_path)
    
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    
    added = 0
    for name, info in PREMIER_LEAGUE_PLAYERS.items():
        if name not in data:
            data[name] = info
            print(f"✅ Added {name}")
            added += 1
        else:
            print(f"⏭️  {name} already exists")
    
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Summary: Added {added} new players. Total: {len(data)}")

if __name__ == "__main__":
    add_players()
