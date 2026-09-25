from src.ir.instruction import IRInstruction
from src.ir.ir_program import IRProgram

class PythonGenerator:
    def __init__(self):
        pass

    def generate(self, program: IRProgram) -> str:
        lines = []
        lines.append("from src.runtime.math_runtime import *")
        lines.append("from src.math_engine.matrix import *")
        lines.append("from src.math_engine.equations import *")
        lines.append("from src.math_engine.metrics import *")
        lines.append("")

        for instr in program.get_instructions():
            op = instr.op
            arg1 = instr.arg1
            arg2 = instr.arg2
            res = instr.result

            if op == "ASSIGN":
                lines.append(f"{res} = {self.format_val(arg1)}")

            elif op == "SHOW":
                # For matrices, print formatted; for scalar, print scalar
                lines.append(f"__val = {self.format_val(arg1)}")
                lines.append("if isinstance(__val, list) and __val and isinstance(__val[0], list):")
                lines.append("    print(format_matrix(__val))")
                lines.append("elif isinstance(__val, float):")
                lines.append("    print(__val)")
                lines.append("else:")
                lines.append("    print(__val)")

            elif op == "EQUATION":
                lines.append(f"{res} = {arg1!r}")

            elif op == "SOLVE_LINEAR":
                lines.append(f"__sol, _ = solve_single_equation({self.format_val(arg1)})")
                lines.append("for __k, __v in __sol.items():")
                lines.append("    print(f'{__k} = {int(__v) if isinstance(__v, float) and __v.is_integer() else __v:g}')")
                lines.append(f"{res} = __sol")

            elif op == "SOLVE_SYSTEM":
                eq_list_str = "[" + ", ".join(self.format_val(a) for a in arg1) + "]"
                lines.append(f"__eqs = {eq_list_str}")
                lines.append(f"__sol, _ = solve_system_2x2(__eqs[0], __eqs[1])")
                lines.append("for __k, __v in __sol.items():")
                lines.append("    print(f'{__k} = {int(__v) if isinstance(__v, float) and __v.is_integer() else __v:g}')")
                lines.append(f"{res} = __sol")

            elif op == "MAT_GET":
                lines.append(f"{res} = mat_get({arg1}, int({self.format_val(arg2[0])}), int({self.format_val(arg2[1])}))")

            elif op in ["+", "-", "*", "/", "%", "^"]:
                py_op = "**" if op == "^" else op
                lines.append(f"__left = {self.format_val(arg1)}")
                lines.append(f"__right = {self.format_val(arg2)}")
                lines.append("if isinstance(__left, list) and isinstance(__right, list):")
                if op == "+":
                    lines.append(f"    {res} = mat_add(__left, __right)")
                elif op == "-":
                    lines.append(f"    {res} = mat_sub(__left, __right)")
                elif op == "*":
                    lines.append(f"    {res} = mat_mul(__left, __right)")
                else:
                    lines.append(f"    raise ValueError('Unsupported matrix operator {op}')")
                lines.append("else:")
                lines.append(f"    {res} = __left {py_op} __right")

            elif op == "NEG":
                lines.append(f"{res} = -{self.format_val(arg1)}")

            elif op == "POS":
                lines.append(f"{res} = +{self.format_val(arg1)}")

            elif op == "CALL":
                fname = arg1.lower()
                if fname == "determinant":
                    fname = "det"
                args_str = ", ".join(self.format_val(a) for a in arg2) if isinstance(arg2, list) else self.format_val(arg2)
                lines.append(f"{res} = {fname}({args_str})")

            elif op == "VECTOR":
                elems_str = ", ".join(self.format_val(e) for e in arg1)
                lines.append(f"{res} = [{elems_str}]")

            elif op == "MATRIX":
                rows_str = ", ".join(f"[{', '.join(self.format_val(e) for e in row)}]" for row in arg1)
                lines.append(f"{res} = [{rows_str}]")

        return "\n".join(lines)

    def format_val(self, val) -> str:
        if isinstance(val, list):
            return f"[{', '.join(self.format_val(x) for x in val)}]"
        return str(val)
