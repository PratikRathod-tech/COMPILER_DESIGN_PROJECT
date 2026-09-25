from typing import Union, List, Any
from src.parser.ast import (
    ASTNode, ProgramNode, AssignmentNode, ShowNode, BinaryOperationNode,
    UnaryOperationNode, NumberNode, IdentifierNode, FunctionCallNode,
    VectorNode, MatrixNode, SolveNode, MatrixIndexNode
)
from src.ir.instruction import IRInstruction
from src.ir.ir_program import IRProgram

class IRGenerator:
    def __init__(self):
        self.program = IRProgram()
        self.temp_counter = 0

    def new_temp(self) -> str:
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def generate(self, node: ASTNode) -> IRProgram:
        self.visit(node)
        return self.program

    def visit(self, node: ASTNode) -> Any:
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: ASTNode) -> Any:
        raise NotImplementedError(f"No visit_{type(node).__name__} method defined.")

    def visit_ProgramNode(self, node: ProgramNode) -> None:
        for stmt in node.statements:
            self.visit(stmt)

    def visit_SolveNode(self, node: SolveNode) -> None:
        eq_temps = []
        for eq_str in node.equations:
            t = self.new_temp()
            self.program.add_instruction(IRInstruction("EQUATION", eq_str, result=t))
            eq_temps.append(t)
        
        solve_temp = self.new_temp()
        if len(eq_temps) == 1:
            self.program.add_instruction(IRInstruction("SOLVE_LINEAR", eq_temps[0], result=solve_temp))
        else:
            self.program.add_instruction(IRInstruction("SOLVE_SYSTEM", eq_temps, result=solve_temp))

    def visit_AssignmentNode(self, node: AssignmentNode) -> None:
        val = self.visit(node.value)
        self.program.add_instruction(IRInstruction("ASSIGN", val, result=node.name))

    def visit_ShowNode(self, node: ShowNode) -> None:
        val = self.visit(node.value)
        self.program.add_instruction(IRInstruction("SHOW", val))

    def visit_NumberNode(self, node: NumberNode) -> Any:
        return node.value

    def visit_IdentifierNode(self, node: IdentifierNode) -> Any:
        return node.name

    def visit_MatrixIndexNode(self, node: MatrixIndexNode) -> str:
        row = self.visit(node.row)
        col = self.visit(node.col)
        temp = self.new_temp()
        self.program.add_instruction(IRInstruction("MAT_GET", node.matrix_name, [row, col], result=temp))
        return temp

    def visit_BinaryOperationNode(self, node: BinaryOperationNode) -> str:
        left = self.visit(node.left)
        right = self.visit(node.right)
        temp = self.new_temp()
        self.program.add_instruction(IRInstruction(node.operator, left, right, result=temp))
        return temp

    def visit_UnaryOperationNode(self, node: UnaryOperationNode) -> str:
        operand = self.visit(node.operand)
        temp = self.new_temp()
        op = "NEG" if node.operator == "-" else "POS"
        self.program.add_instruction(IRInstruction(op, operand, result=temp))
        return temp

    def visit_FunctionCallNode(self, node: FunctionCallNode) -> str:
        args = [self.visit(arg) for arg in node.arguments]
        temp = self.new_temp()
        self.program.add_instruction(IRInstruction("CALL", node.name, args, result=temp))
        return temp

    def visit_VectorNode(self, node: VectorNode) -> str:
        elems = [self.visit(elem) for elem in node.elements]
        temp = self.new_temp()
        self.program.add_instruction(IRInstruction("VECTOR", elems, result=temp))
        return temp

    def visit_MatrixNode(self, node: MatrixNode) -> str:
        rows = []
        for row in node.rows:
            rows.append([self.visit(elem) for elem in row])
        temp = self.new_temp()
        self.program.add_instruction(IRInstruction("MATRIX", rows, result=temp))
        return temp
