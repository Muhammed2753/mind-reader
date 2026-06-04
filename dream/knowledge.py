import json
import requests
import time
import re
from pathlib import Path

# === CONFIG ===
JSON_FILE = "football_characters.json"
IMAGE_DIR = Path("images")
IMAGE_DIR.mkdir(exist_ok=True)

API_KEY = "19ca1d3800c7b2bfa32124eac1bac9cf"
HEADERS = {"x-apisports-key": API_KEY}
SEARCH_URL = "https://v3.football.api-sports.io/players"

# === MANUAL ID OVERRIDE (add more as you find them) ===
MANUAL_ID_MAP = {
    "Abdukodir Khusanov": 21097,
    "Rico Lewis": 19187,
    "James Trafford": 162489,
    "Stefan Ortega": 2938,
    "Joško Gvardiol": 78953,
    "Haqawi Saad": 21538,
    "Al Dawsari Nasser": 278,
    "Al-Dawsari Nasser": 278,
    "Nasser Al-Dawsari": 278,
    "Mohammed Al-Dawsari": 1544,
    "Al Dossary Mohammed": 278,  # Common misspelling
    # Add more based on your data
}

def needs_fixing(url):
    return (
        url == "/static/images/default.png" or
        "players/.png" in url or
        not url.strip()
    )

def extract_id_from_url(url):
    match = re.search(r'/players/(\d+)\.png', url)
    return int(match.group(1)) if match else None

# === LOAD DATA ===
with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

fixed = 0
failed = 0

for name, entry in data.items():
    current_url = entry.get("image_url", "").strip()
    if not needs_fixing(current_url):
        continue

    pid = None

    # 1. Try manual mapping
    if name in MANUAL_ID_MAP:
        pid = MANUAL_ID_MAP[name]
        print(f"✅ Manual match: {name} → ID {pid}")
    
    # 2. Fallback: API search (only if not found manually)
    if pid is None:
        print(f"🔎 Searching API for: {name}")
        try:
            response = requests.get(
                SEARCH_URL,
                headers=HEADERS,
                params={"search": name},
                timeout=10
            )
            if response.status_code == 200:
                players = response.json().get("response", [])
                if players:
                    pid = players[0]["player"]["id"]
                    full_name = players[0]["player"]["name"]
                    print(f"✅ API match: '{name}' → '{full_name}' (ID: {pid})")
                else:
                    print(f"❌ No API match for: {name}")
            else:
                print(f"⚠️ API error ({response.status_code}) for: {name}")
        except Exception as e:
            print(f"💥 Search failed for {name}: {e}")

    # 3. If we have an ID, download image and update
    if pid:
        img_url = f"https://media.api-sports.io/football/players/{pid}.png"
        local_path = IMAGE_DIR / f"{pid}.png"
        relative_path = f"images/{pid}.png"

        if not local_path.exists():
            try:
                img_resp = requests.get(img_url, timeout=10)
                if img_resp.status_code == 200:
                    with open(local_path, "wb") as f:
                        f.write(img_resp.content)
                else:
                    print(f"⚠️ Image download failed for ID {pid}")
                    continue
            except Exception as e:
                print(f"⚠️ Image error for ID {pid}: {e}")
                continue

        entry["image_url"] = relative_path
        entry["id"] = pid  # optional but useful
        fixed += 1
    else:
        failed += 1

    time.sleep(1.0)  # rate limit

# === SAVE ===
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n🎉 Done! Fixed: {fixed}, Failed: {failed}")