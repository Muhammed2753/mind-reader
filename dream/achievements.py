import json
from pathlib import Path
BASE_DIR = Path(__file__).parent
ACHIEVEMENTS_FILE = BASE_DIR / "achievements.json"
ACHIEVEMENTS = {
    "first_win": {"name": "First Victory", "description": "Win your first game", "icon": "🏆"},
    "streak_5": {"name": "Streak Master", "description": "Win 5 games in a row", "icon": "🔥"},
    "streak_10": {"name": "Unstoppable", "description": "Win 10 games in a row", "icon": "⚡"},
    "quick_win": {"name": "Mind Reader", "description": "Win in under 10 questions", "icon": "🧠"},
    "veteran": {"name": "Veteran Player", "description": "Play 50 games", "icon": "🎖️"},
    "perfect_week": {"name": "Perfect Week", "description": "Win 7 games this week", "icon": "💎"}
}
class AchievementTracker:
    def __init__(self, achievements_file=None):
        self.achievements_file = achievements_file or ACHIEVEMENTS_FILE
        self.all_achievements = ACHIEVEMENTS
    def get_unlocked_achievements(self):
        if not self.achievements_file.exists():
            return []
        try:
            with open(self.achievements_file, "r") as f:
                return json.load(f)
        except:
            return []
    def unlock_achievement(self, achievement_id):
        unlocked = self.get_unlocked_achievements()
        if achievement_id not in unlocked:
            unlocked.append(achievement_id)
            try:
                with open(self.achievements_file, "w") as f:
                    json.dump(unlocked, f, indent=2)
            except:
                pass
            return self.all_achievements.get(achievement_id)
        return None
    def check_achievements(self, stats):
        new_achievements = []
        if stats.get("games_won", 0) >= 1:
            ach = self.unlock_achievement("first_win")
            if ach: new_achievements.append(ach)
        current_streak = stats.get("current_streak", 0)
        if current_streak >= 5:
            ach = self.unlock_achievement("streak_5")
            if ach: new_achievements.append(ach)
        if current_streak >= 10:
            ach = self.unlock_achievement("streak_10")
            if ach: new_achievements.append(ach)
        if stats.get("games_played", 0) >= 50:
            ach = self.unlock_achievement("veteran")
            if ach: new_achievements.append(ach)
        return new_achievements
