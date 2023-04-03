from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
from sympy import totient
from sympy.ntheory import factorint

e = 3

# n will be 8 * (100 + 100) = 1600 bits strong which is pretty good
while True:
    p = getPrime(100)
    q = getPrime(100)
    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)
    if d != -1 and GCD(e, phi) == 1:
        break

n = p * q

flag = b"XXXXXXXXXXXXXXXXXXXXXXX"
pt = bytes_to_long(flag)
ct = pow(pt, e, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"ct = {ct}")

pc = 876085676073966724485872356361
qc = 1075170117786959666207828062121

phic = (p-1)*(q-1)
dc = pow(e,-1,phic)

nc = pc*qc

pt = pow(ct, dc, nc)
decrypted = long_to_bytes(pt)
print(decrypted)