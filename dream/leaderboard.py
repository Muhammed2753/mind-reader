import json
import os
from datetime import datetime

class Leaderboard:
    def __init__(self, file_path="leaderboard.json"):
        self.file_path = file_path
        self.data = self._load()
    
    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {"global": [], "weekly": []}
    
    def _save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=2)
    
    def add_score(self, username, score, xp):
        entry = {"username": username, "score": score, "xp": xp, "date": str(datetime.now())}
        
        self.data["global"].append(entry)
        self.data["global"] = sorted(self.data["global"], key=lambda x: x["xp"], reverse=True)[:100]
        
        self.data["weekly"].append(entry)
        self.data["weekly"] = sorted(self.data["weekly"], key=lambda x: x["xp"], reverse=True)[:50]
        
        self._save()
    
    def get_global(self):
        return self.data["global"][:100]
    
    def get_weekly(self):
        return self.data["weekly"][:50]
