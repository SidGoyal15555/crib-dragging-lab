from __future__ import annotations
from scoring.base import PlaintextScorer

class AdjacentDifferenceScorer(PlaintextScorer):
    """
    Simple educational heuristic inspired by the reference article.
    It is NOT Shannon entropy and should not be treated as a reliable language model.
    """

    def score(self, data: bytes) -> float:
        if not data:
            return float("inf")
        filtered = bytes(value for value in data if value != 32)
        if len(filtered) < 2:
            return 255.0
        distance = sum(abs(filtered[i] - filtered[i + 1]) for i in range(len(filtered) - 1))
        return distance / len(data)
