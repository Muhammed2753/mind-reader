import json
import os
from pathlib import Path
BASE_DIR = Path(__file__).parent
STATS_FILE = BASE_DIR / "game_stats.json"
class GameStats:
    def __init__(self, stats_file=None):
        self.stats_file = stats_file or STATS_FILE
    def get_stats(self):
        if not self.stats_file.exists():
            return {"games_played": 0, "games_won": 0, "current_streak": 0, "best_streak": 0, "level": 1}
        try:
            with open(self.stats_file, "r") as f:
                stats = json.load(f)
                stats["level"] = min(1 + stats.get("games_played", 0) // 10, 10)
                return stats
        except Exception as e:
            print(f"Error loading stats: {e}")
            return {"games_played": 0, "games_won": 0, "current_streak": 0, "best_streak": 0, "level": 1}
    def record_win(self, questions, player, time_taken):
        stats = self.get_stats()
        stats["games_played"] += 1
        stats["games_won"] += 1
        stats["current_streak"] += 1
        stats["best_streak"] = max(stats["best_streak"], stats["current_streak"])
        self._save_stats(stats)
    def record_loss(self, questions):
        stats = self.get_stats()
        stats["games_played"] += 1
        stats["current_streak"] = 0
        self._save_stats(stats)
    def _save_stats(self, stats):
        try:
            with open(self.stats_file, "w") as f:
                json.dump(stats, f, indent=2)
        except Exception as e:
            print(f"Error saving stats: {e}")
