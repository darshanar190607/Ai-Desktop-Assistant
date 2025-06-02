# Ai-Desktop-Assistant
Every preson has thier own ai
# 💻 AI Desktop Assistant

An intelligent AI-powered desktop assistant built using **Django** and **MongoDB**, designed to enhance productivity and user engagement with advanced features such as personalized entrepreneurial advice, alarm setting, motivational responses, and a smart fallback system.

---

## 🚀 Features

- 🤖 **Entrepreneur AI**: Offers tailored guidance for startup and business-related queries.
- ⏰ **Alarm Setter**: Lets users set and manage reminders or alarms.
- 🌐 **Smart Edge Panel**: Includes a stylish sidebar with your logo and quick-access tools.
- 💬 **Emotion Detection & Motivation**: Detects sad or negative messages and responds with uplifting quotes.
- 🧠 **Fallback Panel**: Stores unknown queries for developer review or external AI handling (with strict content control).
- 🔐 **Secure Data Handling**: User queries and responses are stored only in **MongoDB**, not shared with third-party AI unless required.

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Django (Python Web Framework)
- **Database**: MongoDB (Atlas or Local)
- **AI Engine**: Local NLP models with optional fallback to external AI (controlled access)

---

## 📁 Project Structure

```bash
ai-desktop-assistant/
│
├── assistant/               # Django app for core features
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # For image/audio uploads if any
├── db/                      # MongoDB database connection
├── fallback/                # Stores unanswerable queries
├── alarms/                  # Alarm setting module
├── sidebar/                 # Edge panel UI module
└── manage.py
