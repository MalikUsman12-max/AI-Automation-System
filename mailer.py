import smtplib
import ssl
import os
import time
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import List, Optional, Tuple, Dict, Any

def test_smtp_connection(email_address: str, app_password: str) -> Tuple[bool, str]:
    """
    Tests Gmail SMTP authentication by connecting and logging in.
    Does not send an email.
    """
    clean_email = email_address.strip()
    clean_pwd = app_password.strip().replace(" ", "")
    
    if not clean_email or not clean_pwd:
        return False, "Email address and App Password cannot be empty."
        
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=12) as server:
            server.login(clean_email, clean_pwd)
        return True, "Successfully authenticated with Gmail SMTP!"
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Please verify your Gmail address and 16-character Google App Password."
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def send_test_email(email_address: str, app_password: str) -> Tuple[bool, str]:
    """
    Sends a test verification email to the user's own address.
    """
    clean_email = email_address.strip()
    clean_pwd = app_password.strip().replace(" ", "")
    
    msg = MIMEMultipart()
    msg['From'] = clean_email
    msg['To'] = clean_email
    msg['Subject'] = "[Test] CSC Outreach Bot Connection Verified"
    
    body = (
        "Hello!\n\n"
        "This is an automated test from your CSC Outreach Agent running on your local machine.\n"
        "Your Gmail credentials and SMTP connection are working perfectly.\n\n"
        "You are now ready to schedule and send personalized scholarship outreach emails!"
    )
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=15) as server:
            server.login(clean_email, clean_pwd)
            server.sendmail(clean_email, clean_email, msg.as_string())
        return True, "Test email sent successfully! Please check your inbox."
    except Exception as e:
        return False, f"Failed to send test email: {str(e)}"

def send_single_outreach(
    sender_email: str,
    app_password: str,
    recipient_email: str,
    subject: str,
    body: str,
    attachment_paths: Optional[List[str]] = None
) -> Tuple[bool, str]:
    """
    Sends a single email with optional attachments (CV, Transcripts).
    """
    clean_sender = sender_email.strip()
    clean_pwd = app_password.strip().replace(" ", "")
    clean_recipient = recipient_email.strip()
    
    msg = MIMEMultipart()
    msg['From'] = clean_sender
    msg['To'] = clean_recipient
    msg['Subject'] = subject
    
    # Body
    msg.attach(MIMEText(body, 'plain'))
    
    # Attachments
    if attachment_paths:
        for fpath in attachment_paths:
            if fpath and os.path.exists(fpath):
                try:
                    with open(fpath, "rb") as f:
                        part = MIMEApplication(f.read(), Name=os.path.basename(fpath))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(fpath)}"'
                    msg.attach(part)
                except Exception as ex:
                    print(f"Warning: Could not attach file {fpath}: {ex}")
                    
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=20) as server:
            server.login(clean_sender, clean_pwd)
            server.sendmail(clean_sender, clean_recipient, msg.as_string())
        return True, "Email successfully delivered."
    except Exception as e:
        return False, f"SMTP Error: {str(e)}"
