from __future__ import annotations
import secrets
from dataclasses import dataclass
from core.xor_engine import XOREngine

@dataclass(frozen=True)
class CiphertextPair:
    ciphertext1: bytes
    ciphertext2: bytes
    key: bytes

class ReusedKeyEncryptor:
    """Teaching-only encryptor that intentionally reuses one key to show the flaw."""

    @staticmethod
    def generate_key(length: int) -> bytes:
        if length <= 0:
            raise ValueError("Key length must be positive.")
        return secrets.token_bytes(length)

    @staticmethod
    def encrypt(plaintext: bytes, key: bytes) -> bytes:
        if len(plaintext) != len(key):
            raise ValueError("For this OTP demo, key and plaintext lengths must match.")
        return XOREngine.xor(plaintext, key)

    @classmethod
    def encrypt_pair(cls, plaintext1: bytes, plaintext2: bytes) -> CiphertextPair:
        if len(plaintext1) != len(plaintext2):
            raise ValueError("The two messages must have equal byte lengths.")
        key = cls.generate_key(len(plaintext1))
        return CiphertextPair(
            cls.encrypt(plaintext1, key),
            cls.encrypt(plaintext2, key),
            key,
        )
