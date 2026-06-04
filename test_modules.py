"""
Test script to verify all new modules work correctly
Run: python test_modules.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dream'))

from hints import HintSystem
from achievements import AchievementTracker, ACHIEVEMENTS
from daily_challenge import DailyChallenge
from leaderboard import Leaderboard
from stats_tracker import StatsTracker
from config import CONFIG

def test_hints():
    print("Testing Hints System...")
    hint_system = HintSystem()
    test_player = {
        "answers": {
            "Is this player's natural position a Forward?": "yes",
            "Is this player born in Portugal?": "yes",
            "Is this player playing for AC Milan?": "yes"
        }
    }
    hints = hint_system.get_hints(test_player)
    assert hints["position"] == "Forward"
    assert hints["nationality"] == "Portugal"
    assert hints["club"] == "AC Milan"
    print("✅ Hints System working!")

def test_achievements():
    print("\nTesting Achievements...")
    tracker = AchievementTracker()
    stats = {"games_won": 1, "current_streak": 0}
    unlocked = tracker.check_achievements(stats)
    assert "first_win" in unlocked
    print(f"✅ Achievements working! Unlocked: {unlocked}")

def test_daily_challenge():
    print("\nTesting Daily Challenge...")
    dc = DailyChallenge()
    test_chars = {"Player1": {}, "Player2": {}, "Player3": {}}
    player = dc.get_daily_player(test_chars)
    assert player in test_chars
    print(f"✅ Daily Challenge working! Today's player: {player}")

def test_leaderboard():
    print("\nTesting Leaderboard...")
    lb = Leaderboard("test_leaderboard.json")
    lb.add_score("TestUser", 100, 500)
    global_lb = lb.get_global()
    assert len(global_lb) > 0
    assert global_lb[0]["username"] == "TestUser"
    os.remove("test_leaderboard.json")
    print("✅ Leaderboard working!")

def test_stats_tracker():
    print("\nTesting Stats Tracker...")
    st = StatsTracker("test_stats.json")
    st.add_win(10, 2, 50, 10)
    stats = st.get_stats()
    assert stats["games_won"] == 1
    assert stats["xp"] == 50
    assert stats["coins"] == 10
    os.remove("test_stats.json")
    print("✅ Stats Tracker working!")

def test_config():
    print("\nTesting Config...")
    assert CONFIG["hints_per_game"] == 3
    assert CONFIG["xp_per_win"] == 50
    print("✅ Config working!")

if __name__ == "__main__":
    print("=" * 50)
    print("Running Module Tests")
    print("=" * 50)
    
    try:
        test_hints()
        test_achievements()
        test_daily_challenge()
        test_leaderboard()
        test_stats_tracker()
        test_config()
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Run: python dream/app.py")
        print("2. Visit: http://localhost:5000")
        print("3. Test the game with new features")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
