from operator import xor

state = [
    [206, 243, 61, 34],
    [171, 11, 93, 31],
    [16, 200, 91, 108],
    [150, 3, 194, 51],
]

round_key = [
    [173, 129, 68, 82],
    [223, 100, 38, 109],
    [32, 189, 53, 8],
    [253, 48, 187, 78],
]

fin = [[0,0,0,0],
         [0,0,0,0],
         [0,0,0,0],
         [0,0,0,0],]

def add_round_key(s, k):
    for i in range(0,4): 
        for j in range(0,4):
            fin[i][j] = (s[i][j] ^ k[i][j])
    return fin

def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    arr = ""
    for i in range (0,4):
        for num in matrix[i]:
            arr += chr(num)
    return arr

print(add_round_key(state, round_key))

print(matrix2bytes(add_round_key(state, round_key)))
