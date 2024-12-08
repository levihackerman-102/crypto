from sympy.ntheory.modular import crt

from Crypto.Util.number import long_to_bytes

# challenge code
c = 3708354049649318175189820619077599798890688075815858391284996256924308912935262733471980964003143534200740113874286537588889431819703343015872364443921848
p = 75000325607193724293694446403116223058337764961074929316352803137087536131383
q = 69376057129404174647351914434400429820318738947745593069596264646867332546443
N = p * q

def root_all(ciph):
    m_p = pow(ciph, (p + 1) // 4, p)
    m_q = pow(ciph, (q + 1) // 4, q)

    r1 = crt([p, q], [m_p, m_q])[0]
    r2 = -r1 % N

    r3 = crt([p, q], [m_p, -m_q])[0]
    r4 = -r3 % N

    s = set()
    s.add(r1)
    s.add(r2)
    s.add(r3)
    s.add(r4)
    return s


round1 = root_all(c)

round2 = set()
for r in round1:
    round2 |= root_all(r)

round3 = set()
for r in round2:
    round3 |= root_all(r)

round4 = set()
for r in round3:
    round4 |= root_all(r)

for x in round4:
    print(long_to_bytes(x))
