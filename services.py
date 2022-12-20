from data_bese import *
from passlib.hash import sha256_crypt
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import smtplib
import ssl
from email.message import EmailMessage
from time import sleep
from user_agents import parse
from datetime import datetime

def hash_password(password):
    password_encrypted = sha256_crypt.hash(password)
    return password_encrypted

def chceck_if_user_exist(username):
    row = get_user_by_username(username)

    if row == None :
        return False
    else:
        return True

def nullpadding(data, length=16):
    return data + b"\x00"*(length-len(data) % length) 


def encrypt_note(note, password):
    key = PBKDF2(password, b"salt")
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    enc_note = cipher.encrypt(note.encode()) + nonce

    return enc_note

def decrypt_note(enc_note, password):
    key = PBKDF2(password, b"salt")

    nonce = enc_note[-16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    dec_text = cipher.decrypt(enc_note[:-16])

    return dec_text.decode()

def send_email_with_password_change_link(receiver_username):
    user_info = get_user_by_username(receiver_username)
    email = user_info[2]
    link = generate_password_change_link()

    subject = "Password change"
    body = """
    Hello """ + receiver_username + """
    You requested password change, you can do it by clicking on this link:
    """ + link

    send_email(email, subject, body)


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

def generate_password_change_link():
    return "link"

# def get_reset_token(self, expires=500):
#     return jwt.encode({'reset_password': self.username,
#                         'exp':    time() + expires},
#                         key=os.getenv('SECRET_KEY_FLASK'))

# def verify_reset_token(token):
#         try:
#             username = jwt.decode(token,
#               key=os.getenv('SECRET_KEY_FLASK'))['reset_password']
#         except Exception as e:
#             print(e)
#             return
#         return User.query.filter_by(username=username).first()

def get_location_info(ip, simple_geoip):
    sleep(2)
    geoip_data = simple_geoip.get_geoip_data(ip)
    country = geoip_data['location']['country']

    if country != 'ZZ':
        city = geoip_data['location']['city']
    else:
        country = 'unknown'
        city = 'unknown'

    location = city + ", " + country
    return location

def get_device(ua):
    user_agent = parse(ua)
    device = str(user_agent)
    return device

def send_email_if_new_device(receiver_username, device, location):
    user_info = get_user_by_username(receiver_username)
    email = user_info[2]
    user_id = user_info[0]
    #link = generate_confiramtion_link()

    subject = "Unusual activity"
    body = """
    Hello """ + receiver_username + """
    There was unusual activity on your account.
    Someone logged in from """ + device + """ in """ + location + """.
    If this was you please confirm by clicking this link:
    """ #+ link

    send_email(email, subject, body)

def send_email_and_block_account_if_needed(username, device, location):
    user_id = get_user_by_username(username)[0]
    records = get_failed_login_by_userid(user_id)

    if( records.len() >= 5):
        count = 0
        for record in records:
            date_str = record[0]
            date = datetime.strptime(date_str, '%y/%m/%d %H:%M:%S')
            if(date >= (datetime.now() - datetime.timedelta(minutes=10))):
                coun += 1

    if (count >= 5):
        deactivate_account_by_username(username)

        user_info = get_user_by_username(username)
        email = user_info[2]

        #link = generate_activation_link()

        subject = "Unusual activity"
        body = """
        Hello """ + username + """
        Your account was temporary deactivated due to too many failed login attempts.
        You can change your password and activate your account here:
        """ #+ link

        send_email(email, subject, body)