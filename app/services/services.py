from data_bese import *
from passlib.hash import sha256_crypt
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

import re

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

def checkpasswordrequirements(password):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

    if(len(password)<10):
        return False
    elif(bool(re.match(r'\w*[A-Z]\w*', password)) == False):
        return False
    elif(bool(re.match(r'\w*[a-z]\w*', password)) == False):
        return False
    elif(bool(re.match(r'\w*[0-9]\w*', password)) == False):
        return False
    elif(regex.search(password) == None):
        return False
    else:
        return True
        

