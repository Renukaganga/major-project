# auth/login.py

import random
import smtplib
from email.message import EmailMessage
from db.mongodb import get_user

# Use a dedicated project email
SMTP_EMAIL = "22b01a1231@svecw.edu.in"
SMTP_PASSWORD = "rtlppursfnurmatr"

def send_otp(email):
    """
    Sends OTP to the given email and returns the OTP
    """
    otp = str(random.randint(100000, 999999))

    msg = EmailMessage()
    msg.set_content(f"Your OTP for Missing Child Finder login is: {otp}")
    msg["Subject"] = "Missing Child Finder - OTP Login"
    msg["From"] = SMTP_EMAIL
    msg["To"] = email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)

    return otp

def verify_user(email):
    """
    Checks if email is registered and returns role
    """
    user = get_user(email)
    if user:
        return user["role"]
    return None
