import pytest
from src.compiler.compiler import Compiler
from src.semantic.semantic_analyzer import SemanticError

def test_basic_integration(capsys):
    compiler = Compiler()
    source = """
    x = 10
    y = 20
    z = x + y
    show z
    """
    tokens, ast, analyzer, ir, opt_ir, code = compiler.compile(source)
    compiler.run(code)
    captured = capsys.readouterr()
    assert "30" in captured.out

def test_functions_integration(capsys):
    compiler = Compiler()
    source = """
    x = 25
    show sqrt(x)
    """
    tokens, ast, analyzer, ir, opt_ir, code = compiler.compile(source)
    compiler.run(code)
    captured = capsys.readouterr()
    assert "5.0" in captured.out

def test_precedence_integration(capsys):
    compiler = Compiler()
    source = """
    x = 10 + 20 * 5
    show x
    """
    tokens, ast, analyzer, ir, opt_ir, code = compiler.compile(source)
    compiler.run(code)
    captured = capsys.readouterr()
    assert "110" in captured.out

def test_errors_integration():
    compiler = Compiler()
    source = """
    raduis = 10
    area = pi * radius^2
    show area
    """
    with pytest.raises(SemanticError) as exc_info:
        compiler.compile(source)
    
    assert "Variable 'radius' is not defined" in str(exc_info.value)
    assert "Did you mean 'raduis'?" in str(exc_info.value)

def test_vectors_integration(capsys):
    compiler = Compiler()
    source = """
    v = [1, 2, 3]
    show norm(v)
    """
    tokens, ast, analyzer, ir, opt_ir, code = compiler.compile(source)
    compiler.run(code)
    captured = capsys.readouterr()
    # norm([1,2,3]) = sqrt(1+4+9) = sqrt(14) approx 3.7416
    assert "3.741" in captured.out

def test_matrices_integration(capsys):
    compiler = Compiler()
    source = """
    A = [
        [1, 2],
        [3, 4]
    ]
    show det(A)
    """
    tokens, ast, analyzer, ir, opt_ir, code = compiler.compile(source)
    compiler.run(code)
    captured = capsys.readouterr()
    # det(A) = 1*4 - 2*3 = -2
    assert "-2" in captured.out
