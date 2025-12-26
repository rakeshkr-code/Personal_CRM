# file: database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('life.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    # 1. PEOPLE TABLE (With JSON for preferences)
    c.execute('''CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        relation_circle TEXT,    -- 'Family', 'Work', 'Friend'
        dob DATE,
        phone TEXT,
        attributes_json JSON,    -- Stores Diet, Hobbies, Socials
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # 2. PLACES TABLE (With Hierarchy and JSON)
    c.execute('''CREATE TABLE IF NOT EXISTS places (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT,               -- 'Hill', 'Cafe', 'City'
        parent_place_id INTEGER, -- Link to City/State
        latitude REAL,
        longitude REAL,
        attributes_json JSON,    -- Stores WiFi, Crowd Level, Vibes
        FOREIGN KEY(parent_place_id) REFERENCES places(id)
    )''')

    # 3. JOURNAL/EVENTS TABLE
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date_time DATETIME,
        place_id INTEGER,
        description TEXT,
        context_json JSON,       -- Weather, Mood, Cost
        FOREIGN KEY(place_id) REFERENCES places(id)
    )''')
    
    conn.commit()
    conn.close()
    print("Database 'life.db' initialized successfully.")

if __name__ == "__main__":
    init_db()