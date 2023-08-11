import requests
from concurrent.futures import ThreadPoolExecutor

NUM_CIPHERTEXTS = 22
ciphertexts = set()

def _collect_ciphertexts():
    global ciphertexts
    while len(ciphertexts) < NUM_CIPHERTEXTS:
        response = requests.get("http://aes.cryptohack.org/stream_consciousness/encrypt/").json()
        ciphertexts.add(bytes.fromhex(response["ciphertext"]))

# Collect ciphertexts (multithread)
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.submit(_collect_ciphertexts)
    
# With multiple ciphertexts and a stream cipher, we have that c1 xor c2 = p1 xor p2
# Therefore, we can use crib dragging to get the whole flag

"""
crib1 = bytes.fromhex("2d1d55503d481707131e5a171b5d14193052771a595f26115431021443510011")
crib2 = bytes.fromhex("371a1c50000a09195a1b595252475c043115131c46132b59542b46405f514c0d")
crib3 = bytes.fromhex("2f1d0f15584f0b195c1b54551e4a0b4d0b1a560c1557305f122b465f595b1b5d")
crib4 = bytes.fromhex("33170b18151f084b5b1c155f134014003601401051132b59507f1246565d025d")
crib5 = bytes.fromhex("2a520a181503174b5f164652525642082d0b471d5c5d381154310214595b185d")
# xor(crib1, b"crypto{") # --> b"No, I'l", next characters probably 'l '?
# xor(bytes(crib1[7:9]), b"l ") # --> flag_known is "crypto{k3"
# xor(crib2, b"crypto{k3") # --> b'The terri', next characters probably 'ble '?
# xor(bytes(crib2[9:13]), b"ble ") # --> flag_known is "crypto{k3y57r"
# xor(crib3, b"crypto{k3y57r") # --> b'Love, probabl', next character is probably 'y'?
# xor(bytes(crib3[13:14]), b"y") # --> flag_known is "crypto{k3y57r3"
# xor(crib4, b"crypto{k3y57r3") # --> b'Perhaps he has', next character is probably ' '?
# xor(bytes(crib4[14:15]), b' ') # --> flag_known is "crypto{k3y57r34"
# xor(crib5, b"crypto{k3y57r34" ) # --> b'I shall lose ev', next characters are "erything " ?
# xor(bytes(crib5[15:24]), b"erything ") # flag_known is "crypto{k3y57r34m_r3u53_1"
# xor(crib3, b"crypto{k3y57r34m_r3u53_1") # --> b'Love, probably? They don', next characters are "'t '"?
# xor(bytes(crib3[24:27]), b"'t ") # flag_known is "crypto{k3y57r34m_r3u53_15_f"
# Googling crib3, we get the whole flag:
# xor(crib1, b"No, I'll go in to Dolly and tell") --> crypto{k3y57r34m_r3u53_15_f474l}
"""
