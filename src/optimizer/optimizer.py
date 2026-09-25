from typing import Dict, Union, Any, List
from src.ir.instruction import IRInstruction
from src.ir.ir_program import IRProgram

class IROptimizer:
    def __init__(self):
        pass

    def optimize(self, program: IRProgram) -> IRProgram:
        current_instrs = program.get_instructions()
        
        changed = True
        iterations = 0
        while changed and iterations < 10:
            iterations += 1
            changed = False
            optimized_instrs: List[IRInstruction] = []
            constants: Dict[str, Union[int, float]] = {}

            for instr in current_instrs:
                arg1 = instr.arg1
                arg2 = instr.arg2
                res = instr.result

                if isinstance(arg1, str) and arg1 in constants:
                    arg1 = constants[arg1]
                if isinstance(arg2, str) and arg2 in constants:
                    arg2 = constants[arg2]

                new_instr = IRInstruction(instr.op, arg1, arg2, res)

                if new_instr.op in ["+", "-", "*", "/", "%", "^"]:
                    left = new_instr.arg1
                    right = new_instr.arg2

                    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                        folded_val = self.fold_binary(new_instr.op, left, right)
                        if folded_val is not None:
                            new_instr = IRInstruction("ASSIGN", folded_val, result=new_instr.result)

                    elif new_instr.op == "+":
                        if left == 0:
                            new_instr = IRInstruction("ASSIGN", right, result=new_instr.result)
                        elif right == 0:
                            new_instr = IRInstruction("ASSIGN", left, result=new_instr.result)
                            
                    elif new_instr.op == "-":
                        if right == 0:
                            new_instr = IRInstruction("ASSIGN", left, result=new_instr.result)
                            
                    elif new_instr.op == "*":
                        if left == 0 or right == 0:
                            new_instr = IRInstruction("ASSIGN", 0, result=new_instr.result)
                        elif left == 1:
                            new_instr = IRInstruction("ASSIGN", right, result=new_instr.result)
                        elif right == 1:
                            new_instr = IRInstruction("ASSIGN", left, result=new_instr.result)
                            
                    elif new_instr.op == "/":
                        if right == 1:
                            new_instr = IRInstruction("ASSIGN", left, result=new_instr.result)
                        elif left == 0 and right != 0:
                            new_instr = IRInstruction("ASSIGN", 0, result=new_instr.result)

                elif new_instr.op in ["NEG", "POS"]:
                    operand = new_instr.arg1
                    if isinstance(operand, (int, float)):
                        folded_val = -operand if new_instr.op == "NEG" else operand
                        new_instr = IRInstruction("ASSIGN", folded_val, result=new_instr.result)

                if new_instr.op == "ASSIGN" and isinstance(new_instr.arg1, (int, float)) and new_instr.result:
                    constants[new_instr.result] = new_instr.arg1

                if repr(new_instr) != repr(instr):
                    changed = True

                optimized_instrs.append(new_instr)

            current_instrs = optimized_instrs

        optimized_program = IRProgram()
        for instr in current_instrs:
            optimized_program.add_instruction(instr)
        return optimized_program

    def fold_binary(self, op: str, left: Union[int, float], right: Union[int, float]) -> Any:
        try:
            if op == "+":
                return left + right
            elif op == "-":
                return left - right
            elif op == "*":
                return left * right
            elif op == "/":
                return left / right if right != 0 else None
            elif op == "%":
                return left % right if right != 0 else None
            elif op == "^":
                return left ** right
        except Exception:
            return None
        return None
