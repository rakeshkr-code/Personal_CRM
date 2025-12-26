# file: app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json

app = Flask(__name__)
DB_NAME = 'life.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

# --- ROUTES ---

@app.route('/')
def index():
    conn = get_db_connection()
    # Simple stats for dashboard
    people_count = conn.execute('SELECT COUNT(*) FROM people').fetchone()[0]
    places_count = conn.execute('SELECT COUNT(*) FROM places').fetchone()[0]
    events_count = conn.execute('SELECT COUNT(*) FROM events').fetchone()[0]
    conn.close()
    return render_template('index.html', stats=[people_count, places_count, events_count])

# --- PEOPLE ROUTES ---
@app.route('/people', methods=('GET', 'POST'))
def people():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['full_name']
        circle = request.form['circle']
        phone = request.form['phone']
        # Convert extra form fields into JSON
        details = {
            "diet": request.form.get('diet'),
            "hobbies": request.form.get('hobbies'),
            "social": request.form.get('social')
        }
        conn.execute('INSERT INTO people (full_name, relation_circle, phone, attributes_json) VALUES (?, ?, ?, ?)',
                     (name, circle, phone, json.dumps(details)))
        conn.commit()
        return redirect(url_for('people'))
    
    people = conn.execute('SELECT * FROM people').fetchall()
    conn.close()
    
    # Process JSON for display
    people_list = []
    for p in people:
        p_dict = dict(p)
        if p_dict['attributes_json']:
            p_dict['attributes'] = json.loads(p_dict['attributes_json'])
        people_list.append(p_dict)
        
    return render_template('people.html', people=people_list)

# --- PLACES ROUTES ---
@app.route('/places', methods=('GET', 'POST'))
def places():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        ptype = request.form['type']
        lat = request.form['lat']
        lon = request.form['lon']
        # Attributes to JSON
        attrs = {
            "vibe": request.form.get('vibe'),
            "wifi": request.form.get('wifi')
        }
        conn.execute('INSERT INTO places (name, type, latitude, longitude, attributes_json) VALUES (?, ?, ?, ?, ?)',
                     (name, ptype, lat, lon, json.dumps(attrs)))
        conn.commit()
        return redirect(url_for('places'))

    places = conn.execute('SELECT * FROM places').fetchall()
    conn.close()
    return render_template('places.html', places=places)

# --- QUERY EXAMPLE ROUTE ---
@app.route('/search')
def search():
    query = request.args.get('q')
    conn = get_db_connection()
    # Example: Searching inside the JSON column using SQLite's json_extract
    # Finds people who have "Vegan" in their diet preference
    sql = "SELECT * FROM people WHERE json_extract(attributes_json, '$.diet') LIKE ?"
    results = conn.execute(sql, ('%' + query + '%',)).fetchall()
    conn.close()
    return render_template('people.html', people=results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)