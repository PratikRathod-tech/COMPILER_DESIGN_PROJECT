from typing import Set, Dict, Optional, Union, Tuple, List, Any
from src.parser.ast import (
    ASTNode, ProgramNode, AssignmentNode, ShowNode, BinaryOperationNode,
    UnaryOperationNode, NumberNode, IdentifierNode, FunctionCallNode,
    VectorNode, MatrixNode, SolveNode, MatrixIndexNode
)
from src.semantic.types import SemanticType
from src.semantic.symbol import Symbol
from src.semantic.symbol_table import SymbolTable
from src.ai.error_suggester import ErrorSuggester
from src.math_engine.equations import parse_linear_side

class SemanticError(Exception):
    def __init__(self, message: str, line: int = 1, column: int = 1):
        super().__init__(f"SEMANTIC ERROR\n\n{message}")
        self.message = message
        self.line = line
        self.column = column

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.error_suggester = ErrorSuggester()
        self.features: Dict[str, Any] = {
            "has_matrix": False,
            "has_equation": False,
            "has_metric": False,
            "matrix_dimensions": 0,
            "operation_type": 0,
            "variable_count": 0
        }
        self.operation_name: str = "Evaluation"
        self.explanation: str = ""
        self.initialize_builtins()

    def initialize_builtins(self) -> None:
        # Math constants
        self.symbol_table.define("pi", Symbol("pi", SemanticType.NUMBER, 0, 0))
        self.symbol_table.define("e", Symbol("e", SemanticType.NUMBER, 0, 0))

        # Basic math functions
        for f in ["sqrt", "sin", "cos", "tan", "log", "abs", "dot", "norm"]:
            self.symbol_table.define(f, Symbol(f, SemanticType.FUNCTION, 0, 0))

        # Built-in metric functions
        for f in ["mae", "mse", "rmse", "r2"]:
            self.symbol_table.define(f, Symbol(f, SemanticType.FUNCTION, 0, 0))
        # Built-in matrix functions
        for f in ["transpose", "determinant", "det", "inverse"]:
            self.symbol_table.define(f, Symbol(f, SemanticType.FUNCTION, 0, 0))

    def analyze(self, node: ASTNode) -> None:
        self.visit(node)
        # Update variable count in features
        user_syms = [k for k in self.symbol_table.symbols if self.symbol_table.symbols[k].type != SemanticType.FUNCTION]
        self.features["variable_count"] = len(user_syms)

    def visit(self, node: ASTNode) -> Tuple[SemanticType, Optional[Tuple[int, ...]]]:
        """
        Returns (SemanticType, shape)
        where shape is (rows, cols) for Matrix, (length,) for Vector, None otherwise.
        """
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: ASTNode) -> Tuple[SemanticType, Optional[Tuple[int, ...]]]:
        raise NotImplementedError(f"No visit_{type(node).__name__} method defined.")

    def visit_ProgramNode(self, node: ProgramNode) -> Tuple[SemanticType, Optional[Tuple[int, ...]]]:
        for stmt in node.statements:
            self.visit(stmt)
        return SemanticType.UNKNOWN, None

    def visit_SolveNode(self, node: SolveNode) -> Tuple[SemanticType, Optional[Tuple[int, ...]]]:
        self.features["has_equation"] = True
        self.features["operation_type"] = 2
        self.operation_name = "Linear Equation"

        all_vars = set()
        for eq_str in node.equations:
            if '=' not in eq_str:
                raise SemanticError("Missing '=' in linear equation.", node.line, node.column)
            left_str, right_str = eq_str.split('=', 1)
            try:
                left_c = parse_linear_side(left_str)
                right_c = parse_linear_side(right_str)
            except Exception as e:
                raise SemanticError(f"Invalid equation syntax: {e}", node.line, node.column)
                
            vars_in_eq = set(k for k in left_c if k != '') | set(k for k in right_c if k != '')
            all_vars.update(vars_in_eq)

        if not all_vars:
            raise SemanticError("No variable found in linear equation.", node.line, node.column)

        if len(node.equations) == 1 and len(all_vars) > 1:
            raise SemanticError(f"Single equation contains multiple variables {list(all_vars)}. Use 'solve:' block for multiple equations.", node.line, node.column)

        if len(node.equations) == 2 and len(all_vars) != 2:
            raise SemanticError(f"System of 2 equations must have exactly 2 variables, found {len(all_vars)} ({all_vars}).", node.line, node.column)

        # Register variable symbols
        for v in all_vars:
            self.symbol_table.define(v, Symbol(v, SemanticType.NUMBER, node.line, node.column))

        return SemanticType.NUMBER, None

    def visit_AssignmentNode(self, node: AssignmentNode) -> Tuple[SemanticType, Optional[Tuple[int, ...]]]:
        val_type, shape = self.visit(node.value)
        if node.is_matrix_decl:
            if val_type != SemanticType.MATRIX:
                raise SemanticError(f"Variable '{node.name}' declared as matrix but assigned {val_type.name}.", node.line, node.column)
            self.features["has_matrix"] = True
            self.features["matrix_dimensions"] = 2

        self.symbol_table.define(node.name, Symbol(node.name, val_type, node.line, node.column, shape=shape))
        return val_type, shape

    def visit_ShowNode(self, node: ShowNode) -> Tuple[SemanticType, Optional[Tuple[int, ...]]]:
        val_type, shape = self.visit(node.value)
        return val_type, shape

    def visit_NumberNode(self, node: NumberNode) -> Tuple[SemanticType, Optional[Tuple[int, ...]]]:
        return SemanticType.NUMBER, None

    def visit_IdentifierNode(self, node: IdentifierNode) -> Tuple[SemanticType, Optional[Tuple[int, ...]]]:
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            all_names = self.symbol_table.get_all_names()
            var_names = [name for name in all_names if self.symbol_table.lookup(name).type != SemanticType.FUNCTION]
            suggestion = self.error_suggester.suggest(node.name, var_names)
            msg = f"Variable '{node.name}' is not defined."
            if suggestion:
                msg += f"\n\nSuggestion:\nDid you mean '{suggestion}'?"
            raise SemanticError(msg, node.line, node.column)
        if symbol.type == SemanticType.FUNCTION:
            raise SemanticError(f"Function '{node.name}' cannot be used as a variable.", node.line, node.column)
        return symbol.type, symbol.shape

    def visit_MatrixIndexNode(self, node: MatrixIndexNode) -> Tuple[SemanticType, Optional[Tuple[int, ...]]]:
        symbol = self.symbol_table.lookup(node.matrix_name)
        if not symbol:
            raise SemanticError(f"Variable '{node.matrix_name}' is not defined.", node.line, node.column)
        if symbol.type != SemanticType.MATRIX:
            raise SemanticError(f"Variable '{node.matrix_name}' is not a matrix.", node.line, node.column)

        row_t, _ = self.visit(node.row)
        col_t, _ = self.visit(node.col)
        if row_t != SemanticType.NUMBER or col_t != SemanticType.NUMBER:
            raise SemanticError(f"Matrix indices must be integers/numbers.", node.line, node.column)
        
        self.features["has_matrix"] = True
        return SemanticType.NUMBER, None

    def visit_VectorNode(self, node: VectorNode) -> Tuple[SemanticType, Optional[Tuple[int, ...]]]:
        for elem in node.elements:
            elem_type, _ = self.visit(elem)
            if elem_type != SemanticType.NUMBER:
                raise SemanticError(f"Vector elements must be numbers, found {elem_type.name}.", node.line, node.column)
        return SemanticType.VECTOR, (len(node.elements),)

    def visit_MatrixNode(self, node: MatrixNode) -> Tuple[SemanticType, Optional[Tuple[int, ...]]]:
        self.features["has_matrix"] = True
        self.features["matrix_dimensions"] = 2

        if not node.rows:
            return SemanticType.MATRIX, (0, 0)

        expected_cols = len(node.rows[0])
        for r_idx, row in enumerate(node.rows):
            if len(row) != expected_cols:
                raise SemanticError(
                    f"Invalid matrix dimensions.\n\n"
                    f"Row 1: {expected_cols} elements\n"
                    f"Row {r_idx + 1}: {len(row)} elements\n\n"
                    f"All rows must have equal dimensions.",
                    node.line, node.column
                )
            for elem in row:
                elem_type, _ = self.visit(elem)
                if elem_type != SemanticType.NUMBER:
                    raise SemanticError(f"Matrices can only contain numbers, found {elem_type.name}.", node.line, node.column)

        return SemanticType.MATRIX, (len(node.rows), expected_cols)

    def visit_BinaryOperationNode(self, node: BinaryOperationNode) -> Tuple[SemanticType, Optional[Tuple[int, ...]]]:
        left_type, left_shape = self.visit(node.left)
        right_type, right_shape = self.visit(node.right)

        if left_type == SemanticType.MATRIX or right_type == SemanticType.MATRIX:
            self.features["has_matrix"] = True
            self.features["matrix_dimensions"] = 2
            self.features["operation_type"] = 1

            if left_type == SemanticType.MATRIX and right_type == SemanticType.MATRIX:
                if node.operator in ["+", "-"]:
                    if left_shape and right_shape and left_shape != right_shape:
                        raise SemanticError(
                            f"Matrix {node.operator} requires identical dimensions: "
                            f"{left_shape[0]}x{left_shape[1]} vs {right_shape[0]}x{right_shape[1]}.",
                            node.line, node.column
                        )
                    self.operation_name = "Matrix Addition" if node.operator == "+" else "Matrix Subtraction"
                    return SemanticType.MATRIX, left_shape
                elif node.operator == "*":
                    self.operation_name = "Matrix Multiplication"
                    if left_shape and right_shape:
                        if left_shape[1] != right_shape[0]:
                            raise SemanticError(
                                f"Matrix multiplication is invalid.\n\n"
                                f"A: {left_shape[0]}×{left_shape[1]}\n"
                                f"B: {right_shape[0]}×{right_shape[1]}\n\n"
                                f"Columns of A must equal rows of B.",
                                node.line, node.column
                            )
                        return SemanticType.MATRIX, (left_shape[0], right_shape[1])
                    return SemanticType.MATRIX, None

        if left_type == SemanticType.NUMBER and right_type == SemanticType.NUMBER:
            if node.operator == "/" and isinstance(node.right, NumberNode) and node.right.value == 0:
                raise SemanticError("Division by zero.", node.line, node.column)
            return SemanticType.NUMBER, None

        return SemanticType.NUMBER, None

    def visit_UnaryOperationNode(self, node: UnaryOperationNode) -> Tuple[SemanticType, Optional[Tuple[int, ...]]]:
        operand_type, shape = self.visit(node.operand)
        return operand_type, shape

    def visit_FunctionCallNode(self, node: FunctionCallNode) -> Tuple[SemanticType, Optional[Tuple[int, ...]]]:
        fname = node.name.lower()
        symbol = self.symbol_table.lookup(fname)
        if not symbol or symbol.type != SemanticType.FUNCTION:
            raise SemanticError(f"Function '{node.name}' is not defined.", node.line, node.column)

        # ML Metrics
        if fname in ["mae", "mse", "rmse", "r2"]:
            self.features["has_metric"] = True
            self.features["operation_type"] = 3
            self.operation_name = f"ML Regression Metric ({fname.upper()})"

            if len(node.arguments) != 2:
                raise SemanticError(f"Metric function '{fname}' expects 2 arguments (actual, predicted), got {len(node.arguments)}.", node.line, node.column)

            t1, s1 = self.visit(node.arguments[0])
            t2, s2 = self.visit(node.arguments[1])

            if t1 != SemanticType.VECTOR or t2 != SemanticType.VECTOR:
                raise SemanticError(f"Metric '{fname}' requires 1D vector arrays for actual and predicted.", node.line, node.column)

            if s1 and s2 and s1[0] != s2[0]:
                raise SemanticError(
                    f"Actual and predicted arrays must have equal length.\n"
                    f"Actual: {s1[0]} elements\n"
                    f"Predicted: {s2[0]} elements",
                    node.line, node.column
                )
            return SemanticType.NUMBER, None

        # Matrix functions
        if fname in ["transpose", "determinant", "det", "inverse"]:
            self.features["has_matrix"] = True
            self.features["matrix_dimensions"] = 2
            self.features["operation_type"] = 1

            if len(node.arguments) != 1:
                raise SemanticError(f"Function '{fname}' expects exactly 1 matrix argument.", node.line, node.column)

            arg_type, shape = self.visit(node.arguments[0])
            if arg_type != SemanticType.MATRIX:
                raise SemanticError(f"Function '{fname}' expects a matrix, got {arg_type.name}.", node.line, node.column)

            if fname in ["determinant", "det", "inverse"]:
                if shape and shape[0] != shape[1]:
                    raise SemanticError(f"Function '{fname}' requires a square matrix, got {shape[0]}x{shape[1]}.", node.line, node.column)
                if fname in ["determinant", "det"]:
                    self.operation_name = "Determinant"
                    return SemanticType.NUMBER, None
                else:
                    self.operation_name = "Matrix Inverse"
                    return SemanticType.MATRIX, shape
            elif fname == "transpose":
                self.operation_name = "Matrix Transpose"
                transposed_shape = (shape[1], shape[0]) if shape else None
                return SemanticType.MATRIX, transposed_shape

        if fname in ["sqrt", "sin", "cos", "tan", "log", "abs"]:
            if len(node.arguments) != 1:
                raise SemanticError(f"Function '{node.name}' expects exactly 1 argument.", node.line, node.column)
            arg_type, _ = self.visit(node.arguments[0])
            if arg_type != SemanticType.NUMBER:
                raise SemanticError(f"Function '{node.name}' expects a numeric argument, got {arg_type.name}.", node.line, node.column)
            # check constant value for sqrt domain
            if isinstance(node.arguments[0], UnaryOperationNode) and node.arguments[0].operator == "-":
                raise SemanticError("Mathematical domain error: sqrt of negative number.", node.line, node.column)
            if isinstance(node.arguments[0], NumberNode) and node.arguments[0].value < 0:
                raise SemanticError("Mathematical domain error: sqrt of negative number.", node.line, node.column)
            return SemanticType.NUMBER, None

        if fname == "norm":
            if len(node.arguments) != 1:
                raise SemanticError("Function 'norm' expects exactly 1 argument.", node.line, node.column)
            t, _ = self.visit(node.arguments[0])
            if t != SemanticType.VECTOR:
                raise SemanticError("Function 'norm' expects a vector argument.", node.line, node.column)
            return SemanticType.NUMBER, None

        if fname == "dot":
            if len(node.arguments) != 2:
                raise SemanticError("Function 'dot' expects exactly 2 arguments.", node.line, node.column)
            t1, _ = self.visit(node.arguments[0])
            t2, _ = self.visit(node.arguments[1])
            if t1 != SemanticType.VECTOR or t2 != SemanticType.VECTOR:
                raise SemanticError("Function 'dot' expects two vectors.", node.line, node.column)
            return SemanticType.NUMBER, None

        return SemanticType.NUMBER, None
