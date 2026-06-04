import random
from datetime import datetime

class DailyChallenge:
    def get_daily_player(self, all_characters):
        today = datetime.now().strftime("%Y-%m-%d")
        seed = int(today.replace("-", ""))
        random.seed(seed)
        
        players = list(all_characters.keys())
        if not players:
            return None
        
        return random.choice(players)
