from data_bese import *
from passlib.hash import sha256_crypt
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

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



        

