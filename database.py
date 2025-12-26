# database.py
import sqlite3
import json
from datetime import datetime

def create_advanced_database():
    """Create comprehensive database schema with all relationships"""
    conn = sqlite3.connect('personal_crm.db')
    c = conn.cursor()
    
    c.execute("PRAGMA foreign_keys = ON;")
    
    print("Creating advanced Personal CRM database...")
    
    # ========== PEOPLE ENTITIES ==========
    
    # Main People Table
    c.execute('''CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        middle_name TEXT,
        last_name TEXT,
        maiden_name TEXT,
        nickname TEXT,
        prefix TEXT,
        suffix TEXT,
        
        -- Core attributes
        gender TEXT,
        pronouns TEXT,
        dob DATE,
        age INTEGER,
        blood_group TEXT,
        nationality TEXT,
        
        -- Contact (primary only, others in contacts table)
        primary_phone TEXT,
        primary_email TEXT,
        
        -- Location
        current_city TEXT,
        current_country TEXT,
        hometown TEXT,
        
        -- Profile
        profile_photo_path TEXT,
        bio TEXT,
        occupation TEXT,
        company TEXT,
        
        -- Metadata
        tags TEXT,
        notes TEXT,
        favorite BOOLEAN DEFAULT 0,
        archived BOOLEAN DEFAULT 0,
        
        -- Advanced attributes (JSON)
        attributes_json JSON,
        
        -- Timestamps
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Contact Methods (One-to-Many)
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        platform TEXT,
        value TEXT NOT NULL,
        label TEXT,
        is_primary BOOLEAN DEFAULT 0,
        is_active BOOLEAN DEFAULT 1,
        FOREIGN KEY(person_id) REFERENCES people(id) ON DELETE CASCADE
    )''')
    
    # Addresses (One-to-Many)
    c.execute('''CREATE TABLE IF NOT EXISTS addresses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        address_type TEXT,
        street TEXT,
        city TEXT,
        state TEXT,
        postal_code TEXT,
        country TEXT,
        latitude REAL,
        longitude REAL,
        is_current BOOLEAN DEFAULT 0,
        start_date DATE,
        end_date DATE,
        FOREIGN KEY(person_id) REFERENCES people(id) ON DELETE CASCADE
    )''')
    
    # Education History
    c.execute('''CREATE TABLE IF NOT EXISTS education (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        institution TEXT NOT NULL,
        degree TEXT,
        field_of_study TEXT,
        start_year INTEGER,
        end_year INTEGER,
        grade TEXT,
        activities TEXT,
        FOREIGN KEY(person_id) REFERENCES people(id) ON DELETE CASCADE
    )''')
    
    # Career History
    c.execute('''CREATE TABLE IF NOT EXISTS career (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        company TEXT NOT NULL,
        job_title TEXT NOT NULL,
        department TEXT,
        start_date DATE,
        end_date DATE,
        is_current BOOLEAN DEFAULT 0,
        description TEXT,
        skills TEXT,
        FOREIGN KEY(person_id) REFERENCES people(id) ON DELETE CASCADE
    )''')
    
    # Groups/Circles
    c.execute('''CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        color TEXT,
        icon TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Person-Group Mapping
    c.execute('''CREATE TABLE IF NOT EXISTS person_groups (
        person_id INTEGER,
        group_id INTEGER,
        joined_date DATE,
        PRIMARY KEY (person_id, group_id),
        FOREIGN KEY(person_id) REFERENCES people(id) ON DELETE CASCADE,
        FOREIGN KEY(group_id) REFERENCES groups(id) ON DELETE CASCADE
    )''')
    
    # Relationships (The Social Graph)
    c.execute('''CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a_id INTEGER NOT NULL,
        person_b_id INTEGER NOT NULL,
        relationship_type TEXT NOT NULL,
        reverse_relationship_type TEXT,
        strength INTEGER DEFAULT 5,
        trust_level INTEGER DEFAULT 5,
        meeting_context TEXT,
        meeting_date DATE,
        start_date DATE,
        end_date DATE,
        is_active BOOLEAN DEFAULT 1,
        notes TEXT,
        FOREIGN KEY(person_a_id) REFERENCES people(id) ON DELETE CASCADE,
        FOREIGN KEY(person_b_id) REFERENCES people(id) ON DELETE CASCADE
    )''')
    
    # Interactions Log
    c.execute('''CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        interaction_type TEXT NOT NULL,
        interaction_date DATETIME NOT NULL,
        method TEXT,
        duration_minutes INTEGER,
        notes TEXT,
        sentiment TEXT,
        FOREIGN KEY(person_id) REFERENCES people(id) ON DELETE CASCADE
    )''')
    
    # ========== PLACES ENTITIES ==========
    
    c.execute('''CREATE TABLE IF NOT EXISTS places (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        native_name TEXT,
        type TEXT NOT NULL,
        category TEXT,
        
        -- Hierarchy
        parent_place_id INTEGER,
        
        -- Geography
        latitude DECIMAL(10, 8),
        longitude DECIMAL(11, 8),
        altitude_meters REAL,
        plus_code TEXT,
        timezone TEXT,
        
        -- Address
        street_address TEXT,
        city TEXT,
        state TEXT,
        postal_code TEXT,
        country TEXT,
        
        -- Status and ratings
        visit_status TEXT DEFAULT 'Not Visited',
        my_rating INTEGER,
        visit_count INTEGER DEFAULT 0,
        
        -- Details
        description TEXT,
        best_time_to_visit TEXT,
        cost_level TEXT,
        tags TEXT,
        
        -- Media
        cover_photo_path TEXT,
        
        -- Metadata
        favorite BOOLEAN DEFAULT 0,
        archived BOOLEAN DEFAULT 0,
        
        -- Advanced attributes (JSON)
        attributes_json JSON,
        
        -- Timestamps
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        
        FOREIGN KEY(parent_place_id) REFERENCES places(id)
    )''')
    
    # Place Reviews/Visits
    c.execute('''CREATE TABLE IF NOT EXISTS place_visits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place_id INTEGER NOT NULL,
        visit_date DATE NOT NULL,
        duration_hours REAL,
        rating INTEGER,
        review TEXT,
        weather TEXT,
        crowd_level TEXT,
        cost_amount REAL,
        cost_currency TEXT DEFAULT 'INR',
        FOREIGN KEY(place_id) REFERENCES places(id) ON DELETE CASCADE
    )''')
    
    # ========== EVENTS/JOURNAL ENTITIES ==========
    
    # Trips (Collections of events)
    c.execute('''CREATE TABLE IF NOT EXISTS trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        start_date DATE,
        end_date DATE,
        status TEXT DEFAULT 'Planned',
        total_budget REAL,
        currency TEXT DEFAULT 'INR',
        cover_photo_path TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Events/Journal Entries
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trip_id INTEGER,
        title TEXT NOT NULL,
        event_type TEXT NOT NULL,
        
        -- Location
        place_id INTEGER NOT NULL,
        
        -- Time
        start_datetime DATETIME NOT NULL,
        end_datetime DATETIME,
        duration_hours REAL,
        timezone TEXT,
        
        -- Content
        description TEXT,
        highlights TEXT,
        lessons_learned TEXT,
        
        -- Logistics
        transport_mode TEXT,
        accommodation TEXT,
        
        -- Financials
        expense_amount REAL,
        expense_currency TEXT DEFAULT 'INR',
        expense_category TEXT,
        
        -- Atmosphere
        weather TEXT,
        temperature REAL,
        mood TEXT,
        energy_level INTEGER,
        
        -- Media
        cover_photo_path TEXT,
        media_folder_path TEXT,
        
        -- Metadata
        tags TEXT,
        is_public BOOLEAN DEFAULT 0,
        favorite BOOLEAN DEFAULT 0,
        
        -- Advanced attributes (JSON)
        context_json JSON,
        
        -- Timestamps
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        
        FOREIGN KEY(trip_id) REFERENCES trips(id) ON DELETE SET NULL,
        FOREIGN KEY(place_id) REFERENCES places(id)
    )''')
    
    # Event Participants (Many-to-Many)
    c.execute('''CREATE TABLE IF NOT EXISTS event_participants (
        event_id INTEGER,
        person_id INTEGER,
        role TEXT,
        attendance_status TEXT DEFAULT 'Confirmed',
        PRIMARY KEY (event_id, person_id),
        FOREIGN KEY(event_id) REFERENCES events(id) ON DELETE CASCADE,
        FOREIGN KEY(person_id) REFERENCES people(id) ON DELETE CASCADE
    )''')
    
    # ========== MEDIA MANAGEMENT ==========
    
    c.execute('''CREATE TABLE IF NOT EXISTS media (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_type TEXT NOT NULL,
        entity_id INTEGER NOT NULL,
        file_path TEXT NOT NULL,
        file_name TEXT,
        media_type TEXT NOT NULL,
        file_size_kb INTEGER,
        caption TEXT,
        taken_date DATETIME,
        location_lat REAL,
        location_lon REAL,
        tags TEXT,
        is_featured BOOLEAN DEFAULT 0,
        uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # ========== SYSTEM TABLES ==========
    
    # Activity Log
    c.execute('''CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_type TEXT NOT NULL,
        entity_type TEXT NOT NULL,
        entity_id INTEGER,
        description TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Tags System
    c.execute('''CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        category TEXT,
        color TEXT,
        usage_count INTEGER DEFAULT 0
    )''')
    
    # Create indexes for better performance
    c.execute('CREATE INDEX IF NOT EXISTS idx_people_name ON people(first_name, last_name)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_places_name ON places(name)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_events_date ON events(start_datetime)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_contacts_person ON contacts(person_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_relationships_people ON relationships(person_a_id, person_b_id)')
    
    # Insert default groups
    default_groups = [
        ('Family', 'Close family members', '#FF6B6B'),
        ('Friends', 'Personal friends', '#4ECDC4'),
        ('Work', 'Work colleagues and connections', '#45B7D1'),
        ('Acquaintances', 'People I know casually', '#96CEB4'),
        ('Professional', 'Professional network', '#FFEAA7'),
        ('Social', 'Social circle', '#DFE6E9')
    ]
    
    c.executemany('INSERT OR IGNORE INTO groups (name, description, color) VALUES (?, ?, ?)', 
                  default_groups)
    
    conn.commit()
    conn.close()
    
    print("✓ Database 'personal_crm.db' created successfully with enhanced schema!")
    print("✓ Tables: people, contacts, addresses, education, career, groups, relationships,")
    print("           places, events, trips, media, and more!")

if __name__ == '__main__':
    create_advanced_database()
