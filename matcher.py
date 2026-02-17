import os
import json
import PyPDF2
from google import genai

# Initialize Gemini Client using Render environment variable (not hardcoded .env path)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def extract_resume_text():
    """Extracts text from resume. On Render, looks in the working directory."""
    pdf_path = os.environ.get("RESUME_PATH", "Borra_Gopi_Resume.pdf")
    try:
        reader = PyPDF2.PdfReader(pdf_path)
        return "".join([page.extract_text() for page in reader.pages])
    except Exception as e:
        print(f"⚠️ Could not read resume PDF ({e}). Using hardcoded profile instead.")
        # Fallback profile so matching still works even without the PDF on Render
        return """
        Gopi Borra | M.Sc. Data Science, Chandigarh University (9.00 SGPA)
        Skills: Python, SQL, Machine Learning, Data Analysis, Power BI, Pandas, NumPy
        Experience: Unified Mentor Data Science Internship | 5 years Aviation Security
        Projects: Job Application Bot, Agentic AI Automation
        """

def is_good_match(job_description):
    """
    Uses Gemini AI to decide if the job matches Gopi's profile.
    Falls back to keyword search if Gemini fails.
    """
    resume_text = extract_resume_text()

    prompt = f"""
    You are an expert HR Analyst. Compare the following Resume and Job Description.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Decision Criteria:
    1. Does the job require Python, SQL, or ML?
    2. Is it suitable for someone with an M.Sc. in Data Science and an internship?
    3. Ignore jobs requiring 10+ years of experience.

    Return ONLY valid JSON with no markdown, no backticks:
    {{"match": true, "reason": "short explanation"}}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        # Safe JSON parsing (never use eval on external data)
        raw = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)

        if data.get("match"):
            print(f"  ✅ AI Match: {data.get('reason')}")
            return True
        else:
            print(f"  ❌ AI Skip: {data.get('reason')}")
            return False

    except Exception as e:
        print(f"  ⚠️ Gemini error, using keyword fallback: {e}")
        keywords = ["python", "sql", "data", "machine learning", "analytics", "ml", "ai"]
        return any(kw in job_description.lower() for kw in keywords)