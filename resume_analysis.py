import os
import fitz  # PyMuPDF
import requests
import json
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Groq API Configuration
GROQ_API_KEY = os.getenv("Your_api_key")
GROQ_MODEL = "openai/gpt-oss-120b"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF resume and checks for empty output."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    extracted_text = "\n".join([page.get_text("text") for page in doc])

    if not extracted_text.strip():
        return "Error: No text extracted from the resume. Please upload a text-based PDF."
    
    return extracted_text

def query_groq_api(prompt):
    """Sends the prompt to Groq API and gets a response."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        
        if response.status_code != 200:
            return f"API Error: {response.status_code} - {response.text}"

        response_json = response.json()
        
        if "choices" not in response_json or not response_json["choices"]:
            return f"Unexpected API Response: {response_json}"
        
        return response_json["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error communicating with Groq API: {str(e)}"

def analyze_resume(resume_file, job_description, analysis_type):
    """Analyzes resume using Groq's Llama 3 70B model."""
    resume_text = extract_text_from_pdf(resume_file)

    # Check if resume text is extracted correctly
    if "Error: No text extracted" in resume_text:
        return resume_text  # Return error message directly

    prompt_templates = {
        "📈 Match Score": """
            Compare the resume with the job description and provide a match score (percentage).
            Explain the methodology behind the score calculation.
        """,
        "❌ Missing Keywords": """
            Identify keywords from the job description that are missing in the resume.
            List them along with their importance.
        """,
        "💡 Skill Suggestions": """
            Analyze the resume and suggest additional skills that would improve the applicant's profile for this job.
        """,
        "📝 AI-Powered Resume Feedback": """
            Provide feedback on the resume's structure, content, formatting, and how well it matches the job description.
            Suggest improvements.
        """,
        "📥 Download Optimized Resume": """
            Rewrite the resume in a more optimized format based on the job description.
            Ensure it is ATS-friendly and highlights relevant skills.
        """,
        "✅ Bullet Point Suggestions": """
            Improve the bullet points in the resume by making them more impactful, clear, and achievement-oriented.
        """,
        "🚀 Skill Gap Analysis": """
            Identify skills required for the job that are missing or underrepresented in the resume.
            Provide recommendations for improvement.
        """,
        "✅ Job Suggestion": """
            Based on the resume, suggest alternative job roles that match the applicant's skills and experience.
        """
    }

    prompt = f"""
    You are an AI-powered ATS Resume Analyzer. Compare the following resume with the given job description.

    Job Description:
    {job_description}

    Resume:
    {resume_text}

    {prompt_templates.get(analysis_type, "Provide a detailed analysis based on the resume and job description.")}
    
    Provide structured results.
    """
    
    return query_groq_api(prompt)

# Streamlit UI
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📄 Resume Analysis"])

if page == "📄 Resume Analysis":
    st.title("📄 Resume Analysis")
    job_description = st.text_area("📌 Paste Job Description", height=200)
    resume_file = st.file_uploader("📂 Upload Your Resume (PDF Only)", type=["pdf"])

    if resume_file and job_description:
        analysis_type = st.selectbox("🔍 Choose Analysis Type", [
            "📈 Match Score", "❌ Missing Keywords", "💡 Skill Suggestions",
            "📝 AI-Powered Resume Feedback", "📥 Download Optimized Resume",
            "✅ Bullet Point Suggestions", "🚀 Skill Gap Analysis", "✅ Job Suggestion"
        ])
        
        if st.button("🚀 Run Analysis"):
            st.success("✅ Analysis Complete!")
            analysis_result = analyze_resume(resume_file, job_description, analysis_type)
            st.text_area("📊 Analysis Results", analysis_result, height=300)
