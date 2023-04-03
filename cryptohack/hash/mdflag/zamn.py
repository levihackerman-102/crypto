from itertools import cycle, islice
from hashlib import md5
import struct
import binascii
import md5py

FLAG = 'crypto{??????????????????????????????????????}'

def bxor(a, b):
    result = ""
    # print(len(a), len(b))
    for i in range(len(a)):
        result += chr(ord(a[i]) ^ ord(b[i]))
    return result

def pad(msg):
	padding = bytearray('', 'ascii')
	msg_len_in_bits = (8*len(msg)) & 0xffffffffffffffff
	padding.append(0x80)
	msg.append(0x80)

	while len(msg)%64 != 56:
		msg.append(0)
		padding.append(0)
		
	msg += struct.pack('<Q', msg_len_in_bits)  # '<' specifies little-endian
	padding += struct.pack('<Q', msg_len_in_bits)
	
	return padding

def hashFromServer(data):
    leng = len(data)
    salted = bxor(data, ''.join(islice(cycle(FLAG), leng)))
    # print "salted : ", salted
    return md5(salted).hexdigest()

# function to perform hash length extension attack
def extend(h, l, a):
    if l%64 != 0:
        l += 64 - l%64
    val = h.decode("hex")
    ex = md5py.new("a"*l)
    ex.A, ex.B, ex.C, ex.D = md5py._bytelist2long(val)
    ex.update(a)
    return ex.hexdigest()

length = 46
n = 4

'''
First, from the server we get the hash of 46*n - 1 bytes of cyclic flag + 9 bytes of padding, let's call this hash X  

To the server, we send 46*n-1 bytes of 00 + xor(b'}crypto{', first 8 bytes of the padding) + xor(9th byte of the padding, y), here y is a brute byte
if we get the same hash as above our brute of y is correct

Call this array of brutes Y[256]
'''

data = "00" * (n*length)
print("data : ", data)
print("decoded : ", binascii.unhexlify(data))
# hash of 46*n-1 length cyclic flag + padding (let this be S)
hash_X = hashFromServer(binascii.unhexlify(data))
print("hash X : ", hash_X)

data_bytearray = bytearray(data, 'ascii')
padding_X = pad(bytearray.fromhex(data))

print("padding X : ", padding_X)

hashes_Y = []
padding_Y = bytearray('', 'ascii')

padding_X = str(padding_X)

for i in range(256):
	data_Y = "\x00" * (n*length - 1) + bxor('}crypto{', padding_X[:8]) + bxor(chr(i), padding_X[-1:])
	# print("data Y : ", data_Y)
	padding_Y = pad(bytearray(data_Y))
	hash_y = hashFromServer(data_Y.encode('hex'))
	hashes_Y.append(hash_y)

print("padding Y : ", padding_Y)

# print("hashes Y : ", hashes_Y)

'''
Now we perform length extension attack on X, to get the hash of X + padding_Y, one of the members of Y should match this hash and we'll thus have our brute_byte
'''
hash_X_extended = extend(hash_X, length*n - 1, str(padding_Y))
print("hash X extended : ", hash_X_extended)

if hash_X_extended in hashes_Y:
	print("brute byte : ", hashes_Y.index(hash_X_extended))
