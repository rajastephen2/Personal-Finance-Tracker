# Personal Finance Tracker

I built this project to solve a real problem — keeping track of where your money goes. It's a full-stack web app that lets users log their income and expenses, see a live summary of their finances, and download a PDF report whenever they need one.

The entire thing was built solo using Python (Flask) on the backend, SQLite for the database, and plain HTML, CSS, and JavaScript on the front end.

---

## What it does

- **Login & Registration** — Accounts are protected with hashed passwords using Werkzeug, so no plain text is ever stored
- **Dashboard** — Shows your total income, total expenses, and net balance at a glance
- **Transaction Management** — Add, edit, view, or delete any income or expense entry
- **PDF Reports** — Generate and download a clean PDF of your transaction history directly from the dashboard
- **Admin Panel** — A separate admin view to oversee all users and transactions
- **Responsive Design** — Works on both desktop and mobile without any UI frameworks

---

## Tech used

| Layer | What I used |
|---|---|
| Backend | Python 3, Flask |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Password Security | Werkzeug |
| PDF Generation | ReportLab + BytesIO |
| Templating | Jinja2 |

---

## How it's structured

The app follows the MVC pattern — Models handle the database, Views are the Jinja2 templates, and Controllers are the Flask route functions that tie everything together.

```
personal_finance_tracker/
│
├── app.py                  # Routes and application logic
├── database.py             # DB setup and connection
├── models/                 # Data models
├── templates/              # HTML templates (login, dashboard, transactions, admin...)
├── static/
│   ├── css/
│   └── js/
└── reports/                # PDF generation
```

SQL queries handle everything from basic CRUD to aggregate calculations like `SUM()` and `AVG()` for the financial summaries on the dashboard.

---

## OOP in practice

This wasn't just a script — it was designed with proper object-oriented principles:

- **Encapsulation** keeps data and logic together in the right places
- **Abstraction** means the route handlers don't deal with raw SQL — that's handled by helper functions
- **Reusability** — things like database connections and session checks are written once and used everywhere
- **Inheritance** is used where classes need to extend base behavior, with `super()` for clean initialization

---

## Running it locally

```bash
git clone https://github.com/rajastephen2/Personal-Finance-Tracker.git
cd Personal-Finance-Tracker

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install flask werkzeug reportlab

python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

---

## A note on the PDF feature

The PDF report is generated entirely in memory using ReportLab and Python's BytesIO — no temporary files are created on the server. The file is built and streamed directly to the browser, which felt like the right way to do it.

---

## About

Built by **Raja Stephen** — MCA student at Vels University (VISTAS), Chennai.

This was a solo project, designed and built end-to-end, primarily to sharpen full-stack development skills and demonstrate them during campus placements.

[github.com/rajastephen2](https://github.com/rajastephen2)
