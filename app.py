import streamlit as st
import requests
from resume_analysis import analyze_resume

# Streamlit UI Configuration
st.set_page_config(page_title="JobScan Pro", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for improved UI
def set_custom_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #1E1E1E;
            color: #F5F5F5;
            font-family: 'Arial', sans-serif;
        }
        .stTextInput, .stTextArea, .stSelectbox, .stFileUploader, .stButton {
            background-color: #2A2A2A !important;
            color: #F5F5F5 !important;
            border-radius: 10px !important;
        }
        .stButton > button {
            background-color: #4CAF50 !important;
            color: white !important;
            border-radius: 10px !important;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #45A049 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_custom_css()

# Sidebar Navigation
st.sidebar.title("📑 Navigation")
page = st.sidebar.radio("", ["🏠 Home", "📊 Resume Analysis"])

# Home Page
if page == "🏠 Home":
    st.title("🚀 Welcome to JobScan Pro")
    st.write("Compare your resume with job descriptions and improve your chances of landing your dream job!")

# Resume Analysis Page
elif page == "📊 Resume Analysis":
    st.title("📑 Resume Analysis")
    
    job_description = st.text_area("📝 Paste the Job Description here:", height=200)
    uploaded_file = st.file_uploader("📂 Upload Your Resume (PDF only)", type=["pdf"])

    analysis_type = st.selectbox("🔍 Choose Analysis Type", [
        "📈 Match Score", "❌ Missing Keywords", "💡 Skill Suggestions",
        "📝 AI-Powered Resume Feedback", "📥 Download Optimized Resume",
        "✅ Bullet Point Suggestions", "🚀 Skill Gap Analysis", "✅ Job Suggestion"
    ])

    if st.button("🚀 Run Analysis"):
        if uploaded_file is not None and job_description.strip():
            st.success("✅ Analysis in Progress... Please wait.")

            # Call the analysis function
            analysis_result = analyze_resume(uploaded_file, job_description, analysis_type)

            st.success("✅ Analysis Complete!")
            st.markdown(analysis_result, unsafe_allow_html=True)
        else:
            st.error("⚠ Please upload a resume and provide a job description!")
