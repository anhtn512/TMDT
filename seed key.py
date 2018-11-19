from Crypto.PublicKey import RSA
from Crypto import Random

#generate for Bank
random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()
print(private_key.exportKey(format='PEM'))
print(public_key.exportKey(format='PEM'))
with open ("Key_store/Bank_private.pem", "wb") as prv_file:
    prv_file.write(private_key.exportKey(format='PEM'))
    prv_file.close()
with open ("Key_store/Bank_public.pem", "wb") as pub_file:
    pub_file.write(public_key.exportKey(format='PEM'))
    pub_file.close()

#generate for Shop
random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()
print(private_key.exportKey(format='PEM'))
print(public_key.exportKey(format='PEM'))
with open ("Key_store/Shop_private.pem", "wb") as prv_file:
    prv_file.write(private_key.exportKey(format='PEM'))
    prv_file.close()
with open ("Key_store/Shop_public.pem", "wb") as pub_file:
    pub_file.write(public_key.exportKey(format='PEM'))
    pub_file.close()

#generate for client
random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()
print(private_key.exportKey(format='PEM'))
print(public_key.exportKey(format='PEM'))
with open ("Key_store/Client_private.pem", "wb") as prv_file:
    prv_file.write(private_key.exportKey(format='PEM'))
    prv_file.close()
with open ("Key_store/Client_public.pem", "wb") as pub_file:
    pub_file.write(public_key.exportKey(format='PEM'))
    pub_file.close()