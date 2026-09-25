# Target Code Generation

This document explains target code generation from Three-Address Code to executable Python source.

---

## Responsibility
The target code generator (`src/codegen/python_generator.py`) maps Three-Address Code instructions to structured Python code.

---

## Mapping Logic

1. **Imports Injection**:
   Every generated file starts with importing math helpers from our runtime:
   ```python
   from src.runtime.math_runtime import *
   ```

2. **Assignments**:
   - `ASSIGN val` $\rightarrow$ `res = val`

3. **Operators mapping**:
   - Arithmetic operators map directly to Python, except `^` which is translated to `**`.
   - Unary minus (`NEG`) $\rightarrow$ `-val`

4. **Functions Mapping**:
   - Built-in functions mapping matches name for name.
   - `abs` is mapped to `abs_val` to prevent overriding python's native `abs`.

5. **Vectors and Matrices**:
   - Emitted directly as Python arrays (lists and nested lists).

6. **Output**:
   - `show expr` is generated as `print(expr)`.

---

## Example Generated Output

### MathLang
```text
radius = 10
area = pi * radius^2
show area
```

### Generated Python
```python
from src.runtime.math_runtime import *

radius = 10
t1 = 10 ** 2
t2 = pi * t1
area = t2
print(t2)
```
*(Note: If optimized, `area = 314.159...` is output directly!)*
