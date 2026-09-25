# Symbol Table

This document explains the Symbol Table implementation.

---

## Responsibility
The Symbol Table (`src/semantic/symbol_table.py`) tracks identifiers, their types, and where they were declared. It provides the base scope environment for the compiler.

---

## Operations
- `define(name, symbol)`: Declares a variable or built-in function in the current scope.
- `lookup(name)`: Resolves an identifier by walking up parent scopes (lexical scoping support).
- `contains(name)`: Returns true if the identifier is defined in the current or any parent scope.
- `get_all_names()`: Returns all active identifier names for spelling correction checks.

---

## Symbols Representation
Each entry is stored as a `Symbol` dataclass:
- `name`: String identifier.
- `type`: `SemanticType` (e.g., `NUMBER`, `VECTOR`, `MATRIX`, `FUNCTION`).
- `line` & `column`: Location tracking.

---

## Global Built-ins Setup
Upon initialization, the semantic analyzer pre-populates the symbol table with:
- Constants: `pi` and `e` (mapped to `SemanticType.NUMBER`).
- Math Functions: `sqrt`, `sin`, `cos`, `tan`, `log`, `abs`, `dot`, `norm`, `transpose`, `det`, `inverse` (mapped to `SemanticType.FUNCTION`).
