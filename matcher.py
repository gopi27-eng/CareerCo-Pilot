import os
import PyPDF2
from google import genai
from dotenv import load_dotenv

# Load variables from .env
load_dotenv(r"C:/Users/Gopi/Desktop/Automate Job Application Agnetic AI/.env")

# Initialize Gemini Client securely
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_resume_text():
    """Extracts text from your resume file defined in .env."""
    pdf_path = os.getenv("RESUME_PATH", "Borra_Gopi_Resume.pdf")
    try:
        reader = PyPDF2.PdfReader(pdf_path)
        return "".join([page.extract_text() for page in reader.pages])
    except Exception as e:
        print(f"⚠️ Could not read resume: {e}")
        return ""

def is_good_match(job_description):
    """
    Uses Gemini AI to decide if the job matches Gopi's M.Sc. Data Science 
    and Unified Mentor internship profile.
    """
    resume_text = extract_resume_text()
    
    prompt = f"""
    You are an expert HR Analyst. Compare the following Resume and Job Description.
    
    Resume: {resume_text}
    Job Description: {job_description}
    
    Decision Criteria:
    1. Does the job require Python, SQL, or ML?
    2. Is it suitable for someone with an M.Sc. in Data Science and an internship?
    3. Ignore jobs requiring 10+ years of experience.
    
    Return ONLY a JSON object: {{"match": true/false, "reason": "short explanation"}}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        # Clean the response and parse JSON
        result = response.text.replace('```json', '').replace('```', '').strip()
        data = eval(result) # Convert string to dict
        
        if data.get("match"):
            print(f"✅ AI Match Found: {data.get('reason')}")
            return True
        else:
            print(f"❌ AI Skip: {data.get('reason')}")
            return False
            
    except Exception as e:
        print(f"⚠️ AI Matching Error, falling back to keyword search: {e}")
        # Fallback to your old keyword logic if API fails
        return "python" in job_description.lower() or "data" in job_description.lower()