from src.lexer.token import Token
from src.lexer.token_type import TokenType

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Lexical Error at line {line}, column {column}: {message}")
        self.message = message
        self.line = line
        self.column = column

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def error(self, message: str) -> None:
        raise LexerError(message, self.line, self.column)

    def peek(self) -> str:
        if self.position >= len(self.source):
            return '\0'
        return self.source[self.position]

    def advance(self) -> str:
        char = self.peek()
        self.position += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def tokenize(self) -> list[Token]:
        tokens = []
        while self.position < len(self.source):
            char = self.peek()

            if char.isspace():
                self.advance()
                continue

            if char == '#':
                # Skip comment line
                while self.peek() != '\n' and self.peek() != '\0':
                    self.advance()
                continue

            # Multi-character tokens
            if char.isdigit():
                tokens.append(self.read_number())
                continue

            if char.isalpha() or char == '_':
                tokens.append(self.read_identifier_or_keyword())
                continue

            # Single-character tokens
            start_line = self.line
            start_column = self.column

            if char == '+':
                self.advance()
                tokens.append(Token(TokenType.PLUS, "+", start_line, start_column))
            elif char == '-':
                self.advance()
                tokens.append(Token(TokenType.MINUS, "-", start_line, start_column))
            elif char == '*':
                self.advance()
                tokens.append(Token(TokenType.MULTIPLY, "*", start_line, start_column))
            elif char == '/':
                self.advance()
                tokens.append(Token(TokenType.DIVIDE, "/", start_line, start_column))
            elif char == '%':
                self.advance()
                tokens.append(Token(TokenType.MODULO, "%", start_line, start_column))
            elif char == '^':
                self.advance()
                tokens.append(Token(TokenType.POWER, "^", start_line, start_column))
            elif char == '=':
                self.advance()
                tokens.append(Token(TokenType.ASSIGN, "=", start_line, start_column))
            elif char == ':':
                self.advance()
                tokens.append(Token(TokenType.COLON, ":", start_line, start_column))
            elif char == '(':
                self.advance()
                tokens.append(Token(TokenType.LPAREN, "(", start_line, start_column))
            elif char == ')':
                self.advance()
                tokens.append(Token(TokenType.RPAREN, ")", start_line, start_column))
            elif char == '[':
                self.advance()
                tokens.append(Token(TokenType.LBRACKET, "[", start_line, start_column))
            elif char == ']':
                self.advance()
                tokens.append(Token(TokenType.RBRACKET, "]", start_line, start_column))
            elif char == ',':
                self.advance()
                tokens.append(Token(TokenType.COMMA, ",", start_line, start_column))
            else:
                self.error(f"Unexpected character: {repr(char)}")

        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens

    def read_number(self) -> Token:
        start_line = self.line
        start_column = self.column
        lexeme_chars = []

        while self.peek().isdigit():
            lexeme_chars.append(self.advance())

        if self.peek() == '.':
            lexeme_chars.append(self.advance())
            if not self.peek().isdigit():
                self.error("Invalid number literal: missing decimal digits")
            while self.peek().isdigit():
                lexeme_chars.append(self.advance())

        lexeme = "".join(lexeme_chars)
        return Token(TokenType.NUMBER, lexeme, start_line, start_column)

    def read_identifier_or_keyword(self) -> Token:
        start_line = self.line
        start_column = self.column
        lexeme_chars = []

        while self.peek().isalnum() or self.peek() == '_':
            lexeme_chars.append(self.advance())

        lexeme = "".join(lexeme_chars)
        
        keywords = {
            "show": TokenType.SHOW,
            "matrix": TokenType.MATRIX,
            "solve": TokenType.SOLVE
        }
        
        token_type = keywords.get(lexeme, TokenType.IDENTIFIER)
        return Token(token_type, lexeme, start_line, start_column)
