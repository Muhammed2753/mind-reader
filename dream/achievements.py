ACHIEVEMENTS = {
    "first_win": {"name": "First Victory", "desc": "Win your first game", "xp": 50, "coins": 10},
    "speed_demon": {"name": "Speed Demon", "desc": "Win in under 10 questions", "xp": 100, "coins": 25},
    "perfect_game": {"name": "Perfect Game", "desc": "Win without using hints", "xp": 150, "coins": 50},
    "streak_5": {"name": "5 Win Streak", "desc": "Win 5 games in a row", "xp": 200, "coins": 75},
    "streak_10": {"name": "10 Win Streak", "desc": "Win 10 games in a row", "xp": 500, "coins": 200},
    "premier_expert": {"name": "Premier League Expert", "desc": "Guess 20 Premier League players", "xp": 150, "coins": 50},
    "laliga_expert": {"name": "La Liga Expert", "desc": "Guess 20 La Liga players", "xp": 150, "coins": 50},
    "century": {"name": "Century", "desc": "Win 100 games", "xp": 1000, "coins": 500},
    "knowledge_master": {"name": "Knowledge Master", "desc": "Add 10 players to database", "xp": 300, "coins": 100},
    "daily_champion": {"name": "Daily Champion", "desc": "Complete 7 daily challenges", "xp": 250, "coins": 100}
}

class AchievementTracker:
    def check_achievements(self, stats):
        unlocked = []
        
        if stats.get("games_won", 0) == 1:
            unlocked.append("first_win")
        if stats.get("current_streak", 0) == 5:
            unlocked.append("streak_5")
        if stats.get("current_streak", 0) == 10:
            unlocked.append("streak_10")
        if stats.get("games_won", 0) == 100:
            unlocked.append("century")
        
        return unlocked
