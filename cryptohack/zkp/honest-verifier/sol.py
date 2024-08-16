from pwn import *
import json
from math import gcd
from Crypto.Util.number import long_to_bytes

FLAG = "crypto{????????????????????????}"

# Diffie-Hellman group (512 bits)
# p = 2*q + 1 where p,q are both prime, and 2 modulo p generates a group of order q
p = 0x1ed344181da88cae8dc37a08feae447ba3da7f788d271953299e5f093df7aaca987c9f653ed7e43bad576cc5d22290f61f32680736be4144642f8bea6f5bf55ef
q = 0xf69a20c0ed4465746e1bd047f57223dd1ed3fbc46938ca994cf2f849efbd5654c3e4fb29f6bf21dd6abb662e911487b0f9934039b5f20a23217c5f537adfaaf7
g = 2


# w,y for the relation `g^w = y mod P` we want to prove knowledge of
# w = random.randint(0,q)
# y = pow(g,w,P)

conn = remote("socket.cryptohack.org", 13427)

print(conn.recvline())
l = conn.recvline()
print(l)

e = json.loads(l.decode()[:-1])["e"]
y = json.loads(l.decode()[:-1])["y"]

z = randint(1,p-1)
a = pow(g,z,p)*pow(pow(y,e,p),-1,p)

conn.sendline(json.dumps({"a": a, "z": z}))

print(conn.recvline())
