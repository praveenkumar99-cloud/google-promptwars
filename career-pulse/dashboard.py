import streamlit as st
from storage import save_user_profile, get_jobs_for_user, get_user_profile
from datetime import date
import pandas as pd

st.set_page_config(page_title="CareerPulse", page_icon="🎯")
st.title("🎯 CareerPulse - Your AI Job Assistant")

tab1, tab2 = st.tabs(["📝 Register", "📊 Today's Jobs"])

with tab1:
    st.header("Set up your job preferences")
    email = st.text_input("Your email address")
    skills_input = st.text_area("Your skills (comma-separated)", "Python, SQL, Machine Learning, AWS")
    if st.button("Save Profile"):
        if email and skills_input:
            save_user_profile(email, skills_input)
            st.success("Profile saved! You'll receive job matches every morning at 8 AM.")
        else:
            st.error("Please fill in both email and skills.")

with tab2:
    st.header("Your recommendations for today")
    email_for_jobs = st.text_input("Enter your email to see today's matches")
    if st.button("Show my jobs"):
        if email_for_jobs:
            profile = get_user_profile(email_for_jobs)
            if not profile:
                st.warning("No profile found. Please register first.")
            else:
                jobs = get_jobs_for_user(email_for_jobs, str(date.today()))
                if jobs:
                    df = pd.DataFrame(jobs)
                    st.dataframe(df[['title', 'company', 'match_score', 'url']])
                else:
                    st.info("No jobs yet. Check back after 8 AM or wait for tomorrow's email.")
        else:
            st.error("Please enter your email.")
