n = int(input('n = '))
m = prime_pi(n)-1
print(m)

p = Primes()
st = 2
cnt = 0
pr = []
while cnt < m:
    pr.append(st)
    st = p.next(st)
    cnt += 1
print(pr)

o = Zmod(n).list_of_elements_of_multiplicative_group()
print(o)

