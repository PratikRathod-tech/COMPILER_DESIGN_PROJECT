from typing import List, Optional
from src.ai.similarity import similarity_score

class ErrorSuggester:
    def __init__(self, threshold: float = 0.6):
        self.threshold = threshold

    def suggest(self, unknown: str, known_symbols: List[str]) -> Optional[str]:
        if not known_symbols:
            return None
        
        best_match = None
        best_score = -1.0

        for symbol in known_symbols:
            score = similarity_score(unknown, symbol)
            if score > best_score:
                best_score = score
                best_match = symbol

        if best_score >= self.threshold:
            return best_match
        return None
