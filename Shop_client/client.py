import socket
from Crypto.Hash import SHA
from Crypto.Cipher import DES
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from base64 import b64encode, b64decode
import os


# OI = input('Order infomation: ')
# PI = input('Payment infomation: ')
OI = "2"
PI = "2"
OIMD = SHA.new(OI.encode())
PIMD = SHA.new(PI.encode())
POMD = OIMD.hexdigest() + "$" + PIMD.hexdigest()
POMD = SHA.new(POMD.encode())
# print(POMD)
key = RSA.importKey(open('Client_private.pem', 'rb').read())
signer = PKCS1_v1_5.new(key)
DS = signer.sign(POMD)
print(DS)
# key2 = RSA.importKey(open('Client_public.pem', 'rb').read())
# verifer = PKCS1_v1_5.new(key2)
# DS2 = verifer.verify(POMD, DS)
# print(DS2)


# key = os.urandom(16)
# iv = Random.get_random_bytes(8)
# des = DES.new(key, DES.MODE_CBC, iv)



# RECV_BUFFER = 4096
# HOST = "localhost"
# PORT = 4000
#
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((HOST,PORT))
#
# while True:
#     message = client.recv(RECV_BUFFER)
#     print(message.decode())
#     message = input('$$$: ')
#     if message:
#         client.send(message.encode())
#     else:
#         break
# client.close()

