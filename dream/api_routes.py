from flask import Blueprint, jsonify, session, request
import json
import os
from hints import HintSystem
from achievements import AchievementTracker
from daily_challenge import DailyChallenge
from leaderboard import Leaderboard
from stats_tracker import StatsTracker

api = Blueprint("api", __name__, url_prefix="/api")

hint_system = HintSystem()
achievement_tracker = AchievementTracker()
daily_challenge = DailyChallenge()
leaderboard = Leaderboard()
stats_tracker = StatsTracker()

def load_json_file(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

@api.route("/hint", methods=["POST"])
def get_hint():
    hints_remaining = session.get("hints_remaining", 0)
    if hints_remaining <= 0:
        return jsonify({"error": "No hints remaining"}), 400
    
    # Get current player from candidates
    answers = session.get("answers", [])
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CHARACTERS_PATH = os.path.join(BASE_DIR, "football_characters.json")
    KNOW_PATH = os.path.join(BASE_DIR, "knowledge_db.json")
    
    base_chars = load_json_file(CHARACTERS_PATH, {})
    user_know = load_json_file(KNOW_PATH, {})
    all_chars = {**base_chars, **user_know}
    
    # Get top candidate
    from app import filter_candidates
    candidates = filter_candidates(answers, all_chars)
    
    if not candidates:
        return jsonify({"error": "No player found"}), 400
    
    player_name, player_data, _ = candidates[0]
    hints = hint_system.get_hints(player_data)
    
    # Pick first available hint
    hint_text = None
    if hints["position"]:
        hint_text = f"Position: {hints['position']}"
    elif hints["nationality"]:
        hint_text = f"Nationality: {hints['nationality']}"
    elif hints["club"]:
        hint_text = f"Club: {hints['club']}"
    else:
        hint_text = "No hint available for this player"
    
    session["hints_remaining"] = hints_remaining - 1
    session["hints_used"] = session.get("hints_used", 0) + 1
    
    return jsonify({"hint": hint_text, "hints_remaining": session["hints_remaining"]})

@api.route("/achievements")
def get_achievements():
    stats = stats_tracker.get_stats()
    unlocked = achievement_tracker.check_achievements(stats)
    return jsonify({"achievements": unlocked})

@api.route("/daily")
def get_daily():
    # Return daily challenge player
    return jsonify({"player": "Daily Player", "completed": False})

@api.route("/leaderboard/<board_type>")
def get_leaderboard(board_type):
    if board_type == "global":
        return jsonify(leaderboard.get_global())
    elif board_type == "weekly":
        return jsonify(leaderboard.get_weekly())
    return jsonify({"error": "Invalid board type"}), 400

@api.route("/stats")
def get_stats():
    return jsonify(stats_tracker.get_stats())
