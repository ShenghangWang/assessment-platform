# Reusable Assessment Engine — Dating Pack Starter

A Django-based reusable assessment platform for building quiz-style products with separate JSON assessment packs.

The first completed demo pack is:

```text
packs/dating_readiness/
```

It currently demonstrates a 15-question dating-readiness assessment with:

- dynamic quiz rendering from `pack.json`
- research-source links on the quiz page
- scoring and result-band mapping
- a paywall step
- AI-generated personalized reports
- a mock payment flow for local demo

---

## Platform Description

This project is a reusable assessment platform built with Django. It is designed to support multiple quiz-based products through a shared engine and separate assessment packs.

The platform separates the **assessment engine** from the **assessment content**. The engine handles page rendering, answer collection, scoring, result-band mapping, paywall routing, and AI report display. The content of each assessment is stored in a separate pack under the `packs/` directory.

The core user flow is organized through reusable HTML templates:

```text
core/templates/core/
├─ landing.html   # Landing page for each assessment product
├─ quiz.html      # Dynamic quiz page generated from pack.json, including optional research links
├─ result.html    # Free result page after scoring
├─ paywall.html   # Monetization gate before the personalized report
└─ report.html    # AI-generated personalized report page
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

The dating pack also includes clickable research-source links for individual questions, allowing users to inspect the reasoning behind the assessment design.

After the free result page, users pass through a paywall page and can unlock a personalized AI-generated report. The report is designed to help users improve their chances of building a healthy romantic relationship through practical advice, including:

- main improvement areas
- strengths
- personalized tips
- 7-day action plan
- 30-day improvement path
- conversation starters
- low-cost date ideas
- disclaimer against deterministic prediction

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

## Main Features

- Reusable Django assessment engine
- JSON-based assessment packs
- Dynamic quiz generation
- Pack-specific dimensions and scoring weights
- Reverse-scored question support
- Result-band mapping
- Clickable research links on quiz questions
- Paywall page before report access
- Mock payment flow for local testing
- OpenAI-powered personalized report generation
- Fallback report logic can be added for API failures
- Designed for future packs such as education, career, and study planning assessments

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

Edit `.env` and add your local settings:

```env
DEBUG=True
SECRET_KEY=change-me
ALLOWED_HOSTS=127.0.0.1,localhost
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
MOCK_PAYMENTS=True
```

Do not commit `.env` to GitHub.

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

## Local Demo Flow

The current demo flow is:

```text
Landing page
→ Quiz page
→ Result page
→ Paywall page
→ Mock payment unlock
→ AI-generated report page
```

When `MOCK_PAYMENTS=True`, the paywall uses a local mock payment unlock so the full product flow can be tested without connecting a real payment provider.

When real payment is added later, `MOCK_PAYMENTS` can be set to `False`, and the report page can require a successful payment before access.

---

## AI Report Generation

The personalized report is generated through the OpenAI API.

The report generation flow uses:

```text
quiz answers
→ dimension scores
→ result band
→ AI prompt
→ structured personalized report
```

The report is intended to provide helpful, non-judgmental, practical suggestions. It should avoid deterministic claims such as “you will definitely find love” or “you will stay single.”

The recommended wording is:

```text
This report is a research-informed self-assessment and improvement guide.
It is not a deterministic prediction, psychological diagnosis, or life decision.
```

### OpenAI API Key

The OpenAI API key should be stored only in `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

For the current code, the API key needs permission for:

```text
Responses (/v1/responses): Write
```

Do not expose the API key in frontend JavaScript, screenshots, README files, or GitHub commits.

---

## Payment Flow

The current payment flow is a mock/demo implementation.

Current behavior:

```text
Result page
→ Paywall page
→ Mock payment button
→ Report page
```

Future production behavior:

```text
Result page
→ Paywall page
→ Create payment order
→ Payment provider callback
→ Mark attempt as paid
→ Report page
```

Possible payment providers for future development include:

- WeChat Pay
- Alipay
- Stripe

The app is already structured so the report can be protected behind payment logic later.

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

Before pushing to GitHub, run:

```bash
git status
```

Make sure the following files are not staged:

```text
.env
db.sqlite3
.venv/
.DS_Store
```

If any of them are staged accidentally, unstage them:

```bash
git restore --staged .env
git restore --staged db.sqlite3
git restore --staged .DS_Store
```

---

## Collaboration Notes

This repository is designed so collaborators can add new assessment products without changing the core engine.

To add a new product, a collaborator usually only needs to:

1. Create a new folder under `packs/`
2. Add a new `pack.json`
3. Define dimensions, questions, scoring weights, result bands, and report prompt
4. Import the pack with `python manage.py import_pack <pack_slug> --publish --update`
5. Test the app at `/p/<pack_slug>/`

This makes the project suitable for building multiple assessment products from the same reusable codebase.