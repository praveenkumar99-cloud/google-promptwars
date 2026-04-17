from google.auth import default
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

def send_job_email(to_email, jobs):
    try:
        credentials, project = default()
        service = build('gmail', 'v1', credentials=credentials)
        message = MIMEMultipart('alternative')
        message['to'] = to_email
        message['subject'] = "🔥 Your Daily Job Matches from CareerPulse"
        html = f"""
        <html>
        <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            .high {{ color: green; font-weight: bold; }}
            .medium {{ color: orange; }}
            .low {{ color: red; }}
        </style>
        </head>
        <body>
        <h2>🎯 Your Personalized Job Matches</h2>
        <p>Here are your top {{len(jobs)}} job matches based on your skills:</p>
        <table>
        <tr><th>Job Title</th><th>Company</th><th>Match Score</th><th>Skills Matched</th><th>Apply</th></tr>
        """
        for _, job in jobs.iterrows():
            score = job['match_score']
            score_class = "high" if score >= 70 else "medium" if score >= 40 else "low"
            matched_skills = job.get('matched_skills', [])
            skills_str = ", ".join(matched_skills[:3])
            html += f"""
            <tr>
                <td>{{job['title']}}</td>
                <td>{{job['company']}}</td>
                <td class="{{score_class}}">{{score}}%</td>
                <td>{{skills_str}}</td>
                <td><a href="{{job['url']}}" target="_blank">Apply →</a></td>
            </tr>
            """
        html += "</table><br><p>💡 Pro Tip: Update your skills profile to get better matches!</p><hr><p style='color:#666;font-size:12px;'>CareerPulse - Your AI Job Assistant</p></body></html>"
        part = MIMEText(html, 'html')
        message.attach(part)
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = {'raw': encoded_message}
        service.users().messages().send(userId='me', body=send_message).execute()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False
