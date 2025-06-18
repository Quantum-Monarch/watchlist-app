
# 🎬 Watchlist App

A personal movie and series tracking app built with Django.

This project lets users keep track of films and shows they’ve watched, are watching, or plan to watch — complete with status updates, ratings, and progress tracking for series.

---

## 🚀 Features

- ✅ User authentication (sign up, log in, log out)
- 🎞️ Browse a catalog of movies and series
- ➕ Add/remove items from your personal watchlist
- ✏️ Update watchlist entries with:
  - Viewing status (Watching, Completed, Plan to Watch)
  - Personal rating
  - Current episode (for series)
- 🔁 Dynamic interface based on watchlist state

---

## 🛠️ Tech Stack

- **Python 3**
- **Django**
- SQLite (default dev database)
- HTML/CSS + Django Templates

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Quantum-Monarch/watchlist-app.git
cd watchlist-app
```


### 2. Create a virtual environment and activate it
```bash
python -m venv .venv
source .venv/bin/activate  *For Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Run the app
```bash
python manage.py runserver
```
Visit: http://127.0.0.1:8000/

## 📁 Project Structure

watchlist-app/
├── mysite/           # Django project settings
├── watchlist/        # App with models, views, URLs
├── templates/        # HTML files
├── static/           # Static files (if used)
└── requirements.txt  # Project dependencies

##  📌 Notes

The project stores the user’s navigation path to support smoother UX when returning to pages.
The app includes logic to differentiate between movies and series and handle each appropriately.
Fully built using function-based views and session handling.

## 🧠 Why I Built This

This started as a personal learning project to dig into Django more deeply. What started simple ended up teaching me a lot about user session handling, model relationships, view logic, and Django’s quirks with redirects. If you’ve ever wanted to scream at a back button, this app will make you feel seen 😂.

## 🪪 License

MIT License — free to use, modify, or build on.