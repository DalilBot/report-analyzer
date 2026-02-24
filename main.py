"""
Discord AI Learning Bot
Main entry point for running the bot
"""
import asyncio
import sys
import os
import threading

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.discord_bot import run_bot, LearningBot
from config import DISCORD_TOKEN, GEMINI_API_KEY, DASHBOARD_PORT
from dashboard.app import create_app, set_bot_instance


def check_configuration():
    """Check if required configuration is set"""
    errors = []
    
    if not DISCORD_TOKEN or DISCORD_TOKEN == "your_discord_bot_token_here":
        errors.append("❌ DISCORD_TOKEN is not set in .env file")
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        errors.append("❌ GEMINI_API_KEY is not set in .env file")
    
    if errors:
        print("\n⚠️  Configuration Errors:")
        for error in errors:
            print(f"   {error}")
        print("\n📝 Please copy .env.example to .env and fill in your API keys.")
        print("   See README.md for setup instructions.\n")
        return False
    
    return True


def run_dashboard(app):
    """Run Flask dashboard in a separate thread"""
    app.run(host='0.0.0.0', port=DASHBOARD_PORT, debug=False, use_reloader=False, threaded=True)


async def main_async():
    """Run bot and dashboard together"""
    # Create the bot instance
    bot = LearningBot()
    
    # Set bot instance for dashboard
    set_bot_instance(bot)
    
    # Create Flask app
    app = create_app()
    
    # Start dashboard in a separate thread
    dashboard_thread = threading.Thread(target=run_dashboard, args=(app,), daemon=True)
    dashboard_thread.start()
    print(f"🌐 Dashboard started at http://localhost:{DASHBOARD_PORT}")
    
    # Run the bot
    await bot.start(DISCORD_TOKEN)


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║     🤖 Discord AI Learning Bot                    ║
    ║     Powered by Google Gemini                      ║
    ╚═══════════════════════════════════════════════════╝
    """)
    
    if not check_configuration():
        sys.exit(1)
    
    print("🚀 Starting bot and dashboard...")
    print("   Press Ctrl+C to stop\n")
    
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user.")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
