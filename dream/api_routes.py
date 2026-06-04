# api_routes.py
from flask import Blueprint, jsonify, session, request
import json  # ✅ ADD THIS
import os
from hints import HintSystem
from achievements import AchievementTracker
from daily_challenge import DailyChallenge
from leaderboard import Leaderboard
from stats_tracker import StatsTracker
from game_logic import filter_candidates  # ✅ CORRECT IMPORT

api = Blueprint("api", __name__, url_prefix="/api")

# Initialize systems (if not using global singletons)
hint_system = HintSystem()
achievement_tracker = AchievementTracker()
daily_challenge = DailyChallenge()
leaderboard = Leaderboard()
stats_tracker = StatsTracker()
@api.route('/achievements')
def get_achievements():
    tracker = AchievementTracker()
    stats = StatsTracker().get_stats()
    unlocked = tracker.check_achievements(stats)
    return jsonify({"achievements": unlocked})

@api.route('/daily')
def get_daily():
    challenge = DailyChallenge()
    return jsonify(challenge.get_current())

@api.route('/leaderboard/<board_type>')
def get_leaderboard(board_type):
    lb = Leaderboard()
    if board_type == 'global':
        return jsonify(lb.get_global())
    elif board_type == 'weekly':
        return jsonify(lb.get_weekly())
    else:
        return jsonify({"error": "Invalid type"}), 400

# Optional: Add root leaderboard fallback
@api.route('/leaderboard')
def leaderboard_default():
    return get_leaderboard('global')