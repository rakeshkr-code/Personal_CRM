# 🏠 Personal CRM - Relationship Management System

A comprehensive Personal CRM (Customer Relationship Management) system designed to help you track people, places, events, and relationships in your personal and professional life. Built with Flask, SQLite, and Bootstrap 5.

![Personal CRM Dashboard](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-3.0+-red)

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [File Descriptions](#file-descriptions)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### 👥 People Management
- Complete profile management with 40+ fields
- Personal details (DOB, blood group, nationality)
- Contact information (phone, email, social media)
- Professional information (occupation, company)
- Personal preferences (diet, hobbies, languages, skills)
- Groups/circles assignment
- Bio and notes

### 🔗 Relationship Tracking
- Bidirectional relationships (Father ↔ Son, Friend ↔ Friend)
- Multiple relationship types (Family, Professional, Social)
- Meeting history and context
- Relationship notes and timeline
- Visual relationship graph visualization
- Editable relationships

### 📍 Places Management
- Location tracking with GPS coordinates
- Visit status (Visited, Want to Visit, Lived)
- Personal ratings and descriptions
- Tags and categorization
- Event associations

### 📅 Events Management
- Track gatherings, meetings, trips
- Participant management
- Location association
- Expense tracking
- Mood and weather logging
- Transport mode tracking

### 📊 Dashboard
- Statistics overview (People, Places, Events, Relationships)
- Recent activity feed
- Upcoming birthdays
- Quick action buttons
- Interactive relationship graph

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.8+, Flask 3.0+ |
| **Database** | SQLite3 |
| **Frontend** | HTML5, Jinja2 Templates, Bootstrap 5.3 |
| **Icons** | Bootstrap Icons |
| **Graph Visualization** | Vis.js Network |
| **Architecture** | MVC Pattern |

---

## 📁 Project Structure

```
Personal_CRM/
│
├── app.py                          # Main Flask application (routes & controllers)
├── models.py                       # Database models & business logic
├── database.py                     # Database schema & initialization
├── config.py                       # Application configuration & constants
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
│
├── templates/                      # HTML templates (Jinja2)
│   ├── base.html                   # Base template with navigation
│   ├── index.html                  # Dashboard homepage
│   ├── people.html                 # People list (cards view)
│   ├── person_detail.html          # Person add/edit/view form
│   ├── places.html                 # Places list
│   ├── place_detail.html           # Place add/edit form
│   ├── events.html                 # Events list
│   ├── event_detail.html           # Event add/edit form
│   ├── relationship_graph.html     # Interactive relationship graph
│   ├── relationship_edit.html      # Edit relationship form
│   └── search.html                 # Search results page
│
├── static/                         # Static assets (CSS, JS, images)
│   ├── css/
│   │   └── custom.css              # Custom styles (optional)
│   ├── js/
│   │   └── custom.js               # Custom JavaScript (optional)
│   └── images/
│       └── logo.png                # Application logo
│
├── migrations/                     # Database migrations (optional)
│   └── migration_add_created_at.py # Example migration script
│
└── personal_crm.db                 # SQLite database (created on first run)
```

---

## 📝 File Descriptions

### **Core Application Files**

#### `app.py` (Main Application)
**Purpose:** Flask application entry point containing all routes and request handlers.

**Key Components:**
- **Dashboard Routes:** `/` - Main dashboard with statistics
- **People Routes:** 
  - `/people` - List all people
  - `/people/add` - Add new person
  - `/people/<id>` - View person details
  - `/people/<id>/edit` - Update person
  - `/people/<id>/delete` - Delete person
- **Relationship Routes:**
  - `/people/<id>/relationships/add` - Add relationship
  - `/relationships/<id>/edit` - Edit relationship
  - `/relationships/<id>/delete` - Delete relationship
  - `/relationships/graph` - Visualize relationship network
- **Places Routes:** `/places`, `/places/add`, `/places/<id>`, etc.
- **Events Routes:** `/events`, `/events/add`, `/events/<id>`, etc.
- **Search Route:** `/search` - Global search
- **API Routes:** `/api/stats` - Statistics endpoint

**Lines of Code:** ~600

---

#### `models.py` (Data Models)
**Purpose:** Database interaction layer using the DAO (Data Access Object) pattern.

**Classes:**
- **`Database`:** Handles database connections and queries
  - `get_connection()` - Returns SQLite connection
  - `execute_query()` - Executes SQL with parameter binding
  
- **`PersonModel`:** People CRUD operations
  - `get_all()` - Fetch all people
  - `get_by_id(id)` - Fetch single person
  - `create(data)` - Insert new person
  - `update(id, data)` - Update person
  - `delete(id)` - Delete person
  - `search(term)` - Search people
  - `get_relationships(id)` - Fetch person's relationships
  
- **`PlaceModel`:** Places CRUD operations
  - Similar methods for places management
  
- **`EventModel`:** Events CRUD operations
  - `get_participants(event_id)` - Fetch event attendees
  - Additional event-specific methods

**Database Abstraction:** Uses parameterized queries to prevent SQL injection.

**Lines of Code:** ~180

---

#### `database.py` (Schema Definition)
**Purpose:** Database schema creation and initialization.

**Key Components:**
- **13 Core Tables:**
  - `people` - Personal profiles (25 columns)
  - `relationships` - Person-to-person connections
  - `groups` - Social/professional circles
  - `person_groups` - Many-to-many people ↔ groups
  - `contacts` - Additional contact methods
  - `addresses` - Physical addresses
  - `education` - Academic history
  - `career` - Professional history
  - `places` - Location records
  - `events` - Event tracking
  - `event_participants` - Many-to-many events ↔ people
  - `media` - Photo/document attachments
  - `interactions` - Communication logs

**Functions:**
- `init_db()` - Creates all tables if they don't exist
- `seed_data()` - Inserts default groups and sample data

**Execution:** Run `python database.py` to initialize database.

**Lines of Code:** ~400

---

#### `config.py` (Configuration)
**Purpose:** Application settings and constants.

**Configuration Options:**
- **Flask Settings:**
  - `SECRET_KEY` - Session encryption key
  - `SQLALCHEMY_DATABASE_URI` - Database path
  
- **Data Constants:**
  - `RELATIONSHIP_TYPES` - List of 20+ relationship types
    - Family: Father, Mother, Sibling, Spouse, Child
    - Professional: Colleague, Manager, Client, Mentor
    - Social: Friend, Best Friend, Acquaintance
    - Extended: Cousin, Uncle, Aunt, Grandparent
  
  - `PLACE_TYPES` - Location categories (Restaurant, Park, Office, etc.)
  - `EVENT_TYPES` - Event categories (Meeting, Party, Trip, etc.)
  - `BLOOD_GROUPS` - Medical blood types (A+, A-, B+, etc.)

**Lines of Code:** ~50

---

### **Template Files (HTML)**

#### `base.html` (Layout Template)
**Purpose:** Master template with navigation and common elements.

**Features:**
- Bootstrap 5.3 navbar with search bar
- Navigation links (Dashboard, People, Places, Events)
- Flash message display area
- Footer with credits
- CSS/JS block placeholders for child templates

---

#### `index.html` (Dashboard)
**Purpose:** Homepage showing statistics and recent activity.

**Components:**
- 4 statistics cards (People, Places, Events, Relationships)
- Quick action buttons (Add Person, Add Place, Add Event)
- Recent events list
- Upcoming birthdays widget
- Relationship graph link

---

#### `people.html` (People List)
**Purpose:** Display all people as interactive cards.

**Features:**
- Card grid layout (4 columns on desktop)
- Avatar circles with initials
- Contact info preview
- View/Delete buttons
- Empty state message

---

#### `person_detail.html` (Person Form)
**Purpose:** Comprehensive form for adding/editing people.

**Sections (9 total):**
1. Basic Identity (prefix, first/middle/last name, nickname)
2. Personal Details (gender, DOB, blood group)
3. Contact Information (phone, email)
4. Location (city, country, hometown)
5. Professional (occupation, company)
6. Groups/Circles assignment
7. Personal Preferences (diet, hobbies, languages)
8. Social Media (Instagram, LinkedIn, Twitter, GitHub)
9. Bio & Notes

**Additional Features (when viewing existing person):**
- Relationships card with Add/Edit/Delete
- Recent events participation
- Dynamic contact addition

**Lines of Code:** ~450

---

#### `relationship_graph.html` (Network Visualization)
**Purpose:** Interactive visual representation of relationships.

**Technology:**
- Vis.js Network library
- Force-directed graph layout
- Interactive nodes (click to view person)
- Hover tooltips
- Zoom/pan controls

**Features:**
- Colored nodes for people
- Directed arrows for relationships
- Edge labels showing relationship type
- Physics simulation for natural layout

---

#### `places.html`, `place_detail.html`
**Purpose:** Location management.

**Fields:**
- Name, type, GPS coordinates
- City, country
- Visit status, rating
- Description, tags
- Custom attributes (WiFi, parking, best season)

---

#### `events.html`, `event_detail.html`
**Purpose:** Event tracking.

**Fields:**
- Title, type, date/time
- Location (linked to places)
- Participants (multi-select people)
- Description, mood, weather
- Expense tracking
- Transport mode

---

### **Supporting Files**

#### `requirements.txt`
**Purpose:** Python package dependencies.

```
Flask>=3.0.0
```

**Install:** `pip install -r requirements.txt`

---

#### `.gitignore`
**Purpose:** Exclude files from version control.

**Ignored:**
- `*.db` - Database files
- `__pycache__/` - Python cache
- `.crmenv/` - Virtual environment
- `*.pyc` - Compiled Python

---

#### `migration_add_created_at.py`
**Purpose:** Database migration example.

**Function:** Adds `created_at` column to `relationships` table.

**Usage:** Run once with `python migration_add_created_at.py`

---

## 🚀 Installation

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### **Step-by-Step Setup**

#### **1. Clone or Download the Repository**
```
# Option A: Clone with Git
git clone https://github.com/yourusername/Personal_CRM.git
cd Personal_CRM

# Option B: Download ZIP and extract
# Then navigate to the folder
cd Personal_CRM
```

#### **2. Create Virtual Environment (Recommended)**
```
# Windows
python -m venv .crmenv
.crmenv\Scripts\activate

# macOS/Linux
python3 -m venv .crmenv
source .crmenv/bin/activate
```

**Why Virtual Environment?**
- Isolates project dependencies
- Prevents conflicts with system Python
- Makes deployment easier

#### **3. Install Dependencies**
```
pip install -r requirements.txt
```

This installs Flask and all required packages.

#### **4. Initialize Database**
```
python database.py
```

**What this does:**
- Creates `personal_crm.db` file
- Creates 13 tables with proper schema
- Seeds default groups (Family, Friends, Work, etc.)
- Adds sample data (optional)

**Expected Output:**
```
✓ Database initialized successfully!
✓ 13 tables created
✓ 5 default groups added
✓ Ready to use!
```

#### **5. (Optional) Run Migrations**
```
python migration_add_created_at.py
```

---

## ▶️ Running the Application

### **Start the Flask Server**

```
python app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
Press CTRL+C to quit
```

### **Access the Application**

Open your web browser and navigate to:
```
http://localhost:5000
```

**What you'll see:**
- Dashboard with statistics (0 people, 0 places, 0 events initially)
- Navigation bar at the top
- Quick action buttons

---

## 📖 Usage Guide

### **Quick Start Tutorial**

#### **Step 1: Add Your First Person**
1. Click **"Add Person"** button on dashboard
2. Fill required fields:
   - First Name (required)
   - Optional: Last name, nickname, DOB, phone, email
3. Scroll down and click **"Create Person"**
4. You'll be redirected to their profile page

#### **Step 2: Add a Second Person**
1. Go back to **"People"** from navigation
2. Click **"Add Person"** again
3. Add another person (e.g., family member, friend)

#### **Step 3: Create a Relationship**
1. Click on one person's card to view their profile
2. Scroll to **"Relationships"** section
3. Click **"Add Relationship"** button
4. Fill the modal:
   - **Related Person:** Select from dropdown
   - **Relationship Type:** Choose (e.g., "Father", "Friend")
   - **Reverse Type:** Choose opposite (e.g., "Son", "Friend")
   - **Meeting Date:** When you met (optional)
   - **Context:** How you met (optional)
5. Click **"Add Relationship"**

**Result:** Both people now have the relationship recorded!

#### **Step 4: View Relationship Graph**
1. Go to **Dashboard**
2. Click **"View Graph"** on Relationships card
3. See interactive network visualization
4. Click nodes to navigate to people

#### **Step 5: Add a Place**
1. Click **"Places"** in navigation
2. Click **"Add Place"**
3. Fill details (name, city, type, coordinates)
4. Rate it and add notes

#### **Step 6: Create an Event**
1. Click **"Events"** in navigation
2. Click **"Add Event"**
3. Fill details:
   - Title, date/time
   - Select location (place)
   - Select participants (people)
   - Add description
4. Save event

---

## 🗄 Database Schema

### **Core Tables Overview**

| Table | Purpose | Key Fields | Relationships |
|-------|---------|------------|---------------|
| `people` | Personal profiles | first_name, dob, occupation | → relationships, events |
| `relationships` | Connections | person_a_id, person_b_id, type | people ↔ people |
| `groups` | Social circles | name, description | → person_groups |
| `places` | Locations | name, GPS, city | → events |
| `events` | Gatherings | title, datetime, place_id | → participants |
| `contacts` | Extra contact methods | person_id, type, value | → people |
| `addresses` | Physical addresses | person_id, street, city | → people |
| `education` | Academic history | person_id, institution | → people |
| `career` | Work history | person_id, company, role | → people |

### **Relationship Types Supported**

**Family (12 types):**
- Father, Mother, Son, Daughter, Brother, Sister
- Spouse, Partner, Grandparent, Grandchild, Uncle, Aunt, Cousin

**Professional (8 types):**
- Colleague, Manager, Employee, Client, Vendor, Mentor, Mentee, Business Partner

**Social (10 types):**
- Friend, Best Friend, Acquaintance, Neighbor, Classmate, Roommate

---

## ⚙️ Configuration

### **Customizing Relationship Types**

Edit `config.py`:

```
RELATIONSHIP_TYPES = [
    "Father", "Mother", "Sibling",
    # Add your custom types:
    "Gym Buddy", "Travel Companion", "Study Partner"
]
```

### **Changing Secret Key (Important for Production!)**

```
# config.py
SECRET_KEY = 'your-super-secret-random-key-here'
```

Generate secure key:
```
import secrets
print(secrets.token_hex(32))
```

### **Database Location**

Default: `personal_crm.db` in project root

To change:
```
# config.py
SQLALCHEMY_DATABASE_URI = 'sqlite:///path/to/your/database.db'
```

---

## 🐛 Troubleshooting

### **Common Issues**

#### **1. "ModuleNotFoundError: No module named 'flask'"**
**Solution:** Install dependencies
```
pip install -r requirements.txt
```

#### **2. "OperationalError: no such table: people"**
**Solution:** Initialize database
```
python database.py
```

#### **3. Port 5000 already in use**
**Solution:** Change port in `app.py`:
```
app.run(debug=True, host='0.0.0.0', port=8080)  # Use 8080 instead
```

#### **4. Relationship graph not showing**
**Solution:** 
- Clear browser cache
- Check console for JavaScript errors (F12)
- Verify Vis.js CDN is loading

#### **5. "No such column: r.created_at"**
**Solution:** Run migration
```
python migration_add_created_at.py
```

#### **6. Groups dropdown empty**
**Solution:** Re-run database initialization
```
python database.py
```

---

## 🔒 Security Notes

### **For Development**
- Debug mode is enabled (shows detailed errors)
- Secret key is exposed in code
- No authentication system

### **For Production Deployment**
⚠️ **Do NOT use this directly in production!**

**Required Changes:**
1. Change `SECRET_KEY` to random secure string
2. Disable debug mode: `app.run(debug=False)`
3. Use production WSGI server (Gunicorn, uWSGI)
4. Add authentication (Flask-Login)
5. Use environment variables for secrets
6. Enable HTTPS
7. Add input validation and sanitization
8. Implement rate limiting

---

## 📈 Future Enhancements

**Planned Features:**
- [ ] User authentication (multi-user support)
- [ ] Photo uploads for people and events
- [ ] Export data (CSV, PDF, JSON)
- [ ] Calendar view for events
- [ ] Reminders and notifications
- [ ] Mobile responsive design improvements
- [ ] Advanced search and filters
- [ ] Timeline view for relationships
- [ ] Import from contacts (VCF, CSV)
- [ ] API documentation (REST endpoints)

---

## 🤝 Contributing

Contributions welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- **Flask** - Lightweight Python web framework
- **Bootstrap 5** - UI framework
- **Vis.js** - Network graph visualization
- **Bootstrap Icons** - Icon library
- **SQLite** - Embedded database

---

## 📞 Support

For questions or issues:
1. Check [Troubleshooting](#troubleshooting) section
2. Search existing GitHub issues
3. Open a new issue with:
   - Error message
   - Steps to reproduce
   - Python version
   - Operating system

---

**Happy CRM Building! 🎉**

---

## Quick Reference Card

```
┌─────────────────────────────────────────────┐
│  QUICK COMMAND REFERENCE                    │
├─────────────────────────────────────────────┤
│  Setup:                                     │
│    python -m venv .crmenv                   │
│    .crmenv\Scripts\activate (Windows)       │
│    source .crmenv/bin/activate (Mac/Linux)  │
│    pip install -r requirements.txt          │
│    python database.py                       │
│                                             │
│  Run:                                       │
│    python app.py                            │
│    → Open http://localhost:5000             │
│                                             │
│  Database:                                  │
│    python database.py        (initialize)   │
│    python migration_*.py     (run migration)│
│                                             │
│  Troubleshoot:                              │
│    Delete personal_crm.db                   │
│    Re-run: python database.py               │
└─────────────────────────────────────────────┘
```

---

**Last Updated:** December 27, 2025  
**Version:** 1.0.0  
**Status:** Active Development
