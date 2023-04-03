import numpy as np
from psutil import swap_memory
 
u = [87502093, 123094980]
v = [846835985, 9834798552]

v1 = np.array(u)
v2 = np.array(v)

m = 1

while m != 0:
    if np.linalg.norm(v1) > np.linalg.norm(v2):
        v1, v2 = v2, v1
    m = (np.dot(v1,v2))//(np.dot(v1,v1))
    print(m)
    if m == 0:
        break
    v2 = v2-m*v1

print(np.dot(v1,v2)) 