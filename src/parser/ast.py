from dataclasses import dataclass, field
from typing import Union, List, Optional

@dataclass
class ASTNode:
    pass

@dataclass
class ProgramNode(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"ProgramNode(statements={self.statements})"

@dataclass
class AssignmentNode(ASTNode):
    name: str
    value: ASTNode
    line: int
    column: int
    is_matrix_decl: bool = False

    def __repr__(self) -> str:
        decl = "matrix " if self.is_matrix_decl else ""
        return f"AssignmentNode({decl}{repr(self.name)} = {self.value})"

@dataclass
class ShowNode(ASTNode):
    value: ASTNode
    line: int
    column: int

    def __repr__(self) -> str:
        return f"ShowNode(value={self.value})"

@dataclass
class SolveNode(ASTNode):
    equations: List[str]
    line: int
    column: int

    def __repr__(self) -> str:
        return f"SolveNode(equations={self.equations})"

@dataclass
class BinaryOperationNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode
    line: int
    column: int

    def __repr__(self) -> str:
        return f"BinaryOperationNode(left={self.left}, operator={repr(self.operator)}, right={self.right})"

@dataclass
class UnaryOperationNode(ASTNode):
    operator: str
    operand: ASTNode
    line: int
    column: int

    def __repr__(self) -> str:
        return f"UnaryOperationNode(operator={repr(self.operator)}, operand={self.operand})"

@dataclass
class NumberNode(ASTNode):
    value: Union[int, float]
    line: int
    column: int

    def __repr__(self) -> str:
        return f"NumberNode(value={self.value})"

@dataclass
class IdentifierNode(ASTNode):
    name: str
    line: int
    column: int

    def __repr__(self) -> str:
        return f"IdentifierNode(name={repr(self.name)})"

@dataclass
class FunctionCallNode(ASTNode):
    name: str
    arguments: List[ASTNode]
    line: int
    column: int

    def __repr__(self) -> str:
        return f"FunctionCallNode(name={repr(self.name)}, arguments={self.arguments})"

@dataclass
class VectorNode(ASTNode):
    elements: List[ASTNode]
    line: int
    column: int

    def __repr__(self) -> str:
        return f"VectorNode(elements={self.elements})"

@dataclass
class MatrixNode(ASTNode):
    rows: List[List[ASTNode]]
    line: int
    column: int

    def __repr__(self) -> str:
        return f"MatrixNode(rows={self.rows})"

@dataclass
class MatrixIndexNode(ASTNode):
    matrix_name: str
    row: ASTNode
    col: ASTNode
    line: int
    column: int

    def __repr__(self) -> str:
        return f"MatrixIndexNode({self.matrix_name}[{self.row}][{self.col}])"
