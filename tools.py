import requests
import os
from dotenv import load_dotenv
from agents import function_tool

import os
import asyncio
import smtplib
from email.message import EmailMessage

load_dotenv(override=True)

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")

pushover_url = "https://api.pushover.net/1/messages.json"

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


USE_EMAIL = EMAIL_ADDRESS and EMAIL_SMTP_SERVER and EMAIL_APP_PASSWORD


@function_tool
def send_email_tool(subject: str, text_body: str, html_body: str) -> str:
    """
    Send out an email with the given subject and body to all sales prospects
    
    Args:
        subject: The subject of the email
        text_body: The body of the email as plain text
        html_body: The HTML body of the email
    """
    result =  send_message(subject, text_body, html_body)
    return result


def send_message(subject, text_body, html_body) -> str:
   if USE_EMAIL:
    send_email(subject, text_body, html_body)
    return "Email sent"
   else:
    if not pushover_user or not pushover_token:
        return "Pushover credentials not configured"
    requests.post(
        pushover_url,
        data={
        "token": pushover_token, 
        "user": pushover_user, 
        "message": f"Subject: {subject}\n\n{text_body}"
        },
    )
    return "Push sent"




def send_email(subject, text_body, html_body):
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = subject
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(EMAIL_SMTP_SERVER, 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.send_message(msg)




 