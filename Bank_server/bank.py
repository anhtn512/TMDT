import socket
from threading import *
import sys

RECV_BUFFER = 4096
HOST = '0.0.0.0'
PORT = 5000

#config server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server.bind((HOST, PORT))
except:
    print ('Bind fail. Somwething was wrong :))')
    sys.exit()
server.listen(10)
print('Server listening in port ' + str(PORT))
list_client = []

def clientThead(conn, addr):
    conn.send(b"Welcome to shop atoz!")
    while True:
        try:
            message = conn.recv(RECV_BUFFER)
            if message:
                print ("<" + addr[0] + "> " + message.decode())
                message_to_send = "<" + addr[0] + "> " + message.decode()
                conn.send(message_to_send.encode())
            else:
                conn.close()
                list_client.remove(conn)
        except:
            print('ahihi')
            continue

while True:
    conn, addr = server.accept()
    list_client.append(conn)
    print(addr[0] + ' connected')
    Thread(target=clientThead, args=(conn, addr,)).start()

server.close()