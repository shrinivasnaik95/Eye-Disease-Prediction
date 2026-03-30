import os
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_APP_PASSWORD = os.getenv("SENDER_APP_PASSWORD")

def _send_email_sync(to_email: str, subject: str, plain_text: str, html_text: str = None):
    """Send an email synchronously."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    # Attach plain text and HTML
    msg.attach(MIMEText(plain_text, "plain"))
    if html_text:
        msg.attach(MIMEText(html_text, "html"))

    # Connect to Gmail SMTP and send
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
        server.send_message(msg)

def send_recommendation_email_async(to_email: str, subject: str, recommendation_text: str, user_name: str = None, wait: bool = False):
    """
    Send email asynchronously in a background thread.
    
    Args:
        to_email: recipient email
        subject: email subject
        recommendation_text: email body
        user_name: optional recipient name
        wait: if True, wait for email to be sent (useful for testing)
    """
    greeting = f"Hello {user_name}," if user_name else "Hello,"
    
    plain = f"""{greeting}

Our OCT model predicted a retinal condition for the image you uploaded.

Recommendation:
{recommendation_text}

If you have questions, reply to this email.

Best,
Your OCT Team
"""
    # Convert Markdown-style formatting (*bold*) to HTML
# Convert Markdown-style formatting (*bold*) to HTML
    formatted_recommendation = (
        recommendation_text
        .replace("", "<b>").replace("*", "")
        .replace("\n", "<br>")
        .replace("-", "•")  # converts dashes to bullet dots
    )

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <p>{greeting}</p>
        <p>Our OCT model predicted a retinal condition for the image you uploaded.</p>
        <h3 style="color: #2E86C1;">Recommendation</h3>
        <p>{formatted_recommendation}</p>
        <hr>
        <p>Best,<br><b>Your OCT Team</b></p>
      </body>
    </html>
    """

    thread = threading.Thread(
        target=_send_email_sync,
        args=(to_email, subject, plain, html),
        daemon=True
    )
    thread.start()

    if wait:
        thread.join() 
    return thread