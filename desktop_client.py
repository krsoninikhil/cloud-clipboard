#!/bin/python3

# This script acts as client on desktop

import requests
import os
import subprocess

server_url = "https://cloudclipboard.herokuapp.com/"

def copy():  
    if os.name == "posix":
        p = subprocess.Popen(["xsel", "-o"], stdout=subprocess.PIPE)
        data = p.communicate()[0].decode("utf-8")
    elif os.name == "nt":
        data = None
    else:
        print("We don't yet support %s Operating System." % os.name)
        exit()
    return data

def upload():
    payload = {"data": copy()}
    res = requests.post(server_url+"copy", data=paylaod)
    if res.status_code == 200:
        print("Copied to Cloud-Clipboard.")
    else:
        print("Cannot copy to Cloud-Clipboard.")

def paste(data):
    p = subprocess.Popen(["xsel", "-bi"], stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE)
    p = p.communicate(data.encode("utf-8"))
    if p[1] is not None:
        print("Error in accessing local clipboard")

def download():
    res = requests.get(server_url+"paste")
    if res.status_code == 200:
        paste(res.text)
    else:
        print("Cannot download the data.")

print("Share you clipboard accross the devices.")

