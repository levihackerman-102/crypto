from base64 import b64decode

CIPHERTEXT_FILE = 'ciphertext.txt'

encrypted = None
with open(CIPHERTEXT_FILE, 'r') as f:
  encrypted = b64decode(f.read())

for i in range(256):
    s = ''.join(chr(c ^ i) for c in encrypted)
    if 'flag' in s:
        print(s)
        break
