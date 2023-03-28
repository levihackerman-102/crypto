from itertools import cycle
from hashlib import md5
# from utils import listener
from pwn import remote
import json

FLAG = b'crypto{??????????????????????????????????????}'

def bxor(a, b):
	return bytes(x ^ y for x, y in zip(a, b))

# STEP 1: append padding bits s.t. the length is congruent to 448 modulo 512
# which is equivalent to saying 56 modulo 64.
# padding before adding the length of the original message is conventionally done as:
# pad a one followed by zeros to become congruent to 448 modulo 512(or 56 modulo 64).
def pad(msg):
	padding = bytearray('', 'ascii')
	msg_len_in_bits = (8*len(msg)) & 0xffffffffffffffff
	padding.append(0x80)
	msg.append(0x80)

	while len(msg)%64 != 56:
		msg.append(0)
		padding.append(0)

	# STEP 2: append a 64-bit version of the length of the length of the original message
	# in the unlikely event that the length of the message is greater than 2^64,
	# only the lower order 64 bits of the length are used.

	# sys.byteorder -> 'little'
	msg += msg_len_in_bits.to_bytes(8, byteorder='little') # little endian convention
	# to_bytes(8...) will return the lower order 64 bits(8 bytes) of the length.
	padding += msg_len_in_bits.to_bytes(8, byteorder='little')
	
	return padding

# class Challenge():
#     def __init__(self):
#         self.before_input = "Enter data\n"

#     def challenge(self, msg):
#         if "option" not in msg:
#             return {"error": "You must send an option to this server."}

#         elif msg["option"] == "message":
#             data = bytes.fromhex(msg["data"])

#             if len(data) < len(FLAG):
#               return {"error": "Bad input"}

#             salted = bxor(data, cycle(FLAG))
#             return {"hash": md5(salted).hexdigest()}

#         else:
#             return {"error": "Invalid option"}


def hashFromServer(data):
	data = bytes.fromhex(data)
	salted = bxor(data, cycle(FLAG))
	return md5(salted).hexdigest()


"""
When you connect, the 'challenge' function will be called on your JSON input.
"""
# listener.start_server(port=13407)

length = 46
n = 4

'''
First, from the server we get the hash of 46*n - 1 bytes of cyclic flag + 9 bytes of padding  

To the server, we send 46*n-1 bytes of 00 + xor(b'}crypto{', first 8 bytes of the padding) + xor(9th byte of the padding, y), here y is a brute byte
if we get the same hash as above our brute of y is correct

padding = 1000 0000 + 8 bytes length field
'''

data = "00" * (n*length - 1)

# hash of 46*n-1 length cyclic flag + padding (let this be S)
hash = hashFromServer(data)
print(hash)

data_bytearray = bytearray(data, 'ascii')
padding = pad(bytearray.fromhex(data))

print("padding : ", padding)

for i in range(256):
	to_send = "00" * (n*length - 1) 
	to_send +=  bxor(b'}crypto{', padding[:8]).hex()
	to_send += bxor(padding[-1:], bytes([i])).hex()
	hashNew = hashFromServer(to_send)
	print(i, hashNew)
	if hashNew == hash:
		print(i)
		break
	
'''
Now we know y, perform hash length extension attack to get the hash of S + x where x is a brute byte
if we get the same hash from the server our brute of x is correct and we move onto the next byte
'''
