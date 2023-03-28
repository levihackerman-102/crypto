import md5py
from pwn import remote
import json

def bxor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def extend(h, l, a):
    if l%64 != 0:
        l += 64 - l%64
    val = h.decode("hex")
    ex = md5py.new("a"*l)
    ex.A, ex.B, ex.C, ex.D = md5py._bytelist2long(val)
    ex.update(a)
    return ex.hexdigest()

len = 46
n = 4

conn = remote('socket.cryptohack.org', '13407')
print(conn.recvline())

data = "00" * (n*len - 1)

x = '{' + f'"option" : "message", "data" : "{data}"' + '}'

print(x)

conn.sendline(x)

hash_json = conn.recvline().decode('utf-8')

json.loads(hash_json)

# hash of 46*n-1 length cyclic flag + padding (let this be S)
hash = json.loads(hash_json)['hash']
print(hash)

'''
To the server, we send 46*n-1 bytes of 00 + xor(b'}crypto{', first 8 bytes of the padding) + xor(9th byte of the padding, y), here y is a brute byte
if we get the same hash as above our brute of y is correct

padding = 1000 0000 + 8 bytes length field
'''
padding = "80"+"00000000000001B8" 

for i in range(256):
    to_send = "00" * (n*len - 1) 
    to_send +=  bxor(b'}crypto{', bytes.fromhex(padding[:16])).hex()
    to_send += bxor(bytes.fromhex(padding[-2:]), bytes([i])).hex()
    x = '{' + f'"option" : "message", "data" : "{to_send}"' + '}'
    conn.sendline(x)
    hash_json = conn.recvline().decode('utf-8')
    print(i, hash_json)
    if json.loads(hash_json)['hash'] == hash:
        print(i)
        break

'''
Now we know y, perform hash length extension attack to get the hash of S + x where x is a brute byte
if we get the same hash from the server our brute of x is correct and we move onto the next byte
'''
