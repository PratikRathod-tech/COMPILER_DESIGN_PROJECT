# Semantic Analysis

This document details the Semantic Analysis phase of the MathLang compiler.

---

## Responsibility
The Semantic Analyzer (`src/semantic/semantic_analyzer.py`) visits the AST and checks rules that cannot be captured by the syntax grammar alone:
1. **Name Resolution**: Check that variables are defined before use.
2. **Type Checking**: Ensure operations are valid for their types (e.g. vectors cannot be added to scalars, functions cannot be read as variables).
3. **Arguments Count Check**: Ensure built-in math calls have correct number of parameters (e.g. `dot` takes 2, `sqrt` takes 1).
4. **Compile-Time Constraint Validation**: Detect division by zero or mathematical domain boundaries (e.g. negative square roots, zero/negative logarithms) on constant values.

---

## Semantic Errors
If validation fails, a `SemanticError` is raised with source positions:
- `Semantic Error at line 3, column 10: Division by zero.`
- `Semantic Error at line 2, column 5: Variable 'x' is not defined.`

---

## Typo Suggestions Integration
If an undefined variable is caught, the analyzer query matches the misspelled name against the names inside the Symbol Table using Levenshtein distance. A suggestion is included in the output error if a close match is found.
