import socket, json
from threading import *
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from base64 import b64encode, b64decode
from time import sleep
import sys

RECV_BUFFER = 4096
HOST = '0.0.0.0'
PORT = 4000
HOST_BANK = '0.0.0.0'
PORT_BANK = 5000
PATH_KEY_PUBLIC = '../Key_store/'

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

def check(data):
    OIMD = SHA.new(data['OI'].encode()).hexdigest()
    POMD = OIMD + "$" + data['PIMD']
    POMD = SHA.new(POMD.encode())
    key = RSA.importKey(open(PATH_KEY_PUBLIC + "Client_public.pem", "rb").read())
    verifer = PKCS1_v1_5.new(key)
    return verifer.verify(POMD, b64decode(data['DS']))

def clientThead(conn, addr):
    print("[" + addr[0] + "]: connected")
    conn.send(b"Welcome to shop atoz!")
    message = conn.recv(RECV_BUFFER)
    if message:
        print('------------------------------------------------------')
        print('Request content:')
        data = json.loads(message)
        print(json.dumps(data, indent=4))
        print('------------------------------------------------------')
        payment_data = data['payment_data']
        check_order_data = check(data)
        if (check_order_data):
            print('Order information is valid: ', data['OI'])
            print('Waiting check the payment information from the bank...')
            print('------------------------------------------------------')
            sleep(5)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST_BANK, PORT_BANK))
            message_check_payment = json.dumps(payment_data).encode()
            client.send(message_check_payment)
            message_check_payment = client.recv(RECV_BUFFER)
            message_check_payment = json.loads(message_check_payment)
            print('Response from bank:')
            print(json.dumps(message_check_payment, indent=4))
            print('------------------------------------------------------')
            if message_check_payment['code']:
                print('Payment information is valid!')
                print('Ready to pay !!!')
            else:
                print('Payment information is invalid!')
            print('------------------------------------------------------')
            message_to_send = message_check_payment

        else:
            print('Purchase information is valid: ', data['OI'])
            message_to_send = {
                'message': 'Order infomation is invalid, something wrong :((',
                'code': False
            }
        conn.send(json.dumps(message_to_send).encode())
    else:
        conn.close()
        list_client.remove(conn)

while True:
    conn, addr = server.accept()
    list_client.append(conn)
    Thread(target=clientThead, args=(conn, addr,)).start()

server.close()