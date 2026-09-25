from src.lexer.token import Token
from src.lexer.token_type import TokenType
from src.parser.ast import (
    ASTNode, ProgramNode, AssignmentNode, ShowNode, BinaryOperationNode,
    UnaryOperationNode, NumberNode, IdentifierNode, FunctionCallNode,
    VectorNode, MatrixNode, SolveNode, MatrixIndexNode
)

class ParserError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Syntax Error at line {line}, column {column}: {message}")
        self.message = message
        self.line = line
        self.column = column

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def peek(self) -> Token:
        if self.current >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type):
            return self.advance()
        token = self.peek()
        raise ParserError(message, token.line, token.column)

    def parse(self) -> ProgramNode:
        return self.parse_program()

    def parse_program(self) -> ProgramNode:
        statements = []
        while not self.is_at_end():
            statements.append(self.parse_statement())
        return ProgramNode(statements)

    def parse_statement(self) -> ASTNode:
        if self.match(TokenType.SHOW):
            return self.parse_show_statement()
        if self.match(TokenType.SOLVE):
            return self.parse_solve_statement()
        return self.parse_assignment()

    def parse_solve_statement(self) -> SolveNode:
        solve_token = self.previous()
        line = solve_token.line
        col = solve_token.column

        equations = []
        if self.match(TokenType.COLON):
            # System of equations: collect until next keyword or EOF
            while not self.is_at_end() and self.peek().type not in [TokenType.SHOW, TokenType.SOLVE, TokenType.MATRIX]:
                eq_str = self.parse_equation_line()
                if eq_str:
                    equations.append(eq_str)
                else:
                    break
        else:
            # Single equation on this line: collect tokens until end of statement / line
            eq_str = self.parse_equation_line()
            equations.append(eq_str)

        if not equations:
            raise ParserError("Expected equation after 'solve'.", line, col)

        return SolveNode(equations, line, col)

    def parse_equation_line(self) -> str:
        # Collect tokens making up an equation (e.g. 2 * x + 5 = 15)
        # Ends when we hit SHOW, SOLVE, MATRIX, or EOF, or if we already parsed an equation and line number changes
        tokens_in_eq = []
        start_line = self.peek().line

        while not self.is_at_end() and self.peek().type not in [TokenType.SHOW, TokenType.SOLVE, TokenType.MATRIX]:
            # If line changed and we already collected tokens that form an equation (contains '='), stop
            if tokens_in_eq and self.peek().line != start_line:
                has_equals = any(t.type == TokenType.ASSIGN for t in tokens_in_eq)
                if has_equals:
                    break
            tokens_in_eq.append(self.advance())

        if not tokens_in_eq:
            return ""

        # Reconstruct equation string with proper spacing
        eq_str = " ".join(t.lexeme for t in tokens_in_eq)
        return eq_str

    def parse_show_statement(self) -> ShowNode:
        show_token = self.previous()
        expr = self.parse_expression()
        return ShowNode(expr, show_token.line, show_token.column)

    def parse_assignment(self) -> AssignmentNode:
        is_matrix = False
        if self.match(TokenType.MATRIX):
            is_matrix = True

        identifier = self.consume(TokenType.IDENTIFIER, "Expected identifier for variable assignment.")
        self.consume(TokenType.ASSIGN, "Expected '=' after variable name.")
        value = self.parse_expression()
        return AssignmentNode(identifier.lexeme, value, identifier.line, identifier.column, is_matrix_decl=is_matrix)

    def parse_expression(self) -> ASTNode:
        expr = self.parse_term()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator_token = self.previous()
            right = self.parse_term()
            expr = BinaryOperationNode(expr, operator_token.lexeme, right, operator_token.line, operator_token.column)
        return expr

    def parse_term(self) -> ASTNode:
        expr = self.parse_power()
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator_token = self.previous()
            right = self.parse_power()
            expr = BinaryOperationNode(expr, operator_token.lexeme, right, operator_token.line, operator_token.column)
        return expr

    def parse_power(self) -> ASTNode:
        expr = self.parse_unary()
        if self.match(TokenType.POWER):
            operator_token = self.previous()
            right = self.parse_power()
            expr = BinaryOperationNode(expr, operator_token.lexeme, right, operator_token.line, operator_token.column)
        return expr

    def parse_unary(self) -> ASTNode:
        if self.match(TokenType.PLUS, TokenType.MINUS):
            operator_token = self.previous()
            operand = self.parse_unary()
            return UnaryOperationNode(operator_token.lexeme, operand, operator_token.line, operator_token.column)
        return self.parse_primary()

    def parse_primary(self) -> ASTNode:
        if self.match(TokenType.NUMBER):
            token = self.previous()
            value = float(token.lexeme) if '.' in token.lexeme else int(token.lexeme)
            return NumberNode(value, token.line, token.column)

        if self.match(TokenType.IDENTIFIER):
            name_token = self.previous()
            # Function call: name(...)
            if self.check(TokenType.LPAREN):
                self.advance()  # consume '('
                arguments = []
                if not self.check(TokenType.RPAREN):
                    arguments.append(self.parse_expression())
                    while self.match(TokenType.COMMA):
                        arguments.append(self.parse_expression())
                self.consume(TokenType.RPAREN, "Expected ')' after function arguments.")
                return FunctionCallNode(name_token.lexeme, arguments, name_token.line, name_token.column)
            
            # Matrix element access: name[row][col]
            if self.check(TokenType.LBRACKET):
                self.advance()  # consume '['
                row_expr = self.parse_expression()
                self.consume(TokenType.RBRACKET, "Expected ']' after row index.")
                self.consume(TokenType.LBRACKET, "Expected second '[' for column index in matrix element access.")
                col_expr = self.parse_expression()
                self.consume(TokenType.RBRACKET, "Expected ']' after col index.")
                return MatrixIndexNode(name_token.lexeme, row_expr, col_expr, name_token.line, name_token.column)

            return IdentifierNode(name_token.lexeme, name_token.line, name_token.column)

        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression.")
            return expr

        if self.match(TokenType.LBRACKET):
            bracket_token = self.previous()
            # If the next token is LBRACKET, it is a matrix
            if self.check(TokenType.LBRACKET):
                rows = []
                rows.append(self.parse_vector_literal())
                while self.match(TokenType.COMMA):
                    rows.append(self.parse_vector_literal())
                self.consume(TokenType.RBRACKET, "Expected ']' at end of matrix.")
                return MatrixNode(rows, bracket_token.line, bracket_token.column)
            else:
                # It is a vector (or empty matrix/vector)
                elements = []
                if not self.check(TokenType.RBRACKET):
                    elements.append(self.parse_expression())
                    while self.match(TokenType.COMMA):
                        elements.append(self.parse_expression())
                self.consume(TokenType.RBRACKET, "Expected ']' at end of array.")
                return VectorNode(elements, bracket_token.line, bracket_token.column)

        token = self.peek()
        raise ParserError(f"Expected expression, found {token.type.name}.", token.line, token.column)

    def parse_vector_literal(self) -> list[ASTNode]:
        self.consume(TokenType.LBRACKET, "Expected '[' to start a matrix row.")
        elements = []
        if not self.check(TokenType.RBRACKET):
            elements.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                elements.append(self.parse_expression())
        self.consume(TokenType.RBRACKET, "Expected ']' to end a matrix row.")
        return elements
