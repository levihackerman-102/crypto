import md5py
import struct
from string import printable
import json
from pwn import remote, xor
from tqdm import tqdm

flag_len = 46
r = remote("socket.cryptohack.org", 13407)
r.recv()

def bxor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def pad(s):
	padlen = 64 - ((len(s) + 8) % 64)
	bit_len = 8*len(s)
	if(padlen < 64):
		s += '\x80' + '\000' * (padlen - 1)
	return s + struct.pack('<q', bit_len)

def extend(h, l, a):
    if l%64 != 0:
        l += 64 - l%64
    val = h.decode("hex")
    ex = md5py.new("a"*l)
    ex.A, ex.B, ex.C, ex.D = md5py._bytelist2long(val)
    ex.update(a)
    return ex.hexdigest()

padding = "\x80\xb8\x05\x00\x00\x00\x00\x00\x00"
known = "}crypto{i" 

r.sendline(json.dumps({"option": "message", "data": "00"*183}))
h = json.loads(r.recvline().strip())["hash"]
print (h)

cache = {}

for c in printable:
    ex = extend(h, 183, c)
    cache[ex] = c

flag = "_"
while True:
    print ("flag: crypto{i%s"%flag)
    
    if flag[-1] == "}":
        break
    
    payload = "00"*183 + xor(known, padding).encode("hex") + "00"*(len(flag) + 1)
    r.sendline(json.dumps({"option": "message", "data": payload}))
    k = json.loads(r.recvline().strip())["hash"]
    for c in printable:
        if extend(h, 183, flag+c) == k:
            flag += c
            break
