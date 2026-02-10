import json, PyPDF2
from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyBhY-PTuMxEzy9daGlkcRKRBRuxnKsr78M")

def extract_resume_text(pdf_path):
    try:
        reader = PyPDF2.PdfReader(pdf_path)
        return "".join([page.extract_text() for page in reader.pages])
    except Exception: return ""

def is_good_match(job_description):
    """
    Evaluates job descriptions against Gopi Borra's Data Science profile.
    Targeting roles that fit an M.Sc. student with internship experience.
    """
    job_desc_lower = job_description.lower()
    
    # 1. High-Value Technical Keywords
    # Based on your PW Skills and Unified Mentor experience
    tech_keywords = [
        "python", "sql", "machine learning", "ml", "data analysis", 
        "power bi", "tableau", "statistics", "pandas", "scikit-learn"
    ]
    
    # 2. Preferred Industry/Level Terms
    # Targeting Entry-to-Intermediate roles for your transition
    level_keywords = ["junior", "associate", "intern", "entry level", "fresher"]

    # 3. Match Scoring Logic
    tech_score = sum(1 for word in tech_keywords if word in job_desc_lower)
    level_match = any(word in job_desc_lower for word in level_keywords)

    # 4. Decision Logic
    # We apply if the job mentions at least 3 tech skills
    # We give a bonus if it's explicitly an entry-level/associate role
    if tech_score >= 3:
        print(f"✅ Match Score: {tech_score}/10. Criteria met.")
        return True
    elif tech_score >= 2 and level_match:
        print(f"✅ Match Score: {tech_score}/10 with Level Match. Criteria met.")
        return True
    
    print(f"❌ Match Score: {tech_score}/10. Requirements not met.")
    return False