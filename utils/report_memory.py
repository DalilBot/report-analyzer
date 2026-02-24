"""
Report Memory Module
Stores daily report data for 7 days and manages reminders
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import asyncio


# Storage file path
MEMORY_FILE = "report_memory.json"


@dataclass
class HomeworkItem:
    """Represents a homework assignment"""
    id: str
    subject: str
    task: str
    due_date: str  # "next session" or actual date
    added_date: str
    completed: bool = False
    reminded: bool = False
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'HomeworkItem':
        return cls(**data)


@dataclass
class ReminderItem:
    """Represents a reminder"""
    id: str
    type: str
    description: str
    date: Optional[str]
    added_date: str
    reminded: bool = False
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ReminderItem':
        return cls(**data)


class ReportMemory:
    """Manages storage and retrieval of report data with 7-day retention"""
    
    def __init__(self, storage_path: str = MEMORY_FILE):
        self.storage_path = storage_path
        self.data: Dict[str, Any] = {
            "homework": [],
            "reminders": [],
            "last_cleanup": None
        }
        self._load()
    
    def _load(self):
        """Load data from storage file"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.data = {"homework": [], "reminders": [], "last_cleanup": None}
    
    def _save(self):
        """Save data to storage file"""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error saving report memory: {e}")
    
    def _generate_id(self, prefix: str) -> str:
        """Generate unique ID for items"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"{prefix}_{timestamp}"
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse various date formats"""
        if not date_str or date_str.lower() in ["next session", "الحصة القادمة", "null", "none"]:
            return None
        
        # Try common date formats
        formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%d-%m-%Y",
            "%Y/%m/%d",
            "%d %B %Y",
            "%B %d, %Y",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return None
    
    def cleanup_old_data(self, days: int = 7):
        """Remove data older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.strftime("%Y-%m-%d")
        
        # Filter homework
        self.data["homework"] = [
            hw for hw in self.data["homework"]
            if hw.get("added_date", "2000-01-01") >= cutoff_str
        ]
        
        # Filter reminders
        self.data["reminders"] = [
            rem for rem in self.data["reminders"]
            if rem.get("added_date", "2000-01-01") >= cutoff_str
        ]
        
        self.data["last_cleanup"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save()
    
    def add_homework(self, subject: str, task: str, due_date: Optional[str] = None) -> HomeworkItem:
        """Add a new homework item"""
        # Default to "next session" if no due date
        if not due_date or due_date.lower() in ["null", "none", ""]:
            due_date = "next session"
        
        # Check for duplicates (same subject and task)
        for hw in self.data["homework"]:
            if hw["subject"].lower() == subject.lower() and hw["task"].lower() == task.lower():
                return HomeworkItem.from_dict(hw)  # Already exists
        
        homework = HomeworkItem(
            id=self._generate_id("hw"),
            subject=subject,
            task=task,
            due_date=due_date,
            added_date=datetime.now().strftime("%Y-%m-%d"),
            completed=False,
            reminded=False
        )
        
        self.data["homework"].append(homework.to_dict())
        self._save()
        return homework
    
    def add_reminder(self, rem_type: str, description: str, date: Optional[str] = None) -> ReminderItem:
        """Add a new reminder"""
        # Check for duplicates
        for rem in self.data["reminders"]:
            if rem["description"].lower() == description.lower():
                return ReminderItem.from_dict(rem)  # Already exists
        
        reminder = ReminderItem(
            id=self._generate_id("rem"),
            type=rem_type,
            description=description,
            date=date,
            added_date=datetime.now().strftime("%Y-%m-%d"),
            reminded=False
        )
        
        self.data["reminders"].append(reminder.to_dict())
        self._save()
        return reminder
    
    def add_from_analysis(self, analysis: Dict[str, Any]) -> Dict[str, int]:
        """Add homework and reminders from AI analysis result"""
        added = {"homework": 0, "reminders": 0}
        
        # Add homework
        for hw in analysis.get("homework", []):
            subject = hw.get("subject", "Unknown")
            task = hw.get("task", "")
            due_date = hw.get("due_date")
            
            if task:
                self.add_homework(subject, task, due_date)
                added["homework"] += 1
        
        # Add reminders
        for rem in analysis.get("reminders", []):
            rem_type = rem.get("type", "note")
            description = rem.get("description", "")
            date = rem.get("date")
            
            if description:
                self.add_reminder(rem_type, description, date)
                added["reminders"] += 1
        
        return added
    
    def get_pending_homework(self) -> List[Dict]:
        """Get all pending (not completed) homework"""
        return [hw for hw in self.data["homework"] if not hw.get("completed", False)]
    
    def get_pending_reminders(self) -> List[Dict]:
        """Get all reminders that haven't been fully reminded"""
        return self.data["reminders"]
    
    def get_due_today(self) -> Dict[str, List[Dict]]:
        """Get homework and reminders due today"""
        today = datetime.now().strftime("%Y-%m-%d")
        today_obj = datetime.now().date()
        
        due_homework = []
        due_reminders = []
        
        for hw in self.get_pending_homework():
            due_date = hw.get("due_date", "")
            
            # Check if it's "next session" (always remind)
            if due_date.lower() in ["next session", "الحصة القادمة"]:
                due_homework.append(hw)
                continue
            
            # Parse the date
            parsed = self._parse_date(due_date)
            if parsed and parsed.date() == today_obj:
                due_homework.append(hw)
        
        for rem in self.get_pending_reminders():
            date = rem.get("date")
            if date:
                parsed = self._parse_date(date)
                if parsed and parsed.date() == today_obj:
                    due_reminders.append(rem)
        
        return {"homework": due_homework, "reminders": due_reminders}
    
    def get_due_soon(self, days: int = 2) -> Dict[str, List[Dict]]:
        """Get homework and reminders due within specified days"""
        today_obj = datetime.now().date()
        soon = today_obj + timedelta(days=days)
        
        due_homework = []
        due_reminders = []
        
        for hw in self.get_pending_homework():
            due_date = hw.get("due_date", "")
            
            # "next session" homework is always included
            if due_date.lower() in ["next session", "الحصة القادمة"]:
                due_homework.append(hw)
                continue
            
            parsed = self._parse_date(due_date)
            if parsed:
                if today_obj <= parsed.date() <= soon:
                    due_homework.append(hw)
        
        for rem in self.get_pending_reminders():
            date = rem.get("date")
            if date:
                parsed = self._parse_date(date)
                if parsed and today_obj <= parsed.date() <= soon:
                    due_reminders.append(rem)
        
        return {"homework": due_homework, "reminders": due_reminders}
    
    def mark_homework_completed(self, hw_id: str) -> bool:
        """Mark a homework item as completed"""
        for hw in self.data["homework"]:
            if hw["id"] == hw_id:
                hw["completed"] = True
                self._save()
                return True
        return False
    
    def mark_homework_reminded(self, hw_id: str) -> bool:
        """Mark a homework item as reminded"""
        for hw in self.data["homework"]:
            if hw["id"] == hw_id:
                hw["reminded"] = True
                self._save()
                return True
        return False
    
    def get_all_data(self) -> Dict[str, Any]:
        """Get all stored data"""
        return self.data
    
    def get_summary(self) -> Dict[str, int]:
        """Get a summary of stored items"""
        pending_hw = len(self.get_pending_homework())
        total_hw = len(self.data["homework"])
        total_rem = len(self.data["reminders"])
        
        return {
            "pending_homework": pending_hw,
            "completed_homework": total_hw - pending_hw,
            "total_homework": total_hw,
            "total_reminders": total_rem
        }


# Singleton instance
report_memory = ReportMemory()
