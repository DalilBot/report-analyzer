"""
Discord Bot Module
Main Discord bot implementation with interactive UI components (buttons, dropdowns)
"""
import discord
from discord.ext import commands, tasks
from discord import app_commands, ui
import asyncio
from typing import Optional, List
from datetime import datetime, time, timedelta
import os
import sys

from config import (
    DISCORD_TOKEN, DISCORD_PREFIX, DIFFICULTY_LEVELS,
    CLASSERA_USERNAME, CLASSERA_PASSWORD, REPORT_CHANNEL_ID,
    REPORT_TIME_HOUR, REPORT_TIME_MINUTE,
    MORNING_REMINDER_HOUR, MORNING_REMINDER_MINUTE,
    WEEKLY_REMINDER_DAY, WEEKLY_REMINDER_HOUR, WEEKLY_REMINDER_MINUTE,
    NIGHT_REMINDER_HOUR, NIGHT_REMINDER_MINUTE
)
from utils.session_manager import session_manager, SessionState, UserSession
from utils.file_handler import file_handler
from utils.powerpoint_generator import powerpoint_generator
from utils.report_memory import report_memory
from utils.assessment_memory import assessment_memory
from services.gemini_service import gemini_service
from services.google_services import GoogleServicesManager, get_google_services

# Import report fetcher
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from report_fetcher import download_daily_report


# ============================================================================
# UI COMPONENTS - Buttons and Dropdowns
# ============================================================================

class StartSessionView(ui.View):
    """Initial view with Start button"""
    
    def __init__(self):
        super().__init__(timeout=300)
    
    @ui.button(label="🚀 Start Learning Session", style=discord.ButtonStyle.green, custom_id="start_session")
    async def start_button(self, interaction: discord.Interaction, button: ui.Button):
        session = session_manager.get_session(interaction.user.id)
        session.reset()
        session.state = SessionState.AWAITING_MATERIALS
        
        embed = discord.Embed(
            title="📚 Learning Session Started!",
            description="Welcome! I'm your AI Learning Assistant powered by Google Gemini.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Step 1: Upload Your Materials",
            value=(
                "Please upload your learning materials. I support:\n"
                "• 📄 Documents (PDF, Word, PowerPoint)\n"
                "• 📊 Spreadsheets (Excel, CSV)\n"
                "• 🖼️ Images (PNG, JPG)\n"
                "• 📝 Text files\n\n"
                "**Upload files by attaching them to messages.**"
            ),
            inline=False
        )
        
        # Disable the button after clicking
        button.disabled = True
        await interaction.response.edit_message(embed=interaction.message.embeds[0], view=self)
        
        # Send new message with upload view
        await interaction.followup.send(embed=embed, view=MaterialUploadView(interaction.user.id))


class MaterialUploadView(ui.View):
    """View for material upload phase with Done and Cancel buttons"""
    
    def __init__(self, user_id: int):
        super().__init__(timeout=600)  # 10 minute timeout for uploads
        self.user_id = user_id
    
    @ui.button(label="✅ Done Uploading", style=discord.ButtonStyle.green, custom_id="done_upload")
    async def done_button(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your session!", ephemeral=True)
            return
        
        session = session_manager.get_session(self.user_id)
        
        if not session.uploaded_files:
            await interaction.response.send_message("⚠️ Please upload at least one file before continuing.", ephemeral=True)
            return
        
        # Move to next state
        session.state = SessionState.AWAITING_MEMBERS
        
        embed = discord.Embed(
            title="📁 Files Received!",
            description=f"I've received **{len(session.uploaded_files)}** file(s).",
            color=discord.Color.green()
        )
        
        # List files
        file_list = "\n".join([f"• {f['filename']}" for f in session.uploaded_files])
        embed.add_field(name="Uploaded Files", value=file_list[:1000], inline=False)
        
        embed.add_field(
            name="Step 2: Add Group Members",
            value=(
                "Now, tell me about your group members.\n\n"
                "Enter member names (comma or newline separated):\n"
                "Example: `Alice, Bob, Charlie`"
            ),
            inline=False
        )
        
        # Disable buttons
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        
        await interaction.followup.send(embed=embed, view=MemberInputView(self.user_id))
    
    @ui.button(label="❌ Cancel", style=discord.ButtonStyle.danger, custom_id="cancel_upload")
    async def cancel_button(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your session!", ephemeral=True)
            return
        
        session = session_manager.get_session(self.user_id)
        session.reset()
        
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        
        await interaction.followup.send("❌ Session cancelled. Use the Start button to begin a new session.")


class MemberInputView(ui.View):
    """View for member input phase"""
    
    def __init__(self, user_id: int):
        super().__init__(timeout=600)
        self.user_id = user_id
    
    @ui.button(label="✅ Done Adding Members", style=discord.ButtonStyle.green, custom_id="done_members")
    async def done_button(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your session!", ephemeral=True)
            return
        
        session = session_manager.get_session(self.user_id)
        
        if not session.group_members:
            await interaction.response.send_message("⚠️ Please add at least one group member.", ephemeral=True)
            return
        
        # Move to difficulty assignment
        session.state = SessionState.AWAITING_DIFFICULTY
        session.current_member_index = 0
        
        # Disable buttons
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        
        # Show difficulty selection for first member
        await show_difficulty_selector(interaction.channel, session)
    
    @ui.button(label="❌ Cancel", style=discord.ButtonStyle.danger, custom_id="cancel_members")
    async def cancel_button(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your session!", ephemeral=True)
            return
        
        session = session_manager.get_session(self.user_id)
        session.reset()
        
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        
        await interaction.followup.send("❌ Session cancelled.")


class DifficultySelect(ui.Select):
    """Dropdown for selecting difficulty level"""
    
    def __init__(self, user_id: int, member_name: str, member_index: int):
        self.user_id = user_id
        self.member_name = member_name
        self.member_index = member_index
        
        options = [
            discord.SelectOption(label=f"Level {level}: {name}", value=str(level), emoji=self._get_emoji(level))
            for level, name in DIFFICULTY_LEVELS.items()
        ]
        
        super().__init__(
            placeholder=f"Select difficulty for {member_name}...",
            options=options,
            custom_id=f"difficulty_{member_index}"
        )
    
    def _get_emoji(self, level: int) -> str:
        emojis = {1: "🌱", 2: "🌿", 3: "🌳", 4: "🔥", 5: "⭐"}
        return emojis.get(level, "📊")
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your session!", ephemeral=True)
            return
        
        session = session_manager.get_session(self.user_id)
        level = int(self.values[0])
        
        # Assign difficulty to member
        member = session.group_members[self.member_index]
        member.difficulty_level = level
        
        # Disable this select
        self.disabled = True
        self.placeholder = f"{self.member_name}: Level {level} ({DIFFICULTY_LEVELS[level]})"
        await interaction.response.edit_message(view=self.view)
        
        await interaction.followup.send(
            f"✅ Set **{self.member_name}**'s level to **{level}** ({DIFFICULTY_LEVELS[level]})",
            ephemeral=False
        )
        
        # Move to next member
        session.current_member_index += 1
        await show_difficulty_selector(interaction.channel, session)


class DifficultyView(ui.View):
    """View containing difficulty dropdown"""
    
    def __init__(self, user_id: int, member_name: str, member_index: int):
        super().__init__(timeout=300)
        self.add_item(DifficultySelect(user_id, member_name, member_index))


class SurveyChoiceView(ui.View):
    """View for survey yes/no choice"""
    
    def __init__(self, user_id: int):
        super().__init__(timeout=300)
        self.user_id = user_id
    
    @ui.button(label="✅ Yes, Create Survey", style=discord.ButtonStyle.green, custom_id="survey_yes")
    async def yes_button(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your session!", ephemeral=True)
            return
        
        session = session_manager.get_session(self.user_id)
        session.wants_survey = True
        
        # Disable buttons
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        
        # Create survey
        cog = interaction.client.get_cog('LearningCog')
        await cog._create_survey(interaction.channel, session)
    
    @ui.button(label="❌ No, Skip Survey", style=discord.ButtonStyle.secondary, custom_id="survey_no")
    async def no_button(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your session!", ephemeral=True)
            return
        
        session = session_manager.get_session(self.user_id)
        session.wants_survey = False
        
        # Disable buttons
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        
        # Ask about PowerPoint instead of completing
        cog = interaction.client.get_cog('LearningCog')
        await cog._ask_powerpoint_choice(interaction.channel, session)


class PowerPointChoiceView(ui.View):
    """View for PowerPoint generation yes/no choice"""
    
    def __init__(self, user_id: int):
        super().__init__(timeout=300)
        self.user_id = user_id
    
    @ui.button(label="🎨 Yes, Generate PowerPoint", style=discord.ButtonStyle.green, custom_id="ppt_yes")
    async def yes_button(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your session!", ephemeral=True)
            return
        
        session = session_manager.get_session(self.user_id)
        session.wants_powerpoint = True
        
        # Disable buttons
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        
        # Create PowerPoint
        cog = interaction.client.get_cog('LearningCog')
        await cog._create_powerpoint(interaction.channel, session)
    
    @ui.button(label="❌ No, Finish Session", style=discord.ButtonStyle.secondary, custom_id="ppt_no")
    async def no_button(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your session!", ephemeral=True)
            return
        
        session = session_manager.get_session(self.user_id)
        session.wants_powerpoint = False
        
        # Disable buttons
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        
        # Complete session
        cog = interaction.client.get_cog('LearningCog')
        await cog._complete_session(interaction.channel, session)


class SlideCountSelect(ui.Select):
    """Dropdown for selecting number of slides"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        
        options = [
            discord.SelectOption(label="5 slides - Quick Overview", value="5", emoji="⚡"),
            discord.SelectOption(label="10 slides - Standard", value="10", emoji="📊", default=True),
            discord.SelectOption(label="15 slides - Detailed", value="15", emoji="📚"),
            discord.SelectOption(label="20 slides - Comprehensive", value="20", emoji="🎓"),
        ]
        
        super().__init__(
            placeholder="Select number of slides...",
            options=options,
            custom_id="slide_count"
        )
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your session!", ephemeral=True)
            return
        
        session = session_manager.get_session(self.user_id)
        num_slides = int(self.values[0])
        
        # Disable select
        self.disabled = True
        self.placeholder = f"Selected: {num_slides} slides"
        await interaction.response.edit_message(view=self.view)
        
        # Store selection and create PowerPoint
        session.wants_powerpoint = True
        
        cog = interaction.client.get_cog('LearningCog')
        await cog._create_powerpoint(interaction.channel, session, num_slides)


class PowerPointOptionsView(ui.View):
    """View with slide count dropdown and cancel button"""
    
    def __init__(self, user_id: int):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.add_item(SlideCountSelect(user_id))
    
    @ui.button(label="❌ Skip PowerPoint", style=discord.ButtonStyle.secondary, row=1)
    async def skip_button(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your session!", ephemeral=True)
            return
        
        session = session_manager.get_session(self.user_id)
        session.wants_powerpoint = False
        
        # Disable all
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        
        cog = interaction.client.get_cog('LearningCog')
        await cog._complete_session(interaction.channel, session)


class NewSessionView(ui.View):
    """View shown at end with button to start new session"""
    
    def __init__(self):
        super().__init__(timeout=None)  # Persistent
    
    @ui.button(label="🔄 Start New Session", style=discord.ButtonStyle.primary, custom_id="new_session")
    async def new_session_button(self, interaction: discord.Interaction, button: ui.Button):
        session = session_manager.get_session(interaction.user.id)
        session.reset()
        session.state = SessionState.AWAITING_MATERIALS
        
        embed = discord.Embed(
            title="📚 New Learning Session Started!",
            description="Let's begin! Upload your learning materials.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Step 1: Upload Your Materials",
            value=(
                "I support:\n"
                "• 📄 Documents (PDF, Word, PowerPoint)\n"
                "• 📊 Spreadsheets (Excel, CSV)\n"
                "• 🖼️ Images (PNG, JPG)\n"
                "• 📝 Text files"
            ),
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, view=MaterialUploadView(interaction.user.id))


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def show_difficulty_selector(channel, session: UserSession):
    """Show difficulty dropdown for the current member"""
    if session.current_member_index >= len(session.group_members):
        # All members have difficulty assigned, process analysis
        cog = channel._state._get_client().get_cog('LearningCog')
        await cog._process_analysis(channel, session)
        return
    
    member = session.group_members[session.current_member_index]
    
    embed = discord.Embed(
        title=f"🎯 Set Difficulty for {member.name}",
        description="Select this member's skill/difficulty level from the dropdown below:",
        color=discord.Color.orange()
    )
    
    difficulty_text = "\n".join([
        f"**{level}** - {name}" for level, name in DIFFICULTY_LEVELS.items()
    ])
    embed.add_field(name="Level Guide", value=difficulty_text, inline=False)
    embed.set_footer(text=f"Member {session.current_member_index + 1} of {len(session.group_members)}")
    
    view = DifficultyView(session.user_id, member.name, session.current_member_index)
    await channel.send(embed=embed, view=view)


# ============================================================================
# MAIN BOT CLASS
# ============================================================================

class LearningBot(commands.Bot):
    """Main Discord Bot class"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.dm_messages = True
        intents.guilds = True
        
        super().__init__(
            command_prefix=DISCORD_PREFIX,
            intents=intents,
            description="AI Learning Assistant powered by Google Gemini"
        )
        
        self.google_services: Optional[GoogleServicesManager] = None
        self.report_sent_today = False  # Track if report was sent today
        self.reminder_sent_today = False  # Track if morning reminder was sent
        self.weekly_assessment_sent = False  # Track weekly assessment reminder
        self.night_exam_reminded_dates = set()  # Track which exam dates we've reminded
    
    async def setup_hook(self):
        """Called when the bot is starting up"""
        # Add cogs
        await self.add_cog(LearningCog(self))
        
        # Register persistent views
        self.add_view(NewSessionView())
        
        # Start session cleanup task
        session_manager.start_cleanup_task(self.loop)
        
        # Start daily report task
        self.daily_report_task.start()
        
        # Start homework reminder task
        self.homework_reminder_task.start()
        
        # Start assessment reminder tasks
        self.weekly_assessment_reminder_task.start()
        self.night_before_exam_task.start()
        
        # Cleanup old report data (7 days retention)
        report_memory.cleanup_old_data(days=7)
        
        # Try to initialize Google services (may fail if not configured)
        try:
            self.google_services = get_google_services()
            print("✅ Google Services initialized successfully")
        except Exception as e:
            print(f"⚠️ Google Services not available: {e}")
            print("   The bot will use local Excel files instead of Google Sheets/Forms")
    
    @tasks.loop(minutes=1)
    async def daily_report_task(self):
        """Check every minute if it's time to send the daily report"""
        now = datetime.now()
        
        # Reset the flag at midnight
        if now.hour == 0 and now.minute == 0:
            self.report_sent_today = False
            self.reminder_sent_today = False
            # Daily cleanup of old data
            report_memory.cleanup_old_data(days=7)
        
        # Check if it's report time and we haven't sent today
        if (now.hour == REPORT_TIME_HOUR and 
            now.minute == REPORT_TIME_MINUTE and 
            not self.report_sent_today):
            
            await self.send_daily_report()
            self.report_sent_today = True
    
    @daily_report_task.before_loop
    async def before_daily_report_task(self):
        """Wait until the bot is ready before starting the task"""
        await self.wait_until_ready()
        print(f"📅 Daily report scheduler started (scheduled for {REPORT_TIME_HOUR:02d}:{REPORT_TIME_MINUTE:02d})")
    
    @tasks.loop(minutes=1)
    async def homework_reminder_task(self):
        """Send morning reminders for pending homework"""
        now = datetime.now()
        
        # Send reminder at configured time every day
        if now.hour == MORNING_REMINDER_HOUR and now.minute == MORNING_REMINDER_MINUTE and not self.reminder_sent_today:
            await self.send_homework_reminders()
            self.reminder_sent_today = True
    
    @homework_reminder_task.before_loop
    async def before_homework_reminder_task(self):
        """Wait until the bot is ready"""
        await self.wait_until_ready()
        print(f"🔔 Homework reminder scheduler started (scheduled for {MORNING_REMINDER_HOUR:02d}:{MORNING_REMINDER_MINUTE:02d})")
    
    async def send_homework_reminders(self):
        """Send reminders for pending homework and upcoming deadlines"""
        if not REPORT_CHANNEL_ID or REPORT_CHANNEL_ID == 0:
            return
        
        channel = self.get_channel(REPORT_CHANNEL_ID)
        if not channel:
            return
        
        # Get items due soon (today and tomorrow)
        due_soon = report_memory.get_due_soon(days=1)
        homework = due_soon.get("homework", [])
        reminders = due_soon.get("reminders", [])
        
        # Get all pending homework
        all_pending = report_memory.get_pending_homework()
        
        if not homework and not reminders and not all_pending:
            return  # Nothing to remind
        
        embed = discord.Embed(
            title="🔔 Morning Homework Reminder",
            description=f"Good morning! Here's what you need to work on today ({datetime.now().strftime('%B %d, %Y')})",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        
        # Due today section
        if homework:
            hw_text = ""
            for hw in homework:
                subject = hw.get("subject", "Unknown")
                task = hw.get("task", "")
                due = hw.get("due_date", "next session")
                hw_text += f"**📚 {subject}**\n"
                hw_text += f"   └ {task}\n"
                hw_text += f"   └ ⏰ Due: {due}\n\n"
            
            if len(hw_text) > 1024:
                hw_text = hw_text[:1000] + "..."
            
            embed.add_field(
                name="⚠️ Due Today / Next Session",
                value=hw_text,
                inline=False
            )
        
        # Upcoming reminders
        if reminders:
            rem_text = ""
            for rem in reminders:
                desc = rem.get("description", "")
                date = rem.get("date", "")
                rem_type = rem.get("type", "note")
                
                emoji = "📌"
                if "test" in rem_type.lower():
                    emoji = "📝"
                elif "event" in rem_type.lower():
                    emoji = "🎉"
                elif "deadline" in rem_type.lower():
                    emoji = "⏰"
                
                rem_text += f"{emoji} {desc}"
                if date:
                    rem_text += f" *(📅 {date})*"
                rem_text += "\n"
            
            if len(rem_text) > 1024:
                rem_text = rem_text[:1000] + "..."
            
            embed.add_field(
                name="📋 Today's Reminders",
                value=rem_text,
                inline=False
            )
        
        # Summary of all pending
        summary = report_memory.get_summary()
        embed.add_field(
            name="📊 Homework Status",
            value=(
                f"• Pending assignments: **{summary['pending_homework']}**\n"
                f"• Completed: **{summary['completed_homework']}**"
            ),
            inline=False
        )
        
        embed.set_footer(text="Use reactions or reply to mark homework as done!")
        
        await channel.send(embed=embed)
        print(f"✅ Morning reminder sent at {datetime.now().strftime('%H:%M:%S')}")
    
    @tasks.loop(minutes=1)
    async def weekly_assessment_reminder_task(self):
        """Send weekly assessment reminders on configured day at configured time"""
        now = datetime.now()
        
        # Reset flag at midnight on the configured day
        if now.weekday() == WEEKLY_REMINDER_DAY and now.hour == 0 and now.minute == 0:
            self.weekly_assessment_sent = False
            assessment_memory.reset_weekly_reminders()
        
        # Send reminder on configured day at configured time
        if now.weekday() == WEEKLY_REMINDER_DAY and now.hour == WEEKLY_REMINDER_HOUR and now.minute == WEEKLY_REMINDER_MINUTE and not self.weekly_assessment_sent:
            await self.send_weekly_assessment_reminder()
            self.weekly_assessment_sent = True
    
    @weekly_assessment_reminder_task.before_loop
    async def before_weekly_assessment_task(self):
        """Wait until the bot is ready"""
        await self.wait_until_ready()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_name = days[WEEKLY_REMINDER_DAY] if 0 <= WEEKLY_REMINDER_DAY <= 6 else 'Unknown'
        print(f"📅 Weekly assessment reminder scheduler started ({day_name} {WEEKLY_REMINDER_HOUR:02d}:{WEEKLY_REMINDER_MINUTE:02d})")
    
    @tasks.loop(minutes=1)
    async def night_before_exam_task(self):
        """Send night-before exam reminders at configured time"""
        now = datetime.now()
        
        # Clear reminded dates at midnight
        if now.hour == 0 and now.minute == 0:
            self.night_exam_reminded_dates.clear()
        
        # Send reminder at configured time
        if now.hour == NIGHT_REMINDER_HOUR and now.minute == NIGHT_REMINDER_MINUTE:
            tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
            
            # Only remind if we haven't reminded for tomorrow's exams yet
            if tomorrow not in self.night_exam_reminded_dates:
                exams_tomorrow = assessment_memory.get_exams_tomorrow()
                if exams_tomorrow:
                    await self.send_night_before_exam_reminder(exams_tomorrow)
                    self.night_exam_reminded_dates.add(tomorrow)
    
    @night_before_exam_task.before_loop
    async def before_night_exam_task(self):
        """Wait until the bot is ready"""
        await self.wait_until_ready()
        print(f"🌙 Night-before exam reminder scheduler started ({NIGHT_REMINDER_HOUR:02d}:{NIGHT_REMINDER_MINUTE:02d})")
    
    async def send_weekly_assessment_reminder(self):
        """Send weekly reminder of upcoming assessments"""
        if not REPORT_CHANNEL_ID or REPORT_CHANNEL_ID == 0:
            return
        
        channel = self.get_channel(REPORT_CHANNEL_ID)
        if not channel:
            return
        
        # Get exams for this week and next week
        this_week = assessment_memory.get_this_week_exams()
        next_week = assessment_memory.get_next_week_exams()
        term_info = assessment_memory.get_term_info()
        
        if not this_week and not next_week:
            return  # No upcoming exams
        
        embed = discord.Embed(
            title="📅 Weekly Assessment Reminder",
            description=f"**{term_info.get('term', 'Term')}** - {term_info.get('grade', 'Grade')}",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        # This week's exams
        if this_week:
            week_text = ""
            for exam in this_week:
                date = exam.get('date', '')
                day = exam.get('day_of_week', '')[:3]
                subject = exam.get('subject', 'Unknown')
                exam_type = exam.get('exam_type', 'Assessment')
                topics = exam.get('topics', [])
                
                week_text += f"**{day} {date}** - {subject} ({exam_type})\n"
                if topics:
                    week_text += f"   📚 Topics: {', '.join(topics[:3])}\n"
            
            if len(week_text) > 1024:
                week_text = week_text[:1000] + "..."
            
            embed.add_field(
                name="⚠️ This Week",
                value=week_text,
                inline=False
            )
        
        # Next week's exams
        if next_week:
            week_text = ""
            for exam in next_week:
                date = exam.get('date', '')
                day = exam.get('day_of_week', '')[:3]
                subject = exam.get('subject', 'Unknown')
                exam_type = exam.get('exam_type', 'Assessment')
                
                week_text += f"**{day} {date}** - {subject} ({exam_type})\n"
            
            if len(week_text) > 1024:
                week_text = week_text[:1000] + "..."
            
            embed.add_field(
                name="📆 Next Week",
                value=week_text,
                inline=False
            )
        
        # Summary
        summary = assessment_memory.get_summary()
        embed.add_field(
            name="📊 Term Progress",
            value=(
                f"• Remaining exams: **{summary['remaining']}**\n"
                f"• Completed: **{summary['completed']}**"
            ),
            inline=False
        )
        
        embed.set_footer(text="Good luck with your studies! 📚")
        
        await channel.send(embed=embed)
        print(f"✅ Weekly assessment reminder sent at {datetime.now().strftime('%H:%M:%S')}")
    
    async def send_night_before_exam_reminder(self, exams: List[dict]):
        """Send reminder the night before exams with material covered"""
        if not REPORT_CHANNEL_ID or REPORT_CHANNEL_ID == 0:
            return
        
        channel = self.get_channel(REPORT_CHANNEL_ID)
        if not channel:
            return
        
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%B %d, %Y")
        
        embed = discord.Embed(
            title=f"🌙 Exam Tomorrow! - {tomorrow}",
            description="Here's everything you need to know for tomorrow's exam(s):",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        
        # Get related homework/material from daily reports (7-day memory)
        all_homework = report_memory.get_pending_homework()
        
        for exam in exams:
            subject = exam.get('subject', 'Unknown')
            exam_type = exam.get('exam_type', 'Assessment')
            topics = exam.get('topics', [])
            notes = exam.get('notes', '')
            
            # Build exam info
            exam_text = f"**Type:** {exam_type}\n"
            
            if topics:
                exam_text += f"**Topics:** {', '.join(topics)}\n"
            
            if notes:
                exam_text += f"**Notes:** {notes}\n"
            
            # Find related homework from the subject
            related_hw = [
                hw for hw in all_homework 
                if subject.lower() in hw.get('subject', '').lower()
            ]
            
            if related_hw:
                exam_text += f"\n**📝 Related homework from this week:**\n"
                for hw in related_hw[:3]:  # Max 3 items
                    task = hw.get('task', '')[:50]
                    exam_text += f"• {task}\n"
            
            if len(exam_text) > 1024:
                exam_text = exam_text[:1000] + "..."
            
            embed.add_field(
                name=f"📚 {subject}",
                value=exam_text,
                inline=False
            )
            
            # Mark as reminded
            assessment_memory.mark_reminded_night_before(exam.get('id', ''))
        
        # Study tips
        embed.add_field(
            name="💡 Quick Tips",
            value=(
                "• Review your notes and homework\n"
                "• Get a good night's sleep\n"
                "• Prepare your materials tonight\n"
                "• Eat a good breakfast tomorrow"
            ),
            inline=False
        )
        
        embed.set_footer(text="You've got this! Good luck! 🍀")
        
        await channel.send(embed=embed)
        print(f"✅ Night-before exam reminder sent for {len(exams)} exam(s)")
    
    async def send_daily_report(self):
        """Download and send the daily report to the configured channel"""
        # Check if configuration is complete
        if not CLASSERA_USERNAME or not CLASSERA_PASSWORD:
            print("⚠️ Classera credentials not configured. Skipping daily report.")
            return
        
        if not REPORT_CHANNEL_ID or REPORT_CHANNEL_ID == 0:
            print("⚠️ Report channel ID not configured. Skipping daily report.")
            return
        
        channel = self.get_channel(REPORT_CHANNEL_ID)
        if not channel:
            print(f"⚠️ Could not find channel with ID {REPORT_CHANNEL_ID}")
            return
        
        print(f"📥 Downloading daily report at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
        
        # Send "downloading" message
        embed = discord.Embed(
            title="📥 Downloading Daily Report...",
            description="Please wait while I fetch today's report from Classera.",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        status_msg = await channel.send(embed=embed)
        
        try:
            # Run the download in a thread to not block the bot
            loop = asyncio.get_event_loop()
            report_path = await loop.run_in_executor(
                None,
                lambda: download_daily_report(
                    username=CLASSERA_USERNAME,
                    password=CLASSERA_PASSWORD,
                    download_path="./daily_reports",
                    quiet=True
                )
            )
            
            if report_path and os.path.exists(report_path):
                # Analyze the report with AI (send PDF directly to Gemini)
                analysis = {}
                embed = discord.Embed(
                    title="🤖 Analyzing Report...",
                    description="Using AI to extract homework and reminders...",
                    color=discord.Color.blue(),
                    timestamp=datetime.now()
                )
                await status_msg.edit(embed=embed)
                
                try:
                    analysis = await gemini_service.analyze_daily_report(report_path)
                except Exception as e:
                    print(f"⚠️ AI analysis failed: {e}")
                
                # Save to 7-day memory
                added = report_memory.add_from_analysis(analysis)
                print(f"📝 Saved to memory: {added['homework']} homework, {added['reminders']} reminders")
                
                # Build the main embed
                embed = discord.Embed(
                    title=f"📄 Daily Report - {datetime.now().strftime('%B %d, %Y')}",
                    description="Here's your daily report summary!",
                    color=discord.Color.green(),
                    timestamp=datetime.now()
                )
                
                # Add homework section
                homework = analysis.get('homework', [])
                if homework:
                    hw_text = ""
                    for i, hw in enumerate(homework, 1):
                        subject = hw.get('subject', 'Unknown')
                        task = hw.get('task', 'No description')
                        due = hw.get('due_date')
                        # Default to "next session" if no due date
                        if not due or due.lower() in ["null", "none", ""]:
                            due = "next session"
                        hw_text += f"**{i}. {subject}**\n"
                        hw_text += f"   📝 {task}\n"
                        hw_text += f"   📅 Due: {due}\n"
                        hw_text += "\n"
                    
                    # Split if too long
                    if len(hw_text) > 1024:
                        hw_text = hw_text[:1000] + "..."
                    
                    embed.add_field(
                        name="📚 Homework",
                        value=hw_text or "No homework found",
                        inline=False
                    )
                else:
                    embed.add_field(
                        name="📚 Homework",
                        value="✅ No homework assigned today!",
                        inline=False
                    )
                
                # Add reminders section
                reminders = analysis.get('reminders', [])
                if reminders:
                    rem_text = ""
                    for i, rem in enumerate(reminders, 1):
                        rem_type = rem.get('type', 'note')
                        desc = rem.get('description', 'No description')
                        date = rem.get('date')
                        
                        # Emoji based on type
                        emoji = "📌"
                        if 'test' in rem_type.lower():
                            emoji = "📝"
                        elif 'event' in rem_type.lower():
                            emoji = "🎉"
                        elif 'deadline' in rem_type.lower():
                            emoji = "⏰"
                        
                        rem_text += f"{emoji} {desc}"
                        if date:
                            rem_text += f" *(📅 {date})*"
                        rem_text += "\n"
                    
                    # Split if too long
                    if len(rem_text) > 1024:
                        rem_text = rem_text[:1000] + "..."
                    
                    embed.add_field(
                        name="🔔 Reminders",
                        value=rem_text or "No reminders",
                        inline=False
                    )
                else:
                    embed.add_field(
                        name="🔔 Reminders",
                        value="No reminders for today",
                        inline=False
                    )
                
                # Add summary if available
                summary = analysis.get('summary')
                if summary:
                    embed.add_field(
                        name="📋 Quick Summary",
                        value=summary,
                        inline=False
                    )
                
                # Show memory status
                memory_summary = report_memory.get_summary()
                embed.add_field(
                    name="📊 7-Day Homework Tracker",
                    value=(
                        f"• Total pending: **{memory_summary['pending_homework']}**\n"
                        f"• Completed: **{memory_summary['completed_homework']}**\n"
                        f"• Active reminders: **{memory_summary['total_reminders']}**"
                    ),
                    inline=False
                )
                
                embed.set_footer(text="Auto-downloaded from Classera • AI-analyzed by Gemini • 7-day memory active")
                
                await status_msg.edit(embed=embed)
                
                # Send the PDF file
                await channel.send(
                    content="📎 **Full Report Attached:**",
                    file=discord.File(report_path)
                )
                
                print(f"✅ Daily report sent successfully: {os.path.basename(report_path)}")
            else:
                # Failed to download
                embed = discord.Embed(
                    title="❌ Report Download Failed",
                    description="Could not download the daily report. Please check manually.",
                    color=discord.Color.red(),
                    timestamp=datetime.now()
                )
                await status_msg.edit(embed=embed)
                print("❌ Failed to download daily report")
                
        except Exception as e:
            print(f"❌ Error during daily report: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"An error occurred: {str(e)[:200]}",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            await status_msg.edit(embed=embed)
    
    async def on_ready(self):
        """Called when the bot is fully ready"""
        print(f'🤖 {self.user} is now running!')
        print(f'📊 Connected to {len(self.guilds)} guilds')
        print('-----------------------------------')
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="DMs | !start to begin"
            )
        )


# ============================================================================
# LEARNING COG
# ============================================================================

class LearningCog(commands.Cog):
    """Cog containing all learning-related commands and handlers"""
    
    def __init__(self, bot: LearningBot):
        self.bot = bot
    
    @commands.command(name='start', aliases=['begin', 'Start', 'START'])
    async def start_session(self, ctx: commands.Context):
        """Start a new learning session"""
        # Only work in DMs
        if not isinstance(ctx.channel, discord.DMChannel):
            embed = discord.Embed(
                title="📨 DM Required",
                description="Please DM me to start a learning session! This keeps your materials private.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return
        
        session = session_manager.get_session(ctx.author.id)
        session.reset()
        
        embed = discord.Embed(
            title="🤖 AI Learning Assistant",
            description=(
                "Welcome! I'll help you:\n"
                "• 📚 Analyze learning materials\n"
                "• 👥 Divide tasks among group members\n"
                "• 📝 Create surveys with predictions\n\n"
                "Click the button below to begin!"
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text="Powered by Google Gemini")
        
        await ctx.send(embed=embed, view=StartSessionView())
    
    @commands.command(name='cancel', aliases=['stop', 'quit'])
    async def cancel_session(self, ctx: commands.Context):
        """Cancel the current session"""
        if not isinstance(ctx.channel, discord.DMChannel):
            return
        
        session = session_manager.get_session(ctx.author.id)
        session.reset()
        
        embed = discord.Embed(
            title="❌ Session Cancelled",
            description="Your session has been cancelled.",
            color=discord.Color.red()
        )
        
        await ctx.send(embed=embed, view=StartSessionView())
    
    @commands.command(name='status')
    async def session_status(self, ctx: commands.Context):
        """Check current session status"""
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("📨 Please DM me to check your session status.")
            return
        
        session = session_manager.get_session(ctx.author.id)
        
        embed = discord.Embed(
            title="📊 Session Status",
            color=discord.Color.green()
        )
        
        # State with emoji
        state_emojis = {
            SessionState.IDLE: "⏸️",
            SessionState.AWAITING_MATERIALS: "📁",
            SessionState.AWAITING_MEMBERS: "👥",
            SessionState.AWAITING_DIFFICULTY: "🎯",
            SessionState.PROCESSING_ANALYSIS: "🔄",
            SessionState.SHOWING_TASK_DIVISION: "📋",
            SessionState.AWAITING_SURVEY_CHOICE: "📝",
            SessionState.CREATING_SURVEY: "⏳",
            SessionState.COMPLETED: "✅"
        }
        
        emoji = state_emojis.get(session.state, "❓")
        embed.add_field(name="State", value=f"{emoji} {session.state.value}", inline=True)
        embed.add_field(name="Files Uploaded", value=f"📁 {len(session.uploaded_files)}", inline=True)
        embed.add_field(name="Group Members", value=f"👥 {len(session.group_members)}", inline=True)
        
        if session.group_members:
            members_list = ", ".join([m.name for m in session.group_members])
            embed.add_field(name="Members", value=members_list[:500], inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Handle incoming messages for conversation flow"""
        # Ignore bot's own messages
        if message.author == self.bot.user:
            return
        
        # Only process DMs
        if not isinstance(message.channel, discord.DMChannel):
            return
        
        # Don't process commands here (let command handler do it)
        if message.content.startswith(DISCORD_PREFIX):
            return
        
        session = session_manager.get_session(message.author.id)
        
        # Handle based on current state
        if session.state == SessionState.AWAITING_MATERIALS:
            await self._handle_materials(message, session)
        
        elif session.state == SessionState.AWAITING_MEMBERS:
            await self._handle_members(message, session)
        
        elif session.state in [SessionState.IDLE, SessionState.COMPLETED]:
            # Handle general questions about tasks, homework, exams
            if message.content.strip():
                await self._handle_dm_question(message)
    
    async def _handle_materials(self, message: discord.Message, session: UserSession):
        """Handle file uploads during material collection phase"""
        # Process file attachments
        if message.attachments:
            async with message.channel.typing():
                for attachment in message.attachments:
                    if not file_handler.is_valid_file(attachment.filename):
                        embed = discord.Embed(
                            title="⚠️ Unsupported File",
                            description=f"Skipped `{attachment.filename}` - unsupported file type.",
                            color=discord.Color.orange()
                        )
                        await message.channel.send(embed=embed)
                        continue
                    
                    # Download file
                    filepath = await file_handler.download_attachment(
                        attachment.url, 
                        attachment.filename
                    )
                    
                    if filepath:
                        # Extract content
                        content = await file_handler.extract_content(filepath)
                        
                        # Handle images specially
                        if content.get('is_binary') and content.get('image_data'):
                            image_analysis = await gemini_service.analyze_image(
                                content['image_data'],
                                content['mime_type']
                            )
                            content['content'] = image_analysis
                        
                        session.uploaded_files.append({
                            "filename": attachment.filename,
                            "filepath": filepath,
                            "size": attachment.size
                        })
                        session.file_contents.append(content)
                        
                        embed = discord.Embed(
                            title="✅ File Received",
                            description=f"`{attachment.filename}`\nTotal files: **{len(session.uploaded_files)}**",
                            color=discord.Color.green()
                        )
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="❌ Download Failed",
                            description=f"Failed to download: `{attachment.filename}`",
                            color=discord.Color.red()
                        )
                        await message.channel.send(embed=embed)
        
        elif message.content.strip():
            # User sent text - remind them to use the button
            embed = discord.Embed(
                title="📎 Upload Files",
                description=(
                    "Please upload files by **attaching them** to your message.\n\n"
                    "When you're done uploading, click the **Done Uploading** button above."
                ),
                color=discord.Color.blue()
            )
            await message.channel.send(embed=embed)
    
    async def _handle_members(self, message: discord.Message, session: UserSession):
        """Handle group member input"""
        content = message.content.strip()
        
        if not content:
            return
        
        # Parse member names (comma or newline separated)
        if ',' in content:
            names = [n.strip() for n in content.split(',') if n.strip()]
        else:
            names = [n.strip() for n in content.split('\n') if n.strip()]
        
        added = []
        for name in names:
            if name and len(name) <= 50:  # Basic validation
                session.add_member(name)
                added.append(name)
        
        if added:
            embed = discord.Embed(
                title="✅ Members Added",
                description="\n".join([f"• **{name}**" for name in added]),
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Total members: {len(session.group_members)}")
            await message.channel.send(embed=embed)
    
    async def _handle_dm_question(self, message: discord.Message):
        """Handle DM questions about homework, tasks, exams, and survey creation"""
        question = message.content.strip()
        
        # Check if user wants to create a survey
        survey_keywords = ['survey', 'استبيان', 'استطلاع', 'poll', 'create survey', 'make survey', 'اعمل استبيان', 'سوي استبيان']
        is_survey_request = any(kw in question.lower() for kw in survey_keywords)
        
        async with message.channel.typing():
            try:
                if is_survey_request:
                    # Handle survey creation request
                    await self._create_dm_survey(message, question)
                else:
                    # Handle general question
                    await self._answer_dm_question(message, question)
                    
            except Exception as e:
                print(f"DM question error: {e}")
                embed = discord.Embed(
                    title="❌ Error",
                    description="Something went wrong. Please try again later.",
                    color=discord.Color.red()
                )
                await message.channel.send(embed=embed)
    
    async def _create_dm_survey(self, message: discord.Message, question: str):
        """Create a survey with predicted responses from 25 people"""
        # Gather context
        context_data = self._build_dm_context()
        
        prompt = f"""You are helping a student create an opinion survey. The student asked:
"{question}"

Context about their studies:
- Homework: {context_data['homework'][:500]}
- Upcoming Exams: {context_data['exams'][:500]}

Create a survey based on their request. If they didn't specify a topic, create a survey about their studies/school life.

IMPORTANT RULES:
1. Create 5-7 survey questions (opinion-based, NO right/wrong answers)
2. Each question should have 3-5 multiple choice options
3. Predict how 25 people would answer each question (distribute realistically)
4. Questions can be in Arabic if the context is Arabic
5. Make questions interesting and relevant

Respond in this EXACT JSON format:
{{
    "survey_title": "Survey title here",
    "survey_description": "Brief description",
    "questions": [
        {{
            "question": "The question text?",
            "options": [
                {{"text": "Option A", "predicted_votes": 8}},
                {{"text": "Option B", "predicted_votes": 10}},
                {{"text": "Option C", "predicted_votes": 7}}
            ]
        }},
        ...more questions
    ],
    "analysis": "Brief analysis of what these predictions suggest about the group"
}}

Make sure predicted_votes for each question sum to exactly 25."""

        response = await gemini_service.generate_response(prompt)
        
        if not response:
            embed = discord.Embed(
                title="❌ Error",
                description="Couldn't generate survey. Please try again.",
                color=discord.Color.red()
            )
            await message.channel.send(embed=embed)
            return
        
        # Parse JSON response
        try:
            # Extract JSON from response
            import json
            import re
            
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                survey_data = json.loads(json_match.group())
            else:
                raise ValueError("No JSON found")
        except Exception as e:
            print(f"Survey JSON parse error: {e}")
            # Send raw response as fallback
            embed = discord.Embed(
                title="📊 Survey Generated",
                description=response[:2000],
                color=discord.Color.purple()
            )
            await message.channel.send(embed=embed)
            return
        
        # Create main survey embed
        main_embed = discord.Embed(
            title=f"📊 {survey_data.get('survey_title', 'Survey')}",
            description=survey_data.get('survey_description', ''),
            color=discord.Color.purple()
        )
        main_embed.set_footer(text="Predicted responses from 25 people")
        await message.channel.send(embed=main_embed)
        
        # Send each question with predictions
        questions = survey_data.get('questions', [])
        for i, q in enumerate(questions, 1):
            question_text = q.get('question', 'Question')
            options = q.get('options', [])
            
            # Build prediction bars
            results_text = ""
            for opt in options:
                text = opt.get('text', 'Option')
                votes = opt.get('predicted_votes', 0)
                percentage = (votes / 25) * 100
                bar_length = int(percentage / 5)  # Max 20 chars
                bar = "█" * bar_length + "░" * (20 - bar_length)
                results_text += f"**{text}**\n{bar} {votes} ({percentage:.0f}%)\n\n"
            
            q_embed = discord.Embed(
                title=f"Q{i}: {question_text}",
                description=results_text,
                color=discord.Color.blue()
            )
            await message.channel.send(embed=q_embed)
        
        # Send analysis
        analysis = survey_data.get('analysis', '')
        if analysis:
            analysis_embed = discord.Embed(
                title="📈 Prediction Analysis",
                description=analysis,
                color=discord.Color.green()
            )
            await message.channel.send(embed=analysis_embed)
    
    async def _answer_dm_question(self, message: discord.Message, question: str):
        """Answer general questions about homework, exams, etc."""
        # Gather context from memory
        context_data = self._build_dm_context()
        
        # Create AI prompt with context
        prompt = f"""You are a helpful learning assistant. A student is asking you a question.
You have access to their current homework, reminders, and upcoming exams.

## Current Data:

### Pending Homework (Last 7 Days):
{context_data['homework']}

### Reminders:
{context_data['reminders']}

### Upcoming Exams (Next 14 Days):
{context_data['exams']}

### Exams Tomorrow:
{context_data['exams_tomorrow']}

## Student's Question:
{question}

## Instructions:
- Answer the student's question based on the data above
- Be helpful, friendly, and concise
- If they ask about specific subjects, filter relevant info
- If they ask "what do I have" or similar, give a summary
- If asking about deadlines, prioritize by date
- Use Arabic if the homework/exam names are in Arabic
- Format dates nicely (e.g., "Sunday, Feb 2" not "2026-02-02")
- If no relevant data exists, let them know kindly
- You can also answer general study questions
- If they want to create a survey, tell them to say "create survey about [topic]"

Respond naturally as a helpful assistant:"""

        # Get AI response
        response = await gemini_service.generate_response(prompt)
        
        if response:
            # Split long responses into multiple messages
            if len(response) <= 2000:
                embed = discord.Embed(
                    title="💬 Assistant",
                    description=response,
                    color=discord.Color.blue()
                )
                embed.set_footer(text="Ask me anything! Say 'create survey' to make a survey.")
                await message.channel.send(embed=embed)
            else:
                # Split into chunks
                chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
                for i, chunk in enumerate(chunks):
                    embed = discord.Embed(
                        title="💬 Assistant" if i == 0 else "💬 (continued)",
                        description=chunk,
                        color=discord.Color.blue()
                    )
                    if i == len(chunks) - 1:
                        embed.set_footer(text="Ask me anything! Say 'create survey' to make a survey.")
                    await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Error",
                description="I couldn't process your question. Please try again.",
                color=discord.Color.red()
            )
            await message.channel.send(embed=embed)
    
    def _build_dm_context(self) -> dict:
        """Build context from homework and exam memory for AI"""
        context = {
            'homework': 'No pending homework.',
            'reminders': 'No reminders.',
            'exams': 'No upcoming exams.',
            'exams_tomorrow': 'No exams tomorrow.'
        }
        
        # Get pending homework
        try:
            pending_hw = report_memory.get_pending_homework()
            if pending_hw:
                hw_lines = []
                for hw in pending_hw[:15]:  # Limit to 15
                    subject = hw.get('subject', 'Unknown')
                    task = hw.get('task', hw.get('description', 'No description'))
                    date = hw.get('date', hw.get('added_date', ''))
                    hw_lines.append(f"• [{subject}] {task} (Added: {date})")
                context['homework'] = "\n".join(hw_lines)
        except Exception as e:
            print(f"Error getting homework: {e}")
        
        # Get reminders
        try:
            all_data = report_memory.get_all_data()
            reminders = all_data.get('reminders', [])
            if reminders:
                reminder_lines = []
                for r in reminders[:10]:  # Limit to 10
                    text = r.get('text', r.get('reminder', 'No text'))
                    date = r.get('date', r.get('added_date', ''))
                    reminder_lines.append(f"• {text} ({date})")
                context['reminders'] = "\n".join(reminder_lines)
        except Exception as e:
            print(f"Error getting reminders: {e}")
        
        # Get upcoming exams
        try:
            upcoming = assessment_memory.get_upcoming_exams(days=14)
            if upcoming:
                exam_lines = []
                for exam in upcoming[:15]:  # Limit to 15
                    subject = exam.get('subject', 'Unknown')
                    topic = exam.get('topic', exam.get('lesson', ''))
                    date = exam.get('date', '')
                    day = exam.get('day', '')
                    exam_lines.append(f"• [{date} - {day}] {subject}: {topic}")
                context['exams'] = "\n".join(exam_lines)
        except Exception as e:
            print(f"Error getting exams: {e}")
        
        # Get exams tomorrow
        try:
            tomorrow = assessment_memory.get_exams_tomorrow()
            if tomorrow:
                tomorrow_lines = []
                for exam in tomorrow:
                    subject = exam.get('subject', 'Unknown')
                    topic = exam.get('topic', exam.get('lesson', ''))
                    tomorrow_lines.append(f"• {subject}: {topic}")
                context['exams_tomorrow'] = "\n".join(tomorrow_lines)
        except Exception as e:
            print(f"Error getting tomorrow exams: {e}")
        
        return context

    async def _process_analysis(self, channel, session: UserSession):
        """Process materials with Gemini and divide tasks"""
        session.state = SessionState.PROCESSING_ANALYSIS
        
        embed = discord.Embed(
            title="🔄 Analyzing Materials...",
            description=(
                "Using AI to analyze your materials and divide tasks.\n"
                "This may take a moment..."
            ),
            color=discord.Color.blue()
        )
        processing_msg = await channel.send(embed=embed)
        
        try:
            async with channel.typing():
                # Analyze materials
                session.material_analysis = await gemini_service.analyze_materials(
                    session.file_contents
                )
                
                # Even if analysis has error, we'll show what we can
                if session.material_analysis.get("error"):
                    embed = discord.Embed(
                        title="⚠️ Analysis Notice",
                        description=f"Partial analysis: {session.material_analysis.get('error', 'Unknown error')}\n\nContinuing with available data...",
                        color=discord.Color.orange()
                    )
                    await processing_msg.edit(embed=embed)
                    # Create a minimal analysis structure
                    if 'summary' not in session.material_analysis:
                        session.material_analysis['summary'] = "Materials uploaded for review."
                
                # Divide tasks among members
                try:
                    session.task_division = await gemini_service.divide_tasks(
                        session.material_analysis,
                        session.get_members_dict()
                    )
                except Exception as e:
                    print(f"Task division error: {e}")
                    session.task_division = {"error": str(e)}
        except Exception as e:
            print(f"Analysis error: {e}")
            session.material_analysis = {"summary": "Analysis encountered an issue.", "error": str(e)}
            session.task_division = {"error": "Could not divide tasks due to analysis issue."}
        
        # Show analysis results (always show something)
        analysis = session.material_analysis or {}
        
        embed = discord.Embed(
            title="📊 Material Analysis Complete!",
            description=analysis.get('summary', 'Analysis completed.')[:2000],
            color=discord.Color.green()
        )
        
        # Topics
        topics = analysis.get('topics', [])
        if topics:
            embed.add_field(
                name="📚 Topics Covered",
                value=", ".join(topics[:10]),
                inline=False
            )
        
        # Difficulty
        embed.add_field(
            name="📈 Overall Difficulty",
            value=f"Level {analysis.get('difficulty_level', 'N/A')}/5",
            inline=True
        )
        
        # Learning objectives
        objectives = analysis.get('learning_objectives', [])
        if objectives:
            embed.add_field(
                name="🎯 Learning Objectives",
                value="\n".join([f"• {obj}" for obj in objectives[:5]]),
                inline=False
            )
        
        await processing_msg.edit(embed=embed)
        
        # Show task division
        await self._show_task_division(channel, session)
    
    async def _show_task_division(self, channel, session: UserSession):
        """Display task division results"""
        session.state = SessionState.SHOWING_TASK_DIVISION
        
        division = session.task_division or {}
        
        try:
            if division.get("error"):
                embed = discord.Embed(
                    title="⚠️ Task Division Notice",
                    description=f"Could not automatically divide tasks: {division.get('error', 'Unknown error')}\n\nYou can still create a survey based on your materials!",
                    color=discord.Color.orange()
                )
                await channel.send(embed=embed)
            else:
                # Send assignments for each member
                assignments = division.get('assignments', [])
                
                if not assignments:
                    embed = discord.Embed(
                        title="📋 Task Division",
                        description="Tasks have been analyzed. Review the material analysis above for guidance on dividing work.",
                        color=discord.Color.blue()
                    )
                    await channel.send(embed=embed)
                else:
                    for assignment in assignments:
                        # Color based on difficulty level
                        level = assignment.get('difficulty_level', 3)
                        colors = {1: 0x90EE90, 2: 0x87CEEB, 3: 0xFFD700, 4: 0xFFA500, 5: 0xFF6347}
                        color = colors.get(level, 0x9B59B6)
                        
                        embed = discord.Embed(
                            title=f"📋 {assignment.get('member_name', 'Member')}'s Tasks",
                            description=f"**Skill Level:** {level}/5 ({DIFFICULTY_LEVELS.get(level, 'N/A')})",
                            color=discord.Color(color)
                        )
                        
                        # Tasks
                        tasks = assignment.get('assigned_tasks', [])
                        for i, task in enumerate(tasks, 1):
                            task_text = task.get('description', '')[:200]
                            if task.get('reason'):
                                task_text += f"\n*💡 {task.get('reason')}*"
                            embed.add_field(
                                name=f"Task {i}: {task.get('task', 'Task')[:50]}",
                                value=task_text or "No description",
                                inline=False
                            )
                        
                        # Time estimate
                        embed.add_field(
                            name="⏱️ Estimated Time",
                            value=assignment.get('estimated_time', 'N/A'),
                            inline=True
                        )
                        
                        # Tips
                        if assignment.get('tips'):
                            embed.add_field(
                                name="💡 Tips",
                                value=assignment.get('tips', '')[:300],
                                inline=False
                            )
                        
                        await channel.send(embed=embed)
                
                # Collaboration suggestions
                suggestions = division.get('collaboration_suggestions', [])
                if suggestions:
                    embed = discord.Embed(
                        title="🤝 Collaboration Suggestions",
                        description="\n".join([f"• {s}" for s in suggestions[:5]]),
                        color=discord.Color.blue()
                    )
                    embed.add_field(
                        name="📅 Recommended Timeline",
                        value=division.get('timeline_recommendation', 'No specific timeline'),
                        inline=False
                    )
                    await channel.send(embed=embed)
        except Exception as e:
            print(f"Error showing task division: {e}")
            embed = discord.Embed(
                title="⚠️ Display Error",
                description="There was an issue displaying task assignments, but you can still continue.",
                color=discord.Color.orange()
            )
            await channel.send(embed=embed)
        
        # ALWAYS ask about survey with buttons - this is guaranteed to run
        session.state = SessionState.AWAITING_SURVEY_CHOICE
        
        embed = discord.Embed(
            title="📝 Create a Survey?",
            description=(
                "Would you like me to create a quiz/survey based on your materials?\n\n"
                "**What you'll get:**\n"
                "• 5 high-quality assessment questions\n"
                "• Google Form for easy distribution\n"
                "• 25 AI-predicted responses\n"
                "• Excel/Google Sheet with statistics"
            ),
            color=discord.Color.gold()
        )
        
        await channel.send(embed=embed, view=SurveyChoiceView(session.user_id))
    
    async def _create_survey(self, channel, session: UserSession):
        """Create survey, form, and spreadsheet"""
        session.state = SessionState.CREATING_SURVEY
        
        embed = discord.Embed(
            title="🔄 Creating Survey...",
            description=(
                "**Progress:**\n"
                "⏳ Generating questions...\n"
                "⏸️ Creating Google Form...\n"
                "⏸️ Generating predictions...\n"
                "⏸️ Creating spreadsheet..."
            ),
            color=discord.Color.blue()
        )
        status_msg = await channel.send(embed=embed)
        
        async with channel.typing():
            # Generate survey questions
            session.survey_questions = await gemini_service.generate_survey_questions(
                session.file_contents,
                num_questions=5
            )
            
            # Update progress
            embed.description = (
                "**Progress:**\n"
                "✅ Generating questions...\n"
                "⏳ Creating Google Form...\n"
                "⏸️ Generating predictions...\n"
                "⏸️ Creating spreadsheet..."
            )
            await status_msg.edit(embed=embed)
            
            if not session.survey_questions or (isinstance(session.survey_questions, list) and len(session.survey_questions) > 0 and "error" in session.survey_questions[0]):
                embed = discord.Embed(
                    title="❌ Error",
                    description="Failed to generate survey questions.",
                    color=discord.Color.red()
                )
                await status_msg.edit(embed=embed)
                await self._complete_session(channel, session)
                return
            
            # Generate fake predictions
            session.survey_predictions = await gemini_service.generate_fake_predictions(
                session.survey_questions,
                num_responses=25
            )
            
            # Update progress
            embed.description = (
                "**Progress:**\n"
                "✅ Generating questions...\n"
                "✅ Predictions generated...\n"
                "⏳ Creating Google Form...\n"
                "⏳ Creating spreadsheet..."
            )
            await status_msg.edit(embed=embed)
            
            # Try to create Google Form
            form_created = False
            sheet_created = False
            
            if self.bot.google_services:
                try:
                    # Create Google Form
                    form_result = await self.bot.google_services.create_google_form(
                        title="Learning Assessment Survey",
                        questions=session.survey_questions,
                        description="Auto-generated survey based on learning materials"
                    )
                    
                    if form_result.get('success'):
                        session.google_form_url = form_result['response_url']
                        form_created = True
                    
                    # Create Google Sheet
                    sheet_result = await self.bot.google_services.create_google_sheet(
                        title="Survey Predictions Analysis",
                        questions=session.survey_questions,
                        predictions=session.survey_predictions
                    )
                    
                    if sheet_result.get('success'):
                        session.google_sheet_url = sheet_result['url']
                        sheet_created = True
                        
                except Exception as e:
                    print(f"Google Services error: {e}")
            
            # Create local Excel as fallback
            try:
                excel_filename = f"temp_files/survey_analysis_{session.user_id}.xlsx"
                os.makedirs("temp_files", exist_ok=True)
                
                if self.bot.google_services:
                    session.excel_file_path = self.bot.google_services.create_local_excel(
                        excel_filename,
                        session.survey_questions,
                        session.survey_predictions
                    )
                else:
                    # Create a minimal excel without full google services
                    from services.google_services import GoogleServicesManager
                    temp_manager = GoogleServicesManager.__new__(GoogleServicesManager)
                    session.excel_file_path = temp_manager.create_local_excel(
                        excel_filename,
                        session.survey_questions,
                        session.survey_predictions
                    )
            except Exception as e:
                print(f"Excel creation error: {e}")
                session.excel_file_path = None
        
        # Final progress update
        embed.description = (
            "**Progress:**\n"
            "✅ Questions generated\n"
            "✅ Predictions generated\n"
            f"{'✅' if form_created else '⚠️'} Google Form\n"
            f"{'✅' if sheet_created else '⚠️'} Google Sheet\n"
            f"{'✅' if session.excel_file_path else '⚠️'} Excel file"
        )
        embed.color = discord.Color.green()
        embed.title = "✅ Survey Created!"
        await status_msg.edit(embed=embed)
        
        # Show survey questions
        embed = discord.Embed(
            title="📋 Generated Questions",
            color=discord.Color.purple()
        )
        
        for i, q in enumerate(session.survey_questions[:5], 1):
            options = q.get('options', {})
            options_text = " | ".join([f"**{k}**" for k in options.keys()])
            embed.add_field(
                name=f"Q{i}: {q.get('question_text', '')[:80]}...",
                value=f"Options: {options_text}\nAnswer: **{q.get('correct_answer', '?')}** | Difficulty: {q.get('difficulty', '?')}",
                inline=False
            )
        
        await channel.send(embed=embed)
        
        # Show links and files
        embed = discord.Embed(
            title="📊 Survey Materials",
            color=discord.Color.green()
        )
        
        links = []
        if session.google_form_url:
            links.append(f"📝 **[Open Google Form]({session.google_form_url})**")
        
        if session.google_sheet_url:
            links.append(f"📈 **[Open Google Sheet]({session.google_sheet_url})**")
        
        if links:
            embed.add_field(name="🔗 Links", value="\n".join(links), inline=False)
        
        if not form_created and not sheet_created:
            embed.add_field(
                name="⚠️ Note",
                value="Google services unavailable. Excel file provided instead.",
                inline=False
            )
        
        # Stats summary
        stats = session.survey_predictions.get('statistics', {})
        embed.add_field(
            name="📉 Prediction Statistics",
            value=(
                f"• **Average Score:** {stats.get('average_score', 'N/A')}/5\n"
                f"• **Average %:** {stats.get('average_percentage', 'N/A')}%\n"
                f"• **Total Predictions:** 25 responses"
            ),
            inline=False
        )
        
        await channel.send(embed=embed)
        
        # Send Excel file if created
        if session.excel_file_path and os.path.exists(session.excel_file_path):
            embed = discord.Embed(
                title="📎 Excel File",
                description="Here's your detailed analysis spreadsheet:",
                color=discord.Color.blue()
            )
            await channel.send(embed=embed, file=discord.File(session.excel_file_path))
        
        # Ask about PowerPoint generation
        await self._ask_powerpoint_choice(channel, session)
    
    async def _ask_powerpoint_choice(self, channel, session: UserSession):
        """Ask if user wants to generate a PowerPoint presentation"""
        session.state = SessionState.AWAITING_POWERPOINT_CHOICE
        
        embed = discord.Embed(
            title="📽️ Generate PowerPoint Presentation?",
            description=(
                "Would you like me to create a **professional PowerPoint presentation** "
                "based on your learning materials?\n\n"
                "**What you'll get:**\n"
                "• 🎨 Beautiful, themed slides\n"
                "• 📝 AI-generated content from your materials\n"
                "• 💬 Speaker notes for each slide\n"
                "• 📊 Professional formatting & design\n\n"
                "Select the number of slides below, or skip to finish."
            ),
            color=discord.Color.purple()
        )
        
        await channel.send(embed=embed, view=PowerPointOptionsView(session.user_id))
    
    async def _create_powerpoint(self, channel, session: UserSession, num_slides: int = 10):
        """Generate PowerPoint presentation using Gemini"""
        session.state = SessionState.CREATING_POWERPOINT
        
        embed = discord.Embed(
            title="🔄 Creating PowerPoint...",
            description=(
                "**Progress:**\n"
                "⏳ Generating slide content with AI...\n"
                "⏸️ Creating presentation file...\n"
                "⏸️ Applying design theme..."
            ),
            color=discord.Color.purple()
        )
        status_msg = await channel.send(embed=embed)
        
        try:
            async with channel.typing():
                # Generate presentation content using Gemini
                session.presentation_content = await gemini_service.generate_presentation_content(
                    session.file_contents,
                    session.material_analysis or {},
                    num_slides=num_slides
                )
                
                # Update progress
                embed.description = (
                    "**Progress:**\n"
                    "✅ Slide content generated\n"
                    "⏳ Creating presentation file...\n"
                    "⏸️ Applying design theme..."
                )
                await status_msg.edit(embed=embed)
                
                if session.presentation_content.get('error'):
                    embed = discord.Embed(
                        title="⚠️ Generation Issue",
                        description=f"Could not generate all content: {session.presentation_content.get('error')}\n\nCreating presentation with available data...",
                        color=discord.Color.orange()
                    )
                    await channel.send(embed=embed)
                
                # Create the PowerPoint file
                os.makedirs("temp_files", exist_ok=True)
                ppt_filename = f"temp_files/presentation_{session.user_id}.pptx"
                
                session.powerpoint_file_path = powerpoint_generator.create_presentation(
                    session.presentation_content,
                    ppt_filename
                )
                
                # Final progress update
                embed.description = (
                    "**Progress:**\n"
                    "✅ Slide content generated\n"
                    "✅ Presentation file created\n"
                    "✅ Design theme applied"
                )
                embed.color = discord.Color.green()
                embed.title = "✅ PowerPoint Created!"
                await status_msg.edit(embed=embed)
            
            # Show presentation summary
            slides = session.presentation_content.get('slides', [])
            theme = session.presentation_content.get('theme_suggestion', 'professional')
            
            embed = discord.Embed(
                title="📽️ Presentation Summary",
                description=f"**{session.presentation_content.get('presentation_title', 'Your Presentation')}**",
                color=discord.Color.purple()
            )
            
            embed.add_field(
                name="📊 Presentation Details",
                value=(
                    f"• **Slides:** {len(slides)}\n"
                    f"• **Theme:** {theme.title()}\n"
                    f"• **Format:** PowerPoint (.pptx)"
                ),
                inline=True
            )
            
            # Show slide outline
            slide_titles = [s.get('title', f"Slide {i+1}") for i, s in enumerate(slides[:8])]
            if len(slides) > 8:
                slide_titles.append(f"... and {len(slides) - 8} more slides")
            
            embed.add_field(
                name="📑 Slide Outline",
                value="\n".join([f"• {title[:40]}" for title in slide_titles]),
                inline=False
            )
            
            await channel.send(embed=embed)
            
            # Send the PowerPoint file
            if session.powerpoint_file_path and os.path.exists(session.powerpoint_file_path):
                embed = discord.Embed(
                    title="📎 Your PowerPoint Presentation",
                    description="Here's your AI-generated presentation! Speaker notes included.",
                    color=discord.Color.green()
                )
                await channel.send(embed=embed, file=discord.File(session.powerpoint_file_path))
            else:
                embed = discord.Embed(
                    title="❌ File Error",
                    description="Could not create the PowerPoint file. Please try again.",
                    color=discord.Color.red()
                )
                await channel.send(embed=embed)
                
        except Exception as e:
            print(f"PowerPoint creation error: {e}")
            embed = discord.Embed(
                title="❌ Error Creating PowerPoint",
                description=f"An error occurred: {str(e)[:200]}",
                color=discord.Color.red()
            )
            await channel.send(embed=embed)
        
        # Complete the session
        await self._complete_session(channel, session)
    
    async def _complete_session(self, channel, session: UserSession):
        """Complete the session and show summary"""
        session.state = SessionState.COMPLETED
        
        embed = discord.Embed(
            title="✅ Session Complete!",
            description="Your learning session has been completed successfully.",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="📊 Summary",
            value=(
                f"• **Files Analyzed:** {len(session.uploaded_files)}\n"
                f"• **Group Members:** {len(session.group_members)}\n"
                f"• **Tasks Assigned:** ✅\n"
                f"• **Survey Created:** {'✅' if session.wants_survey else '❌'}\n"
                f"• **PowerPoint Generated:** {'✅' if session.wants_powerpoint else '❌'}"
            ),
            inline=False
        )
        
        embed.set_footer(text="Thank you for using Learning Bot! 📚")
        
        await channel.send(embed=embed, view=NewSessionView())
        
        # Clean up files
        file_handler.cleanup()


# ============================================================================
# RUN BOT
# ============================================================================

async def run_bot():
    """Run the Discord bot"""
    bot = LearningBot()
    
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        else:
            print(f"Error: {error}")
            embed = discord.Embed(
                title="❌ Error",
                description=str(error)[:200],
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(run_bot())
