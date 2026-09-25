import math
from typing import List, Union

def mae(actual: List[Union[int, float]], predicted: List[Union[int, float]]) -> float:
    if len(actual) != len(predicted):
        raise ValueError(f"Actual ({len(actual)}) and predicted ({len(predicted)}) must have equal length.")
    if len(actual) == 0:
        raise ValueError("Arrays must not be empty.")
    return sum(abs(a - p) for a, p in zip(actual, predicted)) / len(actual)

def mse(actual: List[Union[int, float]], predicted: List[Union[int, float]]) -> float:
    if len(actual) != len(predicted):
        raise ValueError(f"Actual ({len(actual)}) and predicted ({len(predicted)}) must have equal length.")
    if len(actual) == 0:
        raise ValueError("Arrays must not be empty.")
    return sum((a - p) ** 2 for a, p in zip(actual, predicted)) / len(actual)

def rmse(actual: List[Union[int, float]], predicted: List[Union[int, float]]) -> float:
    return math.sqrt(mse(actual, predicted))

def r2(actual: List[Union[int, float]], predicted: List[Union[int, float]]) -> float:
    if len(actual) != len(predicted):
        raise ValueError(f"Actual ({len(actual)}) and predicted ({len(predicted)}) must have equal length.")
    n = len(actual)
    if n == 0:
        raise ValueError("Arrays must not be empty.")
    mean_actual = sum(actual) / n
    ss_tot = sum((a - mean_actual) ** 2 for a in actual)
    ss_res = sum((a - p) ** 2 for a, p in zip(actual, predicted))
    if ss_tot == 0:
        return 1.0 if ss_res == 0 else 0.0
    return 1.0 - (ss_res / ss_tot)
