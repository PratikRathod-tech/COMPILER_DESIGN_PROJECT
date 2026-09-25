import pytest
from src.compiler.compiler import Compiler
from src.math_engine.matrix import mat_add, mat_sub, mat_mul, det, transpose, inverse
from src.math_engine.equations import solve_single_equation, solve_system_2x2
from src.math_engine.metrics import mae, mse, rmse, r2
from src.semantic.semantic_analyzer import SemanticError

def test_manual_metrics():
    actual = [3.0, -0.5, 2.0, 7.0]
    predicted = [2.5, 0.0, 2.0, 8.0]

    assert mae(actual, predicted) == 0.5
    assert mse(actual, predicted) == 0.375
    assert round(rmse(actual, predicted), 4) == 0.6124
    assert round(r2(actual, predicted), 4) == 0.9486

def test_manual_matrix():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    C = mat_mul(A, B)
    assert C == [[19, 22], [43, 50]]
    assert det(A) == -2
    assert transpose(A) == [[1, 3], [2, 4]]

def test_linear_equations():
    sol1, steps1 = solve_single_equation("2*x + 5 = 15")
    assert sol1["x"] == 5.0

    sol2, steps2 = solve_system_2x2("2*x + y = 10", "x - y = 2")
    assert sol2["x"] == 4.0
    assert sol2["y"] == 2.0

def test_compiler_pipeline_phases():
    compiler = Compiler()
    res = compiler.get_phase_outputs("solve 2*x + 5 = 15")
    assert res["ml_category"] == "LINEAR_EQUATION"
    assert "x = 5" in res["execution"]
    assert "ast" in res
    assert "symbols" in res
    assert "ir" in res
    assert "opt_ir" in res

def test_matrix_semantic_dimension_error():
    compiler = Compiler()
    with pytest.raises(SemanticError) as exc_info:
        compiler.compile("matrix A = [[1, 2], [3]]")
    assert "Invalid matrix dimensions" in str(exc_info.value)

def test_metric_length_mismatch_error():
    compiler = Compiler()
    with pytest.raises(SemanticError) as exc_info:
        compiler.compile("""
        actual = [1, 2, 3]
        predicted = [1, 2]
        show mae(actual, predicted)
        """)
    assert "equal length" in str(exc_info.value)
