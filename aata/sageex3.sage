C = CyclicPermutationGroup(8)
D = DihedralGroup(4)
print(C)
print(D)

print(C.order() == D.order())
print(C.is_abelian())
print(D.is_abelian())

print(C.cayley_table())
print(D.cayley_table())

print(C.subgroups())
print(D.subgroups())

