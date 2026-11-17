from __future__ import annotations
from core.xor_engine import XOREngine

class KeyRecovery:
    """Recovers key bytes where corresponding plaintext bytes are known."""

    @staticmethod
    def recover_fragment(ciphertext: bytes, known_plaintext: bytes, offset: int) -> bytes:
        if offset < 0 or offset + len(known_plaintext) > len(ciphertext):
            raise ValueError("Known plaintext fragment does not fit at this offset.")
        return XOREngine.xor(
            ciphertext[offset:offset + len(known_plaintext)],
            known_plaintext,
        )
