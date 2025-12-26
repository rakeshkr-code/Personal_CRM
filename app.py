# # app.py
# from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# import sqlite3
# import json
# from datetime import datetime
# from config import Config
# from models import PersonModel, PlaceModel, EventModel, Database

# app = Flask(__name__)
# app.config.from_object(Config)

# db = Database()
# person_model = PersonModel()
# place_model = PlaceModel()
# event_model = EventModel()

# # Helper function
# def parse_json_safely(json_str):
#     try:
#         return json.loads(json_str) if json_str else {}
#     except:
#         return {}

# # ============= DASHBOARD =============
# @app.route('/')
# def index():
#     conn = db.get_connection()
    
#     # Get statistics
#     stats = {
#         'people_count': conn.execute('SELECT COUNT(*) FROM people WHERE archived=0').fetchone()[0],
#         'places_count': conn.execute('SELECT COUNT(*) FROM places WHERE archived=0').fetchone()[0],
#         'events_count': conn.execute('SELECT COUNT(*) FROM events').fetchone()[0],
#         'relationships_count': conn.execute('SELECT COUNT(*) FROM relationships WHERE is_active=1').fetchone()[0],
#     }
    
#     # Recent activity
#     recent_events = conn.execute('''
#         SELECT e.*, p.name as place_name 
#         FROM events e 
#         LEFT JOIN places p ON e.place_id = p.id 
#         ORDER BY e.start_datetime DESC LIMIT 5
#     ''').fetchall()
    
#     # Upcoming birthdays (simplified)
#     upcoming_birthdays = conn.execute('''
#         SELECT id, first_name, last_name, dob 
#         FROM people 
#         WHERE dob IS NOT NULL AND archived=0
#         ORDER BY substr(dob, 6) LIMIT 5
#     ''').fetchall()
    
#     conn.close()
    
#     return render_template('index.html', 
#                          stats=stats,
#                          recent_events=recent_events,
#                          upcoming_birthdays=upcoming_birthdays)

# # ============= PEOPLE ROUTES =============
# @app.route('/people')
# def people_list():
#     people = person_model.get_all()
#     return render_template('people.html', people=people, config=Config)

# @app.route('/people/add', methods=['GET', 'POST'])
# def person_add():
#     if request.method == 'POST':
#         data = {
#             'first_name': request.form.get('first_name'),
#             'middle_name': request.form.get('middle_name'),
#             'last_name': request.form.get('last_name'),
#             'nickname': request.form.get('nickname'),
#             'gender': request.form.get('gender'),
#             'dob': request.form.get('dob'),
#             'primary_phone': request.form.get('primary_phone'),
#             'primary_email': request.form.get('primary_email'),
#             'current_city': request.form.get('current_city'),
#             'occupation': request.form.get('occupation'),
#             'company': request.form.get('company'),
#             'bio': request.form.get('bio'),
#             'notes': request.form.get('notes'),
#             'attributes': {
#                 'diet': request.form.get('diet'),
#                 'hobbies': request.form.get('hobbies'),
#                 'languages': request.form.get('languages'),
#                 'social_handles': {
#                     'instagram': request.form.get('instagram'),
#                     'linkedin': request.form.get('linkedin'),
#                     'twitter': request.form.get('twitter')
#                 }
#             }
#         }
        
#         person_id = person_model.create(data)
        
#         # Add to group if specified
#         group_id = request.form.get('group_id')
#         if group_id:
#             conn = db.get_connection()
#             conn.execute('INSERT INTO person_groups (person_id, group_id) VALUES (?, ?)',
#                         (person_id, group_id))
#             conn.commit()
#             conn.close()
        
#         flash(f'Person "{data["first_name"]}" added successfully!', 'success')
#         return redirect(url_for('person_detail', person_id=person_id))
    
#     # GET request - show form
#     conn = db.get_connection()
#     groups = conn.execute('SELECT * FROM groups').fetchall()
#     conn.close()
    
#     return render_template('person_detail.html', person=None, groups=groups, config=Config)

# @app.route('/people/<int:person_id>')
# def person_detail(person_id):
#     person = person_model.get_by_id(person_id)
#     if not person:
#         flash('Person not found', 'error')
#         return redirect(url_for('people_list'))
    
#     # Parse JSON attributes
#     person = dict(person)
#     person['attributes'] = parse_json_safely(person.get('attributes_json'))
    
#     # Get relationships
#     relationships = person_model.get_relationships(person_id)
    
#     # Get events
#     conn = db.get_connection()
#     events = conn.execute('''
#         SELECT e.*, p.name as place_name
#         FROM events e
#         JOIN event_participants ep ON e.id = ep.event_id
#         LEFT JOIN places p ON e.place_id = p.id
#         WHERE ep.person_id = ?
#         ORDER BY e.start_datetime DESC LIMIT 10
#     ''', (person_id,)).fetchall()
    
#     groups = conn.execute('''
#         SELECT g.* FROM groups g
#         JOIN person_groups pg ON g.id = pg.group_id
#         WHERE pg.person_id = ?
#     ''', (person_id,)).fetchall()
    
#     all_groups = conn.execute('SELECT * FROM groups').fetchall()
#     conn.close()
    
#     return render_template('person_detail.html', 
#                          person=person, 
#                          relationships=relationships,
#                          events=events,
#                          groups=groups,
#                          all_groups=all_groups,
#                          config=Config)

# @app.route('/people/<int:person_id>/edit', methods=['POST'])
# def person_edit(person_id):
#     data = {
#         'first_name': request.form.get('first_name'),
#         'middle_name': request.form.get('middle_name'),
#         'last_name': request.form.get('last_name'),
#         'nickname': request.form.get('nickname'),
#         'gender': request.form.get('gender'),
#         'dob': request.form.get('dob'),
#         'primary_phone': request.form.get('primary_phone'),
#         'primary_email': request.form.get('primary_email'),
#         'current_city': request.form.get('current_city'),
#         'occupation': request.form.get('occupation'),
#         'company': request.form.get('company'),
#         'bio': request.form.get('bio'),
#         'notes': request.form.get('notes'),
#         'attributes': {
#             'diet': request.form.get('diet'),
#             'hobbies': request.form.get('hobbies'),
#             'languages': request.form.get('languages')
#         }
#     }
    
#     person_model.update(person_id, data)
#     flash('Person updated successfully!', 'success')
#     return redirect(url_for('person_detail', person_id=person_id))

# @app.route('/people/<int:person_id>/delete', methods=['POST'])
# def person_delete(person_id):
#     person = person_model.get_by_id(person_id)
#     name = f"{person['first_name']} {person['last_name']}" if person else "Person"
    
#     person_model.delete(person_id)
#     flash(f'{name} deleted successfully!', 'success')
#     return redirect(url_for('people_list'))

# # ============= PLACES ROUTES =============
# @app.route('/places')
# def places_list():
#     places = place_model.get_all()
#     return render_template('places.html', places=places, config=Config)

# @app.route('/places/add', methods=['GET', 'POST'])
# def place_add():
#     if request.method == 'POST':
#         data = {
#             'name': request.form.get('name'),
#             'type': request.form.get('type'),
#             'latitude': request.form.get('latitude'),
#             'longitude': request.form.get('longitude'),
#             'altitude_meters': request.form.get('altitude_meters'),
#             'city': request.form.get('city'),
#             'country': request.form.get('country'),
#             'visit_status': request.form.get('visit_status'),
#             'my_rating': request.form.get('my_rating'),
#             'description': request.form.get('description'),
#             'tags': request.form.get('tags'),
#             'attributes': {
#                 'vibe': request.form.get('vibe'),
#                 'wifi': request.form.get('wifi'),
#                 'parking': request.form.get('parking'),
#                 'best_season': request.form.get('best_season')
#             }
#         }
        
#         place_id = place_model.create(data)
#         flash(f'Place "{data["name"]}" added successfully!', 'success')
#         return redirect(url_for('place_detail', place_id=place_id))
    
#     return render_template('place_detail.html', place=None, config=Config)

# @app.route('/places/<int:place_id>')
# def place_detail(place_id):
#     place = place_model.get_by_id(place_id)
#     if not place:
#         flash('Place not found', 'error')
#         return redirect(url_for('places_list'))
    
#     place = dict(place)
#     place['attributes'] = parse_json_safely(place.get('attributes_json'))
    
#     # Get events at this place
#     conn = db.get_connection()
#     events = conn.execute('''
#         SELECT * FROM events 
#         WHERE place_id = ? 
#         ORDER BY start_datetime DESC
#     ''', (place_id,)).fetchall()
#     conn.close()
    
#     return render_template('place_detail.html', place=place, events=events, config=Config)

# @app.route('/places/<int:place_id>/edit', methods=['POST'])
# def place_edit(place_id):
#     data = {
#         'name': request.form.get('name'),
#         'type': request.form.get('type'),
#         'latitude': request.form.get('latitude'),
#         'longitude': request.form.get('longitude'),
#         'altitude_meters': request.form.get('altitude_meters'),
#         'city': request.form.get('city'),
#         'country': request.form.get('country'),
#         'visit_status': request.form.get('visit_status'),
#         'my_rating': request.form.get('my_rating'),
#         'description': request.form.get('description'),
#         'tags': request.form.get('tags'),
#         'attributes': {
#             'vibe': request.form.get('vibe'),
#             'wifi': request.form.get('wifi'),
#             'parking': request.form.get('parking')
#         }
#     }
    
#     place_model.update(place_id, data)
#     flash('Place updated successfully!', 'success')
#     return redirect(url_for('place_detail', place_id=place_id))

# @app.route('/places/<int:place_id>/delete', methods=['POST'])
# def place_delete(place_id):
#     place = place_model.get_by_id(place_id)
#     name = place['name'] if place else "Place"
    
#     place_model.delete(place_id)
#     flash(f'{name} deleted successfully!', 'success')
#     return redirect(url_for('places_list'))

# # ============= EVENTS ROUTES =============
# @app.route('/events')
# def events_list():
#     events = event_model.get_all()
#     return render_template('events.html', events=events, config=Config)

# @app.route('/events/add', methods=['GET', 'POST'])
# def event_add():
#     if request.method == 'POST':
#         data = {
#             'title': request.form.get('title'),
#             'event_type': request.form.get('event_type'),
#             'place_id': request.form.get('place_id'),
#             'start_datetime': request.form.get('start_datetime'),
#             'end_datetime': request.form.get('end_datetime'),
#             'description': request.form.get('description'),
#             'transport_mode': request.form.get('transport_mode'),
#             'expense_amount': request.form.get('expense_amount'),
#             'weather': request.form.get('weather'),
#             'mood': request.form.get('mood'),
#             'tags': request.form.get('tags'),
#             'context': {
#                 'accommodation': request.form.get('accommodation'),
#                 'highlights': request.form.get('highlights')
#             }
#         }
        
#         event_id = event_model.create(data)
        
#         # Add participants
#         participant_ids = request.form.getlist('participants')
#         if participant_ids:
#             conn = db.get_connection()
#             for pid in participant_ids:
#                 conn.execute('INSERT INTO event_participants (event_id, person_id) VALUES (?, ?)',
#                            (event_id, pid))
#             conn.commit()
#             conn.close()
        
#         flash(f'Event "{data["title"]}" added successfully!', 'success')
#         return redirect(url_for('event_detail', event_id=event_id))
    
#     # GET - show form
#     conn = db.get_connection()
#     places = conn.execute('SELECT id, name FROM places ORDER BY name').fetchall()
#     people = conn.execute('SELECT id, first_name, last_name FROM people WHERE archived=0 ORDER BY first_name').fetchall()
#     conn.close()
    
#     return render_template('event_detail.html', event=None, places=places, people=people, config=Config)

# @app.route('/events/<int:event_id>')
# def event_detail(event_id):
#     event = event_model.get_by_id(event_id)
#     if not event:
#         flash('Event not found', 'error')
#         return redirect(url_for('events_list'))
    
#     event = dict(event)
#     event['context'] = parse_json_safely(event.get('context_json'))
    
#     participants = event_model.get_participants(event_id)
    
#     conn = db.get_connection()
#     places = conn.execute('SELECT id, name FROM places ORDER BY name').fetchall()
#     people = conn.execute('SELECT id, first_name, last_name FROM people WHERE archived=0 ORDER BY first_name').fetchall()
#     conn.close()
    
#     return render_template('event_detail.html', 
#                          event=event, 
#                          participants=participants,
#                          places=places,
#                          people=people,
#                          config=Config)

# @app.route('/events/<int:event_id>/delete', methods=['POST'])
# def event_delete(event_id):
#     event = event_model.get_by_id(event_id)
#     title = event['title'] if event else "Event"
    
#     event_model.delete(event_id)
#     flash(f'Event "{title}" deleted successfully!', 'success')
#     return redirect(url_for('events_list'))

# # ============= SEARCH =============
# @app.route('/search')
# def search():
#     query = request.args.get('q', '')
#     if not query:
#         return render_template('search.html', query='', results={'people': [], 'places': [], 'events': []})
    
#     results = {
#         'people': person_model.search(query),
#         'places': place_model.search(query),
#         'events': []  # Implement event search if needed
#     }
    
#     return render_template('search.html', query=query, results=results)

# # ============= API ENDPOINTS =============
# @app.route('/api/stats')
# def api_stats():
#     conn = db.get_connection()
#     stats = {
#         'people': conn.execute('SELECT COUNT(*) FROM people WHERE archived=0').fetchone()[0],
#         'places': conn.execute('SELECT COUNT(*) FROM places WHERE archived=0').fetchone()[0],
#         'events': conn.execute('SELECT COUNT(*) FROM events').fetchone()[0],
#     }
#     conn.close()
#     return jsonify(stats)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)


# --------------------------------------------------------------------------------------------------------


# # app.py - UPDATED ROUTES

# from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# import sqlite3
# import json
# from datetime import datetime
# from config import Config
# from models import PersonModel, PlaceModel, EventModel, Database

# app = Flask(__name__)
# app.config.from_object(Config)

# db = Database()
# person_model = PersonModel()
# place_model = PlaceModel()
# event_model = EventModel()

# # Helper function
# def parse_json_safely(json_str):
#     try:
#         return json.loads(json_str) if json_str else {}
#     except:
#         return {}

# # ============= DASHBOARD =============
# @app.route('/')
# def index():
#     conn = db.get_connection()
    
#     # Get statistics
#     stats = {
#         'people_count': conn.execute('SELECT COUNT(*) FROM people WHERE archived=0').fetchone()[0],
#         'places_count': conn.execute('SELECT COUNT(*) FROM places WHERE archived=0').fetchone()[0],
#         'events_count': conn.execute('SELECT COUNT(*) FROM events').fetchone()[0],
#         'relationships_count': conn.execute('SELECT COUNT(*) FROM relationships WHERE is_active=1').fetchone()[0],
#     }
    
#     # Recent activity
#     recent_events = conn.execute('''
#         SELECT e.*, p.name as place_name 
#         FROM events e 
#         LEFT JOIN places p ON e.place_id = p.id 
#         ORDER BY e.start_datetime DESC LIMIT 5
#     ''').fetchall()
    
#     # Upcoming birthdays (simplified)
#     upcoming_birthdays = conn.execute('''
#         SELECT id, first_name, last_name, dob 
#         FROM people 
#         WHERE dob IS NOT NULL AND archived=0
#         ORDER BY substr(dob, 6) LIMIT 5
#     ''').fetchall()
    
#     conn.close()
    
#     return render_template('index.html', 
#                          stats=stats,
#                          recent_events=recent_events,
#                          upcoming_birthdays=upcoming_birthdays)

# # ============= PEOPLE ROUTES =============
# @app.route('/people')
# def people_list():
#     people = person_model.get_all()
#     return render_template('people.html', people=people, config=Config)

# @app.route('/people/add', methods=['GET', 'POST'])
# def person_add():
#     if request.method == 'POST':
#         # Create person
#         data = {
#             'first_name': request.form.get('first_name'),
#             'middle_name': request.form.get('middle_name'),
#             'last_name': request.form.get('last_name'),
#             'maiden_name': request.form.get('maiden_name'),
#             'nickname': request.form.get('nickname'),
#             'prefix': request.form.get('prefix'),
#             'gender': request.form.get('gender'),
#             'pronouns': request.form.get('pronouns'),
#             'dob': request.form.get('dob'),
#             'blood_group': request.form.get('blood_group'),
#             'nationality': request.form.get('nationality'),
#             'primary_phone': request.form.get('primary_phone'),
#             'primary_email': request.form.get('primary_email'),
#             'current_city': request.form.get('current_city'),
#             'current_country': request.form.get('current_country'),
#             'hometown': request.form.get('hometown'),
#             'occupation': request.form.get('occupation'),
#             'company': request.form.get('company'),
#             'bio': request.form.get('bio'),
#             'notes': request.form.get('notes'),
#             'attributes': {
#                 'diet': request.form.get('diet'),
#                 'hobbies': request.form.get('hobbies'),
#                 'languages': request.form.get('languages'),
#                 'skills': request.form.get('skills'),
#                 'interests': request.form.get('interests'),
#                 'social_handles': {
#                     'instagram': request.form.get('instagram'),
#                     'linkedin': request.form.get('linkedin'),
#                     'twitter': request.form.get('twitter'),
#                     'github': request.form.get('github'),
#                     'facebook': request.form.get('facebook')
#                 },
#                 'preferences': {
#                     'clothing_size': request.form.get('clothing_size'),
#                     'shoe_size': request.form.get('shoe_size'),
#                     'favorite_color': request.form.get('favorite_color'),
#                     'favorite_food': request.form.get('favorite_food')
#                 },
#                 'health': {
#                     'allergies': request.form.get('allergies'),
#                     'medications': request.form.get('medications'),
#                     'emergency_contact': request.form.get('emergency_contact')
#                 }
#             }
#         }
        
#         person_id = person_model.create(data)
        
#         # Add to groups if specified
#         group_ids = request.form.getlist('group_ids')
#         if group_ids:
#             conn = db.get_connection()
#             for group_id in group_ids:
#                 if group_id:  # Skip empty values
#                     conn.execute('INSERT INTO person_groups (person_id, group_id, joined_date) VALUES (?, ?, ?)',
#                                 (person_id, group_id, datetime.now().date().isoformat()))
#             conn.commit()
#             conn.close()
        
#         # Add additional contacts
#         contact_types = request.form.getlist('contact_type[]')
#         contact_values = request.form.getlist('contact_value[]')
#         contact_labels = request.form.getlist('contact_label[]')
        
#         if contact_types:
#             conn = db.get_connection()
#             for i, ctype in enumerate(contact_types):
#                 if ctype and i < len(contact_values) and contact_values[i]:
#                     label = contact_labels[i] if i < len(contact_labels) else ''
#                     conn.execute('INSERT INTO contacts (person_id, type, value, label) VALUES (?, ?, ?, ?)',
#                                (person_id, ctype, contact_values[i], label))
#             conn.commit()
#             conn.close()
        
#         flash(f'Person "{data["first_name"]}" added successfully!', 'success')
#         return redirect(url_for('person_detail', person_id=person_id))
    
#     # GET request - show form with all necessary data
#     conn = db.get_connection()
#     groups = conn.execute('SELECT * FROM groups ORDER BY name').fetchall()
#     all_people = conn.execute('SELECT id, first_name, last_name FROM people WHERE archived=0 ORDER BY first_name').fetchall()
#     conn.close()
    
#     return render_template('person_detail.html', 
#                           person=None, 
#                           groups=groups,
#                           all_groups=groups,
#                           all_people=all_people,
#                           relationships=[],
#                           events=[],
#                           contacts=[],
#                           addresses=[],
#                           education=[],
#                           career=[],
#                           config=Config)

# @app.route('/people/<int:person_id>')
# def person_detail(person_id):
#     person = person_model.get_by_id(person_id)
#     if not person:
#         flash('Person not found', 'error')
#         return redirect(url_for('people_list'))
    
#     # Parse JSON attributes
#     person = dict(person)
#     person['attributes'] = parse_json_safely(person.get('attributes_json'))
    
#     # Get relationships
#     relationships = person_model.get_relationships(person_id)
    
#     # Get additional contacts
#     conn = db.get_connection()
#     contacts = conn.execute('SELECT * FROM contacts WHERE person_id = ?', (person_id,)).fetchall()
    
#     # Get addresses
#     addresses = conn.execute('SELECT * FROM addresses WHERE person_id = ? ORDER BY is_current DESC', (person_id,)).fetchall()
    
#     # Get education
#     education = conn.execute('SELECT * FROM education WHERE person_id = ? ORDER BY end_year DESC', (person_id,)).fetchall()
    
#     # Get career
#     career = conn.execute('SELECT * FROM career WHERE person_id = ? ORDER BY is_current DESC, end_date DESC', (person_id,)).fetchall()
    
#     # Get events
#     events = conn.execute('''
#         SELECT e.*, p.name as place_name
#         FROM events e
#         JOIN event_participants ep ON e.id = ep.event_id
#         LEFT JOIN places p ON e.place_id = p.id
#         WHERE ep.person_id = ?
#         ORDER BY e.start_datetime DESC LIMIT 10
#     ''', (person_id,)).fetchall()
    
#     # Get groups
#     person_groups = conn.execute('''
#         SELECT g.* FROM groups g
#         JOIN person_groups pg ON g.id = pg.group_id
#         WHERE pg.person_id = ?
#     ''', (person_id,)).fetchall()
    
#     all_groups = conn.execute('SELECT * FROM groups ORDER BY name').fetchall()
#     all_people = conn.execute('SELECT id, first_name, last_name FROM people WHERE id != ? AND archived=0 ORDER BY first_name', (person_id,)).fetchall()
    
#     conn.close()
    
#     return render_template('person_detail.html', 
#                          person=person, 
#                          relationships=relationships,
#                          events=events,
#                          contacts=contacts,
#                          addresses=addresses,
#                          education=education,
#                          career=career,
#                          groups=person_groups,
#                          all_groups=all_groups,
#                          all_people=all_people,
#                          config=Config)

# @app.route('/people/<int:person_id>/edit', methods=['POST'])
# def person_edit(person_id):
#     data = {
#         'first_name': request.form.get('first_name'),
#         'middle_name': request.form.get('middle_name'),
#         'last_name': request.form.get('last_name'),
#         'maiden_name': request.form.get('maiden_name'),
#         'nickname': request.form.get('nickname'),
#         'prefix': request.form.get('prefix'),
#         'gender': request.form.get('gender'),
#         'pronouns': request.form.get('pronouns'),
#         'dob': request.form.get('dob'),
#         'blood_group': request.form.get('blood_group'),
#         'nationality': request.form.get('nationality'),
#         'primary_phone': request.form.get('primary_phone'),
#         'primary_email': request.form.get('primary_email'),
#         'current_city': request.form.get('current_city'),
#         'current_country': request.form.get('current_country'),
#         'hometown': request.form.get('hometown'),
#         'occupation': request.form.get('occupation'),
#         'company': request.form.get('company'),
#         'bio': request.form.get('bio'),
#         'notes': request.form.get('notes'),
#         'attributes': {
#             'diet': request.form.get('diet'),
#             'hobbies': request.form.get('hobbies'),
#             'languages': request.form.get('languages'),
#             'skills': request.form.get('skills'),
#             'social_handles': {
#                 'instagram': request.form.get('instagram'),
#                 'linkedin': request.form.get('linkedin'),
#                 'twitter': request.form.get('twitter'),
#                 'github': request.form.get('github')
#             }
#         }
#     }
    
#     person_model.update(person_id, data)
#     flash('Person updated successfully!', 'success')
#     return redirect(url_for('person_detail', person_id=person_id))

# @app.route('/people/<int:person_id>/delete', methods=['POST'])
# def person_delete(person_id):
#     person = person_model.get_by_id(person_id)
#     name = f"{person['first_name']} {person['last_name']}" if person else "Person"
    
#     person_model.delete(person_id)
#     flash(f'{name} deleted successfully!', 'success')
#     return redirect(url_for('people_list'))

# # ============= RELATIONSHIP ROUTES =============
# @app.route('/people/<int:person_id>/relationships/add', methods=['POST'])
# def relationship_add(person_id):
#     related_person_id = request.form.get('related_person_id')
#     relationship_type = request.form.get('relationship_type')
#     reverse_type = request.form.get('reverse_relationship_type')
#     meeting_date = request.form.get('meeting_date')
#     meeting_context = request.form.get('meeting_context')
#     notes = request.form.get('notes')
    
#     conn = db.get_connection()
#     conn.execute('''INSERT INTO relationships 
#                     (person_a_id, person_b_id, relationship_type, reverse_relationship_type, 
#                      meeting_date, meeting_context, notes, start_date)
#                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
#                  (person_id, related_person_id, relationship_type, reverse_type,
#                   meeting_date, meeting_context, notes, meeting_date or datetime.now().date().isoformat()))
#     conn.commit()
#     conn.close()
    
#     flash('Relationship added successfully!', 'success')
#     return redirect(url_for('person_detail', person_id=person_id))

# @app.route('/relationships/<int:relationship_id>/delete', methods=['POST'])
# def relationship_delete(relationship_id):
#     person_id = request.form.get('person_id')
#     conn = db.get_connection()
#     conn.execute('DELETE FROM relationships WHERE id = ?', (relationship_id,))
#     conn.commit()
#     conn.close()
    
#     flash('Relationship deleted successfully!', 'success')
#     return redirect(url_for('person_detail', person_id=person_id))

# # ============= PLACES ROUTES (keep existing) =============
# # ... (your existing place routes)
# # ============= PLACES ROUTES =============
# @app.route('/places')
# def places_list():
#     places = place_model.get_all()
#     return render_template('places.html', places=places, config=Config)

# @app.route('/places/add', methods=['GET', 'POST'])
# def place_add():
#     if request.method == 'POST':
#         data = {
#             'name': request.form.get('name'),
#             'type': request.form.get('type'),
#             'latitude': request.form.get('latitude'),
#             'longitude': request.form.get('longitude'),
#             'altitude_meters': request.form.get('altitude_meters'),
#             'city': request.form.get('city'),
#             'country': request.form.get('country'),
#             'visit_status': request.form.get('visit_status'),
#             'my_rating': request.form.get('my_rating'),
#             'description': request.form.get('description'),
#             'tags': request.form.get('tags'),
#             'attributes': {
#                 'vibe': request.form.get('vibe'),
#                 'wifi': request.form.get('wifi'),
#                 'parking': request.form.get('parking'),
#                 'best_season': request.form.get('best_season')
#             }
#         }
        
#         place_id = place_model.create(data)
#         flash(f'Place "{data["name"]}" added successfully!', 'success')
#         return redirect(url_for('place_detail', place_id=place_id))
    
#     return render_template('place_detail.html', place=None, config=Config)

# @app.route('/places/<int:place_id>')
# def place_detail(place_id):
#     place = place_model.get_by_id(place_id)
#     if not place:
#         flash('Place not found', 'error')
#         return redirect(url_for('places_list'))
    
#     place = dict(place)
#     place['attributes'] = parse_json_safely(place.get('attributes_json'))
    
#     # Get events at this place
#     conn = db.get_connection()
#     events = conn.execute('''
#         SELECT * FROM events 
#         WHERE place_id = ? 
#         ORDER BY start_datetime DESC
#     ''', (place_id,)).fetchall()
#     conn.close()
    
#     return render_template('place_detail.html', place=place, events=events, config=Config)

# @app.route('/places/<int:place_id>/edit', methods=['POST'])
# def place_edit(place_id):
#     data = {
#         'name': request.form.get('name'),
#         'type': request.form.get('type'),
#         'latitude': request.form.get('latitude'),
#         'longitude': request.form.get('longitude'),
#         'altitude_meters': request.form.get('altitude_meters'),
#         'city': request.form.get('city'),
#         'country': request.form.get('country'),
#         'visit_status': request.form.get('visit_status'),
#         'my_rating': request.form.get('my_rating'),
#         'description': request.form.get('description'),
#         'tags': request.form.get('tags'),
#         'attributes': {
#             'vibe': request.form.get('vibe'),
#             'wifi': request.form.get('wifi'),
#             'parking': request.form.get('parking')
#         }
#     }
    
#     place_model.update(place_id, data)
#     flash('Place updated successfully!', 'success')
#     return redirect(url_for('place_detail', place_id=place_id))

# @app.route('/places/<int:place_id>/delete', methods=['POST'])
# def place_delete(place_id):
#     place = place_model.get_by_id(place_id)
#     name = place['name'] if place else "Place"
    
#     place_model.delete(place_id)
#     flash(f'{name} deleted successfully!', 'success')
#     return redirect(url_for('places_list'))


# # ============= EVENTS ROUTES (keep existing) =============
# # ... (your existing event routes)
# # ============= EVENTS ROUTES =============
# @app.route('/events')
# def events_list():
#     events = event_model.get_all()
#     return render_template('events.html', events=events, config=Config)

# @app.route('/events/add', methods=['GET', 'POST'])
# def event_add():
#     if request.method == 'POST':
#         data = {
#             'title': request.form.get('title'),
#             'event_type': request.form.get('event_type'),
#             'place_id': request.form.get('place_id'),
#             'start_datetime': request.form.get('start_datetime'),
#             'end_datetime': request.form.get('end_datetime'),
#             'description': request.form.get('description'),
#             'transport_mode': request.form.get('transport_mode'),
#             'expense_amount': request.form.get('expense_amount'),
#             'weather': request.form.get('weather'),
#             'mood': request.form.get('mood'),
#             'tags': request.form.get('tags'),
#             'context': {
#                 'accommodation': request.form.get('accommodation'),
#                 'highlights': request.form.get('highlights')
#             }
#         }
        
#         event_id = event_model.create(data)
        
#         # Add participants
#         participant_ids = request.form.getlist('participants')
#         if participant_ids:
#             conn = db.get_connection()
#             for pid in participant_ids:
#                 conn.execute('INSERT INTO event_participants (event_id, person_id) VALUES (?, ?)',
#                            (event_id, pid))
#             conn.commit()
#             conn.close()
        
#         flash(f'Event "{data["title"]}" added successfully!', 'success')
#         return redirect(url_for('event_detail', event_id=event_id))
    
#     # GET - show form
#     conn = db.get_connection()
#     places = conn.execute('SELECT id, name FROM places ORDER BY name').fetchall()
#     people = conn.execute('SELECT id, first_name, last_name FROM people WHERE archived=0 ORDER BY first_name').fetchall()
#     conn.close()
    
#     return render_template('event_detail.html', event=None, places=places, people=people, config=Config)

# @app.route('/events/<int:event_id>')
# def event_detail(event_id):
#     event = event_model.get_by_id(event_id)
#     if not event:
#         flash('Event not found', 'error')
#         return redirect(url_for('events_list'))
    
#     event = dict(event)
#     event['context'] = parse_json_safely(event.get('context_json'))
    
#     participants = event_model.get_participants(event_id)
    
#     conn = db.get_connection()
#     places = conn.execute('SELECT id, name FROM places ORDER BY name').fetchall()
#     people = conn.execute('SELECT id, first_name, last_name FROM people WHERE archived=0 ORDER BY first_name').fetchall()
#     conn.close()
    
#     return render_template('event_detail.html', 
#                          event=event, 
#                          participants=participants,
#                          places=places,
#                          people=people,
#                          config=Config)

# @app.route('/events/<int:event_id>/delete', methods=['POST'])
# def event_delete(event_id):
#     event = event_model.get_by_id(event_id)
#     title = event['title'] if event else "Event"
    
#     event_model.delete(event_id)
#     flash(f'Event "{title}" deleted successfully!', 'success')
#     return redirect(url_for('events_list'))


# # ============= SEARCH =============
# @app.route('/search')
# def search():
#     query = request.args.get('q', '')
#     if not query:
#         return render_template('search.html', query='', results={'people': [], 'places': [], 'events': []})
    
#     results = {
#         'people': person_model.search(query),
#         'places': place_model.search(query),
#         'events': []
#     }
    
#     return render_template('search.html', query=query, results=results)

# # ============= API ENDPOINTS =============
# @app.route('/api/stats')
# def api_stats():
#     conn = db.get_connection()
#     stats = {
#         'people': conn.execute('SELECT COUNT(*) FROM people WHERE archived=0').fetchone()[0],
#         'places': conn.execute('SELECT COUNT(*) FROM places WHERE archived=0').fetchone()[0],
#         'events': conn.execute('SELECT COUNT(*) FROM events').fetchone()[0],
#     }
#     conn.close()
#     return jsonify(stats)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)


# --------------------------------------------------------------------------------------------------------

# app.py - Complete Personal CRM Flask Application
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import json
from datetime import datetime
from config import Config
from models import PersonModel, PlaceModel, EventModel, Database

# ============= FLASK APP INITIALIZATION =============
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database and models
db = Database()
person_model = PersonModel()
place_model = PlaceModel()
event_model = EventModel()

# ============= HELPER FUNCTIONS =============
def parse_json_safely(json_str):
    """Safely parse JSON string, return empty dict if invalid"""
    try:
        return json.loads(json_str) if json_str else {}
    except:
        return {}

# ============= DASHBOARD =============
@app.route('/')
def index():
    """Main dashboard with statistics and recent activity"""
    conn = db.get_connection()
    
    # Get statistics
    stats = {
        'people_count': conn.execute('SELECT COUNT(*) FROM people WHERE archived=0').fetchone()[0],
        'places_count': conn.execute('SELECT COUNT(*) FROM places WHERE archived=0').fetchone()[0],
        'events_count': conn.execute('SELECT COUNT(*) FROM events').fetchone()[0],
        'relationships_count': conn.execute('SELECT COUNT(*) FROM relationships WHERE is_active=1').fetchone()[0],
    }
    
    # Recent activity
    recent_events = conn.execute('''
        SELECT e.*, p.name as place_name 
        FROM events e 
        LEFT JOIN places p ON e.place_id = p.id 
        ORDER BY e.start_datetime DESC LIMIT 5
    ''').fetchall()
    
    # Upcoming birthdays
    upcoming_birthdays = conn.execute('''
        SELECT id, first_name, last_name, dob 
        FROM people 
        WHERE dob IS NOT NULL AND archived=0
        ORDER BY substr(dob, 6) LIMIT 5
    ''').fetchall()
    
    conn.close()
    
    return render_template('index.html', 
                         stats=stats,
                         recent_events=recent_events,
                         upcoming_birthdays=upcoming_birthdays)

# ============= PEOPLE MANAGEMENT =============

@app.route('/people')
def people_list():
    """Display all people as cards"""
    people = person_model.get_all()
    return render_template('people.html', people=people, config=Config)

@app.route('/people/add', methods=['GET', 'POST'])
def person_add():
    """Add a new person - GET shows form, POST creates person"""
    if request.method == 'POST':
        # Collect all form data
        data = {
            # Basic identity
            'first_name': request.form.get('first_name'),
            'middle_name': request.form.get('middle_name'),
            'last_name': request.form.get('last_name'),
            'maiden_name': request.form.get('maiden_name'),
            'nickname': request.form.get('nickname'),
            'prefix': request.form.get('prefix'),
            
            # Personal details
            'gender': request.form.get('gender'),
            'pronouns': request.form.get('pronouns'),
            'dob': request.form.get('dob'),
            'blood_group': request.form.get('blood_group'),
            'nationality': request.form.get('nationality'),
            
            # Contact info
            'primary_phone': request.form.get('primary_phone'),
            'primary_email': request.form.get('primary_email'),
            
            # Location
            'current_city': request.form.get('current_city'),
            'current_country': request.form.get('current_country'),
            'hometown': request.form.get('hometown'),
            
            # Professional
            'occupation': request.form.get('occupation'),
            'company': request.form.get('company'),
            
            # Notes
            'bio': request.form.get('bio'),
            'notes': request.form.get('notes'),
            
            # JSON attributes
            'attributes': {
                'diet': request.form.get('diet'),
                'hobbies': request.form.get('hobbies'),
                'languages': request.form.get('languages'),
                'skills': request.form.get('skills'),
                'interests': request.form.get('interests'),
                'social_handles': {
                    'instagram': request.form.get('instagram'),
                    'linkedin': request.form.get('linkedin'),
                    'twitter': request.form.get('twitter'),
                    'github': request.form.get('github'),
                    'facebook': request.form.get('facebook')
                },
                'preferences': {
                    'clothing_size': request.form.get('clothing_size'),
                    'shoe_size': request.form.get('shoe_size'),
                    'favorite_color': request.form.get('favorite_color'),
                    'favorite_food': request.form.get('favorite_food')
                },
                'health': {
                    'allergies': request.form.get('allergies'),
                    'medications': request.form.get('medications'),
                    'emergency_contact': request.form.get('emergency_contact')
                }
            }
        }
        
        # Create person in database
        person_id = person_model.create(data)
        
        # Add to groups if specified
        group_ids = request.form.getlist('group_ids')
        if group_ids:
            conn = db.get_connection()
            for group_id in group_ids:
                if group_id:  # Skip empty values
                    conn.execute('INSERT INTO person_groups (person_id, group_id, joined_date) VALUES (?, ?, ?)',
                                (person_id, group_id, datetime.now().date().isoformat()))
            conn.commit()
            conn.close()
        
        # Add additional contacts
        contact_types = request.form.getlist('contact_type[]')
        contact_values = request.form.getlist('contact_value[]')
        contact_labels = request.form.getlist('contact_label[]')
        
        if contact_types:
            conn = db.get_connection()
            for i, ctype in enumerate(contact_types):
                if ctype and i < len(contact_values) and contact_values[i]:
                    label = contact_labels[i] if i < len(contact_labels) else ''
                    conn.execute('INSERT INTO contacts (person_id, type, value, label) VALUES (?, ?, ?, ?)',
                               (person_id, ctype, contact_values[i], label))
            conn.commit()
            conn.close()
        
        flash(f'Person "{data["first_name"]}" added successfully!', 'success')
        return redirect(url_for('person_detail', person_id=person_id))
    
    # GET request - show empty form
    conn = db.get_connection()
    groups = conn.execute('SELECT * FROM groups ORDER BY name').fetchall()
    all_people = conn.execute('SELECT id, first_name, last_name FROM people WHERE archived=0 ORDER BY first_name').fetchall()
    conn.close()
    
    return render_template('person_detail.html', 
                          person=None, 
                          groups=[],
                          all_groups=groups,
                          all_people=all_people,
                          relationships=[],
                          events=[],
                          contacts=[],
                          addresses=[],
                          education=[],
                          career=[],
                          config=Config)

@app.route('/people/<int:person_id>')
def person_detail(person_id):
    """View/edit a specific person's details"""
    person = person_model.get_by_id(person_id)
    if not person:
        flash('Person not found', 'error')
        return redirect(url_for('people_list'))
    
    # Convert to dict and parse JSON
    person = dict(person)
    person['attributes'] = parse_json_safely(person.get('attributes_json'))
    
    # Get all related data
    conn = db.get_connection()
    
    # Relationships
    relationships = person_model.get_relationships(person_id)
    
    # Additional contacts
    contacts = conn.execute('SELECT * FROM contacts WHERE person_id = ?', (person_id,)).fetchall()
    
    # Addresses
    addresses = conn.execute('SELECT * FROM addresses WHERE person_id = ? ORDER BY is_current DESC', (person_id,)).fetchall()
    
    # Education
    education = conn.execute('SELECT * FROM education WHERE person_id = ? ORDER BY end_year DESC', (person_id,)).fetchall()
    
    # Career
    career = conn.execute('SELECT * FROM career WHERE person_id = ? ORDER BY is_current DESC, end_date DESC', (person_id,)).fetchall()
    
    # Events
    events = conn.execute('''
        SELECT e.*, p.name as place_name
        FROM events e
        JOIN event_participants ep ON e.id = ep.event_id
        LEFT JOIN places p ON e.place_id = p.id
        WHERE ep.person_id = ?
        ORDER BY e.start_datetime DESC LIMIT 10
    ''', (person_id,)).fetchall()
    
    # Groups this person belongs to
    person_groups = conn.execute('''
        SELECT g.* FROM groups g
        JOIN person_groups pg ON g.id = pg.group_id
        WHERE pg.person_id = ?
    ''', (person_id,)).fetchall()
    
    # All groups (for dropdown)
    all_groups = conn.execute('SELECT * FROM groups ORDER BY name').fetchall()
    
    # All other people (for relationship dropdown)
    all_people = conn.execute('SELECT id, first_name, last_name FROM people WHERE id != ? AND archived=0 ORDER BY first_name', (person_id,)).fetchall()
    
    conn.close()
    
    return render_template('person_detail.html', 
                         person=person, 
                         relationships=relationships,
                         events=events,
                         contacts=contacts,
                         addresses=addresses,
                         education=education,
                         career=career,
                         groups=person_groups,
                         all_groups=all_groups,
                         all_people=all_people,
                         config=Config)

@app.route('/people/<int:person_id>/edit', methods=['POST'])
def person_edit(person_id):
    """Update person details"""
    data = {
        'first_name': request.form.get('first_name'),
        'middle_name': request.form.get('middle_name'),
        'last_name': request.form.get('last_name'),
        'maiden_name': request.form.get('maiden_name'),
        'nickname': request.form.get('nickname'),
        'prefix': request.form.get('prefix'),
        'gender': request.form.get('gender'),
        'pronouns': request.form.get('pronouns'),
        'dob': request.form.get('dob'),
        'blood_group': request.form.get('blood_group'),
        'nationality': request.form.get('nationality'),
        'primary_phone': request.form.get('primary_phone'),
        'primary_email': request.form.get('primary_email'),
        'current_city': request.form.get('current_city'),
        'current_country': request.form.get('current_country'),
        'hometown': request.form.get('hometown'),
        'occupation': request.form.get('occupation'),
        'company': request.form.get('company'),
        'bio': request.form.get('bio'),
        'notes': request.form.get('notes'),
        'attributes': {
            'diet': request.form.get('diet'),
            'hobbies': request.form.get('hobbies'),
            'languages': request.form.get('languages'),
            'skills': request.form.get('skills'),
            'social_handles': {
                'instagram': request.form.get('instagram'),
                'linkedin': request.form.get('linkedin'),
                'twitter': request.form.get('twitter'),
                'github': request.form.get('github')
            }
        }
    }
    
    person_model.update(person_id, data)
    flash('Person updated successfully!', 'success')
    return redirect(url_for('person_detail', person_id=person_id))

@app.route('/people/<int:person_id>/delete', methods=['POST'])
def person_delete(person_id):
    """Delete a person"""
    person = person_model.get_by_id(person_id)
    name = f"{person['first_name']} {person['last_name']}" if person else "Person"
    
    person_model.delete(person_id)
    flash(f'{name} deleted successfully!', 'success')
    return redirect(url_for('people_list'))

# ============= RELATIONSHIP MANAGEMENT =============

@app.route('/people/<int:person_id>/relationships/add', methods=['POST'])
def relationship_add(person_id):
    """Add a relationship between two people"""
    related_person_id = request.form.get('related_person_id')
    relationship_type = request.form.get('relationship_type')
    reverse_type = request.form.get('reverse_relationship_type')
    meeting_date = request.form.get('meeting_date')
    meeting_context = request.form.get('meeting_context')
    notes = request.form.get('notes')
    
    conn = db.get_connection()
    conn.execute('''INSERT INTO relationships 
                    (person_a_id, person_b_id, relationship_type, reverse_relationship_type, 
                     meeting_date, meeting_context, notes, start_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                 (person_id, related_person_id, relationship_type, reverse_type,
                  meeting_date, meeting_context, notes, meeting_date or datetime.now().date().isoformat()))
    conn.commit()
    conn.close()
    
    flash('Relationship added successfully!', 'success')
    return redirect(url_for('person_detail', person_id=person_id))

@app.route('/relationships/<int:relationship_id>/delete', methods=['POST'])
def relationship_delete(relationship_id):
    """Delete a relationship"""
    person_id = request.form.get('person_id')
    
    conn = db.get_connection()
    conn.execute('DELETE FROM relationships WHERE id = ?', (relationship_id,))
    conn.commit()
    conn.close()
    
    flash('Relationship deleted successfully!', 'success')
    return redirect(url_for('person_detail', person_id=person_id))

# ============= PLACES MANAGEMENT =============

@app.route('/places')
def places_list():
    """Display all places as cards"""
    places = place_model.get_all()
    return render_template('places.html', places=places, config=Config)

@app.route('/places/add', methods=['GET', 'POST'])
def place_add():
    """Add a new place"""
    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'type': request.form.get('type'),
            'latitude': request.form.get('latitude'),
            'longitude': request.form.get('longitude'),
            'altitude_meters': request.form.get('altitude_meters'),
            'city': request.form.get('city'),
            'country': request.form.get('country'),
            'visit_status': request.form.get('visit_status'),
            'my_rating': request.form.get('my_rating'),
            'description': request.form.get('description'),
            'tags': request.form.get('tags'),
            'attributes': {
                'vibe': request.form.get('vibe'),
                'wifi': request.form.get('wifi'),
                'parking': request.form.get('parking'),
                'best_season': request.form.get('best_season')
            }
        }
        
        place_id = place_model.create(data)
        flash(f'Place "{data["name"]}" added successfully!', 'success')
        return redirect(url_for('place_detail', place_id=place_id))
    
    return render_template('place_detail.html', place=None, events=[], config=Config)

@app.route('/places/<int:place_id>')
def place_detail(place_id):
    """View/edit a specific place"""
    place = place_model.get_by_id(place_id)
    if not place:
        flash('Place not found', 'error')
        return redirect(url_for('places_list'))
    
    place = dict(place)
    place['attributes'] = parse_json_safely(place.get('attributes_json'))
    
    # Get events at this place
    conn = db.get_connection()
    events = conn.execute('''
        SELECT * FROM events 
        WHERE place_id = ? 
        ORDER BY start_datetime DESC
    ''', (place_id,)).fetchall()
    conn.close()
    
    return render_template('place_detail.html', place=place, events=events, config=Config)

@app.route('/places/<int:place_id>/edit', methods=['POST'])
def place_edit(place_id):
    """Update place details"""
    data = {
        'name': request.form.get('name'),
        'type': request.form.get('type'),
        'latitude': request.form.get('latitude'),
        'longitude': request.form.get('longitude'),
        'altitude_meters': request.form.get('altitude_meters'),
        'city': request.form.get('city'),
        'country': request.form.get('country'),
        'visit_status': request.form.get('visit_status'),
        'my_rating': request.form.get('my_rating'),
        'description': request.form.get('description'),
        'tags': request.form.get('tags'),
        'attributes': {
            'vibe': request.form.get('vibe'),
            'wifi': request.form.get('wifi'),
            'parking': request.form.get('parking')
        }
    }
    
    place_model.update(place_id, data)
    flash('Place updated successfully!', 'success')
    return redirect(url_for('place_detail', place_id=place_id))

@app.route('/places/<int:place_id>/delete', methods=['POST'])
def place_delete(place_id):
    """Delete a place"""
    place = place_model.get_by_id(place_id)
    name = place['name'] if place else "Place"
    
    place_model.delete(place_id)
    flash(f'{name} deleted successfully!', 'success')
    return redirect(url_for('places_list'))

# ============= EVENTS MANAGEMENT =============

@app.route('/events')
def events_list():
    """Display all events"""
    events = event_model.get_all()
    return render_template('events.html', events=events, config=Config)

@app.route('/events/add', methods=['GET', 'POST'])
def event_add():
    """Add a new event"""
    if request.method == 'POST':
        data = {
            'title': request.form.get('title'),
            'event_type': request.form.get('event_type'),
            'place_id': request.form.get('place_id'),
            'start_datetime': request.form.get('start_datetime'),
            'end_datetime': request.form.get('end_datetime'),
            'description': request.form.get('description'),
            'transport_mode': request.form.get('transport_mode'),
            'expense_amount': request.form.get('expense_amount'),
            'weather': request.form.get('weather'),
            'mood': request.form.get('mood'),
            'tags': request.form.get('tags'),
            'context': {
                'accommodation': request.form.get('accommodation'),
                'highlights': request.form.get('highlights')
            }
        }
        
        event_id = event_model.create(data)
        
        # Add participants
        participant_ids = request.form.getlist('participants')
        if participant_ids:
            conn = db.get_connection()
            for pid in participant_ids:
                if pid:  # Skip empty values
                    conn.execute('INSERT INTO event_participants (event_id, person_id) VALUES (?, ?)',
                               (event_id, pid))
            conn.commit()
            conn.close()
        
        flash(f'Event "{data["title"]}" added successfully!', 'success')
        return redirect(url_for('event_detail', event_id=event_id))
    
    # GET - show form
    conn = db.get_connection()
    places = conn.execute('SELECT id, name FROM places ORDER BY name').fetchall()
    people = conn.execute('SELECT id, first_name, last_name FROM people WHERE archived=0 ORDER BY first_name').fetchall()
    conn.close()
    
    return render_template('event_detail.html', event=None, participants=[], places=places, people=people, config=Config)

@app.route('/events/<int:event_id>')
def event_detail(event_id):
    """View/edit a specific event"""
    event = event_model.get_by_id(event_id)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('events_list'))
    
    event = dict(event)
    event['context'] = parse_json_safely(event.get('context_json'))
    
    participants = event_model.get_participants(event_id)
    
    conn = db.get_connection()
    places = conn.execute('SELECT id, name FROM places ORDER BY name').fetchall()
    people = conn.execute('SELECT id, first_name, last_name FROM people WHERE archived=0 ORDER BY first_name').fetchall()
    conn.close()
    
    return render_template('event_detail.html', 
                         event=event, 
                         participants=participants,
                         places=places,
                         people=people,
                         config=Config)

@app.route('/events/<int:event_id>/delete', methods=['POST'])
def event_delete(event_id):
    """Delete an event"""
    event = event_model.get_by_id(event_id)
    title = event['title'] if event else "Event"
    
    event_model.delete(event_id)
    flash(f'Event "{title}" deleted successfully!', 'success')
    return redirect(url_for('events_list'))

# ============= SEARCH =============

@app.route('/search')
def search():
    """Global search across people, places, and events"""
    query = request.args.get('q', '')
    if not query:
        return render_template('search.html', query='', results={'people': [], 'places': [], 'events': []})
    
    results = {
        'people': person_model.search(query),
        'places': place_model.search(query),
        'events': []  # TODO: Implement event search
    }
    
    return render_template('search.html', query=query, results=results)

# ============= API ENDPOINTS =============

@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    conn = db.get_connection()
    stats = {
        'people': conn.execute('SELECT COUNT(*) FROM people WHERE archived=0').fetchone()[0],
        'places': conn.execute('SELECT COUNT(*) FROM places WHERE archived=0').fetchone()[0],
        'events': conn.execute('SELECT COUNT(*) FROM events').fetchone()[0],
    }
    conn.close()
    return jsonify(stats)

# ============= RELATIONSHIP GRAPH =============

@app.route('/relationships/graph')
def relationships_graph():
    """Visualize relationship network as an interactive graph"""
    conn = db.get_connection()
    
    # Get all people
    people = conn.execute('SELECT id, first_name, last_name, occupation FROM people WHERE archived=0').fetchall()
    
    # Get all active relationships
    relationships = conn.execute('''
        SELECT r.id, r.person_a_id, r.person_b_id, r.relationship_type, r.reverse_relationship_type,
               pa.first_name || " " || COALESCE(pa.last_name, "") as person_a_name,
               pb.first_name || " " || COALESCE(pb.last_name, "") as person_b_name
        FROM relationships r
        JOIN people pa ON r.person_a_id = pa.id
        JOIN people pb ON r.person_b_id = pb.id
        WHERE r.is_active = 1
    ''').fetchall()
    
    conn.close()
    
    # Prepare data for visualization
    nodes = []
    for person in people:
        nodes.append({
            'id': person['id'],
            'label': f"{person['first_name']} {person['last_name'] or ''}".strip(),
            'title': person['occupation'] or 'No occupation'
        })
    
    edges = []
    for rel in relationships:
        edges.append({
            'from': rel['person_a_id'],
            'to': rel['person_b_id'],
            'label': rel['relationship_type'],
            'arrows': 'to',
            'title': f"{rel['person_a_name']} → {rel['relationship_type']} → {rel['person_b_name']}"
        })
    
    return render_template('relationship_graph.html', 
                         nodes=nodes, 
                         edges=edges, 
                         people_count=len(people),
                         relationships_count=len(relationships))


# ============= RUN APPLICATION =============

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
