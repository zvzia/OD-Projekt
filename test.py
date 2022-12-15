import os
import smtplib
import ssl
from email.message import EmailMessage

def send_email(email_receiver, subject, body):
    try:
        email_sender = "appsafenotes@gmail.com"
        email_password = "fnqbxqqdvpqpnnno"
        
        if email_sender is None or email_password is None:
            # no email address or password
            # something is not configured properly
            print("Did you set email address and password correctly?")
            return False

        # create email
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg.set_content(body)

        context = ssl.create_default_context()
        # send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, msg.as_string())
        return True
    except Exception as e:
        print("Problem during send email")
        print(str(e))
    return False

send_email("gaik.zuza@gmail.com", "test", "gowno")