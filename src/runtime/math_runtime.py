import math
from typing import List, Union

# Mathematical constants
pi = math.pi
e = math.e

# Basic math functions
def sqrt(x: Union[int, float]) -> float:
    return math.sqrt(x)

def sin(x: Union[int, float]) -> float:
    return math.sin(x)

def cos(x: Union[int, float]) -> float:
    return math.cos(x)

def tan(x: Union[int, float]) -> float:
    return math.tan(x)

def log(x: Union[int, float]) -> float:
    return math.log(x)

def abs_val(x: Union[int, float]) -> float:
    return abs(x)

# Vector functions
def dot(v1: List[Union[int, float]], v2: List[Union[int, float]]) -> float:
    if len(v1) != len(v2):
        raise ValueError("Vectors must be of the same length for dot product.")
    return sum(x * y for x, y in zip(v1, v2))

def norm(v: List[Union[int, float]]) -> float:
    return math.sqrt(sum(x ** 2 for x in v))

# Matrix functions
def transpose(matrix: List[List[Union[int, float]]]) -> List[List[float]]:
    return [list(x) for x in zip(*matrix)]

def det(matrix: List[List[Union[int, float]]]) -> float:
    n = len(matrix)
    if n == 0:
        return 1.0
    if n == 1:
        return float(matrix[0][0])
    if n == 2:
        return float(matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0])
    
    total = 0.0
    for c in range(n):
        sub_matrix = [row[:c] + row[c+1:] for row in matrix[1:]]
        total += ((-1) ** c) * matrix[0][c] * det(sub_matrix)
    return total

def inverse(matrix: List[List[Union[int, float]]]) -> List[List[float]]:
    d = det(matrix)
    if d == 0:
        raise ValueError("Matrix is singular and cannot be inverted.")
    
    n = len(matrix)
    if n == 1:
        return [[1.0 / matrix[0][0]]]
        
    cofactors = []
    for r in range(n):
        cofactor_row = []
        for c in range(n):
            sub = [row[:c] + row[c+1:] for row_idx, row in enumerate(matrix) if row_idx != r]
            cofactor_row.append(((-1) ** (r + c)) * det(sub))
        cofactors.append(cofactor_row)
        
    cofactors_t = transpose(cofactors)
    return [[val / d for val in row] for row in cofactors_t]
