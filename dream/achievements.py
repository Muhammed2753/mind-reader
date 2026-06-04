import json
import os
from datetime import datetime

# Export ACHIEVEMENTS constant
ACHIEVEMENTS = {
    "first_win": {"name": "First Victory", "description": "Win your first game", "icon": "🏆"},
    "streak_5": {"name": "Streak Master", "description": "Win 5 games in a row", "icon": "🔥"},
    "streak_10": {"name": "Unstoppable", "description": "Win 10 games in a row", "icon": "⚡"},
    "quick_win": {"name": "Mind Reader", "description": "Win in under 10 questions", "icon": "🧠"},
    "veteran": {"name": "Veteran Player", "description": "Play 50 games", "icon": "🎖️"},
    "perfect_week": {"name": "Perfect Week", "description": "Win 7 games this week", "icon": "💎"}
}

class AchievementTracker:
    def __init__(self):
        self.achievements_file = "achievements.json"
        self.all_achievements = ACHIEVEMENTS
    
    def get_unlocked_achievements(self):
        if not os.path.exists(self.achievements_file):
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
                    json.dump(unlocked, f)
            except:
                pass
        return self.all_achievements.get(achievement_id)
    
    def check_achievements(self, stats):
        new_achievements = []
        
        # First win
        if stats.get("games_won", 0) >= 1:
            achievement = self.unlock_achievement("first_win")
            if achievement:
                new_achievements.append(achievement)
        
        # Streak achievements
        current_streak = stats.get("current_streak", 0)
        if current_streak >= 5:
            achievement = self.unlock_achievement("streak_5")
            if achievement:
                new_achievements.append(achievement)
        
        if current_streak >= 10:
            achievement = self.unlock_achievement("streak_10")
            if achievement:
                new_achievements.append(achievement)
        
        # Veteran player
        if stats.get("games_played", 0) >= 50:
            achievement = self.unlock_achievement("veteran")
            if achievement:
                new_achievements.append(achievement)
        
        # Get all unlocked achievements with details
        unlocked_ids = self.get_unlocked_achievements()
        all_unlocked = [self.all_achievements[aid] for aid in unlocked_ids if aid in self.all_achievements]
        
        return all_unlocked