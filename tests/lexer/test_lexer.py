import pytest
from src.lexer.token_type import TokenType
from src.lexer.lexer import Lexer, LexerError

def test_basic_assignment():
    source = "x = 10 + 20"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert len(tokens) == 6
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].lexeme == "x"
    assert tokens[1].type == TokenType.ASSIGN
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].lexeme == "10"
    assert tokens[3].type == TokenType.PLUS
    assert tokens[4].type == TokenType.NUMBER
    assert tokens[4].lexeme == "20"
    assert tokens[5].type == TokenType.EOF

def test_whitespace_and_comments():
    source = """
    # This is a comment
    x = 5  # Inline comment
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    # Should only contain 'x', '=', '5', EOF
    assert len(tokens) == 4
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].lexeme == "x"
    assert tokens[1].type == TokenType.ASSIGN
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].lexeme == "5"
    assert tokens[3].type == TokenType.EOF

def test_decimal_numbers():
    source = "pi = 3.14159"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert len(tokens) == 4
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].lexeme == "3.14159"

def test_invalid_character():
    source = "x = 10 @ 2"
    lexer = Lexer(source)
    with pytest.raises(LexerError) as exc_info:
        lexer.tokenize()
    assert "Unexpected character: '@'" in str(exc_info.value)
    # Checks tracking of line/column
    assert exc_info.value.line == 1
    assert exc_info.value.column == 8

def test_invalid_number():
    source = "x = 10."
    lexer = Lexer(source)
    with pytest.raises(LexerError) as exc_info:
        lexer.tokenize()
    assert "Invalid number literal" in str(exc_info.value)
