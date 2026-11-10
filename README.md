# FixMyCampus – Smart Campus Issue Reporting System

A full-stack, lightweight Flask web application that lets students report campus maintenance issues, receive a unique Complaint ID, and track resolution status. Administrators can manage complaints and update their status through a protected dashboard.

## Features

- Public homepage (no login required) with hero, "How It Works", complaint categories, and benefits sections
- Report an issue: name, email, phone, category, location, description
- Auto-generated unique Complaint ID (e.g. `FMC-2026-A1B2C3`)
- Track any complaint by its Complaint ID
- Admin dashboard: view all complaints, filter by status, update status/priority/admin notes
- Protected admin login (session-based)
- Responsive campus-themed UI (Bootstrap 5, navy + teal palette)
- Flash messages for success/errors
- SQLite for local development; PostgreSQL (Supabase) for production
- Flask-Migrate for database migrations

## Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Bootstrap Icons
- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF
- **Database:** SQLite (local), PostgreSQL / Supabase (production)

## Project Structure

```
FixMyCampus/
├── app/
│   ├── __init__.py        # Flask app factory + error handlers
│   ├── config.py          # Configuration
│   ├── models.py          # Complaint & Admin models
│   ├── forms.py           # Flask-WTF forms
│   └── routes/
│       ├── __init__.py
│       ├── main.py        # Public routes (home, report, track)
│       └── admin.py       # Admin routes (login, dashboard, updates)
├── migrations/            # Flask-Migrate (Alembic) versions
├── instance/              # SQLite database (local dev, gitignored)
├── static/
│   └── css/style.css      # Custom campus theme styles
├── templates/
│   ├── base.html
│   ├── index.html         # Homepage
│   ├── report.html        # Report an issue
│   ├── track.html         # Track by Complaint ID
│   ├── track_result.html  # Complaint status page
│   ├── admin/
│   │   ├── login.html
│   │   └── dashboard.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
├── seed.py                # Seed admin user + sample complaints
├── run.py                 # Application entry point
├── requirements.txt
├── Procfile               # Render
├── render.yaml            # Render service spec
├── .env.example
└── .gitignore
```

## Local Setup

### Prerequisites
- Python 3.10+
- Git

### 1. Clone / open the project
Work directly inside this directory. Do not create a nested `FixMyCampus` folder.

### 2. Create and activate a virtual environment
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure environment
Copy the example env file and adjust values:
```powershell
copy .env.example .env
```

### 5. Initialize the database
```powershell
$env:FLASK_APP="run.py"
flask db upgrade
```

The `migrations/` folder is already included, so `flask db upgrade` applies the initial migration.

### 6. Seed admin user and sample data
```powershell
python seed.py
```

Seed the admin user with `ADMIN_USERNAME` and `ADMIN_PASSWORD` set in `.env` before running `python seed.py`.

### 7. Run the application
```powershell
$env:FLASK_APP="run.py"
flask run
```

Open http://127.0.0.1:5000 in your browser.

### Commands cheat sheet
```powershell
$env:FLASK_APP="run.py"                      # set Flask app (PowerShell)
flask db migrate -m "message"                # create a new migration
flask db upgrade                             # apply migrations
python seed.py                               # (re)seed admin + sample complaints
flask run                                    # start dev server
```

## Deployment (Render + Supabase Free)

### 1. Database (Supabase)
- Create a free project at https://supabase.com
- Note the **Database URL** (PostgreSQL connection string) from Settings → Database

### 2. Web Service (Render)
- Push this project to GitHub
- In Render, create a new **Web Service** connected to your repo
- Runtime: Python
- Build command: `pip install -r requirements.txt && flask db upgrade`
- Start command: `gunicorn run:app`

### 3. Environment variables on Render
| Key | Value |
|-----|-------|
| `SECRET_KEY` | a long random string |
| `ADMIN_USERNAME` | `admin` |
| `ADMIN_PASSWORD` | choose a strong password |
| `DATABASE_URL` | your Supabase PostgreSQL connection string |

Render will run `flask db upgrade` on deploy, creating the tables in PostgreSQL. Then run `python seed.py` once (via Render shell) or seed manually to create the admin user.

## Admin Dashboard
- URL: `/admin/login`
- Log in with the admin credentials configured via `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env`.
- From the dashboard you can filter complaints by status and update status (Pending / In Progress / Resolved / Rejected), priority, and add admin notes.

## Notes
- `instance/` and `venv/` are gitignored.
- SQLite is used locally; the app switches to PostgreSQL automatically when `DATABASE_URL` is set.
- CSRF protection is enabled on all forms.
