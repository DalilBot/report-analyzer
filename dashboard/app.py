"""
Web Dashboard for Discord Learning Bot
Control panel for managing all bot settings, viewing statistics, and triggering actions
"""
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from functools import wraps
import os
import sys
import json
from datetime import datetime, timedelta
import asyncio
import threading

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DASHBOARD_PASSWORD, DASHBOARD_PORT
from utils.report_memory import report_memory
from utils.assessment_memory import assessment_memory

# Global reference to the bot (set by main.py)
bot_instance = None


def set_bot_instance(bot):
    """Set the bot instance for dashboard to control"""
    global bot_instance
    bot_instance = bot


def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.secret_key = os.urandom(24)
    
    def login_required(f):
        """Decorator to require login"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    
    def run_async(coro):
        """Run an async function from sync context using the bot's loop"""
        if bot_instance and bot_instance.loop:
            future = asyncio.run_coroutine_threadsafe(coro, bot_instance.loop)
            return future.result(timeout=120)
        return None
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Login page"""
        error = None
        if request.method == 'POST':
            if request.form['password'] == DASHBOARD_PASSWORD:
                session['logged_in'] = True
                return redirect(url_for('index'))
            else:
                error = 'Invalid password'
        return render_template('login.html', error=error)
    
    @app.route('/logout')
    def logout():
        """Logout"""
        session.pop('logged_in', None)
        return redirect(url_for('login'))
    
    @app.route('/')
    @login_required
    def index():
        """Main dashboard page"""
        return render_template('index.html')
    
    @app.route('/api/stats')
    @login_required
    def get_stats():
        """Get all statistics"""
        # Homework stats
        hw_summary = report_memory.get_summary()
        
        # Assessment stats
        exam_summary = assessment_memory.get_summary()
        term_info = assessment_memory.get_term_info()
        
        # Upcoming exams
        upcoming_7days = assessment_memory.get_upcoming_exams(days=7)
        exams_tomorrow = assessment_memory.get_exams_tomorrow()
        
        # Pending homework
        pending_hw = report_memory.get_pending_homework()
        
        # Bot status
        bot_status = {
            "online": bot_instance is not None and bot_instance.is_ready() if bot_instance else False,
            "guilds": len(bot_instance.guilds) if bot_instance and bot_instance.is_ready() else 0,
            "user": str(bot_instance.user) if bot_instance and bot_instance.is_ready() else "Not connected"
        }
        
        return jsonify({
            "homework": {
                "pending": hw_summary.get("pending_homework", 0),
                "completed": hw_summary.get("completed_homework", 0),
                "total": hw_summary.get("total_homework", 0),
                "reminders": hw_summary.get("total_reminders", 0)
            },
            "assessments": {
                "total": exam_summary.get("total_exams", 0),
                "completed": exam_summary.get("completed", 0),
                "remaining": exam_summary.get("remaining", 0),
                "upcoming_7_days": len(upcoming_7days),
                "tomorrow": len(exams_tomorrow)
            },
            "term": term_info,
            "bot": bot_status,
            "pending_homework": pending_hw[:10],  # Last 10
            "upcoming_exams": upcoming_7days[:10]  # Next 10
        })
    
    @app.route('/api/settings')
    @login_required
    def get_settings():
        """Get current settings from .env"""
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        settings = {}
        
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        # Don't expose sensitive data fully
                        if 'PASSWORD' in key or 'TOKEN' in key or 'API_KEY' in key:
                            settings[key] = '***' + value[-4:] if len(value) > 4 else '****'
                        else:
                            settings[key] = value
        
        return jsonify(settings)
    
    @app.route('/api/settings', methods=['POST'])
    @login_required
    def update_settings():
        """Update settings in .env"""
        data = request.json
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        
        # Read current env file
        lines = []
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        
        # Update values
        updated_keys = set()
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and '=' in stripped:
                key = stripped.split('=', 1)[0]
                if key in data and not data[key].startswith('***'):
                    new_lines.append(f"{key}={data[key]}\n")
                    updated_keys.add(key)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        # Write back
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        return jsonify({"success": True, "message": "Settings updated. Restart bot to apply changes."})
    
    @app.route('/api/homework')
    @login_required
    def get_homework():
        """Get all homework"""
        pending = report_memory.get_pending_homework()
        all_data = report_memory.get_all_data()
        return jsonify({
            "pending": pending,
            "all": all_data.get("homework", []),
            "reminders": all_data.get("reminders", [])
        })
    
    @app.route('/api/homework/<hw_id>/complete', methods=['POST'])
    @login_required
    def complete_homework(hw_id):
        """Mark homework as completed"""
        success = report_memory.mark_homework_completed(hw_id)
        return jsonify({"success": success})
    
    @app.route('/api/exams')
    @login_required
    def get_exams():
        """Get all exams"""
        all_exams = assessment_memory.get_all_exams()
        upcoming = assessment_memory.get_upcoming_exams(days=30)
        this_week = assessment_memory.get_this_week_exams()
        next_week = assessment_memory.get_next_week_exams()
        
        return jsonify({
            "all": all_exams,
            "upcoming_30_days": upcoming,
            "this_week": this_week,
            "next_week": next_week
        })
    
    @app.route('/api/exams/<exam_id>/complete', methods=['POST'])
    @login_required
    def complete_exam(exam_id):
        """Mark exam as completed"""
        success = assessment_memory.mark_exam_completed(exam_id)
        return jsonify({"success": success})
    
    @app.route('/api/trigger/daily-report', methods=['POST'])
    @login_required
    def trigger_daily_report():
        """Trigger daily report download and send"""
        if not bot_instance:
            return jsonify({"success": False, "message": "Bot not connected"})
        
        try:
            run_async(bot_instance.send_daily_report())
            return jsonify({"success": True, "message": "Daily report triggered!"})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    
    @app.route('/api/trigger/morning-reminder', methods=['POST'])
    @login_required
    def trigger_morning_reminder():
        """Trigger morning homework reminder"""
        if not bot_instance:
            return jsonify({"success": False, "message": "Bot not connected"})
        
        try:
            run_async(bot_instance.send_homework_reminders())
            return jsonify({"success": True, "message": "Morning reminder sent!"})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    
    @app.route('/api/trigger/weekly-reminder', methods=['POST'])
    @login_required
    def trigger_weekly_reminder():
        """Trigger weekly assessment reminder"""
        if not bot_instance:
            return jsonify({"success": False, "message": "Bot not connected"})
        
        try:
            run_async(bot_instance.send_weekly_assessment_reminder())
            return jsonify({"success": True, "message": "Weekly reminder sent!"})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    
    @app.route('/api/trigger/night-reminder', methods=['POST'])
    @login_required
    def trigger_night_reminder():
        """Trigger night-before exam reminder"""
        if not bot_instance:
            return jsonify({"success": False, "message": "Bot not connected"})
        
        try:
            exams_tomorrow = assessment_memory.get_exams_tomorrow()
            if exams_tomorrow:
                run_async(bot_instance.send_night_before_exam_reminder(exams_tomorrow))
                return jsonify({"success": True, "message": f"Night reminder sent for {len(exams_tomorrow)} exam(s)!"})
            else:
                return jsonify({"success": False, "message": "No exams tomorrow to remind about"})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    
    @app.route('/api/trigger/test-message', methods=['POST'])
    @login_required
    def trigger_test_message():
        """Send a test message to the channel"""
        if not bot_instance:
            return jsonify({"success": False, "message": "Bot not connected"})
        
        try:
            from config import REPORT_CHANNEL_ID
            import discord
            
            async def send_test():
                channel = bot_instance.get_channel(REPORT_CHANNEL_ID)
                if channel:
                    embed = discord.Embed(
                        title="🧪 Test Message",
                        description="This is a test message from the dashboard!",
                        color=discord.Color.purple(),
                        timestamp=datetime.now()
                    )
                    embed.add_field(name="Status", value="✅ Dashboard connection working!", inline=False)
                    await channel.send(embed=embed)
                    return True
                return False
            
            result = run_async(send_test())
            if result:
                return jsonify({"success": True, "message": "Test message sent!"})
            else:
                return jsonify({"success": False, "message": "Could not find channel"})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    
    @app.route('/api/logs')
    @login_required
    def get_logs():
        """Get recent activity logs"""
        # For now, return empty - could implement file-based logging later
        return jsonify({"logs": []})
    
    return app
