import json
import os

class StatsTracker:
    def __init__(self, file_path="user_stats.json"):
        self.file_path = file_path
        self.stats = self._load()
    
    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {
            "xp": 0, "level": 1, "coins": 0,
            "games_played": 0, "games_won": 0, "games_lost": 0,
            "current_streak": 0, "best_streak": 0,
            "total_questions": 0, "avg_questions": 0,
            "hints_used": 0, "achievements": []
        }
    
    def _save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.stats, f, indent=2)
    
    def add_win(self, questions_asked, hints_used, xp_earned, coins_earned):
        self.stats["games_played"] += 1
        self.stats["games_won"] += 1
        self.stats["current_streak"] += 1
        self.stats["best_streak"] = max(self.stats["best_streak"], self.stats["current_streak"])
        self.stats["total_questions"] += questions_asked
        self.stats["hints_used"] += hints_used
        self.stats["xp"] += xp_earned
        self.stats["coins"] += coins_earned
        
        self.stats["level"] = 1 + (self.stats["xp"] // 100)
        self.stats["avg_questions"] = self.stats["total_questions"] / self.stats["games_played"]
        
        self._save()
    
    def add_loss(self):
        self.stats["games_played"] += 1
        self.stats["games_lost"] += 1
        self.stats["current_streak"] = 0
        self._save()
    
    def get_stats(self):
        return self.stats
