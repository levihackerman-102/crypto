import requests
from itertools import cycle

url = "https://aes.cryptohack.org/bean_counter/encrypt/"

ct_hex = requests.get(url).json()['encrypted']

print(ct_hex)

png_header_hex = '89504e470d0a1a0a0000000d49484452'
png_header = bytes.fromhex(png_header_hex)

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

ct = bytes.fromhex(ct_hex)

keystream = xor(ct, png_header)

print(keystream)

pt = xor(ct, cycle(keystream))

open('flag.png', 'wb').write(pt)
