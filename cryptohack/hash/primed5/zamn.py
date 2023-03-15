from Crypto.Util.number import isPrime, bytes_to_long, long_to_bytes
import hashlib
import json
from pwn import remote

x = "4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa200a8284bf36e8e4b55b35f427593d849676da0d1555d8360fb5f07fea2"
y = "4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa202a8284bf36e8e4b55b35f427593d849676da0d1d55d8360fb5f07fea2"

print("md5(x) : ", hashlib.md5(bytes.fromhex(x)).hexdigest())
print("md5(y) : ", hashlib.md5(bytes.fromhex(y)).hexdigest())

while not isPrime(int(x, 16)):
    # append 1s till prime
    x += "1"
    y += "1"
    print(x + "\n\n")

xx = bytes_to_long(bytes.fromhex(x))
yy = bytes_to_long(bytes.fromhex(y))

print("x+z :", xx)
print("y+z :", yy)

print("md5(x+z) : ", hashlib.md5(bytes.fromhex(x)).hexdigest())
print("md5(y+z) : ", hashlib.md5(bytes.fromhex(y)).hexdigest())

conn = remote("socket.cryptohack.org", 13392)

print(conn.recvline())

to_sign = {
    "option":"sign",
    "prime":str(xx)
}

conn.sendline(json.dumps(to_sign))

signature = json.loads(conn.recvuntil(b'}').decode('utf-8'))['signature']

print(signature)

to_check = {
    "option":"check",
    "prime":str(yy),
    "signature":signature,
    "a":"217489"
}

print(to_check)

conn.send(json.dumps(to_check))

print(conn.recvline())
