from hashlib import sha256
import os
# from utils import listener
from pwn import remote
import json
from Crypto.Util.number import long_to_bytes

FLAG = b"crypto{???????????????????????????????}"


def _xor(a, b):
    return bytes([_a ^ _b for _a, _b in zip(a, b)])

def _and(a, b):
    return bytes([_a & _b for _a, _b in zip(a, b)])

def shuffle(mixed_and, mixed_xor):
    return bytes([mixed_xor[i%len(mixed_xor)] for i in mixed_and])


class Challenge():
    def __init__(self):
        self.before_input = "Oh no, how are you going to unmix this?\n"

    def challenge(self, msg):
        if "option" not in msg:
            return {"error": "You must send an option to this server."}

        elif msg["option"] == "mix":
            if not "data" in msg:
                return {"error": "Please send hex-encoded data"}

            data = bytes.fromhex(msg["data"])
            if len(data) < len(FLAG):
                data += os.urandom(len(FLAG) - len(data))

            mixed_and = _and(FLAG, data)
            mixed_xor = _xor(_xor(FLAG, data), os.urandom(len(FLAG)))

            very_mixed = shuffle(mixed_and, mixed_xor)
            super_mixed = sha256(very_mixed).hexdigest() 

            return {"mixed": super_mixed}

        else:
            return {"error": "Invalid option"}


"""
When you connect, the 'challenge' function will be called on your JSON
input.
"""
# listener.start_server(port=13402)

# Find length of flag first by sending null bytes of increasing length until we get the known hash for b'...'
# (found out later that the ? are length accurate)
def sha256_hashes(length):
    hash_list = []
    for b in range(256):
        byte_array = bytes([b] * length)
        sha256_hash = sha256(byte_array).hexdigest()
        # print(sha256_hash)
        hash_list.append(sha256_hash)
    return hash_list

conn = remote('socket.cryptohack.org', 13402)

print(conn.recvline())

x = "00"
L = 0
while True:
    expected_hash_list = sha256_hashes(len(x)//2)
    to_send = {"option": "mix", "data": x}
    conn.sendline(json.dumps(to_send))
    recv = conn.recvline()
    print(recv)
    hash = json.loads(recv)["mixed"]
    if hash in expected_hash_list:
        print("Found length of flag:", len(x)//2)
        L = len(x)//2
        break
    x += "00"

conn.close()

# Now we know the length of the flag is 39, we can brute force the flag byte by byte

flag = 0

expected_hash_list = sha256_hashes(L)

conn = remote('socket.cryptohack.org', 13402)

print(conn.recvline())

for i in range(8*L):
    print(f"Trying {i}th bit: ")
    data = 0
    data |= (1 << i)
    data = long_to_bytes(data)
    # print(len(data))
    pad_len = L - len(data)
    if pad_len > 0:
        padding = b'\x00' * pad_len
        data = padding + data   
    print(data)
    print(len(data))
    data = data.hex()
    to_send = {"option":"mix","data":data}
    conn.sendline(json.dumps(to_send))
    recv = conn.recvline()
    print(recv)
    hash = json.loads(recv)["mixed"]
    # print(hash)
    if hash in expected_hash_list:
        continue
    flag |= (1 << i)    

print(long_to_bytes(flag))
