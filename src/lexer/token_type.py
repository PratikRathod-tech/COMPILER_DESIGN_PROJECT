from enum import Enum, auto

class TokenType(Enum):
    # Literals
    NUMBER = auto()
    IDENTIFIER = auto()

    # Operators
    PLUS = auto()       # +
    MINUS = auto()      # -
    MULTIPLY = auto()   # *
    DIVIDE = auto()     # /
    MODULO = auto()     # %
    POWER = auto()      # ^
    ASSIGN = auto()     # =

    # Delimiters
    LPAREN = auto()     # (
    RPAREN = auto()     # )
    LBRACKET = auto()   # [
    RBRACKET = auto()   # ]
    COMMA = auto()      # ,
    COLON = auto()      # :

    # Keywords
    SHOW = auto()       # show
    MATRIX = auto()     # matrix
    SOLVE = auto()      # solve

    # End of file
    EOF = auto()
