# LoanSphere - Banking Loan Management System

LoanSphere is a premium digital banking and loan management platform designed with modern glassmorphism aesthetics, a mobile-first responsive layout, and robust security protocols. It utilizes Python Flask for the backend, SQLAlchemy ORM for entity mapping, and MySQL for transaction tracking.

## Technology Stack

- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript (ES6), Chart.js
- **Backend**: Python 3.x, Flask, SQLAlchemy, Flask-Login, Flask-WTF, Flask-Mail
- **Database**: MySQL (PyMySQL connector)
- **PDF Generation**: ReportLab Platypus

---

## Folder Structure

```
LoanSphere/
├── app.py                  # Main Application Factory & DB initialization
├── config.py               # Security keys, MySQL parameters, Upload rules
├── extensions.py           # Circular-safe Flask plugin instances
├── models.py               # Database schemas (Users, Applications, EMIs, Rates)
├── forms.py                # Server-validated WTF Forms (Login, Apply, Contact)
├── routes.py               # Blueprints (Auth, Main clients, Admin reviews)
├── seed.py                 # 100+ User/App dynamic dataset seeder
├── database.sql            # MySQL schema reference backup
├── requirements.txt        # PIP Python package dependencies
├── static/
│   ├── css/
│   │   └── style.css       # Variable-driven Light/Dark theme styles
│   └── js/
│       ├── main.js         # Theme switchers, Counters, Auto-saves, Toasts
│       ├── calculator.js   # Amortization math & Chart binding
│       └── eligibility.js  # AJAX Credit validation & recommendation
└── templates/
    ├── base.html           # Master navbar/footer layout
    ├── index.html          # Hero page, Offers, Stats, Testimonials
    ├── calculator.html     # Loan EMI simulation panel
    ├── eligibility.html    # FOIR/CIBIL credit checks
    ├── admin/              # Admin dashboard & reviewing controls
    └── ...                 # Auth & Profile layouts
```

---

## Installation & Setup

### 1. Prerequisite Packages
Install dependencies listed in the requirements file:
```bash
pip install -r requirements.txt
```

### 2. Database Initialization
Ensure your local MySQL instance is active, then create the database structure.
By default, the application connects to a local server. If your user credentials differ, update them in `config.py` or export them as environment variables:
```bash
# Environment variables setup (Optional)
set DB_USER=your_username
set DB_PASSWORD=your_password
set DB_HOST=localhost
set DB_NAME=loansphere_db
```

Run `app.py` once to build all the tables automatically:
```bash
python app.py
```

### 3. Seed Testing Data
Populate the database with the mock test dataset consisting of 20 loan types, 5 admin accounts, 100 dummy users, and 100 dummy applications complete with historical notifications and EMIs:
```bash
python seed.py
```

---

## Testing Credentials

The seeder creates standard testing profiles:
- **Administrator Login**:
  - Email: `admin1@loansphere.bank` (through `admin5@loansphere.bank`)
  - Password: `adminPass1!` (through `adminPass5!`)
- **Customer Login**:
  - Email: `user1@gmail.com` (through `user100@gmail.com`)
  - Password: `userpass123`

---

## Features Walkthrough

1. **Auto-Save Drafts**: The application form leverages local storage listeners. If a customer exits midway, returning reload brings back typed values instantly.
2. **Credit Simulator**: Modify sliders inside the dashboard to evaluate how a simulated CIBIL score changes your interest tiers or flags warnings.
3. **Interactive EMI**: Input variables to draw Principal vs Interest component splits on a dynamic canvas. Download a detailed PDF schedule.
