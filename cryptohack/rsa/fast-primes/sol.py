#!/usr/bin/env python3

import math
import random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, inverse, long_to_bytes
from gmpy2 import is_prime


FLAG = b"crypto{????????????}"

primes = []


def sieve(maximum=10000):
    # In general Sieve of Sundaram, produces primes smaller
    # than (2*x + 2) for a number given number x. Since
    # we want primes smaller than maximum, we reduce maximum to half
    # This array is used to separate numbers of the form
    # i+j+2ij from others where 1 <= i <= j
    marked = [False]*(int(maximum/2)+1)

    # Main logic of Sundaram. Mark all numbers which
    # do not generate prime number by doing 2*i+1
    for i in range(1, int((math.sqrt(maximum)-1)/2)+1):
        for j in range(((i*(i+1)) << 1), (int(maximum/2)+1), (2*i+1)):
            marked[j] = True

    # Since 2 is a prime number
    primes.append(2)

    # Print other primes. Remaining primes are of the
    # form 2*i + 1 such that marked[i] is false.
    for i in range(1, int(maximum/2)):
        if (marked[i] == False):
            primes.append(2*i + 1)


def get_primorial(n):
    result = 1
    for i in range(n):
        result = result * primes[i]
    return result


def get_fast_prime():
    M = get_primorial(40)
    while True:
        k = random.randint(2**28, 2**29-1)
        a = random.randint(2**20, 2**62-1)
        p = k * M + pow(e, a, M)

        if is_prime(p):
            return p


sieve()

# from http://lapo.it/asn1js/ I decoded attached public key and I received n and e:
n = 4013610727845242593703438523892210066915884608065890652809524328518978287424865087812690502446831525755541263621651398962044653615723751218715649008058509
e = 65537

# from factordb.com I received p and q:

p = 51894141255108267693828471848483688186015845988173648228318286999011443419469
q = 77342270837753916396402614215980760127245056504361515489809293852222206596161

n = p * q
phi = (p - 1) * (q - 1)
d = inverse(e, phi)

key = RSA.construct((n, e, d))
cipher = PKCS1_OAEP.new(key)


ciphertext = 0x249d72cd1d287b1a15a3881f2bff5788bc4bf62c789f2df44d88aae805b54c9a94b8944c0ba798f70062b66160fee312b98879f1dd5d17b33095feb3c5830d28
ciphertext_int = long_to_bytes(ciphertext)
plaintext = cipher.decrypt(ciphertext_int)
print(plaintext)

# ciphertext = cipher.encrypt(FLAG)

# assert cipher.decrypt(ciphertext) == FLAG

exported = key.publickey().export_key()
print(exported)
# with open("fast_primes_key.pem", 'wb') as f:
    # f.write(exported)

# with open('ciphertext.txt', 'w') as f:
    # f.write(ciphertext.hex())
