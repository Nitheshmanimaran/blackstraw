import smtplib
from email.mime.text import MIMEText

def send_test_email():
    smtp_address = "smtp.gmail.com"
    smtp_port = 587
    sender_login = "nithesh.kumar@blackstraw.ai"
    sender_password = "npcr lgni nors byst"
    sender_alias = "Great Expectations"
    receiver_emails = ["nithesh.kumar@blackstraw.ai"]

    msg = MIMEText("This is a test email from Great Expectations.")
    msg["Subject"] = "Test Email"
    msg["From"] = sender_alias
    msg["To"] = ", ".join(receiver_emails)

    try:
        with smtplib.SMTP(smtp_address, smtp_port) as server:
            server.starttls()
            server.login(sender_login, sender_password)
            server.sendmail(sender_login, receiver_emails, msg.as_string())
            print("Test email sent successfully.")
    except Exception as e:
        print(f"Failed to send test email: {e}")

if __name__ == "__main__":
    send_test_email()