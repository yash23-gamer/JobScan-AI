import streamlit as st
import requests
from resume_analysis import analyze_resume

# Page Configuration
st.set_page_config(
    page_title="JobScan Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def set_custom_css():
    st.markdown("""
        <style>
        body {
            background-color: #1E1E1E;
            color: #F5F5F5;
            font-family: Arial, sans-serif;
        }

        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            font-size: 16px;
            padding: 10px 20px;
            border: none;
        }

        .stButton > button:hover {
            background-color: #45A049;
        }

        .stTextArea textarea {
            border-radius: 10px;
        }

        .stFileUploader {
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

set_custom_css()

# Sidebar
st.sidebar.title("📑 Navigation")

page = st.sidebar.radio(
    "Go To",
    ["🏠 Home", "📊 Resume Analysis"]
)

# Home Page
if page == "🏠 Home":

    st.title("🚀 Welcome to JobScan Pro")

    st.markdown("""
    ### AI-Powered ATS Resume Analyzer

    Compare your resume with job descriptions and improve your chances of getting shortlisted.

    ### Features
    - 📈 ATS Match Score
    - ❌ Missing Keywords Detection
    - 💡 Skill Suggestions
    - 📝 Resume Feedback
    - 🚀 Skill Gap Analysis
    - ✅ Job Role Suggestions

    ### Tech Stack
    - Python
    - Streamlit
    - Groq API
    - PyMuPDF
    """)
   
    st.markdown("---")

    st.markdown("""
<div style="
    text-align: center;
    padding: 14px;
    font-size: 17px;
    font-style: italic;
    font-weight: bold;
    font-family: 'Segoe UI', sans-serif;
    letter-spacing: 0.5px;
">
    ☕ Made with passion by 
    <span style="
        background: linear-gradient(90deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    ">
        Yash Umate
    </span>
</div>
""", unsafe_allow_html=True)
# Resume Analysis Page
elif page == "📊 Resume Analysis":

    st.title("📊 Resume Analysis")

    job_description = st.text_area(
        "📝 Paste Job Description",
        height=200,
        placeholder="Paste the job description here..."
    )

    uploaded_file = st.file_uploader(
        "📂 Upload Resume (PDF Only)",
        type=["pdf"]
    )

    analysis_type = st.selectbox(
        "🔍 Select Analysis Type",
        [
            "📈 Match Score",
            "❌ Missing Keywords",
            "💡 Skill Suggestions",
            "📝 AI-Powered Resume Feedback",
            "📥 Download Optimized Resume",
            "✅ Bullet Point Suggestions",
            "🚀 Skill Gap Analysis",
            "✅ Job Suggestion"
        ]
    )

    if st.button("🚀 Run Analysis"):

        if uploaded_file is not None and job_description.strip():

            with st.spinner("🔍 Analyzing Resume... Please wait"):

                analysis_result = analyze_resume(
                    uploaded_file,
                    job_description,
                    analysis_type
                )

            st.success("✅ Analysis Complete!")

            st.markdown("### 📊 Analysis Result")

            st.markdown(analysis_result)

        else:
            st.error("⚠ Please upload a resume and paste a job description.")