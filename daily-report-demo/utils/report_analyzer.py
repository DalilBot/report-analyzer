"""
Report Analyzer - Gemini AI integration for PDF analysis
"""
import os
import google.generativeai as genai
import json
import re


class ReportAnalyzer:
    """Analyzes daily report PDFs using Google Gemini AI"""

    def __init__(self):
        api_key = os.environ.get('GEMINI_API_KEY', '')
        if api_key:
            genai.configure(api_key=api_key)
        self.model_name = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')

    def analyze(self, file_path: str) -> dict:
        """
        Analyze a daily report PDF and extract homework & reminders.
        Sends the PDF directly to Gemini for analysis.
        """
        api_key = os.environ.get('GEMINI_API_KEY', '')
        if not api_key:
            return {'error': 'GEMINI_API_KEY not configured. Add it in Settings.'}

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(self.model_name)

        prompt = """Analyze this daily school report PDF.
Extract ONLY the following - ignore everything about "material covered" / "ما تم دراسته":

1. **Homework (الواجبات)**: Any assignments students need to do at home
2. **Reminders (تنبيهات/ملاحظات)**: Any notes, reminders, announcements, or important dates

For each homework item extract:
- subject: The subject name
- task: What the student needs to do
- due_date: When it's due (if mentioned)

For each reminder extract:
- text: The reminder content
- priority: "high", "medium", or "low"

Respond in this EXACT JSON format:
{
    "homework": [
        {"subject": "Math", "task": "Page 50 exercises 1-10", "due_date": "tomorrow"},
        ...
    ],
    "reminders": [
        {"text": "Bring lab coat on Wednesday", "priority": "high"},
        ...
    ],
    "summary": "Brief 1-2 sentence summary of what's important today"
}

If no homework or reminders found, return empty arrays.
Preserve the original language (Arabic/English) of the content."""

        try:
            uploaded_file = genai.upload_file(file_path)
            response = model.generate_content([uploaded_file, prompt])

            # Clean up uploaded file
            try:
                genai.delete_file(uploaded_file.name)
            except Exception:
                pass

            # Parse JSON from response
            return self._extract_json(response.text)

        except Exception as e:
            return {'error': str(e), 'homework': [], 'reminders': []}

    def _extract_json(self, text: str) -> dict:
        """Extract JSON from AI response text"""
        try:
            # Try direct parse
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try to find JSON block in markdown
        patterns = [
            r'```json\s*([\s\S]*?)\s*```',
            r'```\s*([\s\S]*?)\s*```',
            r'\{[\s\S]*\}'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    json_str = match.group(1) if '```' in pattern else match.group(0)
                    return json.loads(json_str)
                except (json.JSONDecodeError, IndexError):
                    continue

        return {
            'error': 'Could not parse AI response',
            'raw_response': text[:1000],
            'homework': [],
            'reminders': []
        }
