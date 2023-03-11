from pwn import *
import re, json
from tqdm import tqdm
from itertools import count

# See https://nakedsecurity.sophos.com/2020/09/17/zerologon-hacking-windows-servers-with-a-bunch-of-zeros/
# Essentially, sending "\x00" * 8 as the ciphertext and "\x00" * 16 as the IV, the plaintext will be the same byte repeated
# We have a 1/256 chance of the plaintext being "\x00" * 8, and since the password length is the last four bytes of this, we get the empty string as the password
# and then free access

r = remote("socket.cryptohack.org",  13399)
r.recvline()

for i in tqdm(count(1)):
    # Send fake reset password request
    r.sendline(json.dumps({
        "option": "reset_password",
        "token": (b"\x00" * 64).hex()
    })
    )
    r.recvline()
    # Try to authenticate
    r.sendline(json.dumps({
        "option": "authenticate",
        "password": ""
    }))
    response = json.loads(r.recvline())
    print(response)
    if response["msg"] == "Wrong password.":
        r.sendline(json.dumps({
            "option": 'reset_connection'
        }))
        r.recvline()
    else:
        print(response)
        break
