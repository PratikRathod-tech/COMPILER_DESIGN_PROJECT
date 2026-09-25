from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class IRInstruction:
    op: str
    arg1: Union[str, int, float, list]
    arg2: Optional[Union[str, int, float, list]] = None
    result: Optional[str] = None

    def __repr__(self) -> str:
        if self.op == "ASSIGN":
            return f"{self.result} = {self.arg1}"
        elif self.op == "SHOW":
            return f"show {self.arg1}"
        elif self.op == "CALL":
            args_str = ", ".join(map(str, self.arg2)) if isinstance(self.arg2, list) else str(self.arg2)
            return f"{self.result} = {self.arg1}({args_str})"
        elif self.op == "EQUATION":
            return f"{self.result} = equation({self.arg1!r})"
        elif self.op == "SOLVE_LINEAR":
            return f"{self.result} = SOLVE_LINEAR {self.arg1}"
        elif self.op == "SOLVE_SYSTEM":
            args_str = ", ".join(map(str, self.arg1)) if isinstance(self.arg1, list) else str(self.arg1)
            return f"{self.result} = SOLVE_SYSTEM [{args_str}]"
        elif self.op == "MAT_GET":
            return f"{self.result} = {self.arg1}[{self.arg2[0]}][{self.arg2[1]}]"
        elif self.op in ["+", "-", "*", "/", "%", "^"]:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        elif self.op == "NEG":
            return f"{self.result} = -{self.arg1}"
        elif self.op == "POS":
            return f"{self.result} = +{self.arg1}"
        elif self.op == "VECTOR":
            elems_str = ", ".join(map(str, self.arg1)) if isinstance(self.arg1, list) else str(self.arg1)
            return f"{self.result} = [{elems_str}]"
        elif self.op == "MATRIX":
            rows_str = ", ".join(f"[{', '.join(map(str, r))}]" for r in self.arg1)
            return f"{self.result} = [{rows_str}]"
        else:
            return f"{self.result} = {self.op} {self.arg1} {self.arg2}"
