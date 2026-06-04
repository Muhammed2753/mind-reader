import json
import os
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class GameAnalytics:
    def __init__(self):
        self.analytics_file = "game_analytics.json"
        self.ensure_analytics_exists()
    
    def ensure_analytics_exists(self):
        if not os.path.exists(self.analytics_file):
            default_data = {
                "player_popularity": {},
                "question_effectiveness": {},
                "game_sessions": [],
                "daily_stats": {},
                "user_behavior": {
                    "avg_questions_per_game": 0,
                    "most_common_answers": {},
                    "peak_hours": {},
                    "difficulty_preferences": {}
                }
            }
            self.save_analytics(default_data)
    
    def load_analytics(self):
        try:
            with open(self.analytics_file, "r") as f:
                return json.load(f)
        except:
            return {}
    
    def save_analytics(self, data):
        try:
            with open(self.analytics_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving analytics: {e}")
    
    def track_game_session(self, session_data):
        """Track a complete game session"""
        analytics = self.load_analytics()
        
        # Add session to history
        session_data["timestamp"] = datetime.now().isoformat()
        analytics["game_sessions"].append(session_data)
        
        # Update player popularity
        if session_data.get("guessed_player"):
            player = session_data["guessed_player"]
            analytics["player_popularity"][player] = analytics["player_popularity"].get(player, 0) + 1
        
        # Track question effectiveness
        for question, answer in session_data.get("questions_asked", []):
            q_key = question.lower().strip()
            if q_key not in analytics["question_effectiveness"]:
                analytics["question_effectiveness"][q_key] = {
                    "asked_count": 0,
                    "yes_count": 0,
                    "no_count": 0,
                    "effectiveness_score": 0
                }
            
            analytics["question_effectiveness"][q_key]["asked_count"] += 1
            if answer == "yes":
                analytics["question_effectiveness"][q_key]["yes_count"] += 1
            elif answer == "no":
                analytics["question_effectiveness"][q_key]["no_count"] += 1
        
        # Update daily stats
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in analytics["daily_stats"]:
            analytics["daily_stats"][today] = {
                "games_played": 0,
                "avg_questions": 0,
                "popular_players": {},
                "success_rate": 0
            }
        
        analytics["daily_stats"][today]["games_played"] += 1
        
        # Update user behavior
        self.update_user_behavior(analytics, session_data)
        
        # Keep only last 1000 sessions for performance
        if len(analytics["game_sessions"]) > 1000:
            analytics["game_sessions"] = analytics["game_sessions"][-1000:]
        
        self.save_analytics(analytics)
    
    def update_user_behavior(self, analytics, session_data):
        """Update user behavior patterns"""
        behavior = analytics["user_behavior"]
        
        # Update average questions per game
        total_sessions = len(analytics["game_sessions"])
        if total_sessions > 0:
            total_questions = sum(len(s.get("questions_asked", [])) for s in analytics["game_sessions"])
            behavior["avg_questions_per_game"] = round(total_questions / total_sessions, 2)
        
        # Track peak hours
        hour = datetime.now().hour
        behavior["peak_hours"][str(hour)] = behavior["peak_hours"].get(str(hour), 0) + 1
        
        # Track difficulty preferences
        difficulty = session_data.get("difficulty", "medium")
        behavior["difficulty_preferences"][difficulty] = behavior["difficulty_preferences"].get(difficulty, 0) + 1
    
    def get_popular_players(self, limit=10):
        """Get most popular players"""
        analytics = self.load_analytics()
        popularity = analytics.get("player_popularity", {})
        return sorted(popularity.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    def get_question_effectiveness(self, limit=20):
        """Get most effective questions"""
        analytics = self.load_analytics()
        questions = analytics.get("question_effectiveness", {})
        
        # Calculate effectiveness score
        for q_data in questions.values():
            total_asked = q_data["asked_count"]
            if total_asked > 0:
                # Questions that split answers 50/50 are most effective
                yes_ratio = q_data["yes_count"] / total_asked
                effectiveness = 1 - abs(0.5 - yes_ratio) * 2  # Score from 0 to 1
                q_data["effectiveness_score"] = round(effectiveness, 3)
        
        # Sort by effectiveness and frequency
        sorted_questions = sorted(
            questions.items(),
            key=lambda x: (x[1]["effectiveness_score"], x[1]["asked_count"]),
            reverse=True
        )
        
        return sorted_questions[:limit]
    
    def get_daily_insights(self, days=7):
        """Get insights for the last N days"""
        analytics = self.load_analytics()
        daily_stats = analytics.get("daily_stats", {})
        
        # Get last N days
        insights = {}
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            if date in daily_stats:
                insights[date] = daily_stats[date]
        
        return insights
    
    def get_user_behavior_insights(self):
        """Get user behavior patterns"""
        analytics = self.load_analytics()
        behavior = analytics.get("user_behavior", {})
        
        # Find peak hour
        peak_hours = behavior.get("peak_hours", {})
        if peak_hours:
            peak_hour = max(peak_hours.items(), key=lambda x: x[1])
            behavior["peak_hour"] = f"{peak_hour[0]}:00"
        
        # Most preferred difficulty
        diff_prefs = behavior.get("difficulty_preferences", {})
        if diff_prefs:
            preferred_difficulty = max(diff_prefs.items(), key=lambda x: x[1])
            behavior["preferred_difficulty"] = preferred_difficulty[0]
        
        return behavior
    
    def generate_insights_report(self):
        """Generate comprehensive insights report"""
        popular_players = self.get_popular_players(5)
        effective_questions = self.get_question_effectiveness(10)
        daily_insights = self.get_daily_insights(7)
        user_behavior = self.get_user_behavior_insights()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "popular_players": popular_players,
            "effective_questions": [
                {
                    "question": q,
                    "effectiveness": data["effectiveness_score"],
                    "asked_count": data["asked_count"]
                }
                for q, data in effective_questions
            ],
            "daily_insights": daily_insights,
            "user_behavior": user_behavior,
            "recommendations": self.generate_recommendations(popular_players, effective_questions)
        }
        
        return report
    
    def generate_recommendations(self, popular_players, effective_questions):
        """Generate recommendations for improving the game"""
        recommendations = []
        
        # Player recommendations
        if popular_players:
            top_player = popular_players[0][0]
            recommendations.append(f"Consider adding more players similar to {top_player} (most popular)")
        
        # Question recommendations
        ineffective_questions = [q for q, data in effective_questions if data[1]["effectiveness_score"] < 0.3]
        if ineffective_questions:
            recommendations.append(f"Consider revising {len(ineffective_questions)} low-effectiveness questions")
        
        # Add more specific recommendations
        recommendations.extend([
            "Add more questions about player positions for better filtering",
            "Include more recent transfer questions for current players",
            "Consider adding questions about player achievements and awards"
        ])
        
        return recommendations
    
    def cleanup_old_data(self, days_to_keep=30):
        """Clean up old analytics data"""
        analytics = self.load_analytics()
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        # Clean old sessions
        analytics["game_sessions"] = [
            session for session in analytics["game_sessions"]
            if datetime.fromisoformat(session.get("timestamp", "1970-01-01")) > cutoff_date
        ]
        
        # Clean old daily stats
        analytics["daily_stats"] = {
            date: stats for date, stats in analytics["daily_stats"].items()
            if datetime.strptime(date, "%Y-%m-%d") > cutoff_date
        }
        
        self.save_analytics(analytics)

# Flask route integration
def track_game_completion(player_name, questions_asked, success, difficulty="medium"):
    """Helper function to track game completion from Flask routes"""
    analytics = GameAnalytics()
    
    session_data = {
        "guessed_player": player_name if success else None,
        "questions_asked": questions_asked,
        "success": success,
        "difficulty": difficulty,
        "question_count": len(questions_asked)
    }
    
    analytics.track_game_session(session_data)