"""
Assessment Schedule Analyzer
Run this script manually at the start of each term to load the assessment schedule.

Usage:
    python analyze_assessment.py <path_to_pdf>
    python analyze_assessment.py "T2 Assessment Schedule Grade 11.pdf"
"""

import sys
import os
import argparse
import asyncio
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import GEMINI_API_KEY
from utils.assessment_memory import assessment_memory

import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_assessment_schedule(pdf_path: str) -> dict:
    """
    Analyze an assessment schedule PDF using Gemini AI
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary containing extracted exam information
    """
    print(f"\n📄 Analyzing: {os.path.basename(pdf_path)}")
    print("=" * 50)
    
    # Upload the PDF to Gemini
    print("📤 Uploading PDF to Gemini...")
    uploaded_file = genai.upload_file(pdf_path)
    
    prompt = """
    Analyze this assessment schedule document and extract ALL exams, tests, quizzes, and assessments.
    
    For EACH assessment found, extract:
    1. Subject name
    2. Type of assessment (Quiz, Test, Exam, Project, Presentation, Final, etc.)
    3. Date (convert to YYYY-MM-DD format)
    4. Day of the week
    5. Topics or chapters covered (if mentioned)
    6. Any additional notes
    
    Also extract:
    - Term/Semester information (e.g., "Term 2", "Semester 1")
    - Grade level
    - Academic year
    
    IMPORTANT: 
    - Convert ALL dates to YYYY-MM-DD format
    - If the year is not specified, assume 2026
    - Include ALL assessments, even if some info is missing
    
    Respond in JSON format:
    {
        "term": "Term 2",
        "grade": "Grade 11",
        "year": "2025-2026",
        "exams": [
            {
                "subject": "Mathematics",
                "exam_type": "Quiz",
                "date": "2026-02-15",
                "day_of_week": "Sunday",
                "topics": ["Chapter 5", "Trigonometry"],
                "notes": "Calculator allowed"
            },
            ...
        ]
    }
    """
    
    print("🤖 Analyzing with Gemini AI...")
    response = model.generate_content([uploaded_file, prompt])
    
    # Clean up uploaded file
    try:
        genai.delete_file(uploaded_file.name)
    except:
        pass
    
    # Extract JSON from response
    import re
    import json
    
    text = response.text
    
    # Try to find JSON in code block
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
    if json_match:
        json_str = json_match.group(1)
    else:
        # Try to find raw JSON
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            json_str = json_match.group(0)
        else:
            print("❌ Could not extract JSON from response")
            print("Raw response:", text[:500])
            return {"exams": []}
    
    try:
        result = json.loads(json_str)
        return result
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        return {"exams": []}


def display_exams(exams: list):
    """Display extracted exams in a formatted table"""
    if not exams:
        print("\n❌ No exams found in the schedule.")
        return
    
    print(f"\n📋 Found {len(exams)} assessments:\n")
    print("-" * 80)
    print(f"{'Date':<12} {'Day':<10} {'Subject':<20} {'Type':<15} {'Topics'}")
    print("-" * 80)
    
    for exam in sorted(exams, key=lambda x: x.get('date', '9999-99-99')):
        date = exam.get('date', 'N/A')
        day = exam.get('day_of_week', 'N/A')[:9]
        subject = exam.get('subject', 'Unknown')[:19]
        exam_type = exam.get('exam_type', 'N/A')[:14]
        topics = ', '.join(exam.get('topics', []))[:30]
        
        print(f"{date:<12} {day:<10} {subject:<20} {exam_type:<15} {topics}")
    
    print("-" * 80)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze assessment schedule PDF and save to memory',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python analyze_assessment.py "T2 Assessment Schedule Grade 11.pdf"
    python analyze_assessment.py schedule.pdf --clear
    
This will:
1. Analyze the PDF using Gemini AI
2. Extract all exams, tests, quizzes
3. Save them to assessment_schedule.json
4. The Discord bot will then send reminders automatically
        """
    )
    
    parser.add_argument('pdf_path', help='Path to the assessment schedule PDF')
    parser.add_argument('--clear', action='store_true', help='Clear existing schedule before adding')
    parser.add_argument('--show', action='store_true', help='Only show current schedule, do not analyze')
    
    args = parser.parse_args()
    
    # Show current schedule
    if args.show:
        term_info = assessment_memory.get_term_info()
        exams = assessment_memory.get_all_exams()
        
        print("\n📅 Current Assessment Schedule")
        print("=" * 50)
        print(f"Term: {term_info['term']}")
        print(f"Grade: {term_info['grade']}")
        print(f"Year: {term_info['year']}")
        print(f"Last Updated: {term_info['last_updated']}")
        
        display_exams(exams)
        
        summary = assessment_memory.get_summary()
        print(f"\n📊 Summary:")
        print(f"   Total: {summary['total_exams']}")
        print(f"   Completed: {summary['completed']}")
        print(f"   Remaining: {summary['remaining']}")
        return
    
    # Check if PDF exists
    if not os.path.exists(args.pdf_path):
        print(f"❌ File not found: {args.pdf_path}")
        sys.exit(1)
    
    # Clear existing if requested
    if args.clear:
        print("🗑️ Clearing existing schedule...")
        assessment_memory.clear_schedule()
    
    # Analyze the PDF
    try:
        analysis = analyze_assessment_schedule(args.pdf_path)
    except Exception as e:
        print(f"❌ Error analyzing PDF: {e}")
        sys.exit(1)
    
    # Display term info
    print(f"\n📚 Term Information:")
    print(f"   Term: {analysis.get('term', 'Unknown')}")
    print(f"   Grade: {analysis.get('grade', 'Unknown')}")
    print(f"   Year: {analysis.get('year', 'Unknown')}")
    
    # Display extracted exams
    exams = analysis.get('exams', [])
    display_exams(exams)
    
    # Ask for confirmation
    print(f"\n❓ Save these {len(exams)} assessments to memory? (y/n): ", end='')
    confirm = input().strip().lower()
    
    if confirm in ['y', 'yes']:
        count = assessment_memory.add_exams_from_analysis(analysis)
        print(f"\n✅ Saved {count} assessments to assessment_schedule.json")
        
        # Show upcoming
        upcoming = assessment_memory.get_upcoming_exams(days=14)
        if upcoming:
            print(f"\n📅 Upcoming in next 2 weeks ({len(upcoming)} exams):")
            for exam in upcoming:
                print(f"   • {exam['date']} - {exam['subject']} ({exam['exam_type']})")
        
        print("\n🔔 The Discord bot will now send:")
        print("   • Weekly reminders every Sunday at 6 PM")
        print("   • Night-before reminders at 8 PM")
        print("   • Material covered from daily reports")
    else:
        print("\n❌ Cancelled. No changes saved.")


if __name__ == "__main__":
    main()
