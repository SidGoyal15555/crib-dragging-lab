from __future__ import annotations
from abc import ABC, abstractmethod

class PlaintextScorer(ABC):
    """Abstraction for interchangeable candidate-scoring strategies."""

    @abstractmethod
    def score(self, data: bytes) -> float:
        """Return a score where lower values should indicate a better candidate."""
        raise NotImplementedError
