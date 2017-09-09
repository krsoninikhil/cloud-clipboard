#!/Usr/bin/env python3

# This script acts as desktop client

import os
import sys
import json
import subprocess
import requests
import pyperclip

server_url = "https://cloudcb.herokuapp.com/"
#server_url =  "http://localhost:8000/"

def copy():
    """
    Returns the current text on clipboard.
    """
    data = pyperclip.paste()
    ## before using pyperclip
    # if os.name == "posix":
    #     p = subprocess.Popen(["xsel", "-bo"], stdout=subprocess.PIPE)
    #     data = p.communicate()[0].decode("utf-8")
    # elif os.name == "nt":
    #     data = None
    # else:
    #     print("We don't yet support %s Operating System." % os.name)
    #     exit()
    return data

def upload(username, password):
    """
    Sends the copied text to server.
    """
    payload = {"text": copy(), "device": ""}
    res = requests.post(
        server_url+"copy-paste/",
        data = payload,
        auth = (username, password)
    )
    if res.status_code == 200:
        print("Succeses! Copied to Cloud-Clipboard.")
    else:
        print("Error: ", res.text)

def paste(data):
    """
    Copies 'data' to local clipboard which enables pasting.
    """
    # p = subprocess.Popen(["xsel", "-bi"], stdout=subprocess.PIPE,
    #                      stdin=subprocess.PIPE)
    # p = p.communicate(data.encode("utf-8"))
    # if p[1] is not None:
    #     print("Error in accessing local clipboard")
    pyperclip.copy(data)

def download(username, password):
    """
    Downloads from server and updates the local clipboard.
    """
    res = requests.get(server_url+"copy-paste/", auth=(username, password))
    if res.status_code == 200:
        paste(json.loads(res.text)["text"])
    else:
        print("Cannot download the data.")

def register(username, password):
    """
    To let user register.
    """
    payload = {"username": username, "password": password}
    res = requests.post(server_url+"register/", data=payload)
    if res.status_code == 201:
        print("Hi %s! You are all set." % username)
    else:
        print("Error: ", res.text)

def usage():
    print("Error: Unknown argument")
    print("Usage: cloudcb.py copy|paste|register <email> <password>")
    

if __name__ == "__main__":
    #print("Cloud Clipboard -- Share you clipboard accross the devices.")
    if len(sys.argv) == 4:
        username = sys.argv[2]
        password = sys.argv[3]
        if sys.argv[1] == "copy":
            upload(username, password)
        elif sys.argv[1] == "paste":
            download(username, password)
        elif sys.argv[1] == "register":
            register(username, password)
        else:
            usage()
    else:
        usage()
