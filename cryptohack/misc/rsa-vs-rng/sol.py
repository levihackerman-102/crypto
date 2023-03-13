from Crypto.Util.number import *
from math import gcd, floor

MOD = 2**512
A = 2287734286973265697461282233387562018856392913150345266314910637176078653625724467256102550998312362508228015051719939419898647553300561119192412962471189
B = 4179258870716283142348328372614541634061596292364078137966699610370755625435095397634562220121158928642693078147104418972353427207082297056885055545010537

N = 95397281288258216755316271056659083720936495881607543513157781967036077217126208404659771258947379945753682123292571745366296203141706097270264349094699269750027004474368460080047355551701945683982169993697848309121093922048644700959026693232147815437610773496512273648666620162998099244184694543039944346061
E = 65537 
ciphertext = "04fee34327a820a5fb72e71b8b1b789d22085630b1b5747f38f791c55573571d22e454bfebe0180631cbab9075efa80796edb11540404c58f481f03d12bb5f3655616df95fb7a005904785b86451d870722cc6a0ff8d622d5cb1bce15d28fee0a72ba67ba95567dc5062dfc2ac40fe76bc56c311b1c3335115e9b6ecf6282cca"

won = False

n = 0 
g = gcd(A-1, MOD)

coeff = pow((A-1) // g, -1, MOD) * B

def getp2(x):
    p2 = 0
    while x % 2 == 0:
        x //= 2
        p2 += 1
    return p2

# the n here is the one in 2^n
def solve(a,b,c,n = 512,x = MOD):
    for i in range(n):
        if p2c > 0:
            x &= ~(1 << i)
            solve(2*a,b,c//2,n-1,x)
        else:
            x |= (1 << i)
            solve(2*a,2*a + b,a//2 + floor(b//2) + floor(c//2) + 1,n-1,x)
    return x

def solvex2(x,c,s):
    

def solveRSA(P,Q):
    phi = (P-1)*(Q-1)
    d = inverse(E, phi)
    ct = int(ciphertext, 16)
    m = pow(ct, d, N)
    pt = long_to_bytes(m)
    return pt

while not won:
    n += 1
    print("n: ", n)
    a = pow(A,n,MOD)
    
    b = coeff * (pow(A, n) -1)
    b = b % MOD

    c = -N % MOD

    p2a = 0
    p2b = getp2(b)
    p2c = 0

    print("p2b: ", p2b)
    print("\n\n")

    # no solution
    if p2b == 0:
        continue

    if p2b > 0:
        B2 = b // 2
        s = (pow(a,-2,MOD)*pow(B2,2,MOD) - pow(a,-1,MOD)*c) % MOD
        r = getp2(s)
        q = s // 2**r
        if getp2(r) == 0 or q % 8 != 1:
            # no solution
            continue
        else:
            print(pow(2,r // 2 + 2), " solutions exist")
            a = s
            # x = x + a^-1 * B2
            f = getp2(a)
            if f == 
        # P = solve(a,b,c)
        # Q = N // P
        # plaintext = solveRSA(P,Q)
        # if b'crypto{' in plaintext:
        #     print(plaintext)
        #     won = True
        #     break
