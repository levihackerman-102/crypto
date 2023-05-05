from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import inverse
import hashlib
from sympy.ntheory.residue_ntheory import discrete_log

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('utf-8')
    else:
        return plaintext.decode('utf-8')
p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
A = 0x190766d4be1c2ec1c00f7838764a46288c28567d5e093e49ef71587272f80bed58f8c47c70a99f4b0eceab6d659ce8d2c8475b10f93fc5123017fb54a875a9b18191af5dac0d857c28953fba4d10b2a1dfcb83bbb0f29bfa10fdb15ce8af2b8d441a00b1cf0f2e0634bb0aa912a9a6107b205b225a52a6d822ad7c31c402ae93a6d2d77b5664cae2703433170fdf1703abf7f30f353752ad9cc98db09f6f1e891e20535081cfe86f5e1415d5f2aca3956f2eb6691901d3e55cfcbe3f2a3a550b
g = 0x2
a = A * inverse(g, p)
B = 0x92092dfaafe2de9fa585c26f79aa763c1069cb6e37d0f68c655d89fc9e99f17703c9336558b8cd49bc72de084a2e7736644d7c79147ee4bd93c8bffe883a9442a2bbf269a07c9af81b56b5af1fe523d7201acd9636e52e3f0a07ae124e986d94560c044a9a62ae916ec89c4450c2a31a3b6c400d21b00bbb292611bf504d5a22282dc767dca91f0573da8fa35a8deaa1307bf272589af97052d6402b69c34313fa5d7a4c06d6cbca70b0e74979821cf09f5f581a2f3fb86c6f455863caa9f0b0

shared_secret = (a * B) % p

iv = "317c46f08dd3bbe5138d8b53163402ea"
ciphertext = "636a2cab48228912618557d1355cda5dc104839b1db454b5aa62c397c92dd876a56d13a3c291f4dfbfddfd37b837f5e0"

print(decrypt_flag(shared_secret, iv, ciphertext))
