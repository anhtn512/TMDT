import socket, json, sys
from threading import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from base64 import b64encode, b64decode

BLOCK_SIZE = 16
RECV_BUFFER = 4096
HOST = '0.0.0.0'
PORT = 5000
PATH_KEY_PUBLIC = '../Key_store/'

def encryptAES(key, msg):
    PAD = '#'
    msg = msg + PAD * (BLOCK_SIZE - len(msg) % BLOCK_SIZE)
    cipher = AES.new(key)
    return b64encode(cipher.encrypt(msg)).decode()

def decryptAES(key, msg):
    PAD = '#'
    cipher = AES.new(key)
    return cipher.decrypt(b64decode(msg)).decode().rstrip(PAD)

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
    bank_key_private = RSA.importKey(open('Bank_private.pem', 'rb').read())
    keyAES = bank_key_private.decrypt(eval(data['digital_envelope']))
    payment_data = decryptAES(keyAES, data['payment_encrypt'])
    payment_data = json.loads(payment_data)
    print('Payment infomation:')
    print(json.dumps(payment_data, indent=4))
    PIMD = SHA.new(payment_data['PI'].encode()).hexdigest()
    POMD = payment_data['OIMD'] + "$" + PIMD
    POMD = SHA.new(POMD.encode())
    key = RSA.importKey(open(PATH_KEY_PUBLIC + "Client_public.pem", "rb").read())
    verifer = PKCS1_v1_5.new(key)
    if verifer.verify(POMD, b64decode(payment_data['DS'])):
        return payment_data['PI']
    return False

def clientThead(conn, addr):
    message = conn.recv(RECV_BUFFER)
    print("[" + addr[0] + "]: connected")
    if message:
        print('Request content:')
        data = json.loads(message)
        print(json.dumps(data, indent=4))
        check_payment_data = check(data)
        if check_payment_data:
            print('Payment information is valid: ', check_payment_data)
            message_to_send = {
                'message': 'All infomation is valid, ready to pay',
                'code': True
            }
        else:
            print('Payment information is invalid')
            message_to_send = {
                'message': 'Payment infomation is invalid, something wrong :((',
                'code': False
            }

        conn.send(json.dumps(message_to_send).encode())
    else:
        conn.close()
        list_client.remove(conn)

while True:
    conn, addr = server.accept()
    list_client.append(conn)
    print(addr[0] + ' connected')
    Thread(target=clientThead, args=(conn, addr,)).start()

server.close()