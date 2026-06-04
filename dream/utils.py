import json
import os
import re

# Cache for JSON files
_JSON_CACHE = {}
_CACHE_TIMESTAMPS = {}


def load_json_file(path, default):
    if not os.path.exists(path):
        return default
    try:
        mtime = os.path.getmtime(path)
        if path in _JSON_CACHE and _CACHE_TIMESTAMPS.get(path) == mtime:
            return _JSON_CACHE[path]
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        _JSON_CACHE[path] = data
        _CACHE_TIMESTAMPS[path] = mtime
        return data
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return default


def save_json_file(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving {path}: {e}")


def normalize_answer(raw):
    s = raw.strip().lower() if raw else ""
    if s in ("idk", "i don't know", "dont know", "unknown"):
        return "i don't know"
    if s in ("yes", "y", "yeah", "yep", "sure"):
        return "yes"
    if s in ("no", "n", "nope", "nah"):
        return "no"
    if s in ("sometimes", "maybe", "occasionally", "not really"):
        return "sometimes"
    return "i don't know"


def normalize_key(q):
    return re.sub(r"[^\w]", "", q.lower().strip())


def normalize_continent_name(continent_str):
    return continent_str.strip().lower().replace(" ", "_").replace("-", "_")


# Profanity Filter
PROFANITY_WORDS = {
    "fuck", "shit", "bitch", "asshole", "dick", "piss", "cunt", "slut",
    "whore", "nigga", "nigger", "fag", "faggot", "cock", "twat", "crap",
    "arse", "bollocks", "wanker", "prick", "douche", "motherfucker",
    "bastard", "damn", "hell", "sucker", "retard", "idiot", "mad", "moron"
}


def contains_profanity(text):
    if not text:
        return False
    # Normalize: lowercase + remove punctuation
    clean = re.sub(r"[^\w\s]", "", text.lower())
    words = set(clean.split())
    return bool(words & PROFANITY_WORDS)
