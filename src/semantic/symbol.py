from dataclasses import dataclass
from typing import Optional, Tuple
from src.semantic.types import SemanticType

@dataclass
class Symbol:
    name: str
    type: SemanticType
    line: int
    column: int
    shape: Optional[Tuple[int, ...]] = None  # (rows, cols) for Matrix, (length,) for Vector
