from pwn import *
from Crypto.Util.number import *
import json
import codecs

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import math
import sympy

r = remote('socket.cryptohack.org', 13373)

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

r.recvuntil("Intercepted from Alice: ")
res = json_recv()
p = int(res["p"], 16)
g = int(res["g"], 16)
A = int(res["A"], 16)

r.recvuntil("Intercepted from Bob: ")
res = json_recv()

r.recvuntil("Intercepted from Alice: ")
res = json_recv()
iv = res["iv"]
ciphertext = res["encrypted"]

r.recvuntil("send him some parameters: ")
json_send({
    "p": hex(p),
    "g": hex(A),
    "A": hex(1)
    })

r.recvuntil("Bob says to you: ")
res = json_recv()
shared_secret = int(res["B"], 16)


def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

print(decrypt_flag(shared_secret, iv, ciphertext))

r.interactive()
