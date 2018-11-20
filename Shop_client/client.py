import socket, json, os
from base64 import b64encode, b64decode
from Crypto.Hash import SHA
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

BLOCK_SIZE = 16
RECV_BUFFER = 4096
HOST = "localhost"
PORT = 4000

def encryptAES(key, msg):
    PAD = '#'
    msg = msg + PAD * (BLOCK_SIZE - len(msg) % BLOCK_SIZE)
    cipher = AES.new(key)
    return b64encode(cipher.encrypt(msg)).decode()

def decryptAES(key, msg):
    PAD = '#'
    cipher = AES.new(key)
    return cipher.decrypt(b64decode(msg)).decode().rstrip(PAD)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))
message = client.recv(RECV_BUFFER)
print(message.decode())

OI = input('Order infomation: ')
PI = input('Payment infomation: ')
# OI = "2"
# PI = "2"
OIMD = SHA.new(OI.encode()).hexdigest()
PIMD = SHA.new(PI.encode()).hexdigest()
POMD = OIMD + "$" + PIMD
POMD = SHA.new(POMD.encode())
client_key_private = RSA.importKey(open('Client_private.pem', 'rb').read())
signer = PKCS1_v1_5.new(client_key_private)
DS = b64encode(signer.sign(POMD)).decode()

payment_data = {
    "PI": PI,
    "OIMD": OIMD,
    "DS": DS
}
# print(payment_data)

payment_data = json.dumps(payment_data)
keyAES = os.urandom(BLOCK_SIZE)
payment_encrypt = encryptAES(keyAES,payment_data)
bank_key_public = RSA.importKey(open('../Key_store/Bank_public.pem', 'rb').read())
digital_envelope = str(bank_key_public.encrypt(keyAES, 32))

request_message = {
    "payment_data": {
        "payment_encrypt": payment_encrypt,
        "digital_envelope": digital_envelope
    },
    "PIMD": PIMD,
    "OI": OI,
    "DS": DS
}

# print(json.dumps(request_message, indent=4))
print("initialize request message to shop done. sending....")


# Test verify DS
# key2 = RSA.importKey(open('Client_public.pem', 'rb').read())
# verifer = PKCS1_v1_5.new(key2)
# print(DS)
# DS2 = verifer.verify(POMD, b64decode(DS))
# print(DS2)

# test decrypt payment data
# bank_key_private = RSA.importKey(open('../Key_store/Bank_private.pem', 'rb').read())
# keyAES2 = bank_key_private.decrypt(eval(digital_envelope))
# print(keyAES2)
# payment_data2 = AES.new(keyAES2).decrypt(b64decode(payment_encrypt))
# print(json.loads(decryptAES(keyAES2, payment_encrypt)))

message = json.dumps(request_message)
client.send(message.encode())
message = client.recv(RECV_BUFFER)
data = json.loads(message)
print('Response content:')
print(json.dumps(data, indent=4))

client.close()
#
