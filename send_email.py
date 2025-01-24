import os
import smtplib
from email.message import EmailMessage
# from pathlib import Path
from dotenv import load_dotenv

PORT = 465  # For SSL
EMAIL_SERVER = "smtp.gmail.com"

# Load the environment variables
# current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
# envars = current_dir / ".env"
# envars = "/home/aloo/Desktop/mini project/auto-email/.env"  
# load_dotenv(envars)

# Read environment variables
sender_email ="srwat04@gmail.com"
password_email ="kejc uzxc swzy djkz"

print(f"Sender Email: {sender_email}")
print(f"Password: {password_email}")

def send_email(subject, receiver_email, name, due_date, invoice_no, amount):
    # Create the base text message.
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    msg.set_content(
        f"""\
        Hi {name},
        I hope you are well.
        I just wanted to drop you a quick note to remind you that {amount} INR in respect of our invoice {invoice_no} is due for payment on {due_date}.
        I would be really grateful if you could confirm that everything is on track for payment.
        Best regards
        Alankrit Dabral
        """
    )

    # Connect to the server and send the email
    with smtplib.SMTP_SSL(EMAIL_SERVER, PORT) as server:
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())

if __name__ == "__main__":
    send_email(
        subject="Invoice Reminder",
        name="Sarthak",
        receiver_email="srthkrajvanshi@gmail.com",
        due_date="20, JUL 2024",
        invoice_no="INV-21-12-009",
        amount="5",
    )
