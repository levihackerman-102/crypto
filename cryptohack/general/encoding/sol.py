from pwn import *
import json
import base64
import codecs
from Crypto.Util.number import long_to_bytes

conn = remote('socket.cryptohack.org', 13377)

while(True):
    enc_json = conn.recvline().decode()
    print(enc_json)      
    type = json.loads(enc_json)["type"]  
    enc = json.loads(enc_json)["encoded"]
    
    decoded = ""

    match type:
        case "base64":
            decoded = base64.b64decode(enc).decode()
        case "hex":
            decoded = bytes.fromhex(enc).decode()
        case "rot13":
            decoded = codecs.decode(enc, 'rot_13')
        case "bigint":
            decoded = long_to_bytes(int(enc,16)).decode()
        case "utf-8":
            decoded = ''.join([chr(b) for b in enc])

    print(decoded)
    to_send = '{' + f'"decoded" : "{decoded}"' + '}'

    print(to_send)

    conn.sendline(to_send)
