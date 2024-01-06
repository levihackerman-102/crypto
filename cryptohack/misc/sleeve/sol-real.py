from sage.all import *
from fastecdsa.curve import P256
from fastecdsa.point import Point
from Crypto.Random import random
from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long
from sage.rings.integer import Integer
from pwn import *
from json import loads, dumps

class RNG:
        def __init__(self, seed, P, Q):
            self.seed = seed
            self.P = P
            self.Q = Q

        def next(self):
            t = self.seed
            s = int((t * self.P)[0])
            self.seed = s
            r = int((s * self.Q)[0])
            return r & (2**(8 * 30) - 1)
        
def rebase(n, b=37):
      if n < b:
        return [n]
      else:
        return [n % b] + rebase(n//b, b)

conn = remote("socket.cryptohack.org", 13387)

while True:
    print(conn.recvline())

    # Generate Q
    a = P256.a
    b = P256.b
    p = P256.p
    E = EllipticCurve(GF(p), [a, b])
    q = E.order()
    P = E(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
    d = 123456789
    invd = inverse(d, q)
    Q = invd*P

    print("Q = ", Q)

    x = hex(Q[0])[2:]   
    y = hex(Q[1])[2:]
    conn.sendline(dumps({"x": x, "y":y}))
    print(conn.recvline())
