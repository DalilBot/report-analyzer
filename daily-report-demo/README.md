# 📊 Daily Report Analyzer

> AI-powered school daily report analyzer. Upload PDF reports and let **Google Gemini** extract homework & reminders automatically.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0+-green?logo=flask)
![Gemini](https://img.shields.io/badge/Google_Gemini-AI-orange?logo=google)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 📄 **PDF Upload** — Drag & drop daily report PDFs
- 🤖 **AI Analysis** — Google Gemini extracts homework & reminders
- 📝 **Homework Tracker** — Track & check off completed homework
- 🔔 **Reminders** — See prioritized reminders (high/medium/low)
- 📅 **7-Day Memory** — Keeps data for the last 7 days
- 🌙 **Dark/Light Mode** — Beautiful responsive UI
- 🌐 **Arabic Support** — Works with Arabic PDF reports

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/daily-report-analyzer.git
cd daily-report-analyzer
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_key_here
```

> 🔑 Get a free API key at [Google AI Studio](https://aistudio.google.com/apikey)

### 3. Run

```bash
python app.py
```

Open **http://localhost:5000** in your browser.

## ☁️ Deploy

### Render (Recommended — Free tier)

1. Fork this repo
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Add environment variable: `GEMINI_API_KEY`
5. Deploy! 🚀

### Railway

```bash
railway init
railway add --name GEMINI_API_KEY
railway up
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

## 📁 Project Structure

```
daily-report-analyzer/
├── app.py                    # Flask backend
├── requirements.txt          # Python dependencies
├── Procfile                  # Deployment command
├── render.yaml               # Render config
├── .env.example              # Environment template
├── static/
│   ├── css/style.css         # Stylesheet
│   └── js/app.js             # Frontend logic
├── templates/
│   └── index.html            # Main page
└── utils/
    ├── report_analyzer.py    # Gemini AI integration
    └── report_memory.py      # 7-day data persistence
```

## 🖼️ Screenshots

| Dark Mode | Light Mode |
|-----------|------------|
| Upload PDF → Get results | Toggle with one click |

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **AI:** Google Gemini (gemini-2.5-flash)
- **Frontend:** Vanilla HTML/CSS/JS
- **Icons:** Font Awesome 6
- **Font:** Inter (Google Fonts)

## 📝 License

MIT — feel free to use this for your own school projects!
