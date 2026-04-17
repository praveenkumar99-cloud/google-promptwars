from fastapi import FastAPI, BackgroundTasks
from datetime import date
from storage import get_all_users, get_user_profile, save_jobs_for_user
from job_fetcher import fetch_all_jobs
from job_matcher import filter_and_sort_jobs
from gmail_sender import send_job_email

app = FastAPI(title="CareerPulse Job Agent")

@app.get("/")
def root():
    return {"message": "CareerPulse Job Agent is running", "status": "healthy"}

@app.get("/daily-job")
def daily_job_processor(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_all_users)
    return {"status": "processing", "message": "Job recommendations being sent"}

def process_all_users():
    users = get_all_users()
    if not users:
        return
    all_jobs = fetch_all_jobs()
    if all_jobs.empty:
        return
    for email in users:
        profile = get_user_profile(email)
        if not profile:
            continue
        skills = profile.get('skills', [])
        matched = filter_and_sort_jobs(all_jobs, skills)
        if matched.empty:
            continue
        save_jobs_for_user(email, matched.to_dict('records'), str(date.today()))
        send_job_email(email, matched)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
