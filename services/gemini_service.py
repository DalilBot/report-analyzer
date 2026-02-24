"""
Google Gemini AI Service Module
Handles all AI-related operations using Google's Gemini API
"""
import google.generativeai as genai
from typing import List, Dict, Any, Optional
import json
import re
from config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiService:
    """Service class for interacting with Google Gemini API"""
    
    def __init__(self):
        """Initialize the Gemini service with API key"""
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.vision_model = genai.GenerativeModel("gemini-1.5-pro")
    
    async def analyze_materials(self, file_contents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze uploaded learning materials and extract key information
        
        Args:
            file_contents: List of dictionaries with file info and content
            
        Returns:
            Dictionary containing analysis results
        """
        prompt = """
        Analyze the following learning materials and provide:
        1. A summary of the main topics covered
        2. Key concepts that need to be understood
        3. Estimated difficulty level (1-5 scale)
        4. Suggested breakdown of tasks/sections
        5. Learning objectives
        
        Materials:
        """
        
        for file_info in file_contents:
            prompt += f"\n\n--- File: {file_info['filename']} ---\n"
            prompt += file_info.get('content', '[Binary content - image or document]')
        
        prompt += """
        
        Please respond in JSON format:
        {
            "summary": "overall summary",
            "topics": ["topic1", "topic2", ...],
            "key_concepts": ["concept1", "concept2", ...],
            "difficulty_level": 3,
            "task_sections": [
                {"section": "name", "description": "desc", "estimated_difficulty": 2},
                ...
            ],
            "learning_objectives": ["objective1", "objective2", ...]
        }
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Extract JSON from response
            result = self._extract_json(response.text)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    async def divide_tasks(
        self, 
        analysis: Dict[str, Any], 
        members: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Divide tasks among group members based on their difficulty levels
        
        Args:
            analysis: The analysis results from analyze_materials
            members: List of member dictionaries with name and difficulty_level
            
        Returns:
            Dictionary mapping member names to their assigned tasks
        """
        prompt = f"""
        Based on the following material analysis and group members with their skill levels,
        divide the tasks appropriately so that:
        - Beginners (level 1-2) get simpler, foundational tasks
        - Intermediate (level 3) get moderate tasks
        - Advanced (level 4-5) get complex, challenging tasks
        
        Material Analysis:
        {json.dumps(analysis, indent=2)}
        
        Group Members:
        {json.dumps(members, indent=2)}
        
        Please distribute the task_sections fairly while considering each member's difficulty level.
        
        Respond in JSON format:
        {{
            "assignments": [
                {{
                    "member_name": "name",
                    "difficulty_level": 2,
                    "assigned_tasks": [
                        {{"task": "task name", "description": "what to do", "reason": "why assigned"}}
                    ],
                    "estimated_time": "2 hours",
                    "tips": "helpful tips for this member"
                }},
                ...
            ],
            "collaboration_suggestions": ["suggestion1", "suggestion2"],
            "timeline_recommendation": "suggested overall timeline"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = self._extract_json(response.text)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    async def generate_survey_questions(
        self, 
        file_contents: List[Dict[str, Any]], 
        num_questions: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate survey/quiz questions based on uploaded materials
        
        Args:
            file_contents: List of file content dictionaries
            num_questions: Number of questions to generate
            
        Returns:
            List of question dictionaries
        """
        prompt = f"""
        Based on the following learning materials, create {num_questions} high-quality 
        multiple choice survey/quiz questions that test understanding of the key concepts.
        
        Materials:
        """
        
        for file_info in file_contents:
            prompt += f"\n\n--- File: {file_info['filename']} ---\n"
            prompt += file_info.get('content', '[Content from document]')[:5000]  # Limit content
        
        prompt += f"""
        
        Create exactly {num_questions} questions. For each question:
        - Make it test genuine understanding, not just memorization
        - Include 4 answer options (A, B, C, D)
        - Mark the correct answer
        - Vary difficulty levels
        
        Respond in JSON format:
        {{
            "questions": [
                {{
                    "question_number": 1,
                    "question_text": "question here",
                    "options": {{
                        "A": "option A",
                        "B": "option B", 
                        "C": "option C",
                        "D": "option D"
                    }},
                    "correct_answer": "A",
                    "difficulty": "easy/medium/hard",
                    "topic": "related topic"
                }},
                ...
            ]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = self._extract_json(response.text)
            return result.get("questions", [])
        except Exception as e:
            return [{"error": str(e)}]
    
    async def generate_fake_predictions(
        self, 
        questions: List[Dict[str, Any]], 
        num_responses: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Generate fake/simulated survey responses for predictions
        
        Args:
            questions: List of question dictionaries
            num_responses: Number of fake responses to generate
            
        Returns:
            List of simulated response dictionaries
        """
        prompt = f"""
        Given the following survey questions, simulate {num_responses} realistic student responses.
        Consider that students have varying levels of understanding:
        - Some students (about 20%) will answer most questions correctly (high performers)
        - Most students (about 60%) will have mixed results (average performers)
        - Some students (about 20%) will struggle with the material (need help)
        
        Questions:
        {json.dumps(questions, indent=2)}
        
        Generate {num_responses} simulated responses with realistic patterns.
        Include some common misconceptions where wrong answers are chosen.
        
        Respond in JSON format:
        {{
            "responses": [
                {{
                    "respondent_id": 1,
                    "respondent_type": "high_performer/average/needs_help",
                    "answers": {{
                        "Q1": "A",
                        "Q2": "B",
                        ...
                    }},
                    "score": 4,
                    "score_percentage": 80
                }},
                ...
            ],
            "statistics": {{
                "average_score": 3.5,
                "average_percentage": 70,
                "question_difficulty": {{
                    "Q1": {{"correct_count": 20, "percentage": 80}},
                    ...
                }},
                "common_wrong_answers": {{
                    "Q1": {{"most_common_wrong": "B", "count": 3}},
                    ...
                }}
            }}
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = self._extract_json(response.text)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    async def generate_presentation_content(
        self, 
        file_contents: List[Dict[str, Any]],
        analysis: Dict[str, Any],
        num_slides: int = 10
    ) -> Dict[str, Any]:
        """
        Generate PowerPoint presentation content based on materials
        
        Args:
            file_contents: List of file content dictionaries
            analysis: The material analysis results
            num_slides: Target number of slides
            
        Returns:
            Dictionary with presentation structure
        """
        prompt = f"""
        Based on the following learning materials and analysis, create a comprehensive 
        PowerPoint presentation with approximately {num_slides} slides.
        
        Material Analysis:
        {json.dumps(analysis, indent=2)}
        
        Original Materials Summary:
        """
        
        for file_info in file_contents:
            prompt += f"\n\n--- {file_info.get('filename', 'File')} ---\n"
            content = file_info.get('content', '')
            prompt += content[:3000] if content else '[Content not available]'
        
        prompt += f"""
        
        Create a well-structured presentation with:
        1. Title slide with a compelling title and subtitle
        2. Overview/Agenda slide
        3. Main content slides covering key topics
        4. Summary/Key Takeaways slide
        5. Questions/Discussion slide
        
        For each slide, provide:
        - A clear, concise title
        - Bullet points (3-5 per slide, keep them brief)
        - Speaker notes for elaboration
        - Suggested visual/image description if applicable
        
        Respond in JSON format:
        {{
            "presentation_title": "Main Title",
            "presentation_subtitle": "Subtitle or tagline",
            "slides": [
                {{
                    "slide_number": 1,
                    "slide_type": "title/content/summary/questions",
                    "title": "Slide Title",
                    "bullet_points": ["Point 1", "Point 2", "Point 3"],
                    "speaker_notes": "Detailed notes for presenter...",
                    "visual_suggestion": "Description of suggested image/diagram",
                    "layout": "title_slide/bullet_points/two_column/image_with_text"
                }},
                ...
            ],
            "theme_suggestion": "professional/academic/creative/minimal",
            "color_scheme": {{
                "primary": "#hex_color",
                "secondary": "#hex_color", 
                "accent": "#hex_color"
            }}
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = self._extract_json(response.text)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    async def analyze_image(self, image_data: bytes, mime_type: str) -> str:
        """
        Analyze an image using Gemini Vision
        
        Args:
            image_data: Raw image bytes
            mime_type: Image MIME type (e.g., 'image/png')
            
        Returns:
            Text description/analysis of the image
        """
        try:
            image_part = {
                "mime_type": mime_type,
                "data": image_data
            }
            
            prompt = "Describe the content of this image in detail. If it contains text, extract and include it. If it's educational material, summarize the key points."
            
            response = self.vision_model.generate_content([prompt, image_part])
            return response.text
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
    
    def _extract_json(self, text: str) -> Dict[str, Any]:
        """
        Extract JSON from response text that may contain markdown code blocks
        
        Args:
            text: Raw response text
            
        Returns:
            Parsed JSON dictionary
        """
        # Try to find JSON in code blocks first
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find raw JSON
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                json_str = json_match.group(0)
            else:
                return {"raw_response": text}
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return {"raw_response": text}
    
    async def analyze_daily_report(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a daily school report PDF directly and extract homework and reminders only.
        Does NOT include material covered today.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary containing homework and reminders
        """
        prompt = """
        You are analyzing a daily school report. Extract ONLY the following information:
        
        1. **Homework/Assignments**: Any homework, assignments, or tasks that students need to complete at home
        2. **Reminders**: Important reminders, upcoming tests, deadlines, events, or notes for parents/students
        
        DO NOT include:
        - Material covered in class today
        - What was taught or learned
        - Class activities or discussions
        
        Please respond in JSON format:
        {
            "homework": [
                {
                    "subject": "Subject name",
                    "task": "Description of homework",
                    "due_date": "Due date if mentioned, otherwise null"
                }
            ],
            "reminders": [
                {
                    "type": "test/event/deadline/note",
                    "description": "Description of the reminder",
                    "date": "Date if mentioned, otherwise null"
                }
            ],
            "summary": "Brief one-line summary of important tasks"
        }
        
        If there is no homework, return an empty array for homework.
        If there are no reminders, return an empty array for reminders.
        Respond in the same language as the report (Arabic or English).
        """
        
        try:
            # Upload the PDF file to Gemini
            uploaded_file = genai.upload_file(file_path)
            
            # Send the file directly to Gemini for analysis
            response = self.model.generate_content([uploaded_file, prompt])
            result = self._extract_json(response.text)
            
            # Clean up the uploaded file
            try:
                genai.delete_file(uploaded_file.name)
            except:
                pass
            
            return result
        except Exception as e:
            return {"error": str(e), "homework": [], "reminders": []}
    
    async def generate_response(self, prompt: str) -> Optional[str]:
        """
        Generate a general text response from Gemini
        
        Args:
            prompt: The prompt to send to Gemini
            
        Returns:
            Generated text response or None on error
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini generate_response error: {e}")
            return None


# Singleton instance
gemini_service = GeminiService()
