from Crypto.Util.number import *
from math import gcd, floor

MOD = 2**512
A1 = 2287734286973265697461282233387562018856392913150345266314910637176078653625724467256102550998312362508228015051719939419898647553300561119192412962471189
B1 = 4179258870716283142348328372614541634061596292364078137966699610370755625435095397634562220121158928642693078147104418972353427207082297056885055545010537

N1 = 95397281288258216755316271056659083720936495881607543513157781967036077217126208404659771258947379945753682123292571745366296203141706097270264349094699269750027004474368460080047355551701945683982169993697848309121093922048644700959026693232147815437610773496512273648666620162998099244184694543039944346061
E1 = 65537 
ciphertext = "04fee34327a820a5fb72e71b8b1b789d22085630b1b5747f38f791c55573571d22e454bfebe0180631cbab9075efa80796edb11540404c58f481f03d12bb5f3655616df95fb7a005904785b86451d870722cc6a0ff8d622d5cb1bce15d28fee0a72ba67ba95567dc5062dfc2ac40fe76bc56c311b1c3335115e9b6ecf6282cca"

won = False
n = 0 

gpsum = 0

def getb(n):
    global gpsum 
    gpsum += pow(A1, n-1, MOD)
    return (B1 * gpsum) % MOD

def getp2(x):
    if(x == 0):
        return 512
    p2 = 0
    while x % 2 == 0:
        x //= 2
        p2 += 1
    return p2

def ej(x):
    if x % 2 == 0:
        return 1
    else:
        return 0

# the n here is the one in 2^n
# def solve33(a,b,c,n = 512,x = MOD):
#     for i in range(n):
#         if getp2(c) > 0:
#             x &= ~(1 << i)
#             solve33(2*a,b,c//2,n-1,x)
#         else:
#             x |= (1 << i)
#             solve33(2*a,2*a + b,a//2 + floor(b//2) + floor(c//2) + 1,n-1,x)
#     return x

# def solve34(a,b,c, n = 512):
#     delta = solve33(2*a,b,c // 2,n-1)
#     print("delta: ", delta)
#     pi = 2*delta
#     rho = solve33(2*a,2*a+b,(a+b+c) // 2,n-1)
#     eps = 2*rho + 1
#     return pi % 2**n, eps % 2**n

def solveRSA(P,Q):
    phi = (P-1)*(Q-1)
    d = inverse(E1, phi)
    ct = int(ciphertext, 16)
    m = pow(ct, d, N1)
    pt = long_to_bytes(m)
    return pt

def legendre_symbol(a, p):
    """
    Legendre symbol
    Define if a is a quadratic residue modulo odd prime
    http://en.wikipedia.org//wiki//Legendre_symbol
    """
    ls = pow(a, (p - 1)//2, p)
    if ls == p - 1:
        return -1
    return ls

def _prime_mod_sqrt(a, p):
    """
    Square root modulo prime number
    Solve the equation:
        x^2 = a mod p
    and return x. Note that p - x is also a solution.
    Variable a must be a quadratic residue modulo p
    Variable p must be an odd prime
    http://en.wikipedia.org//wiki//Tonelli-Shanks_algorithm
    """
    # Reduce a mod p
    a %= p

    # Special case which solution is simple
    if p % 4 == 3:
        x = pow(a, (p + 1)//4, p)
        return x

    # Factor p-1 on the form q * 2^s (with Q odd)
    q, s = p - 1, 0
    while q % 2 == 0:
        q, s = q >> 1, s + 1

    # Select a z which is a quadratic non resudue modulo p
    z = 1
    while legendre_symbol(z, p) != -1:
        z += 1
    c = pow(z, q, p)

    # Search for a solution
    x = pow(a, (q + 1)//2, p)
    t = pow(a, q, p)
    m = s
    while t != 1:
        # Find the lowest i such that t^(2^i) = 1
        e = 2
        for i in range(1, m):
            if pow(t, e, p) == 1:
                break
            e *= 2

        # Update next value to iterate
        b = pow(c, 1 << (m - i - 1), p)
        x = (x * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i

    return x

def prime_mod_sqrt(a, p, e=1):
    """
    Square root modulo prime power number
    Solve the equation:
        x^2 = a mod p^e
    and return list of x solution
    http://en.wikipedia.org//wiki//Hensel's_lemma
    http://www.johndcook.com//quadratic_congruences.html
    """
    # Reduce a mod p^e
    a %= p**e

    # Handle prime 2 special case
    if p == 2:
        if e >= 3 and a % 8 == 1:
            res = []
            for x in [1, 3]:
                for k in range(3, e):
                    i = (x*x - a)//(2**k) % 2
                    x = x + i*2**(k-1)
                res.append(x)
                res.append(p**e - x)
            return res
        # No solution if a is odd and a % 8 != 1
        if e >= 3 and a % 2 == 1:
            return []
        # Force brut if a is even or e < 3 (for now)
        return [x for x in range(0, p**e) if x*x % p**e == a % p**e]

    # Check solution existence on odd prime
    ls = legendre_symbol(a, p)
    if ls == -1:
        return []

    # Case were a is 0 or p multiple
    if ls == 0:
        if a % p**e == 0:
            return [0]
        return []

    # Hensel lemma lifting from x^2 = a mod p solution
    x  = _prime_mod_sqrt(a, p)
    for i in range(1, e):
        f = x*x - a
        fd = 2*x
        t = - (f // p**i) * pow(fd, -1, p**i)
        x = x + t * p**i % p**(i+1)
    return [x, p**e - x]


while not won:
    n += 1
    print("n: ", n)
    
    a = pow(A1,n,MOD)
    b = getb(n)
    c = -N1 % MOD

    p2a = getp2(a)
    p2b = getp2(b)
    p2c = getp2(c)

    print("p2a: ", p2a)
    print("p2b: ", p2b)
    print("p2c: ", p2c)

    # no solution
    if p2b == 0:
        print("\n\n")
        continue

    if p2b > 0:
        print("p2b > 0")
        B = b // 2
        print("B: ", B)
        s = (pow(a,-2,MOD)*pow(B,2,MOD) - pow(a,-1,MOD)*c) % MOD
        print("s: ", s)
        r = getp2(s)
        print("r: ", r)
        q = s // 2**r
        print("q: ", q)

        if getp2(r) == 0 or q % 8 != 1:
            # no solution
            print("\n\n")
            continue
        else:
            # (x + a^-1 * B2) ** 2 = s (mod 2^n)
            print(pow(2,r // 2 + 2), " solutions exist")
            xx = prime_mod_sqrt(s, 2, 512)
            print("xx: ", xx)
            x = [(z - (pow(a,-1,MOD)*B)) % MOD for z in xx] #(xx - (pow(a,-1,MOD)*B)) % MOD
            
            for P in x:
                if isPrime(P):
                    Q = N1 // P
                    plaintext = solveRSA(P,Q)
                    if b'crypto{' in plaintext:
                        print("plaintext: ", plaintext)
                        won = True 
            
    print("\n\n")
