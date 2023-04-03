from pwn import *
import json
import hashpumpy

s = remote("socket.cryptohack.org", 13407)
s.recvline()

def bxor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def query(msg):
    data = {"option": "message",
            "data": msg.hex()}
    s.sendline(json.dumps(data))
    return json.loads(s.recvline().decode())["hash"]

flaglen = 46
querylen = 4 * flaglen  - 1
print(querylen)
md5pad = bytes.fromhex("80b805000000000000") # the 9 padding bytes
print(bytes(querylen))
h1 = query(bytes(querylen)) # H(s)
'''
h1 = hash of 46*n -1 bytes of flag + 9 padding bytes
'''
print(h1)
knownflag = b""

hashes = [query(bytes(querylen) + bxor(md5pad, b'}crypto{' + bytes([byte1])) + b"\x00") for byte1 in range(128)] # H(S + P + D) for random D
'''
hashes is an array of hashes of one of which will contain the hash of pre image of h1 + 1 null byte
'''

for byte2 in range(128):
    h = hashpumpy.hashpump(h1, 'a', bytes([byte2]), querylen-1)[0] 
    '''
    h extends h1 by 1 brute byte so we get the hash of pre image of h1 + 1 brute byte
    '''
    if h in hashes:
        firstbyte = bytes([hashes.index(h)])
        knownflag += bytes([byte2])
        print("sice")
        print(knownflag)
        break
