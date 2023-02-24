import requests
import json

url='http://aes.cryptohack.org/ecb_oracle/encrypt/'

def hex(s):
    return s.encode('utf-8').hex()

charList = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}'

flag = ''
input = 'A'*32
k = 0

while k <= 32:
    for i in charList:
        r = requests.get(url+hex(input[:-1]))
        ref_block=json.loads(r.text)["ciphertext"][:64] #Reference block
        r = requests.get(url+hex(input[:-1]+flag+i))
        if json.loads(r.text)["ciphertext"][:64]==ref_block:
            flag+=i
            print("\r"+flag, flush=True, end='') #crypto{p3n6u1n5_h473_3cb}
            break
    k+=1
    input=input[:-1]
