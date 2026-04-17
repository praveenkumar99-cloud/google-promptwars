import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
import json
import random

# Page config
st.set_page_config(
    page_title="CareerPulse - AI Job Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    /* Main container */
    .main { padding: 0rem 1rem; }
    
    /* Custom card style */
    .job-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #2563EB;
    }
    
    /* Match score badges */
    .match-high {
        background-color: #10B981;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .match-medium {
        background-color: #F59E0B;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
    .match-low {
        background-color: #EF4444;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
    
    /* Skill tags */
    .skill-tag {
        background-color: #E0E7FF;
        color: #2563EB;
        padding: 2px 8px;
        border-radius: 15px;
        font-size: 12px;
        display: inline-block;
        margin: 2px;
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1.2rem;
        text-align: center;
    }
    
    /* Dark mode */
    .dark-mode {
        background-color: #1F2937;
        color: white;
    }
    
    /* Metric card */
    .metric-card {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "https://career-pulse-665822784067.us-central1.run.app"

# Check backend health
try:
    health_response = requests.get(f"{BACKEND_URL}/", timeout=5)
    backend_healthy = health_response.status_code == 200
except:
    backend_healthy = False

# Sidebar navigation
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🎯 CareerPulse</h2>", unsafe_allow_html=True)
    
    if backend_healthy:
        st.success("✅ Backend Connected")
    else:
        st.error("⚠️ Backend Unavailable")
    
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Register Profile", "Job Matches", "Application Tracker", "Analytics", "Skill Gap"],
        icons=["house", "pencil-square", "briefcase", "check-circle", "graph-up", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        styles={
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#2563EB"},
        }
    )

# Initialize session state
if 'profile' not in st.session_state:
    st.session_state.profile = None
if 'saved_jobs' not in st.session_state:
    st.session_state.saved_jobs = []
if 'applications' not in st.session_state:
    st.session_state.applications = []

# Mock job data (will be replaced with real API calls later)
def get_mock_jobs():
    skills_list = ["Python", "SQL", "Java", "AWS", "Docker", "Kubernetes", "React", "Django", "FastAPI", "MongoDB"]
    companies = ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "Spotify", "Stripe", "Shopify"]
    titles = ["Software Engineer", "Data Scientist", "DevOps Engineer", "Frontend Developer", "Backend Engineer", "Full Stack Developer"]
    
    jobs = []
    for i in range(25):
        job_skills = random.sample(skills_list, random.randint(3, 6))
        match_score = random.randint(40, 98)
        jobs.append({
            'id': i,
            'title': random.choice(titles),
            'company': random.choice(companies),
            'description': f"We are looking for a {random.choice(titles)} to join our team. Required skills: {', '.join(job_skills[:4])}...",
            'skills_required': job_skills,
            'match_score': match_score,
            'match_level': 'high' if match_score >= 70 else 'medium' if match_score >= 40 else 'low',
            'url': f"https://example.com/job/{i}",
            'posted_date': (datetime.now() - timedelta(days=random.randint(0, 14))).strftime("%Y-%m-%d"),
            'source': random.choice(["LinkedIn", "Indeed", "RemoteOK"])
        })
    return sorted(jobs, key=lambda x: x['match_score'], reverse=True)

# HOME PAGE
if selected == "Home":
    st.title("🎯 CareerPulse")
    st.markdown("### Your AI-Powered Job Hunting Assistant")
    st.markdown("Stop wasting hours searching. Get personalized job matches delivered daily.")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Jobs Analyzed", "10,000+", "+12%")
    with col2:
        st.metric("🎯 Avg Match Score", "78%", "+5%")
    with col3:
        st.metric("✅ Success Rate", "94%", "+3%")
    with col4:
        st.metric("👥 Active Users", "1,247", "+18%")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 How It Works")
        st.markdown("""
        1. **Register** - Tell us your skills and preferences
        2. **Get Matches** - We find jobs matching your profile
        3. **Apply Smart** - Track applications and get insights
        4. **Improve** - See skill gaps and learn what's in demand
        """)
        
        if st.button("📝 Get Started Now", type="primary", use_container_width=True):
            st.session_state.selected = "Register Profile"
            st.rerun()
    
    with col2:
        st.subheader("🔥 Recent Success Stories")
        st.info("💼 **Sarah K.** found a Senior Python role with 92% match")
        st.success("💻 **Michael T.** got 3 interviews in first week")
        st.warning("📈 **Jessica L.** increased matches by 40% after skill recommendations")

# REGISTER PROFILE PAGE
elif selected == "Register Profile":
    st.title("📝 Create Your Profile")
    st.markdown("Tell us about yourself so we can find the best job matches.")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *", placeholder="John Doe")
            email = st.text_input("Email Address *", placeholder="john@example.com")
            experience = st.selectbox("Experience Level", ["Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior Level (6-9 years)", "Lead (10+ years)"])
        
        with col2:
            location = st.text_input("Location", placeholder="New York, NY (or Remote)")
            job_type = st.multiselect("Job Type Preferences", ["Remote", "Hybrid", "Onsite"], default=["Remote"])
            salary_expectation = st.selectbox("Expected Salary Range", ["$60k-$80k", "$80k-$100k", "$100k-$120k", "$120k-$150k", "$150k+"])
        
        skills_default = ["Python", "SQL", "JavaScript", "Java", "AWS", "Docker", "React", "Django"]
        skills = st.multiselect("Your Skills *", skills_default + ["FastAPI", "Kubernetes", "TensorFlow", "PyTorch", "Spring Boot", "C#", "Ruby", "Go", "Rust", "Angular", "Vue.js", "MongoDB", "PostgreSQL", "Redis", "Kafka", "Airflow", "Spark", "Hadoop", "Tableau", "Power BI"])
        
        submitted = st.form_submit_button("💾 Save Profile", type="primary", use_container_width=True)
        
        if submitted:
            if full_name and email and skills:
                st.session_state.profile = {
                    "name": full_name,
                    "email": email,
                    "experience": experience,
                    "location": location,
                    "job_type": job_type,
                    "salary": salary_expectation,
                    "skills": skills,
                    "registered_at": datetime.now().isoformat()
                }
                st.success("✅ Profile saved successfully! You'll receive job matches daily.")
                st.balloons()
            else:
                st.error("Please fill in all required fields (*).")
    
    if st.session_state.profile:
        st.divider()
        st.subheader("📋 Your Profile Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {st.session_state.profile['name']}")
            st.write(f"**Email:** {st.session_state.profile['email']}")
            st.write(f"**Experience:** {st.session_state.profile['experience']}")
        with col2:
            st.write(f"**Location:** {st.session_state.profile['location']}")
            st.write(f"**Job Type:** {', '.join(st.session_state.profile['job_type'])}")
            st.write(f"**Skills:** {', '.join(st.session_state.profile['skills'][:5])}...")

# JOB MATCHES PAGE
elif selected == "Job Matches":
    st.title("💼 Your Job Matches")
    st.markdown("Personalized recommendations based on your skills and preferences.")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        min_score = st.slider("Minimum Match Score", 0, 100, 40)
    with col2:
        sort_by = st.selectbox("Sort By", ["Match Score (High to Low)", "Match Score (Low to High)", "Date Posted (Newest)"])
    with col3:
        days_filter = st.selectbox("Posted Within", ["Any time", "Last 3 days", "Last 7 days", "Last 14 days"])
    
    # Get jobs (mock for now - can connect to real API)
    jobs = get_mock_jobs()
    
    # Apply filters
    filtered_jobs = [j for j in jobs if j['match_score'] >= min_score]
    
    if days_filter != "Any time":
        days = int(days_filter.split()[1])
        cutoff = datetime.now() - timedelta(days=days)
        filtered_jobs = [j for j in filtered_jobs if datetime.strptime(j['posted_date'], "%Y-%m-%d") >= cutoff]
    
    if sort_by == "Match Score (High to Low)":
        filtered_jobs = sorted(filtered_jobs, key=lambda x: x['match_score'], reverse=True)
    elif sort_by == "Match Score (Low to High)":
        filtered_jobs = sorted(filtered_jobs, key=lambda x: x['match_score'])
    else:
        filtered_jobs = sorted(filtered_jobs, key=lambda x: x['posted_date'], reverse=True)
    
    st.markdown(f"**Found {len(filtered_jobs)} jobs matching your criteria**")
    
    # Display job cards
    for job in filtered_jobs[:20]:
        with st.container():
            match_class = "match-high" if job['match_score'] >= 70 else "match-medium" if job['match_score'] >= 40 else "match-low"
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{job['title']}** at **{job['company']}**")
                st.caption(f"📅 Posted: {job['posted_date']} | 📍 {job['source']}")
                
                # Skill tags
                skill_html = "".join([f'<span class="skill-tag">{s}</span>' for s in job['skills_required'][:4]])
                st.markdown(f"Skills: {skill_html}", unsafe_allow_html=True)
                
                st.caption(job['description'][:120] + "...")
            
            with col2:
                st.markdown(f'<div class="{match_class}" style="text-align: center;">{job["match_score"]}% Match</div>', unsafe_allow_html=True)
                if st.button(f"Apply Now", key=f"apply_{job['id']}"):
                    st.markdown(f'<a href="{job["url"]}" target="_blank">Click here to apply</a>', unsafe_allow_html=True)
                if st.button(f"💾 Save", key=f"save_{job['id']}"):
                    if job not in st.session_state.saved_jobs:
                        st.session_state.saved_jobs.append(job)
                        st.toast(f"Saved {job['title']} for later!", icon="✅")
        
        st.divider()

# APPLICATION TRACKER PAGE
elif selected == "Application Tracker":
    st.title("📊 Application Tracker")
    st.markdown("Keep track of your job applications and follow-ups.")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        if st.button("➕ Add Application Manually", use_container_width=True):
            st.session_state.show_add_form = True
        
        if st.button("📥 Export to CSV", use_container_width=True):
            if st.session_state.applications:
                df = pd.DataFrame(st.session_state.applications)
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", csv, "applications.csv", "text/csv")
    
    # Add application form
    if st.session_state.get('show_add_form', False):
        with st.form("add_application"):
            st.subheader("Add Job Application")
            job_title = st.text_input("Job Title")
            company = st.text_input("Company")
            date_applied = st.date_input("Date Applied")
            status = st.selectbox("Status", ["Applied", "Interviewing", "Offer Received", "Rejected"])
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Save Application"):
                st.session_state.applications.append({
                    "job_title": job_title,
                    "company": company,
                    "date_applied": str(date_applied),
                    "status": status,
                    "notes": notes
                })
                st.session_state.show_add_form = False
                st.success("Application saved!")
                st.rerun()
    
    # Display applications table
    if st.session_state.applications:
        df_apps = pd.DataFrame(st.session_state.applications)
        
        # Status badges
        status_colors = {"Applied": "🟡", "Interviewing": "🔵", "Offer Received": "🟢", "Rejected": "🔴"}
        df_apps["Status"] = df_apps["status"].apply(lambda x: f"{status_colors.get(x, '⚪')} {x}")
        
        st.dataframe(df_apps[["job_title", "company", "date_applied", "Status", "notes"]], use_container_width=True)
        
        # Status distribution chart
        st.subheader("📈 Application Status Distribution")
        status_counts = df_apps["status"].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index, title="")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No applications yet. Save jobs from the Job Matches page to track them here.")

# ANALYTICS PAGE
elif selected == "Analytics":
    st.title("📈 Analytics Dashboard")
    st.markdown("Insights about your job search and market trends.")
    
    jobs = get_mock_jobs()
    df_jobs = pd.DataFrame(jobs)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Match Score Distribution")
        fig = px.histogram(df_jobs, x="match_score", nbins=20, title="")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Jobs by Source")
        source_counts = df_jobs["source"].value_counts()
        fig = px.pie(values=source_counts.values, names=source_counts.index, title="")
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Top In-Demand Skills")
    all_skills = []
    for job in jobs:
        all_skills.extend(job['skills_required'])
    skill_counts = pd.Series(all_skills).value_counts().head(10)
    
    fig = px.bar(x=skill_counts.values, y=skill_counts.index, orientation='h', title="")
    st.plotly_chart(fig, use_container_width=True)

# SKILL GAP PAGE
elif selected == "Skill Gap":
    st.title("🎯 Skill Gap Analyzer")
    st.markdown("See what skills you're missing and how to improve your matches.")
    
    if not st.session_state.profile:
        st.warning("Please complete your profile first on the Register Profile page.")
    else:
        user_skills = set(st.session_state.profile["skills"])
        jobs = get_mock_jobs()
        
        all_job_skills = []
        for job in jobs:
            all_job_skills.extend(job['skills_required'])
        demand_skills = pd.Series(all_job_skills).value_counts().head(15)
        
        missing_skills = []
        for skill in demand_skills.index:
            if skill not in user_skills:
                missing_skills.append({"skill": skill, "demand_count": demand_skills[skill]})
        
        df_missing = pd.DataFrame(missing_skills)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Your Skills vs Market Demand")
            fig = go.Figure(data=[
                go.Bar(name="Your Skills", x=list(user_skills)[:10], y=[1]*min(10, len(user_skills))),
                go.Bar(name="Market Demand", x=demand_skills.index[:10], y=demand_skills.values[:10])
            ])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🚀 Skills to Learn")
            for _, row in df_missing.head(8).iterrows():
                st.markdown(f"""
                <div style="background-color: #F3F4F6; border-radius: 10px; padding: 10px; margin-bottom: 8px;">
                    <strong>{row['skill']}</strong><br>
                    <span style="color: #2563EB;">Appears in {row['demand_count']} jobs</span><br>
                    <a href="https://www.coursera.org/search?query={row['skill']}" target="_blank">📚 Find courses →</a>
                </div>
                """, unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 CareerPulse | Your AI Job Hunting Assistant | Backend: " + BACKEND_URL)
