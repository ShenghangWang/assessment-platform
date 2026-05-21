# Reusable Assessment Engine — Dating Pack Starter

Run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
```



# Project Structure

```text
assessment_platform/
├─ manage.py
├─ requirements.txt
├─ .env.example
├─ README.md
├─ db.sqlite3                  # local only 
├─ config/
│  ├─ __init__.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ asgi.py
│  └─ wsgi.py
├─ core/
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ forms.py
│  ├─ views.py
│  ├─ urls.py
│  ├─ scoring.py
│  ├─ pack_loader.py
│  ├─ report_generator.py
│  ├─ ai_client.py
│  ├─ payment.py
│  ├─ utils.py
│  ├─ management/
│  │  ├─ __init__.py
│  │  └─ commands/
│  │     ├─ __init__.py
│  │     └─ import_pack.py
│  ├─ migrations/
│  │  ├─ __init__.py
│  │  └─ 0001_initial.py
│  ├─ templates/
│  │  └─ core/
│  │     ├─ base.html
│  │     ├─ landing.html
│  │     ├─ quiz.html
│  │     ├─ result.html
│  │     ├─ paywall.html
│  │     └─ report.html
│  └─ static/
│     └─ core/
│        ├─ css/
│        │  └─ styles.css
│        └─ js/
│           └─ app.js
├─ packs/
│  ├─ dating_readiness/
│  │  ├─ pack.json
│  │  └─ assets/
│  ├─ physics_major_fit/
│  │  ├─ pack.json
│  │  └─ assets/
│  └─ career_fit/
│     ├─ pack.json
│     └─ assets/
└─ tests/
   ├─ test_pack_loader.py
   ├─ test_scoring.py
   ├─ test_band_mapping.py
   └─ test_endpoints.py
```

> Note: `db.sqlite3`, `.env`, `.venv/`, `__pycache__/`, and `staticfiles/` are local development files and should usually be excluded from GitHub with `.gitignore`.



## Import an assessment pack

This project uses JSON-based assessment packs. Before users can submit quiz attempts, the pack must be imported into the database.

For the dating-readiness pack, run:

```bash
python manage.py import_pack dating_readiness --publish --update
python manage.py runserver
```

Open `http://127.0.0.1:8000/p/dating_readiness/`