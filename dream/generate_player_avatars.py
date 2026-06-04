"""
Generate player avatar images using UI Avatars (free service)
Creates nice looking avatars with player initials
"""

import json
import os
import urllib.parse

def generate_avatar_url(name):
    """Generate avatar URL from player name"""
    # UI Avatars service - free, no API key needed
    encoded_name = urllib.parse.quote(name)
    return f"https://ui-avatars.com/api/?name={encoded_name}&size=200&background=667eea&color=fff&bold=true"

def update_all_images(file_path="football_characters.json"):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(BASE_DIR, file_path)
    
    if not os.path.exists(full_path):
        print("❌ football_characters.json not found!")
        return
    
    with open(full_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    updated = 0
    for player_name in data.keys():
        # Only update if image is missing or is placeholder
        current_img = data[player_name].get("image_url", "")
        if not current_img or ".png" in current_img and "api-sports" in current_img:
            data[player_name]["image_url"] = generate_avatar_url(player_name)
            print(f"✅ Generated avatar for {player_name}")
            updated += 1
    
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Generated {updated} player avatars")
    print("🎨 Using UI Avatars service (free, no API key needed)")

if __name__ == "__main__":
    update_all_images()
