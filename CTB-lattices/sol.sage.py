

# This file was *autogenerated* from the file sol.sage
from sage.all_cmdline import *   # import sage library

_sage_const_33 = Integer(33); _sage_const_79 = Integer(79); _sage_const_29 = Integer(29); _sage_const_41 = Integer(41); _sage_const_47 = Integer(47); _sage_const_27 = Integer(27); _sage_const_39 = Integer(39); _sage_const_44 = Integer(44); _sage_const_90 = Integer(90); _sage_const_83 = Integer(83); _sage_const_58 = Integer(58); _sage_const_1 = Integer(1); _sage_const_38 = Integer(38); _sage_const_32 = Integer(32); _sage_const_13 = Integer(13); _sage_const_15 = Integer(15); _sage_const_96 = Integer(96); _sage_const_72 = Integer(72); _sage_const_82 = Integer(82); _sage_const_88 = Integer(88); _sage_const_23 = Integer(23); _sage_const_73300 = Integer(73300); _sage_const_167887 = Integer(167887); _sage_const_243754 = Integer(243754); _sage_const_254984 = Integer(254984); _sage_const_458756 = Integer(458756); _sage_const_0 = Integer(0); _sage_const_2 = Integer(2); _sage_const_3 = Integer(3); _sage_const_4 = Integer(4)
from itertools import permutations

P1 = matrix([[_sage_const_33 ,_sage_const_79 ,_sage_const_29 ,_sage_const_41 ,_sage_const_47 ],[_sage_const_79 ,_sage_const_27 ,_sage_const_39 ,_sage_const_79 ,_sage_const_44 ],[_sage_const_90 ,_sage_const_83 ,_sage_const_58 ,_sage_const_1 ,_sage_const_90 ],[_sage_const_38 ,_sage_const_32 ,_sage_const_13 ,_sage_const_15 ,_sage_const_96 ],[_sage_const_72 ,_sage_const_82 ,_sage_const_88 ,_sage_const_83 ,_sage_const_23 ]])

numbers = [_sage_const_73300 ,_sage_const_167887 ,_sage_const_243754 ,_sage_const_254984 ,_sage_const_458756 ]
combinations = permutations(numbers, len(numbers)) 

for i, combo in enumerate(combinations, _sage_const_1 ):
    P2 = Matrix([[combo[_sage_const_0 ]], [combo[_sage_const_1 ]], [combo[_sage_const_2 ]], [combo[_sage_const_3 ]], [combo[_sage_const_4 ]]])
    solution = P1.solve_right(P2) 
    if all(t.denominator()==_sage_const_1  for t in solution):
        print(solution)

