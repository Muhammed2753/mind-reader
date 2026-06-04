import json
import os
from datetime import datetime
import random

class DailyChallenge:
    def __init__(self):
        self.challenge_file = "daily_challenge.json"
        self.players_pool = [
            "Lionel Messi", "Cristiano Ronaldo", "Kylian Mbappé", "Erling Haaland",
            "Kevin De Bruyne", "Virgil van Dijk", "Mohamed Salah", "Robert Lewandowski",
            "Luka Modrić", "Karim Benzema", "Sadio Mané", "Harry Kane",
            "Neymar Jr", "Sergio Ramos", "N'Golo Kanté", "Bruno Fernandes"
        ]
    
    def get_today_date(self):
        return datetime.now().strftime("%Y-%m-%d")
    
    def get_daily_challenge(self):
        today = self.get_today_date()
        
        # Try to load existing challenge
        if os.path.exists(self.challenge_file):
            try:
                with open(self.challenge_file, "r") as f:
                    data = json.load(f)
                    if data.get("date") == today:
                        return data
            except:
                pass
        
        # Generate new challenge for today
        random.seed(today)  # Consistent random for the day
        challenge_player = random.choice(self.players_pool)
        
        challenge_data = {
            "date": today,
            "player": challenge_player,
            "completed": False,
            "attempts": 0,
            "max_attempts": 3,
            "reward_points": 50,
            "hint": f"This player is one of the most famous footballers in the world!"
        }
        
        # Save challenge
        try:
            with open(self.challenge_file, "w") as f:
                json.dump(challenge_data, f, indent=2)
        except:
            pass
        
        return challenge_data
    
    def complete_challenge(self, success=True):
        challenge = self.get_daily_challenge()
        challenge["completed"] = success
        challenge["attempts"] += 1
        
        try:
            with open(self.challenge_file, "w") as f:
                json.dump(challenge, f, indent=2)
        except:
            pass
        
        return challenge
    
    def get_challenge_status(self):
        challenge = self.get_daily_challenge()
        return {
            "player": challenge["player"],
            "completed": challenge["completed"],
            "attempts": challenge["attempts"],
            "max_attempts": challenge["max_attempts"],
            "reward_points": challenge["reward_points"],
            "hint": challenge["hint"],
            "time_left": "Resets at midnight"
        }