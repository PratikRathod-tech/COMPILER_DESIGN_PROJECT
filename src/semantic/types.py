from enum import Enum, auto

class SemanticType(Enum):
    NUMBER = auto()
    BOOLEAN = auto()
    VECTOR = auto()
    MATRIX = auto()
    FUNCTION = auto()
    UNKNOWN = auto()
