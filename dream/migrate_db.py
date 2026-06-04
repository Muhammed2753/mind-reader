import sqlite3
import json
from pathlib import Path

def migrate_to_sqlite():
    """Migrate JSON data to SQLite for better performance"""
    
    # Create database
    conn = sqlite3.connect('football_game.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        image_url TEXT,
        age_group TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        FOREIGN KEY (player_id) REFERENCES players(id)
    )''')
    
    c.execute('''CREATE INDEX IF NOT EXISTS idx_player_name ON players(name)''')
    c.execute('''CREATE INDEX IF NOT EXISTS idx_answers_player ON answers(player_id)''')
    
    # Load JSON data
    json_file = Path('football_characters.json')
    if json_file.exists():
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Insert data
        for name, info in data.items():
            c.execute('INSERT OR IGNORE INTO players (name, image_url, age_group) VALUES (?, ?, ?)',
                     (name, info.get('image_url', ''), info.get('age_group', 'unknown')))
            
            player_id = c.lastrowid
            for question, answer in info.get('answers', {}).items():
                c.execute('INSERT INTO answers (player_id, question, answer) VALUES (?, ?, ?)',
                         (player_id, question, answer))
    
    conn.commit()
    conn.close()
    print("✅ Migration complete!")

if __name__ == '__main__':
    migrate_to_sqlite()