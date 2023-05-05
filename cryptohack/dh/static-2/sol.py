from pwn import *
from Crypto.Util.number import *
import json
import codecs
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import math
import sympy

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

def json_recv():
    line = remote.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    remote.sendline(request)

remote = remote('socket.cryptohack.org', 13378)

remote.recvuntil("Intercepted from Alice: ")
res = json_recv()
p = int(res["p"], 16)
g = int(res["g"], 16)
A = int(res["A"], 16)

remote.recvuntil("Intercepted from Bob: ")
res = json_recv()
B = int(res["B"], 16)

remote.recvuntil("Intercepted from Alice: ")
res = json_recv()
iv = res["iv"]
ciphertext = res["encrypted"]

def smooth_p():
    mul = 1
    i = 1
    while 1:
        mul *= i
        if (mul + 1).bit_length() >= 1536 and isPrime(mul + 1):
            return mul + 1
        i += 1

s_p = smooth_p()
remote.recvuntil("send him some parameters: ")
json_send({
    "p": hex(s_p),
    "g": hex(2),
    "A": hex(A)
    })

remote.recvuntil("Bob says to you: ")
res = json_recv()
B = int(res["B"], 16)
print("Running little step giant step")
b = sympy.ntheory.residue_ntheory.discrete_log(s_p, B, 2)

shared_secret = pow(A,b,p)

print(decrypt_flag(shared_secret, iv, ciphertext))
