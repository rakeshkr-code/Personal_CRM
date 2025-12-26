# models.py
import sqlite3
import json
from datetime import datetime
from config import Config

class Database:
    def __init__(self, db_name='personal_crm.db'):
        self.db_name = db_name
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def execute_query(self, query, params=(), fetch_one=False, fetch_all=False):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid
        
        conn.close()
        return result

# class PersonModel:
#     def __init__(self):
#         self.db = Database()
    
#     def get_all(self, include_archived=False):
#         query = "SELECT * FROM people"
#         if not include_archived:
#             query += " WHERE archived = 0"
#         query += " ORDER BY first_name, last_name"
#         return self.db.execute_query(query, fetch_all=True)
    
#     def get_by_id(self, person_id):
#         query = "SELECT * FROM people WHERE id = ?"
#         return self.db.execute_query(query, (person_id,), fetch_one=True)
    
#     def create(self, data):
#         query = '''INSERT INTO people 
#                    (first_name, middle_name, last_name, nickname, gender, dob, 
#                     primary_phone, primary_email, current_city, occupation, 
#                     company, bio, notes, attributes_json)
#                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
#         return self.db.execute_query(query, (
#             data.get('first_name'), data.get('middle_name'), data.get('last_name'),
#             data.get('nickname'), data.get('gender'), data.get('dob'),
#             data.get('primary_phone'), data.get('primary_email'), data.get('current_city'),
#             data.get('occupation'), data.get('company'), data.get('bio'), 
#             data.get('notes'), json.dumps(data.get('attributes', {}))
#         ))
    
#     def update(self, person_id, data):
#         query = '''UPDATE people SET 
#                    first_name=?, middle_name=?, last_name=?, nickname=?, gender=?, dob=?,
#                    primary_phone=?, primary_email=?, current_city=?, occupation=?,
#                    company=?, bio=?, notes=?, attributes_json=?, updated_at=?
#                    WHERE id=?'''
#         return self.db.execute_query(query, (
#             data.get('first_name'), data.get('middle_name'), data.get('last_name'),
#             data.get('nickname'), data.get('gender'), data.get('dob'),
#             data.get('primary_phone'), data.get('primary_email'), data.get('current_city'),
#             data.get('occupation'), data.get('company'), data.get('bio'),
#             data.get('notes'), json.dumps(data.get('attributes', {})),
#             datetime.now().isoformat(), person_id
#         ))
    
#     def delete(self, person_id):
#         query = "DELETE FROM people WHERE id = ?"
#         return self.db.execute_query(query, (person_id,))
    
#     def search(self, search_term):
#         query = '''SELECT * FROM people 
#                    WHERE first_name LIKE ? OR last_name LIKE ? OR nickname LIKE ? 
#                    OR primary_phone LIKE ? OR primary_email LIKE ?
#                    AND archived = 0'''
#         term = f'%{search_term}%'
#         return self.db.execute_query(query, (term, term, term, term, term), fetch_all=True)
    
#     def get_relationships(self, person_id):
#         query = '''SELECT r.*, 
#                    p.first_name || ' ' || COALESCE(p.last_name, '') as related_person_name,
#                    p.id as related_person_id
#                    FROM relationships r
#                    JOIN people p ON (r.person_b_id = p.id)
#                    WHERE r.person_a_id = ? AND r.is_active = 1'''
#         return self.db.execute_query(query, (person_id,), fetch_all=True)

# ------------------------------------------------------------------------------------------------

# # models.py - UPDATED PersonModel class
# class PersonModel:
#     def __init__(self):
#         self.db = Database()
    
#     def get_all(self, include_archived=False):
#         query = "SELECT * FROM people"
#         if not include_archived:
#             query += " WHERE archived = 0"
#         query += " ORDER BY first_name, last_name"
#         return self.db.execute_query(query, fetch_all=True)
    
#     def get_by_id(self, person_id):
#         query = "SELECT * FROM people WHERE id = ?"
#         return self.db.execute_query(query, (person_id,), fetch_one=True)
    
#     def create(self, data):
#         query = '''INSERT INTO people 
#                    (first_name, middle_name, last_name, maiden_name, nickname, prefix, 
#                     gender, pronouns, dob, blood_group, nationality,
#                     primary_phone, primary_email, current_city, current_country, hometown,
#                     occupation, company, bio, notes, attributes_json)
#                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
#         return self.db.execute_query(query, (
#             data.get('first_name'), data.get('middle_name'), data.get('last_name'),
#             data.get('maiden_name'), data.get('nickname'), data.get('prefix'),
#             data.get('gender'), data.get('pronouns'), data.get('dob'),
#             data.get('blood_group'), data.get('nationality'),
#             data.get('primary_phone'), data.get('primary_email'), 
#             data.get('current_city'), data.get('current_country'), data.get('hometown'),
#             data.get('occupation'), data.get('company'), data.get('bio'), 
#             data.get('notes'), json.dumps(data.get('attributes', {}))
#         ))
    
#     def update(self, person_id, data):
#         query = '''UPDATE people SET 
#                    first_name=?, middle_name=?, last_name=?, maiden_name=?, nickname=?, prefix=?,
#                    gender=?, pronouns=?, dob=?, blood_group=?, nationality=?,
#                    primary_phone=?, primary_email=?, current_city=?, current_country=?, hometown=?,
#                    occupation=?, company=?, bio=?, notes=?, attributes_json=?, updated_at=?
#                    WHERE id=?'''
#         return self.db.execute_query(query, (
#             data.get('first_name'), data.get('middle_name'), data.get('last_name'),
#             data.get('maiden_name'), data.get('nickname'), data.get('prefix'),
#             data.get('gender'), data.get('pronouns'), data.get('dob'),
#             data.get('blood_group'), data.get('nationality'),
#             data.get('primary_phone'), data.get('primary_email'),
#             data.get('current_city'), data.get('current_country'), data.get('hometown'),
#             data.get('occupation'), data.get('company'), data.get('bio'),
#             data.get('notes'), json.dumps(data.get('attributes', {})),
#             datetime.now().isoformat(), person_id
#         ))
    
#     def delete(self, person_id):
#         query = "DELETE FROM people WHERE id = ?"
#         return self.db.execute_query(query, (person_id,))
    
#     def search(self, search_term):
#         query = '''SELECT * FROM people 
#                    WHERE (first_name LIKE ? OR last_name LIKE ? OR nickname LIKE ? 
#                    OR primary_phone LIKE ? OR primary_email LIKE ? OR occupation LIKE ?)
#                    AND archived = 0'''
#         term = f'%{search_term}%'
#         return self.db.execute_query(query, (term, term, term, term, term, term), fetch_all=True)
    
#     def get_relationships(self, person_id):
#         query = '''SELECT r.*, 
#                    p.first_name || ' ' || COALESCE(p.last_name, '') as related_person_name,
#                    p.id as related_person_id
#                    FROM relationships r
#                    JOIN people p ON (r.person_b_id = p.id)
#                    WHERE r.person_a_id = ? AND r.is_active = 1
#                    ORDER BY r.created_at DESC'''
#         return self.db.execute_query(query, (person_id,), fetch_all=True)

# ------------------------------------------------------------------------------------------------

class PersonModel:
    def __init__(self):
        self.db = Database()
    
    def get_all(self, include_archived=False):
        query = "SELECT * FROM people"
        if not include_archived:
            query += " WHERE archived = 0"
        query += " ORDER BY first_name, last_name"
        return self.db.execute_query(query, fetch_all=True)
    
    def get_by_id(self, person_id):
        query = "SELECT * FROM people WHERE id = ?"
        return self.db.execute_query(query, (person_id,), fetch_one=True)
    
    def create(self, data):
        query = '''INSERT INTO people 
                   (first_name, middle_name, last_name, maiden_name, nickname, prefix, 
                    gender, pronouns, dob, blood_group, nationality,
                    primary_phone, primary_email, current_city, current_country, hometown,
                    occupation, company, bio, notes, attributes_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        return self.db.execute_query(query, (
            data.get('first_name'), data.get('middle_name'), data.get('last_name'),
            data.get('maiden_name'), data.get('nickname'), data.get('prefix'),
            data.get('gender'), data.get('pronouns'), data.get('dob'),
            data.get('blood_group'), data.get('nationality'),
            data.get('primary_phone'), data.get('primary_email'), 
            data.get('current_city'), data.get('current_country'), data.get('hometown'),
            data.get('occupation'), data.get('company'), data.get('bio'), 
            data.get('notes'), json.dumps(data.get('attributes', {}))
        ))
    
    def update(self, person_id, data):
        query = '''UPDATE people SET 
                   first_name=?, middle_name=?, last_name=?, maiden_name=?, nickname=?, prefix=?,
                   gender=?, pronouns=?, dob=?, blood_group=?, nationality=?,
                   primary_phone=?, primary_email=?, current_city=?, current_country=?, hometown=?,
                   occupation=?, company=?, bio=?, notes=?, attributes_json=?, updated_at=?
                   WHERE id=?'''
        return self.db.execute_query(query, (
            data.get('first_name'), data.get('middle_name'), data.get('last_name'),
            data.get('maiden_name'), data.get('nickname'), data.get('prefix'),
            data.get('gender'), data.get('pronouns'), data.get('dob'),
            data.get('blood_group'), data.get('nationality'),
            data.get('primary_phone'), data.get('primary_email'),
            data.get('current_city'), data.get('current_country'), data.get('hometown'),
            data.get('occupation'), data.get('company'), data.get('bio'),
            data.get('notes'), json.dumps(data.get('attributes', {})),
            datetime.now().isoformat(), person_id
        ))
    
    def delete(self, person_id):
        query = "DELETE FROM people WHERE id = ?"
        return self.db.execute_query(query, (person_id,))
    
    def search(self, search_term):
        query = '''SELECT * FROM people 
                   WHERE (first_name LIKE ? OR last_name LIKE ? OR nickname LIKE ? 
                   OR primary_phone LIKE ? OR primary_email LIKE ? OR occupation LIKE ?)
                   AND archived = 0'''
        term = f'%{search_term}%'
        return self.db.execute_query(query, (term, term, term, term, term, term), fetch_all=True)
    
    # def get_relationships(self, person_id):
    #     """FIXED: Removed r.created_at from ORDER BY"""
    #     query = '''SELECT r.*, 
    #                p.first_name || ' ' || COALESCE(p.last_name, '') as related_person_name,
    #                p.id as related_person_id
    #                FROM relationships r
    #                JOIN people p ON (r.person_b_id = p.id)
    #                WHERE r.person_a_id = ? AND r.is_active = 1
    #                ORDER BY r.relationship_type, p.first_name'''
    #     return self.db.execute_query(query, (person_id,), fetch_all=True)
    
    def get_relationships(self, person_id):
        query = '''SELECT r.*, 
                p.first_name || ' ' || COALESCE(p.last_name, '') as related_person_name,
                p.id as related_person_id
                FROM relationships r
                JOIN people p ON (r.person_b_id = p.id)
                WHERE r.person_a_id = ? AND r.is_active = 1
                ORDER BY r.relationship_type, p.first_name'''
        return self.db.execute_query(query, (person_id,), fetch_all=True)



class PlaceModel:
    def __init__(self):
        self.db = Database()
    
    def get_all(self, include_archived=False):
        query = "SELECT * FROM places"
        if not include_archived:
            query += " WHERE archived = 0"
        query += " ORDER BY name"
        return self.db.execute_query(query, fetch_all=True)
    
    def get_by_id(self, place_id):
        query = "SELECT * FROM places WHERE id = ?"
        return self.db.execute_query(query, (place_id,), fetch_one=True)
    
    def create(self, data):
        query = '''INSERT INTO places 
                   (name, type, latitude, longitude, altitude_meters, city, country,
                    visit_status, my_rating, description, tags, attributes_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        return self.db.execute_query(query, (
            data.get('name'), data.get('type'), data.get('latitude'), data.get('longitude'),
            data.get('altitude_meters'), data.get('city'), data.get('country'),
            data.get('visit_status', 'Not Visited'), data.get('my_rating'),
            data.get('description'), data.get('tags'), json.dumps(data.get('attributes', {}))
        ))
    
    def update(self, place_id, data):
        query = '''UPDATE places SET 
                   name=?, type=?, latitude=?, longitude=?, altitude_meters=?, city=?, country=?,
                   visit_status=?, my_rating=?, description=?, tags=?, attributes_json=?, updated_at=?
                   WHERE id=?'''
        return self.db.execute_query(query, (
            data.get('name'), data.get('type'), data.get('latitude'), data.get('longitude'),
            data.get('altitude_meters'), data.get('city'), data.get('country'),
            data.get('visit_status'), data.get('my_rating'), data.get('description'),
            data.get('tags'), json.dumps(data.get('attributes', {})),
            datetime.now().isoformat(), place_id
        ))
    
    def delete(self, place_id):
        query = "DELETE FROM places WHERE id = ?"
        return self.db.execute_query(query, (place_id,))
    
    def search(self, search_term):
        query = '''SELECT * FROM places 
                   WHERE name LIKE ? OR city LIKE ? OR country LIKE ? OR type LIKE ?
                   AND archived = 0'''
        term = f'%{search_term}%'
        return self.db.execute_query(query, (term, term, term, term), fetch_all=True)

class EventModel:
    def __init__(self):
        self.db = Database()
    
    def get_all(self):
        query = "SELECT e.*, p.name as place_name FROM events e LEFT JOIN places p ON e.place_id = p.id ORDER BY e.start_datetime DESC"
        return self.db.execute_query(query, fetch_all=True)
    
    def get_by_id(self, event_id):
        query = "SELECT e.*, p.name as place_name FROM events e LEFT JOIN places p ON e.place_id = p.id WHERE e.id = ?"
        return self.db.execute_query(query, (event_id,), fetch_one=True)
    
    def create(self, data):
        query = '''INSERT INTO events 
                   (title, event_type, place_id, start_datetime, end_datetime,
                    description, transport_mode, expense_amount, weather, mood, tags, context_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        return self.db.execute_query(query, (
            data.get('title'), data.get('event_type'), data.get('place_id'),
            data.get('start_datetime'), data.get('end_datetime'), data.get('description'),
            data.get('transport_mode'), data.get('expense_amount'), data.get('weather'),
            data.get('mood'), data.get('tags'), json.dumps(data.get('context', {}))
        ))
    
    def update(self, event_id, data):
        query = '''UPDATE events SET 
                   title=?, event_type=?, place_id=?, start_datetime=?, end_datetime=?,
                   description=?, transport_mode=?, expense_amount=?, weather=?, mood=?, 
                   tags=?, context_json=?, updated_at=?
                   WHERE id=?'''
        return self.db.execute_query(query, (
            data.get('title'), data.get('event_type'), data.get('place_id'),
            data.get('start_datetime'), data.get('end_datetime'), data.get('description'),
            data.get('transport_mode'), data.get('expense_amount'), data.get('weather'),
            data.get('mood'), data.get('tags'), json.dumps(data.get('context', {})),
            datetime.now().isoformat(), event_id
        ))
    
    def delete(self, event_id):
        query = "DELETE FROM events WHERE id = ?"
        return self.db.execute_query(query, (event_id,))
    
    def get_participants(self, event_id):
        query = '''SELECT p.* FROM event_participants ep
                   JOIN people p ON ep.person_id = p.id
                   WHERE ep.event_id = ?'''
        return self.db.execute_query(query, (event_id,), fetch_all=True)
