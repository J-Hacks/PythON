# Email Scheduler
import smtplib
import schedule
import time

def send_email():
    sender_email = "your_email@gmail.com"
    receiver_email = "recipient_email@gmail.com"
    password = "your_email_password"

    subject = "Automated Email"
    body = "This is an automated email sent using Python."

    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

# Schedule the email to be sent daily at 8 AM
schedule.every().day.at("08:00").do(send_email)

while True:
    schedule.run_pending()
    time.sleep(1)

