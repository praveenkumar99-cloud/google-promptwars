import pandas as pd

def calculate_match_score(job_description, job_title, user_skills):
    if not user_skills:
        return 0, []
    text = (str(job_description) + " " + str(job_title)).lower()
    matched_skills = []
    for skill in user_skills:
        if skill.lower() in text:
            matched_skills.append(skill)
    score = (len(matched_skills) / len(user_skills)) * 100
    return round(score, 1), matched_skills

def filter_and_sort_jobs(jobs_df, user_skills, min_score=20):
    if jobs_df.empty or not user_skills:
        return pd.DataFrame()
    scores = []
    matched_skills_list = []
    for _, job in jobs_df.iterrows():
        score, matched = calculate_match_score(job['description'], job['title'], user_skills)
        scores.append(score)
        matched_skills_list.append(matched)
    jobs_df['match_score'] = scores
    jobs_df['matched_skills'] = matched_skills_list
    filtered = jobs_df[jobs_df['match_score'] >= min_score]
    return filtered.sort_values('match_score', ascending=False).head(10)
