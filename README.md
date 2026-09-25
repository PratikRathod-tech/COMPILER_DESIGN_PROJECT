# ML Math Compiler

A minimal, simple, fully working **ML Math Compiler** built as a local web application and CLI tool.

It demonstrates the complete 10-phase compiler design pipeline:
```text
Source Code
     ↓
1. Lexical Analysis
     ↓
2. Syntax Analysis / Parsing
     ↓
3. AST Generation
     ↓
4. Semantic Analysis
     ↓
5. Symbol Table
     ↓
6. Local ML Classification (Decision Tree on AST features)
     ↓
7. Intermediate Representation (IR)
     ↓
8. Optimization (Constant Folding & Propagation)
     ↓
9. Code Generation / Execution
     ↓
10. Final Result
```

---

## 1. Supported Operations (Strict Scope)

1. **2D Matrix Operations**
   * Creation: `matrix A = [[1,2],[3,4]]`
   * Matrix addition (`+`), subtraction (`-`), multiplication (`*`)
   * Built-in matrix functions: `transpose(A)`, `determinant(A)` or `det(A)`, `inverse(A)`
   * Matrix element access: `A[0][0]`
   * Strict dimension checking & row consistency validation

2. **Linear Equations**
   * Single equation: `solve 2*x + 5 = 15` -> `x = 5`
   * 2x2 System of linear equations:
     ```text
     solve:
     2*x + y = 10
     x - y = 2
     ```
     -> `x = 4`, `y = 2`

3. **ML Regression Metrics**
   * Pure Python manual formulas (no sklearn metric functions used):
     * `mae(actual, predicted)`
     * `mse(actual, predicted)`
     * `rmse(actual, predicted)`
     * `r2(actual, predicted)`

4. **Local ML Classifier**
   * Embedded `DecisionTreeClassifier` (via scikit-learn).
   * Classifies problems (`MATRIX_OPERATION`, `LINEAR_EQUATION`, `REGRESSION_METRIC`) using features extracted from the AST (`has_matrix`, `has_equation`, `has_metric`, `matrix_dimensions`, `operation_type`, `variable_count`).
   * No cloud APIs, no external network requests, zero API keys.

---

## 2. Project Structure

```text
MLMathCompiler/
│
├── main.py                     # Web server & CLI runner with 10-phase terminal printing
├── requirements.txt
├── README.md
│
├── examples/
│   ├── matrix.math             # 2D matrix multiplication example
│   ├── linear.math             # Single linear equation example
│   └── metrics.math            # ML regression metrics example
│
├── src/
│   ├── lexer/                  # Tokenizer & TokenType definitions
│   ├── parser/                 # Recursive-descent parser & AST nodes
│   ├── semantic/               # Type & dimension checking, Symbol table
│   ├── ml/                     # Local DecisionTree classifier on AST features
│   ├── ir/                     # 3-address code IR representation
│   ├── optimizer/              # Constant folding & algebraic simplification
│   ├── math_engine/            # Pure Python matrix, equation & metric engines
│   │   ├── matrix.py           # Add, sub, mul, det, transpose, inverse
│   │   ├── equations.py        # 1-var and 2-var linear equation solvers
│   │   └── metrics.py          # MAE, MSE, RMSE, R² manual formulas
│   ├── codegen/                # Python target code generator
│   └── compiler/               # Central compiler orchestrator
│
├── web/
│   ├── index.html              # Split-screen UI (Editor top, Output bottom)
│   ├── style.css               # Clean modern dark theme
│   └── app.js                  # Frontend logic, Phase explorer & Workflow view
│
└── tests/
    └── test_ml_math_compiler.py
```

---

## 3. Running the Project

### A. Local Web Application (Horizontal Split-Screen)

Run:
```bash
python main.py
```
Then open your browser at:
```
http://localhost:5000
```

Features in the browser:
* **Top half**: Simple input editor with preset quick-loaders (`2D Matrix`, `Linear Eq`, `2x2 System`, `ML Metrics`) and buttons: `[Run]`, `[Clear]`, `[Workflow]`.
* **Bottom half**: Clean output view showing:
  * Final mathematical result
  * Detected operation name & local ML classification + confidence
  * Mathematical step explanation
* **Workflow Button**: Shows the full compiler pipeline step-by-step with collapsible accordions.
* **Phase Explorer**: Individual buttons `[Tokens]`, `[AST]`, `[Semantic]`, `[Symbols]`, `[ML]`, `[IR]`, `[Optimized IR]`, `[Execution]` to inspect each phase individually.
* **Terminal output**: Every compilation logs all 10 stages in detail to the console.

### B. CLI Runner

You can also run any source file directly in the terminal:
```bash
python main.py examples/matrix.math
python main.py examples/linear.math
python main.py examples/metrics.math
```

### C. Running Tests

```bash
pytest
```
All 32 unit and integration tests pass.
