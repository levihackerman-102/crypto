import requests
from pwn import xor

ENC_URL = "https://aes.cryptohack.org/ecbcbcwtf/encrypt_flag/"  # flag CBC encryption link
DEC_URL = "https://aes.cryptohack.org/ecbcbcwtf/decrypt/"  # flag ECB encryption link

r1 = requests.get(f"{ENC_URL}")
data1 = r1.json()
# get the random flag cipher text. The ciphertext contains the 16 hex values of iv at the beginning
# so we suppose block size is 16 (also this is based to the fact that ciphertext has 48 (3*16) hex values)
flag_ciphertext = data1["ciphertext"]
print(f"iv + AES CBC Encryption of flag: {flag_ciphertext}")

iv = flag_ciphertext[:32] # first 16 hex values are the iv
print(f"iv: {iv}")
flag_ciphertext = flag_ciphertext[32:]  # cipher text
print(f"AES CBC Encryption of flag: {flag_ciphertext}")
print(f"Hex values: {len(flag_ciphertext)/2}")  # 32
print()

r2 = requests.get(f"{DEC_URL}/{flag_ciphertext}/")
data2 = r2.json()
# Get the unxored plaintext. We will use flag_ciphertext parts and iv to xor the parts of this to get the answer
flag_unxored = data2["plaintext"]
print(f"AES ECB Decryption of flag: {flag_unxored}")
print(f"Hex values: {len(flag_unxored)/2}")  # 32
print()

# Unxored Plain text Block 1 XOR vi:
first_block_bytes = xor(bytes.fromhex(flag_unxored[:32]), bytes.fromhex(iv) )
print(f"Unxored Plain text Block 1: {flag_unxored[:32]}")
print(f"vi: {iv}")
print(f"Plain text block 1 bytes: {first_block_bytes}")
print()

# Unxored Plain text Block 2 XOR Cipher text block 1:
second_block_bytes = xor(bytes.fromhex(flag_unxored[32:]), bytes.fromhex(flag_ciphertext[:32]) )
print(f"Unxored Plain text Block 2: {flag_unxored[32:]}")
print(f"Cipher text block 1: {flag_ciphertext[:32]}")
print(f"Plain text block 2 bytes: {second_block_bytes}")
print()

# flag
print(f"FLAG is {first_block_bytes + second_block_bytes}")
