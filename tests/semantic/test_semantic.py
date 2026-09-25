import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.semantic_analyzer import SemanticAnalyzer, SemanticError

def test_valid_variables():
    source = """
    x = 10
    y = x + 5
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)  # Should not raise any error

def test_undefined_variable():
    source = "y = x + 5"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    analyzer = SemanticAnalyzer()
    with pytest.raises(SemanticError) as exc_info:
        analyzer.analyze(ast)
    assert "Variable 'x' is not defined" in str(exc_info.value)

def test_ai_suggestion():
    source = """
    raduis = 10
    area = pi * radius^2
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    analyzer = SemanticAnalyzer()
    with pytest.raises(SemanticError) as exc_info:
        analyzer.analyze(ast)
    
    assert "Variable 'radius' is not defined" in str(exc_info.value)
    assert "Did you mean 'raduis'?" in str(exc_info.value)

def test_division_by_zero():
    source = "x = 10 / 0"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    analyzer = SemanticAnalyzer()
    with pytest.raises(SemanticError) as exc_info:
        analyzer.analyze(ast)
    assert "Division by zero." in str(exc_info.value)

def test_math_domain_error():
    source = "x = sqrt(-25)"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    analyzer = SemanticAnalyzer()
    with pytest.raises(SemanticError) as exc_info:
        analyzer.analyze(ast)
    assert "Mathematical domain error" in str(exc_info.value)
