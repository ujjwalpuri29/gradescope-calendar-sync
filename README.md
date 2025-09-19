# 📅 Gradescope → Google Calendar Sync

This project syncs your **Gradescope assignment deadlines** directly into your **Google Calendar** using FastAPI, Google OAuth, and BeautifulSoup.

No more missing deadlines — all your assignments show up as events in your calendar with automatic reminders.

## ✨ Features

- 🔐 Secure Google Calendar OAuth login
- 📥 Scrapes assignment deadlines from Gradescope
- 📅 Adds deadlines as Google Calendar events
- ✅ Prevents duplicate events (no clutter)
- ⏰ Adds popup reminders (due date and a day before)
- 🌍 Configurable timezones

## 🛠️ Tech Stack

- **FastAPI** – backend framework
- **Google Calendar API** – event management
- **BeautifulSoup4** – web scraping
- **dotenv** – secure env variable management


## 📂 Project Structure

```
gradescope-calendar-sync/
│── main.py              # FastAPI app (routes + homepage)
│── google_utils.py      # Google Calendar auth & helper functions
│── gradescope.py        # Gradescope scraping (login + assignments)
│── token.json           # OAuth token (auto-generated after login)
│── .env                 # Environment variables
│── requirements.txt     # Python dependencies
│── README.md            # Documentation
```

## ⚙️ Setup

### 1️⃣ Clone Repository

```
git clone https://github.com/ujjwalpuri29/gradescope-calendar-sync.git
cd gradescope-calendar-sync
```

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Enable Google Calendar API

1. Go to [Google Cloud Console ↗️](https://console.cloud.google.com/)
2. Create a project → Enable Google Calendar API
3. Create OAuth 2.0 credentials → Download **client_secret.json**
4. Save it in the project root

### 4️⃣ Configure .env

Create a .env file in the root directory:

```
# Google OAuth
GOOGLE_CLIENT_SECRETS_FILE=client_secret.json
GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/oauth2callback
TIMEZONE=UTC

# Gradescope credentials
GRADESCOPE_EMAIL=your_email@example.com
GRADESCOPE_PASSWORD=your_password
GRADESCOPE_COURSE_URL=https://www.gradescope.com/courses/123456
COURSE_ID=ABC123
```

> ⚠️ Never commit .env or credentials to GitHub!


## 🚀 Running the App

Start the FastAPI server:

```
uvicorn main:app --reload
```

Visit:

👉 http://127.0.0.1:8000/

- Click Sync Now
- Login with your Google account (first-time login only)


## 🔔 Reminders

Each synced event will have:
- ⏰ Popup reminder at 15 hours before the deadline
- ⏰ Popup reminder at 39 hours before the deadline

## 🛡️ Security

- Credentials stored securely in .env
- OAuth tokens auto-refreshed, stored in token.json
- No passwords or secrets hardcoded

## 🚧 Roadmap

- ⬜ Add background task to auto-sync daily
- ⬜ Deploy on cloud (e.g., Heroku, Render, or Fly.io)
- ⬜ Support multiple users with DB-backed sessions

## 📜 License

MIT License © 2025 Ujjwal Puri