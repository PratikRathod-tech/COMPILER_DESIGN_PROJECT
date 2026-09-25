# Lexical Analysis (Lexer)

This document explains the Lexical Analysis phase of the MathLang compiler.

---

## Responsibility
The Lexer (`src/lexer/lexer.py`) is responsible for scanning the raw input character-by-character and grouping characters into logical units called **Tokens**.
- It ignores redundant whitespace.
- It skips comments starting with `#`.
- It tracks the current **line number** and **column number** for accurate compiler diagnostics.
- It raises lexical errors if an invalid character or invalid float literal is scanned.

---

## Token Representation
Each token is represented by a `Token` dataclass containing:
- `type`: `TokenType` enum (e.g. `NUMBER`, `IDENTIFIER`, `PLUS`, etc.)
- `lexeme`: The actual string segment matched in the source code.
- `line`: The 1-indexed line number where the token starts.
- `column`: The 1-indexed column number where the token starts.

---

## Example Tokenization

### Source Code
```text
x = 10 + 20
```

### Resulting Tokens
```text
Token(type=IDENTIFIER, lexeme='x', line=1, column=1)
Token(type=ASSIGN, lexeme='=', line=1, column=3)
Token(type=NUMBER, lexeme='10', line=1, column=5)
Token(type=PLUS, lexeme='+', line=1, column=8)
Token(type=NUMBER, lexeme='20', line=1, column=10)
Token(type=EOF, lexeme='', line=1, column=12)
```
