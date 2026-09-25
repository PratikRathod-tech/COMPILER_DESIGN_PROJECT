# MathLang Language Specification

This document details the lexical grammar, keywords, variables, operators, math functions, vectors, and matrices supported in the MathLang DSL.

---

## 1. Variables
Variables are declared and assigned using the syntax:
```text
identifier = expression
```
Variables must be declared before they are read. Re-assignment updates their values.

---

## 2. Numbers
MathLang supports numeric constants including integers and decimals:
- Integers: `10`, `0`, `-5` (where the negative sign is handled by unary operations)
- Decimals: `10.5`, `3.14159`

---

## 3. Mathematical Constants
- `pi`: Represents the ratio of a circle's circumference to its diameter (~`3.141592653589793`).
- `e`: Represents Euler's number (~`2.718281828459045`).

---

## 4. Arithmetic Operators
Supported in order of standard mathematical precedence:
- `+` (Addition)
- `-` (Subtraction)
- `*` (Multiplication)
- `/` (Division)
- `%` (Modulo)
- `^` (Power / Exponentiation)

---

## 5. Parentheses
Group operations to override standard operator precedence:
```text
x = (10 + 20) * 5
```

---

## 6. Built-in Functions
- `sqrt(x)`: Square root of $x$ (requires $x \ge 0$).
- `sin(x)`: Sine of $x$.
- `cos(x)`: Cosine of $x$.
- `tan(x)`: Tangent of $x$.
- `log(x)`: Natural logarithm of $x$ (requires $x > 0$).
- `abs(x)`: Absolute value of $x$.

---

## 7. Vector Operations
Vectors are declared as list literals:
```text
v = [1, 2, 3]
```
Supported functions:
- `dot(v1, v2)`: Returns the dot product of two vectors of equal length.
- `norm(v)`: Returns the Euclidean norm (length) of a vector.

---

## 8. Matrix Operations
Matrices are declared as nested lists of rows:
```text
A = [
    [1, 2],
    [3, 4]
]
```
Supported functions:
- `transpose(A)`: Returns the transpose matrix.
- `det(A)`: Returns the determinant of a square matrix.
- `inverse(A)`: Returns the inverse of a square invertible matrix.

---

## 9. Show Statement
Used to print out values/expressions:
```text
show area
show 10 + 20
```

---

## 10. Comments
Single line comments start with `#`:
```text
# This is a comment
```
