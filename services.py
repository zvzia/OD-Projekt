from data_bese import *
from passlib.hash import sha256_crypt
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import smtplib
import ssl
from email.message import EmailMessage

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

