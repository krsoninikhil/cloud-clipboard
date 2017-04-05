#!/usr/bin/env python3

# This script acts as desktop client

import requests
import os
import sys
import subprocess

server_url = "https://cloudcb.herokuapp.com/" # "http://localhost:8000/"

def copy():
    """
    Returns the current text on clipboard.
    """
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
    """
    Sends the copied text to server.
    """
    payload = {"text": copy(), "device": ""}
    res = requests.put(
        server_url+"copy-paste/",
        data = payload,
        auth = ('nik', 'nik#RA.1')
    )
    if res.status_code == 200:
        print("Succeses! Copied to Cloud-Clipboard.")
    else:
        print("Error:", res.text)

def paste(data):
    """
    Copies 'data' to local clipboard which enables pasting.
    """
    p = subprocess.Popen(["xsel", "-bi"], stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE)
    p = p.communicate(data.encode("utf-8"))
    if p[1] is not None:
        print("Error in accessing local clipboard")

def download():
    """
    Downloads from server and updates the local clipboard.
    """
    res = requests.get(server_url+"copy-paste/", auth=('nik', 'nik#RA.1'))
    if res.status_code == 200:
        paste(res.text)
    else:
        print("Cannot download the data.")

def usage():
    print("Error: Unknown argument")
    print("Usage: ccb.py copy|paste")
    

if __name__ == "__main__":
    #print("Cloud Clipboard -- Share you clipboard accross the devices.")
    if len(sys.argv) == 2:
        if sys.argv[1] == "copy":
            upload()
        elif sys.argv[1] == "paste":
            download()
        else:
            usage()
    else:
        usage()
