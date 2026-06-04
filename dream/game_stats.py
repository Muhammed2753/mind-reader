import json
import os
from datetime import datetime

class GameStats:
    def __init__(self):
        self.stats_file = "game_stats.json"
        
    def get_stats(self):
        if not os.path.exists(self.stats_file):
            return {"games_played": 0, "games_won": 0, "current_streak": 0, "best_streak": 0}
        try:
            with open(self.stats_file, "r") as f:
                return json.load(f)
        except:
            return {"games_played": 0, "games_won": 0, "current_streak": 0, "best_streak": 0}
    
    def record_win(self, questions, player, time_taken):
        stats = self.get_stats()
        stats["games_played"] = stats.get("games_played", 0) + 1
        stats["games_won"] = stats.get("games_won", 0) + 1
        stats["current_streak"] = stats.get("current_streak", 0) + 1
        stats["best_streak"] = max(stats.get("best_streak", 0), stats["current_streak"])
        self._save_stats(stats)
    
    def record_loss(self, questions):
        stats = self.get_stats()
        stats["games_played"] = stats.get("games_played", 0) + 1
        stats["current_streak"] = 0
        self._save_stats(stats)
    
    def _save_stats(self, stats):
        try:
            with open(self.stats_file, "w") as f:
                json.dump(stats, f)
        except:
            pass