# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    DATABASE = 'personal_crm.db'
    DEBUG = True
    
    # Relationship types
    RELATIONSHIP_TYPES = [
        'Father', 'Mother', 'Brother', 'Sister', 'Son', 'Daughter',
        'Spouse', 'Partner', 'Friend', 'Colleague', 'Manager', 'Mentor',
        'Acquaintance', 'Neighbor', 'Classmate', 'Roommate'
    ]
    
    # Circle types
    CIRCLE_TYPES = ['Family', 'Work', 'Friends', 'Acquaintance', 'Professional', 'Social']
    
    # Place types
    PLACE_TYPES = [
        'City', 'Town', 'Village', 'Country', 'State',
        'Restaurant', 'Cafe', 'Bar', 'Hotel', 'Resort',
        'Hill', 'Mountain', 'River', 'Lake', 'Beach', 'Forest', 'Park',
        'Office', 'School', 'University', 'Hospital', 'Airport', 'Station',
        'Temple', 'Church', 'Mosque', 'Monument', 'Museum',
        'Exam Center', 'Conference Hall', 'Stadium', 'Mall', 'Market'
    ]
    
    # Event types
    EVENT_TYPES = [
        'Trip', 'Vacation', 'Business Trip', 'Day Trip',
        'Meeting', 'Conference', 'Interview', 'Exam',
        'Dinner', 'Party', 'Wedding', 'Birthday', 'Festival',
        'Hike', 'Trek', 'Adventure', 'Sport',
        'Concert', 'Movie', 'Theater', 'Exhibition'
    ]
