from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pwn import xor
from string import printable
from itertools import product
from tqdm import tqdm

with open("public/output.txt") as f:
    ct = f.read().strip()
    
ct = b64decode(ct)

print(ct)

key = ct[:16]
ct = ct[16:]

def backtrack(m5):
    c5 = ct[-16:]
    x5 =  xor(c5, m5)
    x4 = AES.new(key, AES.MODE_ECB).decrypt(x5)
    x3 = AES.new(key, AES.MODE_ECB).decrypt(x4)
    x2 = AES.new(key, AES.MODE_ECB).decrypt(x3)
    x1 = AES.new(key, AES.MODE_ECB).decrypt(x2)
    x0 = AES.new(key, AES.MODE_ECB).decrypt(x1)
    iv = x0
    flag = AES.new(key, AES.MODE_OFB, iv).decrypt(ct)
    if b"firebird" in flag:
        print(flag)
        return True
    return False

brutset = printable[:62]

# m5 is of the form ??}XX..X so we can bruteforce the last 3 characters of the flag
for i in tqdm(product(brutset, repeat=3)):
    m5 = ''.join(i).encode() + b'}' + b'\x0c'*12
    if backtrack(m5):
        break
