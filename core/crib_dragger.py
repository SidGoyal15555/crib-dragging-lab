from __future__ import annotations
from dataclasses import dataclass
from core.xor_engine import XOREngine

@dataclass(frozen=True)
class CribCandidate:
    offset: int
    crib: bytes
    output: bytes

class CribDragger:
    """Slides a guessed plaintext fragment across Z = C1 XOR C2."""

    @staticmethod
    def drag_at(combined: bytes, crib: bytes, offset: int) -> bytes:
        if not crib:
            raise ValueError("Crib cannot be empty.")
        if offset < 0 or offset + len(crib) > len(combined):
            raise ValueError("Crib offset is outside the valid range.")
        return XOREngine.xor(combined[offset:offset + len(crib)], crib)

    @classmethod
    def all_offsets(cls, combined: bytes, crib: bytes) -> list[CribCandidate]:
        if not crib or len(crib) > len(combined):
            raise ValueError("Crib must be non-empty and no longer than the data.")
        return [
            CribCandidate(i, crib, cls.drag_at(combined, crib, i))
            for i in range(len(combined) - len(crib) + 1)
        ]
