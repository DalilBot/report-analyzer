"""
Session Manager Module
Manages user conversation sessions and state
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass, field

from config import SESSION_TIMEOUT


class SessionState(Enum):
    """Enum representing the current state of a user session"""
    IDLE = "idle"
    AWAITING_MATERIALS = "awaiting_materials"
    AWAITING_MEMBERS = "awaiting_members"
    AWAITING_DIFFICULTY = "awaiting_difficulty"
    PROCESSING_ANALYSIS = "processing_analysis"
    SHOWING_TASK_DIVISION = "showing_task_division"
    AWAITING_SURVEY_CHOICE = "awaiting_survey_choice"
    CREATING_SURVEY = "creating_survey"
    AWAITING_POWERPOINT_CHOICE = "awaiting_powerpoint_choice"
    CREATING_POWERPOINT = "creating_powerpoint"
    COMPLETED = "completed"


@dataclass
class GroupMember:
    """Represents a group member"""
    name: str
    difficulty_level: int = 3  # 1-5 scale
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "difficulty_level": self.difficulty_level
        }


@dataclass
class UserSession:
    """Represents a user's conversation session"""
    user_id: int
    state: SessionState = SessionState.IDLE
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    
    # Session data
    uploaded_files: List[Dict[str, Any]] = field(default_factory=list)
    file_contents: List[Dict[str, Any]] = field(default_factory=list)
    group_members: List[GroupMember] = field(default_factory=list)
    current_member_index: int = 0
    
    # Analysis results
    material_analysis: Optional[Dict[str, Any]] = None
    task_division: Optional[Dict[str, Any]] = None
    
    # Survey data
    wants_survey: bool = False
    survey_questions: Optional[List[Dict[str, Any]]] = None
    survey_predictions: Optional[Dict[str, Any]] = None
    google_form_url: Optional[str] = None
    google_sheet_url: Optional[str] = None
    excel_file_path: Optional[str] = None
    
    # PowerPoint data
    wants_powerpoint: bool = False
    presentation_content: Optional[Dict[str, Any]] = None
    powerpoint_file_path: Optional[str] = None
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
    
    def is_expired(self) -> bool:
        """Check if session has expired"""
        return datetime.now() - self.last_activity > timedelta(seconds=SESSION_TIMEOUT)
    
    def reset(self):
        """Reset session to initial state"""
        self.state = SessionState.IDLE
        self.uploaded_files = []
        self.file_contents = []
        self.group_members = []
        self.current_member_index = 0
        self.material_analysis = None
        self.task_division = None
        self.wants_survey = False
        self.survey_questions = None
        self.survey_predictions = None
        self.google_form_url = None
        self.google_sheet_url = None
        self.excel_file_path = None
        self.wants_powerpoint = False
        self.presentation_content = None
        self.powerpoint_file_path = None
        self.update_activity()
    
    def add_member(self, name: str, difficulty_level: int = 3) -> GroupMember:
        """Add a group member"""
        member = GroupMember(name=name, difficulty_level=difficulty_level)
        self.group_members.append(member)
        return member
    
    def get_members_dict(self) -> List[Dict[str, Any]]:
        """Get members as list of dictionaries"""
        return [m.to_dict() for m in self.group_members]


class SessionManager:
    """Manages all user sessions"""
    
    def __init__(self):
        self.sessions: Dict[int, UserSession] = {}
        self._cleanup_task: Optional[asyncio.Task] = None
    
    def get_session(self, user_id: int) -> UserSession:
        """Get or create a session for a user"""
        if user_id not in self.sessions:
            self.sessions[user_id] = UserSession(user_id=user_id)
        
        session = self.sessions[user_id]
        
        # Check if expired
        if session.is_expired():
            session.reset()
        else:
            session.update_activity()
        
        return session
    
    def delete_session(self, user_id: int):
        """Delete a user's session"""
        if user_id in self.sessions:
            del self.sessions[user_id]
    
    def start_cleanup_task(self, loop: asyncio.AbstractEventLoop):
        """Start background task to clean up expired sessions"""
        async def cleanup():
            while True:
                await asyncio.sleep(300)  # Check every 5 minutes
                expired = [
                    user_id for user_id, session in self.sessions.items()
                    if session.is_expired()
                ]
                for user_id in expired:
                    del self.sessions[user_id]
        
        self._cleanup_task = loop.create_task(cleanup())
    
    def stop_cleanup_task(self):
        """Stop the cleanup background task"""
        if self._cleanup_task:
            self._cleanup_task.cancel()


# Singleton instance
session_manager = SessionManager()
