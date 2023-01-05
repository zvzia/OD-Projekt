from data_bese import *
import smtplib
import ssl
from email.message import EmailMessage
from time import sleep
from datetime import datetime, timedelta 
from uuid import uuid4

from services.services import *

def send_email(email_receiver, subject, body):
    try:
        email_sender = "appsafenotes@gmail.com"
        email_password = "fnqbxqqdvpqpnnno"
        
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

def generate_link(action, user_id):
    token = str(uuid4())
    insert_token(user_id, action, token)

    link = "https://127.0.0.1:5000/securityaction?action=" + action + "&token="+ token
    return link


def send_email_with_password_change_link(receiver_username):
    sleep(3)
    user_info = get_user_by_username(receiver_username)
    user_id = user_info[0]
    email = user_info[2]
    link = generate_link("changepassword", user_id)

    subject = "Password change"
    body = """
    Hello """ + receiver_username + """
    You requested password change, you can do it by clicking on this link:
    """ + link

    send_email(email, subject, body)

def send_email_if_new_device(receiver_username, device, location):
    sleep(3)
    user_info = get_user_by_username(receiver_username)
    email = user_info[2]
    user_id = user_info[0]
    link = generate_link("confirmlogin", user_id)
    link = link + "&device="+ device + "&location=" + location

    subject = "Unusual activity"
    body = """
    Hello """ + receiver_username + """
    There was unusual activity on your account.
    Someone logged in from """ + device + """ in """ + location + """.
    If this was you please confirm by clicking this link:
    """ + link

    send_email(email, subject, body)

def send_email_and_block_account_if_needed(username, device, location):
    sleep(3)
    user_id = get_user_by_username(username)[0]
    records = get_failed_login_by_userid(user_id)
    count = 0

    if( len(records) >= 5):
        for record in records:
            date_str = record[0]
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            if(date >= (datetime.now() - timedelta(minutes=10))):
                count += 1

    if (count >= 5):
        deactivate_account_by_username(username)

        user_info = get_user_by_username(username)
        email = user_info[2]

        link = generate_link("activateaccount", user_id)

        subject = "Unusual activity"
        body = """
        Hello """ + username + """
        Your account was temporary deactivated due to too many failed login attempts.
        You can activate your account by changing your password here:
        """ + link

        send_email(email, subject, body)