import json
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SERIE_A_PLAYERS = {
    "Rafael Leão": {
        "answers": {
            "Is this person a football player?": "yes",
            "Is this player currently active?": "yes",
            "Is this player born in Portugal?": "yes",
            "Is this player playing in Italy?": "yes",
            "Is this player playing in Serie A?": "yes",
            "Is this player playing for AC Milan?": "yes",
            "Is this player's natural position a Winger?": "yes",
            "Is this player between 23 and 35 years old?": "yes"
        },
        "image_url": "https://example.com/leao.png"
    },
    "Lautaro Martínez": {
        "answers": {
            "Is this person a football player?": "yes",
            "Is this player currently active?": "yes",
            "Is this player born in Argentina?": "yes",
            "Is this player playing in Italy?": "yes",
            "Is this player playing in Serie A?": "yes",
            "Is this player playing for Inter Milan?": "yes",
            "Is this player's natural position a Striker?": "yes",
            "Is this player between 23 and 35 years old?": "yes"
        },
        "image_url": "https://example.com/lautaro.png"
    },
    "Paulo Dybala": {
        "answers": {
            "Is this person a football player?": "yes",
            "Is this player currently active?": "yes",
            "Is this player born in Argentina?": "yes",
            "Is this player playing in Italy?": "yes",
            "Is this player playing in Serie A?": "yes",
            "Is this player playing for Roma?": "yes",
            "Is this player's natural position a Forward?": "yes",
            "Is this player between 23 and 35 years old?": "yes"
        },
        "image_url": "https://example.com/dybala.png"
    }
}

def add_players(file_path="football_characters.json"):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    
    for name, info in SERIE_A_PLAYERS.items():
        if name not in data:
            data[name] = info
            logging.info(f"Added {name}")
        else:
            logging.info(f"{name} already exists")
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    logging.info(f"Total players: {len(data)}")

if __name__ == "__main__":
    add_players()
