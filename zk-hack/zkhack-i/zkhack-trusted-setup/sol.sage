# the fields F1 = F_q and F2 = F_{q^2}, and u in F2 with u^2 + 1 = 0
q = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
F1 = GF(q)
R.<x> = PolynomialRing(F1)
F2.<u> = F1.extension(x^2+1)

# the elliptic curves E1 and E2 as described in the write-up
E1 = EllipticCurve(F1,[0,4])
E2 = EllipticCurve(F2,[0,4*(1+u)])

# the points g1, [s]g1, g2, [s]g2 (extracted from the puzzle files)
g1 = E1(0x0F99F411A5F6C484EC5CAD7B9F9C0F01A3D2BB73759BB95567F1FE4910331D32B95ED87E36681230273C9A6677BE3A69, 0x12978C5E13A226B039CE22A0F4961D329747F0B78350988DAB4C1263455C826418A667CA97AC55576228FC7AA77D33E5)
sg1 = E1(0x16C2385B2093CC3EDBC0F2257E8F23E98E775F8F6628767E5F4FC0E495285B95B1505F487102FE083E65DC8E9E3A9181, 0x0F4B73F63C6FD1F924EAE2982426FC94FBD03FCEE12D9FB01BAF52BE1246A14C53C152D64ED312494A2BC32C4A3E7F9A)
g2 = E2(0x1173F10AD9F2DBEE8B6C0BB2624B05D72EEC87925F5C3633E2C000E699A580B842D3F35AF1BE77517C86AEBCA1130AE4 + u*0x0434043A97DA28EF7100AE559167FC613F057B85451476ABABB27CFF0238A32831A0B4D14BA83C4F97247C8AC339841F, 0x0BEBEC70446CB91BB3D4DC5C8412915E99D612D8807C950AB06BC41583F528FDA9F42EC0FE7CD2991638187EF44258D3 + u*0x19528E3B5C90C73A7092BB9AFDC73F86C838F551CCD9DBBA5CC6244CF76AB3372193DBE5B62383FAAE728728D4C1E649)
sg2 = E2(0x165830F15309C878BFE6DD55697860B8823C1AFBDADCC2EF3CD52B56D4956C05A099D52FE4545816830C525F5484A5FA + u*0x179E34EB67D9D2DD32B224CDBA57D4BB7CF562B4A3E33382E88F33882D91663B14738B6772BF53A24653CE1DD2BFE2FA, 0x150598FC4225B44437EC604204BE06A2040FD295A28230B789214B1B12BF9C9DAE6F3759447FD195E92E2B42E03B5006 + u*0x12E23B19E117418C568D4FF05B7824E5B54673C3C08D8BCD6D8D107955287A2B075100A51C81EBA44BF5A1ABAD4764A8)

r = 0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001
ord_g1 = g1.order()
ord_g2 = 13 * 23 * 2713 * 11953 * 262069 * 402096035359507321594726366720466575392706800671181159425656785868777272553337714697862511267018014931937703598282857976535744623203249 * r

# use pohlig-hellman

def compute_s_mod_p_g1(p):
    lamb = Integer(ord_g1/p)
    return (lamb * g1).discrete_log(lamb * sg1)

def compute_s_mod_p_g2(p):
    lamb = Integer(ord_g2/p)
    return (lamb * g2).discrete_log(lamb * sg2, ord=p)

p_g1 = [3, 11, 10177, 859267, 52437899]
p_g2 = [13, 23, 2713, 11953, 262069]
s_mod_p_g1 = [compute_s_mod_p_g1(n) for n in p_g1]
s_mod_p_g2 = [compute_s_mod_p_g2(n) for n in p_g2]

s_temp = crt(s_mod_p_g1 + s_mod_p_g2, p_g1 + p_g2)

m = prod(p_g1 + p_g2)
current_point = s_temp * g1
diff_point = m * g1
k = 0

while current_point != sg1:
    current_point = current_point + diff_point
    k = k + 1

s = s_temp + k * m
print(s * g1 == sg1)
print(s)