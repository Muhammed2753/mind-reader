import json
import os
from datetime import datetime, timedelta

class Leaderboard:
    def __init__(self):
        self.leaderboard_file = "leaderboard.json"
        self.ensure_leaderboard_exists()
    
    def ensure_leaderboard_exists(self):
        if not os.path.exists(self.leaderboard_file):
            default_data = {
                "global": [
                    {"name": "Champion", "score": 150, "games_won": 25, "best_streak": 12},
                    {"name": "Master", "score": 120, "games_won": 20, "best_streak": 8},
                    {"name": "Expert", "score": 100, "games_won": 15, "best_streak": 6},
                    {"name": "Pro", "score": 80, "games_won": 12, "best_streak": 4},
                    {"name": "Rookie", "score": 50, "games_won": 8, "best_streak": 3}
                ],
                "weekly": [
                    {"name": "WeeklyKing", "score": 45, "games_won": 7, "week": "2024-W08"},
                    {"name": "WeeklyAce", "score": 35, "games_won": 5, "week": "2024-W08"},
                    {"name": "WeeklyPro", "score": 25, "games_won": 4, "week": "2024-W08"}
                ]
            }
            try:
                with open(self.leaderboard_file, "w") as f:
                    json.dump(default_data, f, indent=2)
            except:
                pass
    
    def get_leaderboard_data(self):
        try:
            with open(self.leaderboard_file, "r") as f:
                return json.load(f)
        except:
            return {"global": [], "weekly": []}
    
    def get_global(self):
        data = self.get_leaderboard_data()
        return sorted(data.get("global", []), key=lambda x: x.get("score", 0), reverse=True)[:10]
    
    def get_weekly(self):
        data = self.get_leaderboard_data()
        current_week = datetime.now().strftime("%Y-W%U")
        weekly_data = data.get("weekly", [])
        # Filter for current week and sort by score
        current_week_data = [entry for entry in weekly_data if entry.get("week") == current_week]
        return sorted(current_week_data, key=lambda x: x.get("score", 0), reverse=True)[:10]
    
    def add_score(self, name, score, games_won, streak):
        data = self.get_leaderboard_data()
        current_week = datetime.now().strftime("%Y-W%U")
        
        # Add to global leaderboard
        global_entry = {"name": name, "score": score, "games_won": games_won, "best_streak": streak}
        data["global"].append(global_entry)
        data["global"] = sorted(data["global"], key=lambda x: x.get("score", 0), reverse=True)[:50]
        
        # Add to weekly leaderboard
        weekly_entry = {"name": name, "score": score, "games_won": games_won, "week": current_week}
        data["weekly"].append(weekly_entry)
        
        try:
            with open(self.leaderboard_file, "w") as f:
                json.dump(data, f, indent=2)
        except:
            pass