# Code Optimization

This document explains the optimization passes implemented on the intermediate representation.

---

## Responsibility
The IROptimizer (`src/optimizer/optimizer.py`) performs optimizations to make the compiled code run faster and consume fewer memory allocations.
The optimizer runs in a fixed-point loop (multi-pass execution) to propagate improvements until no further changes are observed.

---

## Implemented Optimizations

### 1. Constant Propagation
If a variable is assigned a known constant value, its occurrences downstream are replaced with that constant value.
- **Before**:
  ```text
  x = 10
  y = x + 5
  ```
- **After**:
  ```text
  x = 10
  y = 10 + 5
  ```

### 2. Constant Folding
Arithmetic operations where all operands are numeric constants are computed at compile time.
- **Before**:
  ```text
  y = 10 + 5
  ```
- **After**:
  ```text
  y = 15
  ```

### 3. Algebraic Simplification
Redundant arithmetic operations are simplified:
- `x + 0` or `0 + x` $\rightarrow$ `x`
- `x - 0` $\rightarrow$ `x`
- `x * 1` or `1 * x` $\rightarrow$ `x`
- `x / 1` $\rightarrow$ `x`
- `x * 0` or `0 * x` $\rightarrow$ `0`
- Unary positive `+x` $\rightarrow$ `x`
