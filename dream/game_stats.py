import json
import os
from datetime import datetime

class GameStats:
    def __init__(self, stats_file="game_stats.json"):
        self.stats_file = stats_file
        self.stats = self.load_stats()
    
    def load_stats(self):
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "total_games": 0,
            "total_wins": 0,
            "current_streak": 0,
            "best_streak": 0,
            "total_questions": 0,
            "fastest_win": None,
            "games_history": []
        }
    
    def save_stats(self):
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def record_win(self, questions_count, player_name, time_taken):
        self.stats["total_games"] += 1
        self.stats["total_wins"] += 1
        self.stats["current_streak"] += 1
        self.stats["total_questions"] += questions_count
        
        if self.stats["current_streak"] > self.stats["best_streak"]:
            self.stats["best_streak"] = self.stats["current_streak"]
        
        if self.stats["fastest_win"] is None or questions_count < self.stats["fastest_win"]:
            self.stats["fastest_win"] = questions_count
        
        self.stats["games_history"].append({
            "player": player_name,
            "questions": questions_count,
            "time": time_taken,
            "date": str(datetime.now()),
            "result": "win"
        })
        
        if len(self.stats["games_history"]) > 50:
            self.stats["games_history"] = self.stats["games_history"][-50:]
        
        self.save_stats()
    
    def record_loss(self, questions_count):
        self.stats["total_games"] += 1
        self.stats["current_streak"] = 0
        self.stats["total_questions"] += questions_count
        
        self.stats["games_history"].append({
            "player": "Unknown",
            "questions": questions_count,
            "date": str(datetime.now()),
            "result": "loss"
        })
        
        if len(self.stats["games_history"]) > 50:
            self.stats["games_history"] = self.stats["games_history"][-50:]
        
        self.save_stats()
    
    def get_stats(self):
        avg_questions = 0
        if self.stats["total_games"] > 0:
            avg_questions = round(self.stats["total_questions"] / self.stats["total_games"], 1)
        
        return {
            **self.stats,
            "avg_questions": avg_questions,
            "win_rate": round((self.stats["total_wins"] / max(1, self.stats["total_games"])) * 100, 1)
        }
