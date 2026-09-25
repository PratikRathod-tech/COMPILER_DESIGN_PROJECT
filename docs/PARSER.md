# Syntax Analysis (Parser)

This document explains the Syntax Analysis and Abstract Syntax Tree (AST) construction.

---

## Recursive Descent Parsing
The parser (`src/parser/parser.py`) is implemented as a **Recursive Descent Parser**, which is a top-down parsing technique.
Each grammar rule corresponds directly to a method in the parser:
- `parse_program()`
- `parse_statement()`
- `parse_assignment()`
- `parse_expression()`
- `parse_term()`
- `parse_power()`
- `parse_unary()`
- `parse_primary()`

---

## Operator Precedence Resolution
To guarantee standard mathematical precedence, rules are nested from lowest precedence to highest:
1. **Expressions (`+`, `-`)** call **Terms (`*`, `/`, `%`)**.
2. **Terms** call **Powers (`^`)**.
3. **Powers** call **Unary operators (`-`, `+`)**.
4. **Unary** call **Primary expressions (parentheses, numbers, identifiers, function calls, vector/matrix literals)**.

### Power Associativity
The power operator (`^`) is right-associative (e.g. `2^3^2` represents `2^(3^2)`). This is parsed recursively by having the power operator call `parse_power()` on its right-hand side rather than `parse_unary()`.

---

## AST Generation
As the parser traverses the grammatical constructs, it returns concrete subclasses of `ASTNode`:
- `ProgramNode`: Root of the tree containing statements.
- `AssignmentNode`: Represents variable updates (`x = value`).
- `ShowNode`: Represents output calls (`show value`).
- `BinaryOperationNode`: Represents operations like `a + b`, `a * b`, `a ^ b`.
- `UnaryOperationNode`: Represents negative/positive operations, e.g. `-a`.
- `NumberNode`: Literal values.
- `IdentifierNode`: Variable reads.
- `FunctionCallNode`: Built-in function calls.
- `VectorNode` & `MatrixNode`: Vector and matrix literal blocks.
