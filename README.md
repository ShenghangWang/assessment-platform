# Reusable Assessment Engine — Dating Pack Starter

A Django-based reusable assessment platform for building quiz-style products with separate JSON assessment packs.

The first completed demo pack is:

```text
packs/dating_readiness/
```

It currently demonstrates a 15-question dating-readiness assessment.

---

## Platform Description

This project is a reusable assessment platform built with Django. It is designed to support multiple quiz-based products through a shared engine and separate assessment packs.

The platform separates the **assessment engine** from the **assessment content**. The engine handles page rendering, answer collection, scoring, result-band mapping, and report display. The content of each assessment is stored in a separate pack under the `packs/` directory.

The core user flow is organized through reusable HTML templates:

```text
core/templates/core/
├─ landing.html   # Landing page for each assessment product
├─ quiz.html      # Dynamic quiz page generated from pack.json
├─ result.html    # Free result page after scoring
├─ paywall.html   # Possible future monetization page for unlocking paid insights
└─ report.html    # Possible future monetization page for AI-generated personalized reports
```

Current and possible assessment packs include:

```text
packs/
├─ dating_readiness/     # Completed and currently demonstrated
├─ physics_major_fit/    # Possible future use case
└─ career_fit/           # Possible future use case
```

### Current Use Case

`dating_readiness/` is the first completed demonstration pack. It asks users 15 questions and gives a relationship-readiness result based on dimensions such as social opportunity, motivation, anxiety/avoidance, actionability, personality, and financial stability.

### Possible Future Use Cases

`physics_major_fit/` could assess whether a student is suitable for choosing a fundamental science major such as physics, considering factors like scientific interest, math readiness, persistence, family support, financial pressure, and tolerance for delayed career payoff.

`career_fit/` could assess whether a user is suitable for different career paths based on personality, skills, motivation, risk tolerance, learning ability, and market demand.

Other possible assessment products include:

- study-abroad readiness assessment
- graduate-school readiness assessment
- startup-founder readiness assessment
- sales-career fit assessment
- AI-career transition readiness assessment
- language-learning strategy assessment
- relationship communication style assessment
- financial risk-tolerance assessment

The long-term goal is to make the platform a flexible **assessment engine**, where new products can be created mainly by adding a new `pack.json` file instead of rewriting the application code.

---

## Quick Start

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the local environment file:

```bash
cp .env.example .env
```

Run database migrations:

```bash
python manage.py migrate
```

Import the dating-readiness assessment pack:

```bash
python manage.py import_pack dating_readiness --publish --update
```

Start the development server:

```bash
python manage.py runserver
```

Open the app:

```text
http://127.0.0.1:8000/p/dating_readiness/
```

---

## Project Structure

```text
assessment_platform/
├─ manage.py
├─ requirements.txt
├─ .env.example
├─ README.md
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

> Note: `db.sqlite3`, `.env`, `.venv/`, `__pycache__/`, `.DS_Store`, and `staticfiles/` are local development files and should be excluded from GitHub with `.gitignore`.

---

## Import an Assessment Pack

This project uses JSON-based assessment packs. Before users can submit quiz attempts, the pack must be imported into the database.

For the dating-readiness pack, run:

```bash
python manage.py import_pack dating_readiness --publish --update
```

Then start the server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/p/dating_readiness/
```

### Adding a New Pack

To add a new assessment product, create a new folder under `packs/`.

Example:

```text
packs/physics_major_fit/pack.json
```

Then import it:

```bash
python manage.py import_pack physics_major_fit --publish --update
```

Then open:

```text
http://127.0.0.1:8000/p/physics_major_fit/
```

---

## GitHub Safety Notes

Do not commit local secrets or runtime files such as:

```text
.env
db.sqlite3
.venv/
.DS_Store
__pycache__/
staticfiles/
```

Keep `.env.example` in the repository so collaborators know which environment variables are needed.