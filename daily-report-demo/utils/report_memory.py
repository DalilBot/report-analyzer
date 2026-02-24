"""
Report Memory - 7-day rolling memory for homework and reminders
Uses a local JSON file for persistence
"""
import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Optional


DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'memory.json')


class ReportMemory:
    """Stores homework & reminders with 7-day retention"""

    def __init__(self):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        self._load()

    def _load(self):
        """Load data from disk"""
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                self.data = {'reports': [], 'homework': [], 'reminders': []}
        except (json.JSONDecodeError, IOError):
            self.data = {'reports': [], 'homework': [], 'reminders': []}

    def _save(self):
        """Save data to disk"""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error saving memory: {e}")

    def _cleanup_old(self):
        """Remove entries older than 7 days"""
        cutoff = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        self.data['homework'] = [
            hw for hw in self.data['homework']
            if hw.get('added_date', '') >= cutoff
        ]
        self.data['reminders'] = [
            r for r in self.data['reminders']
            if r.get('added_date', '') >= cutoff
        ]
        self.data['reports'] = [
            r for r in self.data['reports']
            if r.get('date', '') >= cutoff
        ]

    def add_report(self, date: str, analysis: dict):
        """Add analyzed report data to memory"""
        self._cleanup_old()

        # Add report record
        self.data['reports'].append({
            'date': date,
            'analyzed_at': datetime.now().isoformat(),
            'homework_count': len(analysis.get('homework', [])),
            'reminder_count': len(analysis.get('reminders', [])),
            'summary': analysis.get('summary', '')
        })

        # Add homework items
        for hw in analysis.get('homework', []):
            self.data['homework'].append({
                'id': uuid.uuid4().hex[:8],
                'subject': hw.get('subject', 'Unknown'),
                'task': hw.get('task', ''),
                'due_date': hw.get('due_date', ''),
                'added_date': date,
                'completed': False
            })

        # Add reminders
        for r in analysis.get('reminders', []):
            self.data['reminders'].append({
                'id': uuid.uuid4().hex[:8],
                'text': r.get('text', ''),
                'priority': r.get('priority', 'medium'),
                'added_date': date
            })

        self._save()

    def toggle_homework(self, hw_id: str) -> bool:
        """Toggle homework completion"""
        for hw in self.data['homework']:
            if hw['id'] == hw_id:
                hw['completed'] = not hw['completed']
                self._save()
                return True
        return False

    def get_all(self) -> dict:
        """Get all stored data"""
        self._cleanup_old()
        return {
            'homework': sorted(self.data['homework'], key=lambda x: x.get('added_date', ''), reverse=True),
            'reminders': sorted(self.data['reminders'], key=lambda x: x.get('added_date', ''), reverse=True),
            'reports': sorted(self.data['reports'], key=lambda x: x.get('date', ''), reverse=True)
        }

    def get_summary(self) -> dict:
        """Get summary statistics"""
        self._cleanup_old()
        hw = self.data['homework']
        return {
            'total_homework': len(hw),
            'pending': len([h for h in hw if not h.get('completed')]),
            'completed': len([h for h in hw if h.get('completed')]),
            'total_reminders': len(self.data['reminders']),
            'total_reports': len(self.data['reports']),
            'days_covered': len(set(r.get('date', '') for r in self.data['reports']))
        }

    def clear(self):
        """Clear all data"""
        self.data = {'reports': [], 'homework': [], 'reminders': []}
        self._save()
