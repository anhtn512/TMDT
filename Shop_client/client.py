import socket


OI = input('Order infomation: ')
PI = input('Payment infomation: ')


RECV_BUFFER = 4096
HOST = "localhost"
PORT = 4000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))

while True:
    message = client.recv(RECV_BUFFER)
    print(message.decode())
    message = input('$$$: ')
    if message:
        client.send(message.encode())
    else:
        break
client.close()

