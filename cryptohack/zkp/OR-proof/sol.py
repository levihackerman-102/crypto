import random
from params import p, q, g
import os
from pwn import *

# w,y for the relation `g^w = y mod p` we want to prove knowledge of
# w = random.randint(0,q)
# y = pow(g,w,p)
w0 = 0x5a0f15a6a725003c3f65238d5f8ae4641f6bf07ebf349705b7f1feda2c2b051475e33f6747f4c8dc13cd63b9dd9f0d0dd87e27307ef262ba68d21a238be00e83
y0 = 0x514c8f56336411e75d5fa8c5d30efccb825ada9f5bf3f6eb64b5045bacf6b8969690077c84bea95aab74c24131f900f83adf2bfe59b80c5a0d77e8a9601454e5
# w1 = REDACTED
y1 = 0x1ccda066cd9d99e0b3569699854db7c5cf8d0e0083c4af57d71bf520ea0386d67c4b8442476df42964e5ed627466db3da532f65a8ce8328ede1dd7b35b82ed617
assert (y0%p) >= 1 and (y1%p) >= 1
assert pow(y0, q, p) == 1 and pow(y1, q, p) == 1

conn = remote("archive.cryptohack.org", 11840)

print(conn.recvline())
print(conn.recvline())

r0 = randint(1,q-1)
r1 = randint(1,q-1)

z1 = randint(1,p-1)
e1 = randint(0,2**511)

a0 = pow(g,r0,p)
a1 = pow(g,z1,p)*pow(pow(y1,e1,p),-1,p)

conn.sendline(f'{a0}')
conn.sendline(f'{a1}')

l = conn.recvline()
print(l)

s = int(l.split()[-1].decode())
print(s)

e0 = s ^ e1
z0 = (r0 + e0*w0) % q

conn.sendline(f'{e0}')
conn.sendline(f'{e1}')
conn.sendline(f'{z0}')
conn.sendline(f'{z1}')

print(conn.recvuntil(f'give me a witness!'))

conn.sendline(f'{w0}')
print(conn.recvline())