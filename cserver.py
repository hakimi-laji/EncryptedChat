# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
from _thread import *
from Crypto.Cipher import AES
import random, string, base64

# socket stuffs
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# bind socket with inputted ip and port
#IP_address = '192.168.1.10'
#Port = 8081
IP_address = input('IP Address: ')
Port = input('Port: ')
Port = int(Port)
server.bind((IP_address, Port)) 

# listens for 100 active connections. This number can be increased as per convenience. 
server.listen(100) 
print ("Server online. Waiting for connections...")

list_of_clients = [] 

def clientthread(conn, addr): 

	# sends a message to the client whose user object is conn 
	conn.send("Welcome to the secured chatroom. Press CTRL+C to exit anytime. Have fun!".encode('utf-8')) 

	while True: 
			try: 
				message = conn.recv(2048).decode('utf-8')
				if message: 

					# prints the message and address
					print ("<" + addr[0] + "> " + message[48:]) 

					# Calls broadcast function to send message to all 
					#message_to_send = "<" + addr[0] + "> " + message 
					broadcast(message, conn) 

				else: 
					# message may have no content if the connection is broken, in this case we remove the connection
					remove(conn) 

			except: 
				continue

# broadcast message to all active clients
def broadcast(message, connection): 
	for clients in list_of_clients: 
		if clients!=connection: 
			try: 
				clients.send(message.encode('utf-8')) 
			except: 
				clients.close() 

				# if the link is broken, we remove the client 
				remove(clients) 

# removes the object from the list that was created at the beginning of the program
def remove(connection): 
	if connection in list_of_clients: 
		list_of_clients.remove(connection) 

while True: 

	# Accepts a connection request 
	conn, addr = server.accept() 

	# Maintains a list of clients for ease of broadcasting 
	list_of_clients.append(conn) 

	# prints the address of the user that just connected 
	print (addr[0] + " connected") 

	# creates and individual thread for every user 
	# that connects 
	start_new_thread(clientthread,(conn,addr)) 

conn.close() 
server.close() 