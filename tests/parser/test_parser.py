import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser, ParserError
from src.parser.ast import (
    ProgramNode, AssignmentNode, ShowNode, BinaryOperationNode,
    UnaryOperationNode, NumberNode, IdentifierNode, FunctionCallNode
)

def test_operator_precedence():
    source = "x = 10 + 20 * 5"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    assert isinstance(ast, ProgramNode)
    assert len(ast.statements) == 1
    
    stmt = ast.statements[0]
    assert isinstance(stmt, AssignmentNode)
    assert stmt.name == "x"
    
    # Value should be BinaryOperationNode(10, "+", BinaryOperationNode(20, "*", 5))
    expr = stmt.value
    assert isinstance(expr, BinaryOperationNode)
    assert expr.operator == "+"
    assert isinstance(expr.left, NumberNode)
    assert expr.left.value == 10
    
    right = expr.right
    assert isinstance(right, BinaryOperationNode)
    assert right.operator == "*"
    assert isinstance(right.left, NumberNode)
    assert right.left.value == 20
    assert isinstance(right.right, NumberNode)
    assert right.right.value == 5

def test_parentheses_precedence():
    source = "x = (10 + 20) * 5"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    assert isinstance(ast, ProgramNode)
    stmt = ast.statements[0]
    expr = stmt.value
    
    # Value should be BinaryOperationNode(BinaryOperationNode(10, "+", 20), "*", 5)
    assert isinstance(expr, BinaryOperationNode)
    assert expr.operator == "*"
    assert isinstance(expr.right, NumberNode)
    assert expr.right.value == 5
    
    left = expr.left
    assert isinstance(left, BinaryOperationNode)
    assert left.operator == "+"
    assert isinstance(left.left, NumberNode)
    assert left.left.value == 10
    assert isinstance(left.right, NumberNode)
    assert left.right.value == 20

def test_function_call():
    source = "show sqrt(25)"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    assert isinstance(ast, ProgramNode)
    assert len(ast.statements) == 1
    stmt = ast.statements[0]
    assert isinstance(stmt, ShowNode)
    
    func = stmt.value
    assert isinstance(func, FunctionCallNode)
    assert func.name == "sqrt"
    assert len(func.arguments) == 1
    assert isinstance(func.arguments[0], NumberNode)
    assert func.arguments[0].value == 25

def test_parser_error():
    source = "x = 10 +"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    with pytest.raises(ParserError) as exc_info:
        parser.parse()
    assert "Expected expression" in str(exc_info.value)
