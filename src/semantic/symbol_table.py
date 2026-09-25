from typing import Dict, Optional
from src.semantic.symbol import Symbol

class SymbolTable:
    def __init__(self, parent: Optional['SymbolTable'] = None):
        self.symbols: Dict[str, Symbol] = {}
        self.parent = parent

    def define(self, name: str, symbol: Symbol) -> None:
        self.symbols[name] = symbol

    def lookup(self, name: str) -> Optional[Symbol]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

    def contains(self, name: str) -> bool:
        return self.lookup(name) is not None

    def get_all_names(self) -> list[str]:
        names = list(self.symbols.keys())
        if self.parent:
            names.extend(self.parent.get_all_names())
        return list(set(names))
