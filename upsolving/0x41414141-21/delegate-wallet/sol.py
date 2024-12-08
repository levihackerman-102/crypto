from pwn import *
import gmpy2 as gmpy

r = remote('185.172.165.118', 4008)

print (r.recvline())
print (r.recvline())
r.sendline('1')
s1 = int(r.recvline().split(' ')[-1])
print (s1)


print (r.recvline())
print (r.recvline())
r.sendline('1')
s2 = int(r.recvline().split(' ')[-1])
print (s2)

print (r.recvline())
print (r.recvline())
r.sendline('1')
s3 = int(r.recvline().split(' ')[-1])
print (s3)


n = pow(2, 607) -1
m = ((s3 - s2)*gmpy.invert(s2 - s1, n))%n
print("m: ", m)
c = (s3 - m*s2)%n
print("c: ", c)

s4 = (s3*m + c)%n

print("s4: ", (s3*m + c)%n)


r.sendline('2')
r.sendline(str(s4))
r.interactive()
