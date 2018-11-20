from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import os
import json
from base64 import b64encode, b64decode
BLOCK_SIZE = 16
PAD = '{'
s = {"data" : "hoc vien ky thuat mat ma"}
s = json.dumps(s)
s = s + PAD*(BLOCK_SIZE - len(s) % BLOCK_SIZE)
print(s)
key = os.urandom(BLOCK_SIZE)
print(key)
# cipher = AES.new(key)
# encrypt = b64encode(cipher.encrypt(s))
# print(encrypt.decode())
# decrypt = cipher.decrypt(b64decode(encrypt))
# print(decrypt.decode().rstrip(PAD))

bank_key_public = RSA.importKey(open('../Key_store/Bank_public.pem', 'rb').read())
digital_envelope = bank_key_public.encrypt(key, 32)
print(digital_envelope)
print(eval(str(digital_envelope)))