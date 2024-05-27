

# This file was *autogenerated* from the file sol.sage
from sage.all_cmdline import *   # import sage library

_sage_const_13322168333598193507807385110954579994440518298037390249219367653433362879385570348589112466639563190026187881314341273227495066439490025867330585397455471 = Integer(13322168333598193507807385110954579994440518298037390249219367653433362879385570348589112466639563190026187881314341273227495066439490025867330585397455471); _sage_const_30 = Integer(30); _sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_128 = Integer(128); _sage_const_16 = Integer(16)
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.number import *
from Crypto.Util.Padding import pad, unpad

import json


FLAG = b'crypto{?????????????????????????????????????}'

P = _sage_const_13322168333598193507807385110954579994440518298037390249219367653433362879385570348589112466639563190026187881314341273227495066439490025867330585397455471 
N = _sage_const_30 

def load_matrix(fname):
    data = open(fname, 'r').read().strip()
    rows = [list(map(int, row.split(' '))) for row in data.splitlines()]
    return Matrix(GF(P), rows)

G = load_matrix("generator.txt")
g, p = G.jordan_form(transformation=True)

f1 = open('output.txt', 'r')
dh = json.loads(f1.readline())
v = vector(GF(P), dh['v'])
w = vector(GF(P), dh['w'])

a = p.inverse() * v
b = p.inverse() * w 
theta = g[N - _sage_const_2 ][N - _sage_const_2 ]

# Solution to dlog
SECRET = theta * (b[N - _sage_const_2 ] - (a[N - _sage_const_2 ] * b[N - _sage_const_1 ]) / a[N - _sage_const_1 ]) / b[N - _sage_const_1 ]
KEY_LENGTH = _sage_const_128 
KEY = SHA256.new(data=str(SECRET).encode()).digest()[:KEY_LENGTH]

ct = open('flag.enc', 'r')
enc_flag = json.loads(ct.readline())
iv = bytes.fromhex(enc_flag['iv'])
ciphertext = bytes.fromhex(enc_flag['ciphertext'])

cipher = AES.new(KEY, AES.MODE_CBC, iv)
print(unpad(cipher.decrypt(ciphertext), _sage_const_16 ))

