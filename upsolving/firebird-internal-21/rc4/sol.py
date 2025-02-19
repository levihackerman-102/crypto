# Lines 16-17, chall.py
def convert_key(s):
    return [ord(c) for c in s]

# Lines 23-34, rc4.py
def KSA(key):
    keylength = len(key)

    # In Python 3, `range` returns an iterator instead of a list...
    S = list(range(256))

    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % keylength]) % 256
        S[i], S[j] = S[j], S[i]  # swap

    return S

from pwn import *
from pwnlib.util.packing import p32

r = remote('darkness', 50004)
key1 = r.recvline()[5:].strip(b'\n')
print(key1)
keysched1 = KSA(key1)

import unicodedata
from tqdm import tqdm

def gen_key2():
    print(r.recvuntil('🔑 '))
    for codepoint in tqdm(range(256, 0x11000)):
        char = chr(codepoint)
        if unicodedata.category(char)[0] == "C":  # Exclude control characters
            continue
        key2 = list(key1[:-1])
        key2.append(ord(chr(codepoint)))
        if key2 == key1:
            continue
        # print(key2)
        if KSA(key2) == keysched1:
            print(f"Found key2: {key2}")
            key2 = ''.join(chr(c) for c in key2)
            r.sendline(key2)
            print(r.recvline())
            return
        else:
            continue
gen_key2()
# print(gen_key2())
