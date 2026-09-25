# Intermediate Representation (IR)

This document explains Three-Address Code (TAC) generation.

---

## Responsibility
The Intermediate Representation phase (`src/ir/ir_generator.py`) flattens nested AST structures into a list of linear instructions. This makes optimizations and target code generation much simpler.

---

## Three-Address Code (TAC)
Each instruction is represented by `IRInstruction` containing:
- `op`: Operator name.
- `arg1`: First argument.
- `arg2`: Second argument (optional).
- `result`: Target destination (optional).

---

## Example Translation

### MathLang Code
```text
x = (a + b) * c
```

### Generated IR (TAC)
```text
t1 = a + b
t2 = t1 * c
x = t2
```
Here, `t1` and `t2` are temporary variables created dynamically by the IR generator.
Vector and matrix literals are stored as structured arguments (`VECTOR` and `MATRIX` operations) to preserve items layout for target translation.
