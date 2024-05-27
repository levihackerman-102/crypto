from pwn import *
import json
from sage.all import Matrix, vector, var, Zmod

r = remote('socket.cryptohack.org', 13411)

coeffs = []
B = []

r.recvuntil('Would you like to encrypt your own message, or see an encryption of a character in the flag?\n')

for i in range(64):
    m = json.dumps({"option": "encrypt", "message": 0})
    r.sendline(m)
    recv = r.recvuntil('}').decode('utf-8')
    print(recv)
    A_strings = json.loads(recv)['A'].strip('[]').split(', ')
    A = [int(num) for num in A_strings]
    print(A)
    coeffs.append(A)
    b = int(json.loads(recv)['b'])
    print(b)
    B.append(b)

print(coeffs)
print(B)

variables = var(['x{}'.format(i) for i in range(1, 65)])

Z = Zmod(65537)

A = Matrix(Z, 64, coeffs)
B = vector(Z, 64, B)

S = A.solve_right(B)
print(S)

flag = ''
i = 0
while True:
    m = json.dumps({"option": "get_flag", "index": i})
    r.sendline(m)
    recv = r.recvuntil('}').decode('utf-8')
    print(recv)
    if 'error' in recv:
        break
    A_strings = json.loads(recv)['A'].strip('[]').split(', ')
    A = [int(num) for num in A_strings]
    print(A)
    b = int(json.loads(recv)['b'])
    print(b)
    A = vector(Z, 64, A)   
    flag += chr(b - A * S)
    i += 1

print(flag)
