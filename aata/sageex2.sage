p = next_prime(pow(10,8))
q = next_prime(p)
print(p,q)

g,x,y = xgcd(p,q) 
print(x,y)

c = 4598037234
f =  factor(c)
print(f)
