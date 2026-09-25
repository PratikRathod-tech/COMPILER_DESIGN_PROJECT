# Compiler Architecture & Pipeline Mapping

This document describes the compiler phases, their data transformations, responsibilities, and implementation paths.

---

## Architecture Flow

```text
Source Code (str)
    │
    ▼ [Lexical Analysis] (src/lexer/lexer.py)
Tokens (list[Token])
    │
    ▼ [Syntax Analysis] (src/parser/parser.py)
AST (ProgramNode)
    │
    ▼ [Semantic Analysis] (src/semantic/semantic_analyzer.py)
Checked AST & Symbol Table (src/semantic/symbol_table.py)
    │
    ▼ [Intermediate Code Gen] (src/ir/ir_generator.py)
Three-Address Code (IRProgram)
    │
    ▼ [Optimization] (src/optimizer/optimizer.py)
Optimized TAC (IRProgram)
    │
    ▼ [Target Code Gen] (src/codegen/python_generator.py)
Executable Python String (str)
    │
    ▼ [Runtime Environment] (src/runtime/math_runtime.py)
Execution Output (Console output)
```

---

## Phase Responsibility Mapping

| Compiler Phase | Input | Output | Responsibility | Associated Files |
| :--- | :--- | :--- | :--- | :--- |
| **Token Definitions** | N/A | Enum & Dataclass | Define vocabulary symbols. | [`token_type.py`](../src/lexer/token_type.py), [`token.py`](../src/lexer/token.py) |
| **Lexical Analysis** | Source string | Token stream | Strip whitespace/comments, generate tokens, track lines/cols. | [`lexer.py`](../src/lexer/lexer.py) |
| **Syntax Analysis** | Token stream | AST Node Tree | Consume tokens, validate grammar structure, maintain precedence. | [`ast.py`](../src/parser/ast.py), [`parser.py`](../src/parser/parser.py) |
| **Semantic Analysis** | AST Tree | AST Tree | Validate variable scopes, type compatibility, math domain bounds. | [`types.py`](../src/semantic/types.py), [`symbol.py`](../src/semantic/symbol.py), [`symbol_table.py`](../src/semantic/symbol_table.py), [`semantic_analyzer.py`](../src/semantic/semantic_analyzer.py) |
| **IR Generation** | AST Tree | Three-Address Code | Flatten nesting into linear operations using temporary variables. | [`instruction.py`](../src/ir/instruction.py), [`ir_program.py`](../src/ir/ir_program.py), [`ir_generator.py`](../src/ir/ir_generator.py) |
| **Optimization** | Raw TAC | Optimized TAC | Constant propagation, folding, and algebraic reductions. | [`optimizer.py`](../src/optimizer/optimizer.py) |
| **Code Generation** | Optimized TAC | Python Source Code | Format TAC operations into a python execution sequence. | [`python_generator.py`](../src/codegen/python_generator.py) |
| **Math Runtime** | Python program | System Output | Provide standard scalar, vector, and matrix mathematical helpers. | [`math_runtime.py`](../src/runtime/math_runtime.py) |
| **Orchestrator & CLI**| System args | Pipeline display | Link all phases together and present compiler details. | [`compiler.py`](../src/compiler/compiler.py), [`main.py`](../main.py) |
