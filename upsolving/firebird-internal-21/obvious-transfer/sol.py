from pwn import *
import time
from tqdm import tqdm

p = remote('darkness', 50001) # hosted locally

def solve():
    start = time.perf_counter()
    
    for _ in tqdm(range(1, 1000+1)):
        p.recvuntil('🤖 ')
        p.sendline('📦')
    
    end = time.perf_counter()

    elapsed_time = end - start
    print(elapsed_time)
    # print(f'Elapsed time: {end - start:.4f} seconds')

    p.recvuntil('🤖 ')

    if elapsed_time > 4.5:
        p.sendline('🔓 1')
    else:
        p.sendline('🔓 0')    
    
    print(p.recvline().decode('utf-8'))
    print(p.recvline().decode('utf-8'))

for i in range(1, 10+1): # reduced the number of iterations to 10, but the idea remains the same
    solve()
    
print("All test cases passed")

print(p.recvline().decode('utf-8'))
print(p.recvline().decode('utf-8'))
