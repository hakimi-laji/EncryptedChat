# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
from Crypto.Cipher import AES
import random, string, base64

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# bind socket with inputted ip and port
#IP_address = '192.168.1.10'
#Port = 8081
IP_address = input('IP Address: ')
Port = input('Port: ')
server.connect((IP_address, Port)) 

while True: 

	# maintains a list of possible input streams 
    sockets_list = [sys.stdin, server] 

	# socket stuff, pls ignore
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048).decode('utf-8')
            if message[0] == 'W':
                print (message) 
            else:
                # decryption
                key = message[:32]
                iv = message[32:48]
                message = message[48:]
                decryption_suite = AES.new(key.encode('utf-8'), AES.MODE_CFB, iv.encode('utf-8'))
                plain_text = decryption_suite.decrypt(base64.b64decode(message))
                print('<Anonymous> ' + plain_text.decode('utf-8'))
                
                
        else: 
            messagetext = sys.stdin.readline()
            messageinput = messagetext.encode()

            # encryption
            key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32))
            iv = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
            enc_s = AES.new(key.encode('utf-8'), AES.MODE_CFB, iv.encode('utf-8'))
            cipher_text = enc_s.encrypt(messageinput)
            encoded_cipher_text = base64.b64encode(cipher_text)
            message = key + iv + encoded_cipher_text.decode('utf-8')

            server.send(message.encode('utf-8')) 
            sys.stdout.write("<You> " + messagetext) 
            sys.stdout.flush() 

server.close() 
