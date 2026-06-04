# Implementation Guide

## Quick Start (5 Minutes)

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the App**
```bash
python dream/app.py
```

3. **Test New Features**
- Visit http://localhost:5000
- Start a game and use hints
- Check stats at /api/stats

## Feature Integration

### 1. Hints System

**Backend (Already Integrated)**
- hints.py provides HintSystem class
- Session tracks hints_remaining (3 per game)
- API endpoint: POST /api/hint

**Frontend Integration**
Add to question.html:
```html
<button onclick="getHint()">Use Hint ({{ session.hints_remaining }} left)</button>
<script>
function getHint() {
    fetch('/api/hint', {method: 'POST'})
        .then(r => r.json())
        .then(data => alert(data.hint));
}
</script>
```

### 2. Stats Tracking

**Backend (Already Integrated)**
- stats_tracker.py tracks all user stats
- Automatically updates on win/loss
- API endpoint: GET /api/stats

**Frontend Integration**
Add to index.html:
```html
<div id="stats"></div>
<script>
fetch('/api/stats')
    .then(r => r.json())
    .then(data => {
        document.getElementById('stats').innerHTML = `
            Level ${data.level} | XP: ${data.xp} | Coins: ${data.coins}
        `;
    });
</script>
```

### 3. Achievements

**Backend (Already Integrated)**
- achievements.py defines 10 achievements
- Auto-checks on game completion
- API endpoint: GET /api/achievements

**Frontend Integration**
Create achievements.html and link from index.html

### 4. Daily Challenge

**Backend (Already Integrated)**
- daily_challenge.py selects daily player
- Same player for all users each day
- API endpoint: GET /api/daily

**Frontend Integration**
Add daily challenge button to index.html

### 5. Leaderboard

**Backend (Already Integrated)**
- leaderboard.py manages rankings
- Global (top 100) & Weekly (top 50)
- API endpoints: GET /api/leaderboard/global, /api/leaderboard/weekly

**Frontend Integration**
Create leaderboard.html with tabs for global/weekly

## Testing Checklist

- [ ] Start game and verify hints_remaining = 3
- [ ] Use hint and verify count decreases
- [ ] Win game and check stats update
- [ ] Check achievements unlock
- [ ] Verify daily challenge consistency
- [ ] Test leaderboard updates

## Deployment

1. Set environment variables
2. Use production WSGI server (gunicorn)
3. Enable HTTPS
4. Set up database backups
5. Configure monitoring

## Next Steps

1. Add frontend UI for all features
2. Implement user authentication
3. Migrate to PostgreSQL
4. Add payment integration
5. Launch marketing campaign
