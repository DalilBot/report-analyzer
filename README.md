# 🤖 Discord AI Learning Bot

An intelligent Discord bot powered by **Google Gemini** that helps enhance learning by analyzing materials, dividing tasks among group members, and creating assessment surveys.

## ✨ Features

- **📚 Material Analysis**: Upload PDFs, documents, spreadsheets, images, and text files for AI analysis
- **👥 Smart Task Division**: Automatically divide learning tasks based on each member's skill level
- **📝 Survey Generation**: Create quizzes with 5 high-quality questions from your materials
- **📊 Google Forms Integration**: Automatically create Google Forms for survey distribution
- **📈 Prediction Analytics**: Generate 25 simulated responses with statistics
- **📋 Excel/Google Sheets**: Export all data to spreadsheets for analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Discord Bot Token
- Google Gemini API Key
- (Optional) Google Cloud credentials for Forms/Sheets

### Installation

1. **Clone/Download the project**

2. **Install dependencies**:
   ```bash
   cd my_analyzer
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   # Copy the example file
   copy .env.example .env
   
   # Edit .env with your API keys
   notepad .env
   ```

4. **Run the bot**:
   ```bash
   python main.py
   ```

## 🔑 Getting API Keys

### Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to "Bot" section and click "Add Bot"
4. Click "Reset Token" and copy the token
5. Enable these **Privileged Gateway Intents**:
   - Message Content Intent
   - Server Members Intent (optional)
6. Go to OAuth2 > URL Generator:
   - Select `bot` scope
   - Select permissions: `Send Messages`, `Embed Links`, `Attach Files`, `Read Message History`, `Use Slash Commands`
7. Use the generated URL to invite the bot to your server

### Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key to your `.env` file

### Google Cloud Credentials (Optional - for Forms/Sheets)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable these APIs:
   - Google Forms API
   - Google Sheets API
   - Google Drive API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the JSON file and save as `credentials.json`
6. On first run, you'll be prompted to authorize in your browser

## 📖 Usage Guide

### Starting a Session

1. **DM the bot** and type `!start`
2. The bot will guide you through each step

### Workflow

```
!start
   │
   ▼
📁 Upload Materials (files)
   │  - PDFs, Word docs, Excel, images, text files
   │  - Type "done" when finished
   │
   ▼
👥 Add Group Members
   │  - Enter names (comma or newline separated)
   │  - Type "done" when finished
   │
   ▼
🎯 Assign Difficulty Levels (1-5)
   │  - Rate each member's skill level
   │
   ▼
🤖 AI Analysis & Task Division
   │  - Materials analyzed by Gemini
   │  - Tasks divided based on difficulty
   │
   ▼
📝 Survey Option (yes/no)
   │  - 5 quiz questions generated
   │  - Google Form created
   │  - 25 predicted responses
   │  - Excel/Sheets with statistics
   │
   ▼
✅ Session Complete!
```

### Commands

| Command | Description |
|---------|-------------|
| `!start` | Start a new learning session |
| `!cancel` | Cancel the current session |
| `!status` | Check session status |

## 📁 Project Structure

```
my_analyzer/
├── main.py                 # Entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your API keys (create this)
├── credentials.json       # Google Cloud credentials (optional)
│
├── bot/
│   ├── __init__.py
│   └── discord_bot.py     # Discord bot implementation
│
├── services/
│   ├── __init__.py
│   ├── gemini_service.py  # Google Gemini AI integration
│   └── google_services.py # Google Forms/Sheets integration
│
├── utils/
│   ├── __init__.py
│   ├── file_handler.py    # File download and parsing
│   └── session_manager.py # User session management
│
└── temp_files/            # Temporary file storage
```

## 🛠️ Supported File Types

| Type | Extensions |
|------|------------|
| Documents | `.pdf`, `.docx`, `.doc`, `.txt` |
| Spreadsheets | `.xlsx`, `.xls`, `.csv` |
| Presentations | `.pptx`, `.ppt` |
| Images | `.png`, `.jpg`, `.jpeg` |

## ⚠️ Troubleshooting

### Bot doesn't respond
- Check that Message Content Intent is enabled in Discord Developer Portal
- Verify DISCORD_TOKEN in `.env` is correct
- Ensure bot has proper permissions in the server

### Gemini errors
- Verify GEMINI_API_KEY is correct
- Check API quota at Google AI Studio
- Some content may be blocked by safety filters

### Google Forms/Sheets not working
- This feature requires additional setup (credentials.json)
- The bot will fallback to local Excel files if unavailable
- Check that APIs are enabled in Google Cloud Console

### File upload issues
- Maximum file size is 25MB (Discord limit)
- Ensure file type is in the supported list
- Check temp_files folder permissions

## 📝 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Made with ❤️ using Google Gemini AI
