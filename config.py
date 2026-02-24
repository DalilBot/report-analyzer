"""
Configuration settings for the Discord Learning Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_PREFIX = "!"

# Google Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"  # or "gemini-1.5-flash" for faster responses

# Google Cloud Configuration (for Forms and Sheets)
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
GOOGLE_TOKEN_FILE = "token.json"

# Google API Scopes
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file"
]

# File upload settings
ALLOWED_FILE_EXTENSIONS = [
    ".pdf", ".txt", ".docx", ".doc", 
    ".xlsx", ".xls", ".csv",
    ".pptx", ".ppt",
    ".png", ".jpg", ".jpeg"
]
MAX_FILE_SIZE_MB = 25  # Discord's limit for non-nitro

# Session timeout (in seconds)
SESSION_TIMEOUT = 3600  # 1 hour

# Daily Report Configuration (Classera)
CLASSERA_USERNAME = os.getenv("CLASSERA_USERNAME")
CLASSERA_PASSWORD = os.getenv("CLASSERA_PASSWORD")
REPORT_CHANNEL_ID = int(os.getenv("REPORT_CHANNEL_ID", "0"))  # Discord channel ID to send reports
REPORT_TIME_HOUR = int(os.getenv("REPORT_TIME_HOUR", "15"))  # 24-hour format (default 15 = 3 PM)
REPORT_TIME_MINUTE = int(os.getenv("REPORT_TIME_MINUTE", "15"))  # Minutes (default 15)

# Morning Homework Reminder Time
MORNING_REMINDER_HOUR = int(os.getenv("MORNING_REMINDER_HOUR", "7"))  # Default 7 AM
MORNING_REMINDER_MINUTE = int(os.getenv("MORNING_REMINDER_MINUTE", "0"))  # Default :00

# Weekly Assessment Reminder
WEEKLY_REMINDER_DAY = int(os.getenv("WEEKLY_REMINDER_DAY", "6"))  # 0=Monday, 6=Sunday (default)
WEEKLY_REMINDER_HOUR = int(os.getenv("WEEKLY_REMINDER_HOUR", "18"))  # Default 6 PM
WEEKLY_REMINDER_MINUTE = int(os.getenv("WEEKLY_REMINDER_MINUTE", "0"))  # Default :00

# Night-Before Exam Reminder
NIGHT_REMINDER_HOUR = int(os.getenv("NIGHT_REMINDER_HOUR", "20"))  # Default 8 PM
NIGHT_REMINDER_MINUTE = int(os.getenv("NIGHT_REMINDER_MINUTE", "0"))  # Default :00

# Web Dashboard Configuration
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "5000"))
DASHBOARD_PASSWORD = os.getenv("DASHBOARD_PASSWORD", "admin123")

# Difficulty levels
DIFFICULTY_LEVELS = {
    1: "Beginner",
    2: "Elementary", 
    3: "Intermediate",
    4: "Advanced",
    5: "Expert"
}
