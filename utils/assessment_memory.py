"""
Assessment Memory Module
Stores term assessment schedules and manages exam reminders
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


# Storage file path
ASSESSMENT_FILE = "assessment_schedule.json"


@dataclass
class ExamItem:
    """Represents an exam/assessment"""
    id: str
    subject: str
    exam_type: str  # Quiz, Test, Project, Final, etc.
    date: str  # YYYY-MM-DD format
    day_of_week: str
    topics: List[str]  # Topics/chapters covered
    notes: str
    reminded_weekly: bool = False
    reminded_night_before: bool = False
    completed: bool = False
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ExamItem':
        return cls(**data)


class AssessmentMemory:
    """Manages storage and retrieval of assessment schedules"""
    
    def __init__(self, storage_path: str = ASSESSMENT_FILE):
        self.storage_path = storage_path
        self.data: Dict[str, Any] = {
            "term": "",
            "grade": "",
            "year": "",
            "exams": [],
            "last_updated": None,
            "last_weekly_reminder": None
        }
        self._load()
    
    def _load(self):
        """Load data from storage file"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
    
    def _save(self):
        """Save data to storage file"""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error saving assessment memory: {e}")
    
    def _generate_id(self) -> str:
        """Generate unique ID for exams"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"exam_{timestamp}"
    
    def clear_schedule(self):
        """Clear all exams (for new term)"""
        self.data["exams"] = []
        self.data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save()
    
    def set_term_info(self, term: str, grade: str, year: str):
        """Set term information"""
        self.data["term"] = term
        self.data["grade"] = grade
        self.data["year"] = year
        self.data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save()
    
    def add_exam(
        self, 
        subject: str, 
        exam_type: str, 
        date: str, 
        day_of_week: str = "",
        topics: List[str] = None,
        notes: str = ""
    ) -> ExamItem:
        """Add an exam to the schedule"""
        # Check for duplicates
        for exam in self.data["exams"]:
            if (exam["subject"].lower() == subject.lower() and 
                exam["date"] == date and
                exam["exam_type"].lower() == exam_type.lower()):
                return ExamItem.from_dict(exam)
        
        exam = ExamItem(
            id=self._generate_id(),
            subject=subject,
            exam_type=exam_type,
            date=date,
            day_of_week=day_of_week,
            topics=topics or [],
            notes=notes,
            reminded_weekly=False,
            reminded_night_before=False,
            completed=False
        )
        
        self.data["exams"].append(exam.to_dict())
        self.data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save()
        return exam
    
    def add_exams_from_analysis(self, analysis: Dict[str, Any]) -> int:
        """Add exams from AI analysis result"""
        count = 0
        
        # Set term info if available
        if analysis.get("term"):
            self.data["term"] = analysis["term"]
        if analysis.get("grade"):
            self.data["grade"] = analysis["grade"]
        if analysis.get("year"):
            self.data["year"] = analysis["year"]
        
        for exam in analysis.get("exams", []):
            self.add_exam(
                subject=exam.get("subject", "Unknown"),
                exam_type=exam.get("exam_type", "Assessment"),
                date=exam.get("date", ""),
                day_of_week=exam.get("day_of_week", ""),
                topics=exam.get("topics", []),
                notes=exam.get("notes", "")
            )
            count += 1
        
        self._save()
        return count
    
    def get_all_exams(self) -> List[Dict]:
        """Get all exams"""
        return self.data["exams"]
    
    def get_upcoming_exams(self, days: int = 7) -> List[Dict]:
        """Get exams within the next N days"""
        today = datetime.now().date()
        cutoff = today + timedelta(days=days)
        
        upcoming = []
        for exam in self.data["exams"]:
            if exam.get("completed"):
                continue
            try:
                exam_date = datetime.strptime(exam["date"], "%Y-%m-%d").date()
                if today <= exam_date <= cutoff:
                    upcoming.append(exam)
            except (ValueError, KeyError):
                continue
        
        # Sort by date
        upcoming.sort(key=lambda x: x.get("date", "9999-99-99"))
        return upcoming
    
    def get_exams_tomorrow(self) -> List[Dict]:
        """Get exams scheduled for tomorrow"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        exams = []
        for exam in self.data["exams"]:
            if exam.get("date") == tomorrow and not exam.get("completed"):
                exams.append(exam)
        
        return exams
    
    def get_exams_on_date(self, date: str) -> List[Dict]:
        """Get exams on a specific date"""
        return [
            exam for exam in self.data["exams"]
            if exam.get("date") == date and not exam.get("completed")
        ]
    
    def get_this_week_exams(self) -> List[Dict]:
        """Get exams for the current week (Sunday to Saturday)"""
        today = datetime.now().date()
        # Find start of week (Sunday)
        start_of_week = today - timedelta(days=today.weekday() + 1)
        if today.weekday() == 6:  # If today is Sunday
            start_of_week = today
        end_of_week = start_of_week + timedelta(days=6)
        
        week_exams = []
        for exam in self.data["exams"]:
            if exam.get("completed"):
                continue
            try:
                exam_date = datetime.strptime(exam["date"], "%Y-%m-%d").date()
                if start_of_week <= exam_date <= end_of_week:
                    week_exams.append(exam)
            except (ValueError, KeyError):
                continue
        
        week_exams.sort(key=lambda x: x.get("date", "9999-99-99"))
        return week_exams
    
    def get_next_week_exams(self) -> List[Dict]:
        """Get exams for next week"""
        today = datetime.now().date()
        # Find start of next week (Sunday)
        days_until_sunday = (6 - today.weekday()) % 7
        if days_until_sunday == 0:
            days_until_sunday = 7
        start_of_next_week = today + timedelta(days=days_until_sunday)
        end_of_next_week = start_of_next_week + timedelta(days=6)
        
        week_exams = []
        for exam in self.data["exams"]:
            if exam.get("completed"):
                continue
            try:
                exam_date = datetime.strptime(exam["date"], "%Y-%m-%d").date()
                if start_of_next_week <= exam_date <= end_of_next_week:
                    week_exams.append(exam)
            except (ValueError, KeyError):
                continue
        
        week_exams.sort(key=lambda x: x.get("date", "9999-99-99"))
        return week_exams
    
    def mark_exam_completed(self, exam_id: str) -> bool:
        """Mark an exam as completed"""
        for exam in self.data["exams"]:
            if exam["id"] == exam_id:
                exam["completed"] = True
                self._save()
                return True
        return False
    
    def mark_reminded_weekly(self, exam_id: str) -> bool:
        """Mark exam as reminded in weekly reminder"""
        for exam in self.data["exams"]:
            if exam["id"] == exam_id:
                exam["reminded_weekly"] = True
                self._save()
                return True
        return False
    
    def mark_reminded_night_before(self, exam_id: str) -> bool:
        """Mark exam as reminded night before"""
        for exam in self.data["exams"]:
            if exam["id"] == exam_id:
                exam["reminded_night_before"] = True
                self._save()
                return True
        return False
    
    def reset_weekly_reminders(self):
        """Reset weekly reminder flags (call at start of each week)"""
        for exam in self.data["exams"]:
            exam["reminded_weekly"] = False
        self._save()
    
    def get_term_info(self) -> Dict[str, str]:
        """Get term information"""
        return {
            "term": self.data.get("term", ""),
            "grade": self.data.get("grade", ""),
            "year": self.data.get("year", ""),
            "last_updated": self.data.get("last_updated", "")
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of assessments"""
        total = len(self.data["exams"])
        completed = sum(1 for e in self.data["exams"] if e.get("completed"))
        upcoming = len(self.get_upcoming_exams(days=30))
        
        return {
            "total_exams": total,
            "completed": completed,
            "remaining": total - completed,
            "upcoming_30_days": upcoming,
            "term": self.data.get("term", "Unknown"),
            "grade": self.data.get("grade", "Unknown")
        }


# Singleton instance
assessment_memory = AssessmentMemory()
