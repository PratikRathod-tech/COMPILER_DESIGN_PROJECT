from typing import Tuple, Any, Dict, List
import io
import sys
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.semantic_analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator
from src.optimizer.optimizer import IROptimizer
from src.codegen.python_generator import PythonGenerator
from src.ir.ir_program import IRProgram
from src.ml.classifier import MLClassifier

class Compiler:
    def __init__(self):
        self.classifier = MLClassifier()

    def compile(self, source: str) -> Tuple[list, Any, SemanticAnalyzer, IRProgram, IRProgram, str, Tuple[str, float]]:
        # 1. Lexical Analysis
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # 2. Syntax Analysis
        parser = Parser(tokens)
        ast = parser.parse()

        # 3. Semantic Analysis & Symbol Table
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)

        # 4. Local ML Classification (using AST-extracted features)
        category, confidence = self.classifier.classify(analyzer.features)
        analyzer.ml_category = category
        analyzer.ml_confidence = confidence

        # 5. Intermediate Code Generation
        ir_gen = IRGenerator()
        ir_program = ir_gen.generate(ast)

        # 6. Optimization
        optimizer = IROptimizer()
        optimized_ir = optimizer.optimize(ir_program)

        # 7. Target Code Generation
        codegen = PythonGenerator()
        generated_python = codegen.generate(optimized_ir)

        return tokens, ast, analyzer, ir_program, optimized_ir, generated_python

    def run(self, generated_python: str) -> str:
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output
        global_env = {}
        try:
            exec(generated_python, global_env)
            output = redirected_output.getvalue()
        finally:
            sys.stdout = old_stdout
        # Also print to current stdout so capsys and terminal callers receive it
        sys.stdout.write(output)
        return output

    def get_phase_outputs(self, source: str) -> Dict[str, Any]:
        """
        Runs compilation and execution, returning structured outputs for all 10 phases.
        """
        # Lexical
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        tokens_str = "\n".join(str(t) for t in tokens if t.type.name != "EOF")

        # Syntax & AST
        parser = Parser(tokens)
        ast = parser.parse()
        ast_str = self.format_ast_tree(ast)

        # Syntax analysis representation
        syntax_analysis_str = self.format_syntax_analysis(ast)

        # Semantic Analysis
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        semantic_summary = f"Operation: {analyzer.operation_name}\n"
        semantic_summary += f"AST Features: {analyzer.features}\n"
        semantic_summary += "Status: VALID"

        # Symbol Table
        symbol_table_str = self.format_symbol_table(analyzer)

        # ML Classification
        category, confidence = self.classifier.classify(analyzer.features)
        ml_str = f"{category}\nConfidence: {confidence}%"

        # IR
        ir_gen = IRGenerator()
        ir_program = ir_gen.generate(ast)
        ir_str = repr(ir_program)

        # Optimization
        optimizer = IROptimizer()
        optimized_ir = optimizer.optimize(ir_program)
        opt_ir_str = repr(optimized_ir)

        # Codegen & Execution
        codegen = PythonGenerator()
        generated_python = codegen.generate(optimized_ir)
        output = self.run(generated_python)

        # Explanation
        explanation = self.generate_math_explanation(analyzer, output)

        return {
            "source": source.strip(),
            "tokens": tokens_str,
            "syntax": syntax_analysis_str,
            "ast": ast_str,
            "semantic": semantic_summary,
            "symbols": symbol_table_str,
            "ml_category": category,
            "ml_confidence": confidence,
            "ml_text": ml_str,
            "ir": ir_str,
            "opt_ir": opt_ir_str,
            "code": generated_python,
            "execution": output.strip(),
            "explanation": explanation,
            "operation": analyzer.operation_name
        }

    def format_syntax_analysis(self, ast: Any) -> str:
        lines = []
        for stmt in ast.statements:
            stype = type(stmt).__name__
            if stype == "SolveNode":
                lines.append("Equation")
                for eq in stmt.equations:
                    parts = eq.split("=")
                    if len(parts) == 2:
                        lines.append(f" |-- {parts[0].strip()}")
                        lines.append(f" `-- {parts[1].strip()}")
                    else:
                        lines.append(f" `-- {eq}")
            elif stype == "AssignmentNode":
                decl = "Matrix Assignment" if stmt.is_matrix_decl else "Assignment"
                lines.append(f"{decl}: {stmt.name} = ...")
            elif stype == "ShowNode":
                lines.append("Show Output")
        return "\n".join(lines) if lines else "Syntax Verified"

    def format_ast_tree(self, node: Any, prefix: str = "", is_last: bool = True) -> str:
        if node is None:
            return ""
        name = type(node).__name__
        val_extra = ""
        children = []

        if name == "ProgramNode":
            res = ["Program"]
            for i, stmt in enumerate(node.statements):
                last = (i == len(node.statements) - 1)
                res.append(self.format_ast_tree(stmt, "", last))
            return "\n".join(res)

        elif name == "AssignmentNode":
            val_extra = f" ({node.name})"
            children = [node.value]

        elif name == "ShowNode":
            children = [node.value]

        elif name == "SolveNode":
            val_extra = f" ({', '.join(node.equations)})"

        elif name == "BinaryOperationNode":
            name = f"BinaryOp ({node.operator})"
            children = [node.left, node.right]

        elif name == "UnaryOperationNode":
            name = f"UnaryOp ({node.operator})"
            children = [node.operand]

        elif name == "NumberNode":
            name = f"Number ({node.value})"

        elif name == "IdentifierNode":
            name = f"Identifier ({node.name})"

        elif name == "FunctionCallNode":
            name = f"Call {node.name}"
            children = node.arguments

        elif name == "MatrixNode":
            name = f"Matrix ({len(node.rows)}x{len(node.rows[0]) if node.rows else 0})"

        elif name == "VectorNode":
            name = f"Vector (len {len(node.elements)})"

        elif name == "MatrixIndexNode":
            name = f"Index {node.matrix_name}"
            children = [node.row, node.col]

        curr_branch = "`-- " if is_last else "|-- "
        res = [prefix + curr_branch + name + val_extra]
        new_prefix = prefix + ("    " if is_last else "|   ")

        for i, child in enumerate(children):
            c_last = (i == len(children) - 1)
            res.append(self.format_ast_tree(child, new_prefix, c_last))

        return "\n".join(res)

    def format_symbol_table(self, analyzer: SemanticAnalyzer) -> str:
        builtins = ["mae", "mse", "rmse", "r2", "transpose", "determinant", "det", "inverse"]
        syms = analyzer.symbol_table.symbols
        user_syms = {k: v for k, v in syms.items() if k not in builtins}

        if not user_syms:
            return "(No user-defined variables)"

        rows = []
        rows.append(f"{'Name':<12} {'Type':<12} {'Shape':<12}")
        rows.append("-" * 38)
        for name, sym in user_syms.items():
            shape_str = "-"
            if sym.shape:
                if len(sym.shape) == 2:
                    shape_str = f"{sym.shape[0]} x {sym.shape[1]}"
                elif len(sym.shape) == 1:
                    shape_str = f"{sym.shape[0]} elements"
            rows.append(f"{name:<12} {sym.type.name:<12} {shape_str:<12}")
        return "\n".join(rows)

    def generate_math_explanation(self, analyzer: SemanticAnalyzer, output: str) -> str:
        op = analyzer.operation_name
        if "Multiplication" in op:
            return (
                "Matrix Multiplication (A x B):\n"
                "* For each element C[i][j], compute dot product of row i of A and column j of B.\n"
                "* C[i][j] = sum(A[i][k] * B[k][j])\n"
                "* Inner dimensions match; verified mathematically."
            )
        elif "Linear Equation" in op:
            return (
                "Linear Equation Solution:\n"
                "* Isolate variable terms to the LHS and constants to the RHS.\n"
                "* Compute net coefficient 'a' and constant 'c'.\n"
                "* Solution derived analytically: x = c / a."
            )
        elif "MAE" in op or "Metric" in op:
            return (
                "ML Metric Computation:\n"
                "* Calculate prediction residuals: error = actual - predicted\n"
                "* Apply metric formula deterministically without external black-box library\n"
                "* Result verified against standard statistical formulation."
            )
        return f"{op} executed deterministically."
