from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from scoring.base import PlaintextScorer
from core.crib_dragger import CribDragger

@dataclass(frozen=True)
class ScoredCandidate:
    offset: int
    output: bytes
    score: float

class AttackRunner:
    """Scores all possible crib offsets using a configurable worker pool."""

    def __init__(self, scorer: PlaintextScorer):
        self.scorer = scorer

    def scan(self, combined: bytes, crib: bytes, max_workers: int = 4) -> list[ScoredCandidate]:
        candidates = CribDragger.all_offsets(combined, crib)

        def evaluate(candidate):
            return ScoredCandidate(
                offset=candidate.offset,
                output=candidate.output,
                score=self.scorer.score(candidate.output),
            )

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            scored = list(executor.map(evaluate, candidates))

        return sorted(scored, key=lambda item: item.score)
