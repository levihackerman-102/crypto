from itertools import permutations

P1 = matrix([[33,79,29,41,47],[79,27,39,79,44],[90,83,58,1,90],[38,32,13,15,96],[72,82,88,83,23]])

numbers = [73300,167887,243754,254984,458756]
combinations = permutations(numbers, len(numbers)) 

for i, combo in enumerate(combinations, 1):
    P2 = Matrix([[combo[0]], [combo[1]], [combo[2]], [combo[3]], [combo[4]]])
    solution = P1.solve_right(P2) 
    if all(t.denominator()==1 for t in solution):
        print(solution)
