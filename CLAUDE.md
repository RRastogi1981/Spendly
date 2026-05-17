# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
# Activate venv (Git Bash)
source ../venv/Scripts/activate

# Run the dev server (port 5001)
python app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Run a single test by name
pytest tests/test_auth.py::test_login_success
```

## Architecture

This is a **Flask + SQLite** expense tracker called **Spendly**, structured as a teaching scaffold where students implement features step by step.

### Key files

- `app.py` — All Flask routes. Currently has full routes for `/`, `/register`, `/login` and stub routes for `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`.
- `database/db.py` — **Must be implemented by students.** Should expose three functions:
  - `get_db()` — returns a SQLite connection with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`
  - `init_db()` — creates all tables using `CREATE TABLE IF NOT EXISTS`
  - `seed_db()` — inserts sample data for development
- `templates/base.html` — Shared layout with navbar and footer. All other templates extend this via `{% extends "base.html" %}`.
- `static/css/style.css` — All styling (DM Sans + DM Serif Display fonts from Google Fonts).
- `static/js/main.js` — Placeholder; students add JS as features are built.

### Implementation steps (as referenced in app.py comments)

1. Database Setup (`database/db.py`)
2. User Registration (POST `/register`)
3. User Login/Logout (POST `/login`, `/logout`)
4. Profile page (`/profile`)
5–6. Expense list/dashboard
7. Add expense (POST `/expenses/add`)
8. Edit expense (POST `/expenses/<id>/edit`)
9. Delete expense (`/expenses/<id>/delete`)

### Database location

SQLite file is `expense_tracker.db` at the project root (excluded from git via `.gitignore`).

### Template conventions

All templates extend `base.html` and use `{% block content %}`. Flash messages use `{% if error %}` with the `.auth-error` CSS class. Forms POST to their route URL directly (e.g. `action="/login"`).
