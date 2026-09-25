import math
from typing import List, Union

def transpose(matrix: List[List[Union[int, float]]]) -> List[List[float]]:
    if not matrix:
        return []
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
    if abs(d) < 1e-12:
        raise ValueError("Matrix is singular and cannot be inverted (determinant is 0).")
    
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

def mat_add(A: List[List[Union[int, float]]], B: List[List[Union[int, float]]]) -> List[List[float]]:
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError(f"Cannot add matrices with shapes ({len(A)}x{len(A[0])}) and ({len(B)}x{len(B[0])}).")
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def mat_sub(A: List[List[Union[int, float]]], B: List[List[Union[int, float]]]) -> List[List[float]]:
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError(f"Cannot subtract matrices with shapes ({len(A)}x{len(A[0])}) and ({len(B)}x{len(B[0])}).")
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def mat_mul(A: List[List[Union[int, float]]], B: List[List[Union[int, float]]]) -> List[List[float]]:
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        raise ValueError(f"Matrix multiplication invalid: columns of A ({cols_A}) != rows of B ({rows_B}).")
    result = [[0.0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            result[i][j] = sum(A[i][k] * B[k][j] for k in range(cols_A))
    return result

def mat_get(matrix: List[List[Union[int, float]]], row: int, col: int) -> float:
    if row < 0 or row >= len(matrix) or col < 0 or col >= len(matrix[0]):
        raise IndexError(f"Matrix index ({row}, {col}) out of bounds for shape ({len(matrix)}, {len(matrix[0])}).")
    return matrix[row][col]

def format_matrix(matrix: List[List[Union[int, float]]]) -> str:
    lines = []
    for row in matrix:
        lines.append(" ".join(f"{x:g}" if isinstance(x, float) and x.is_integer() else f"{x}" for x in row))
    return "\n".join(lines)
