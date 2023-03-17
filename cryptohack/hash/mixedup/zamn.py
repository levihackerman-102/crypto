from pwn import remote
import json
import hashlib

def sha256_hashes(p, L):
    result = {}
    for i in range(256):
        # Create a byte array with all bytes set to 0 except byte at position p
        ba = bytearray([i]*L)
        for j in range(256):
            ba[p] = j

            # Calculate the SHA256 hash of the byte array
            hash = hashlib.sha256(bytes(ba)).hexdigest()

            # Add the byte array and hash to the result dictionary
            result[ba] = hash
    return result


bins = ["10000000", "01000000", "00100000", "00010000", "00001000", "00000100", "00000010", "00000001"]
bins_hex = ["80", "40", "20", "10", "08", "04", "02", "01"]

conn = remote('socket.cryptohack.org', 13402)

print(conn.recvline())

L = 39

for i in range(L):
    data = "00"*L
    for j in range(8):
        data_mod = data[:2*i] + bins_hex[j] + data[2*i+2:]
        # print(format(int(data_mod,16), '0156b'))
        # print(data_mod)
        to_send = {"option": "mix", "data": data_mod}
        conn.sendline(json.dumps(to_send))

