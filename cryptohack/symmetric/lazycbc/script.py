import requests
import json

def get_ciphertext(plaintext):
    data = requests.get("https://aes.cryptohack.org/lazy_cbc/encrypt/"+plaintext)
    data = json.loads(data.content)
    return data["ciphertext"]

def get_plaintext(ciphertext):
    data = requests.get("https://aes.cryptohack.org/lazy_cbc/receive/"+ciphertext)
    data = json.loads(data.content)["error"]
    plainhex = data.split(" ")[-1]
    return plainhex

def get_flag(key):
    data = requests.get("https://aes.cryptohack.org/lazy_cbc/get_flag/"+key)
    flag = json.loads(data.content)["plaintext"]
    return flag

cipher_hex = get_ciphertext("0"*32)
print(cipher_hex)

plain_hex = get_plaintext("0"*32 + cipher_hex)
print(plain_hex)

flag_blok = plain_hex[32:]
print(flag_blok)

flag_hex = get_flag(flag_blok)
print(flag_hex)

flag = bytes.fromhex(flag_hex).decode()
print(flag)
