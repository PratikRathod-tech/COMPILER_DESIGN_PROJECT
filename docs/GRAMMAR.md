# MathLang Formal Grammar

This document specifies the Context-Free Grammar (CFG) of the MathLang DSL, expressed in Extended Backus-Naur Form (EBNF).

---

## EBNF Grammar

```ebnf
program         → statement* EOF

statement       → assignment
                | showStatement

assignment      → IDENTIFIER "=" expression

showStatement   → "show" expression

expression      → term (("+" | "-") term)*

term            → power (("*" | "/" | "%") power)*

power           → unary ("^" power)?

unary           → ("+" | "-") unary
                | primary

primary         → NUMBER
                | IDENTIFIER
                | functionCall
                | "(" expression ")"
                | vector
                | matrix

functionCall    → IDENTIFIER "(" arguments? ")"

arguments       → expression ("," expression)*

vector          → "[" (expression ("," expression)*)? "]"

matrix          → "[" vector ("," vector)* "]"
```

---

## Precedence Rules
Precedence is encoded directly into the grammar rules:
1. **Parentheses, Groupings, and Literals**: handled by `primary`
2. **Function Calls**: handled by `primary` (checking for `IDENTIFIER ( arguments )`)
3. **Power (`^`)**: handled by `power` (right-associative)
4. **Unary (`+`, `-`)**: handled by `unary`
5. **Multiplication/Division/Modulo (`*`, `/`, `%`)**: handled by `term` (left-associative)
6. **Addition/Subtraction (`+`, `-`)**: handled by `expression` (left-associative)
