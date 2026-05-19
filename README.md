# Reusable Assessment Engine — Dating Pack Starter

Run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/p/dating_readiness/`

# Project Structure

'''
assessment_platform/
├─ manage.py
├─ requirements.txt
├─ .env.example
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
│        ├─ css/styles.css
│        └─ js/app.js
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
'''

