encrypted = ''

with open('encrypted.txt', 'rb') as f:
    encrypted = f.read()


def decrypt(key):
    plaintext = ''
    for i in range(0, 256):
        pos = (3**(key + i)) % 257 - 1
        plaintext += chr(((encrypted[pos]) ^ i) ^ pos)
    return plaintext

for key in range(1, 257):
    plaintext = decrypt(key)
    if '{FLG' in plaintext:
        with open(plain,'wb') as plaint:
            plaint.write(bytes(plaintext))
        print(plaintext)