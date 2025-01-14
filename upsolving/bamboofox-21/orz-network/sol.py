from pwn import *
import hashlib
import sys
from sage.all import factor, Zmod, discrete_log, power_mod


'''
Find the minimum spanning tree by traversing only those vertices where pohlig hellman is fast enough
'''

def proof_of_work(prefix, difficulty):
    zeros = "0" * difficulty

    def is_valid(digest):
        bits = "".join(bin(i)[2:].zfill(8) for i in digest)
        return bits[:difficulty] == zeros

    i = 0
    while True:
        i += 1
        s = prefix + str(i)
        if is_valid(hashlib.sha256(s.encode()).digest()):
            return i


def solve(p, g, a, b):
    fs = factor(p - 1)
    mxp = max([x[0] for x in fs])
    if mxp > 1000000:
        # Not smooth enough
        return
    Z = Zmod(p)
    n_a = discrete_log(Z(a), Z(g))
    return int(Z(b) ** n_a)


def pr(a, b):
    return (a, b) if a < b else (b, a)


p = remote("chall.ctf.bamboofox.tw", 10369)
p.recvuntil("sha256(")
prefix = p.recv(16).decode()
result = proof_of_work(prefix, 20)
p.sendlineafter(b"Answer:", str(result))
msg = p.recvline().decode().strip()
words = msg.split(" ")
n_computers = int(words[2])
n_connections = int(words[5])
print(n_computers, n_connections)
p.recvuntil(b"lines):")  # Press Enter to print all connection logs (# lines):
p.sendline("")  # Enter

connected = {}
for i in range(n_connections):
    established = p.recvline().decode().strip()
    ews = established.split(" ")
    alice_id = int(ews[5][1:])
    bob_id = int(ews[9][1:])
    dh = p.recvline().decode().strip()
    dhs = dh.split(" ")
    modulus = int(dhs[4][:-1])
    base = int(dhs[7][:-1])
    alice_pub = int(dhs[12][:-1])
    bob_pub = int(dhs[17])  # No "," at the end of Bob's public key...
    sec = solve(modulus, base, alice_pub, bob_pub)
    if sec != None:
        connected[pr(alice_id, bob_id)] = sec

secret_keys = []
visited = [False] * (n_computers + 1)

queue = [1]
visited[1] = True
parent = {}
while len(queue) > 0:
    cur = queue.pop(0)
    for i in range(1, n_computers + 1):
        if i == cur:
            continue
        k = pr(cur, i)
        if k in connected and not visited[i]:
            print(f"{cur} -> {i}")
            visited[i] = True
            parent[i] = cur
            secret_keys.append(connected[k])
            queue.append(i)

assert all(visited[1:])


def print_path(x):
    def helper(y):
        print(f" <- {y}", end="")
        if y != 1:
            helper(parent[y])

    print(x, end="")
    if x != 1:
        helper(parent[x])
    print()


for i in range(1, n_computers + 1):
    print_path(i)

ans = " ".join(map(str, sorted(secret_keys)))
p.sendlineafter(
    b"Enter a list of 419 secret keys you've stolen, separated by whitespace characters:",
    ans,
)
print(p.recvall().decode())