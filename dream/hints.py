import re

class HintSystem:
    def get_hints(self, player_data):
        answers = player_data.get("answers", {})
        hints = {"position": None, "nationality": None, "club": None}
        
        for q, ans in answers.items():
            if ans == "yes":
                if "position" in q.lower() and not hints["position"]:
                    match = re.search(r"position a ([^?]+)", q, re.IGNORECASE)
                    hints["position"] = match.group(1) if match else "Unknown"
                
                if "born in" in q.lower() and not hints["nationality"]:
                    match = re.search(r"born in ([^?]+)", q, re.IGNORECASE)
                    hints["nationality"] = match.group(1) if match else "Unknown"
                
                if "playing for" in q.lower() and not hints["club"]:
                    match = re.search(r"playing for ([^?]+)", q, re.IGNORECASE)
                    hints["club"] = match.group(1) if match else "Unknown"
        
        return hints
