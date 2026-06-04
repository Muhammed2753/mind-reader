# Feature Map

## Game Flow

```
START
  ↓
[Role Selection] → Player/Manager/Owner
  ↓
[Status Check] → Active/Retired/Deceased
  ↓
[Location] → Continent → Country → League → Club
  ↓
[Attributes] → Position/Age/Honors
  ↓
[Guess] → Correct? → WIN
         → Wrong? → Continue (max 3 wrong)
                  → Learn New Player
```

## User Journey

```
New User
  ↓
Play First Game → Unlock "First Victory" Achievement
  ↓
Use Hints (3 per game) → Learn Strategy
  ↓
Win Games → Earn XP & Coins → Level Up
  ↓
Daily Challenge → Extra Rewards
  ↓
Leaderboard → Compete Globally
  ↓
Premium Upgrade → Unlimited Hints
```

## System Architecture

```
Frontend (HTML/JS)
  ↓
Flask App (app.py)
  ↓
├── Hints System (hints.py)
├── Achievements (achievements.py)
├── Daily Challenge (daily_challenge.py)
├── Leaderboard (leaderboard.py)
├── Stats Tracker (stats_tracker.py)
└── API Routes (api_routes.py)
  ↓
Data Storage
├── football_characters.json (base players)
├── knowledge_db.json (user-added players)
├── user_stats.json (user progress)
└── leaderboard.json (rankings)
```

## Feature Dependencies

```
Core Game
  ↓
├── Hints System (independent)
├── Stats Tracking (independent)
└── Achievements (depends on stats)
  ↓
├── Daily Challenge (depends on core game)
└── Leaderboard (depends on stats)
  ↓
Premium Features (depends on all above)
```

## Data Flow

```
User Action → Flask Route → Business Logic → Data Update → JSON Save → Response
```

## Tech Stack

**Current**
- Backend: Flask (Python)
- Frontend: HTML/CSS/JS
- Storage: JSON files
- Session: Flask sessions

**Future (Roadmap)**
- Backend: Flask + PostgreSQL + Redis
- Frontend: React
- Auth: JWT + OAuth
- Hosting: AWS/Heroku
- CDN: CloudFlare
