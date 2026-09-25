from dataclasses import dataclass
from src.lexer.token_type import TokenType

@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token(type={self.type.name}, lexeme={repr(self.lexeme)}, line={self.line}, column={self.column})"
