from collections import namedtuple
from Crypto.Util.number import *
from Crypto.Cipher import AES

# Copied functions from source
Complex = namedtuple("Complex", ["re", "im"])

def complex_mult(c1, c2, modulus):
    return Complex(
        (c1.re * c2.re - c1.im * c2.im) % modulus,  # real part
        (c1.re * c2.im + c1.im * c2.re) % modulus,  # image part
    )


def complex_pow(c, exp, modulus):
    result = Complex(1, 0)
    while exp > 0:
        if exp & 1:
            result = complex_mult(result, c, modulus)
        c = complex_mult(c, c, modulus)
        exp >>= 1
    return result

# data
g = Complex(re=20878314020629522511110696411629430299663617500650083274468525283663940214962,
            im=16739915489749335460111660035712237713219278122190661324570170645550234520364)
order = 364822540633315669941067187619936391080373745485429146147669403317263780363306505857156064209602926535333071909491
n = 42481052689091692859661163257336968116308378645346086679008747728668973847769
public_key = Complex(re=11048898386036746197306883207419421777457078734258168057000593553461884996107,
                     im=34230477038891719323025391618998268890391645779869016241994899690290519616973)
encrypted_flag = b'\'{\xda\xec\xe9\xa4\xc1b\x96\x9a\x8b\x92\x85\xb6&p\xe6W\x8axC)\xa7\x0f(N\xa1\x0b\x05\x19@<T>L9!\xb7\x9e3\xbc\x99\xf0\x8f\xb3\xacZ:\xb3\x1c\xb9\xb7;\xc7\x8a:\xb7\x10\xbd\x07"\xad\xc5\x84'

def f(c):
    return (c.re**2 + c.im**2)%n

print('[+] Computing Discrete Log')

# Passing it to Pari as sage will result in a crash
k = int(pari(f"znlog({f(public_key)}, Mod({f(g)}, {n}))"))

assert pow(f(g), k, n) == f(public_key)
print(f'[+] Discrete log result: {k}')

# computing the order
p = sqrt(n)
o = p*(p-1)//2
assert pow(f(g), k+o, n) == f(public_key)

# All that's left is to decrypt the flag
for i in range(0, 100):
    private_key = long_to_bytes(k + i * o)
    flag = AES.new(private_key, AES.MODE_ECB).decrypt(encrypted_flag)
    if b"TetCTF" in flag:
        break

flag = flag.strip(b'\x00').decode()
print(f'[+] Flag: {flag}')