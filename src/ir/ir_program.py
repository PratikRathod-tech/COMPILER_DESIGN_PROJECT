from typing import List
from src.ir.instruction import IRInstruction

class IRProgram:
    def __init__(self):
        self.instructions: List[IRInstruction] = []

    def add_instruction(self, instr: IRInstruction) -> None:
        self.instructions.append(instr)

    def get_instructions(self) -> List[IRInstruction]:
        return self.instructions

    def __repr__(self) -> str:
        return "\n".join(repr(instr) for instr in self.instructions)

    def print(self) -> None:
        print(repr(self))
