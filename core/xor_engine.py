from __future__ import annotations

class XOREngine:
    """Byte-oriented XOR operations used by the OTP demonstration."""

    @staticmethod
    def xor(left: bytes, right: bytes) -> bytes:
        if len(left) != len(right):
            raise ValueError("XOR inputs must have equal byte lengths.")
        return bytes(a ^ b for a, b in zip(left, right))

    @staticmethod
    def xor_many(*values: bytes) -> bytes:
        if not values:
            return b""
        result = values[0]
        for value in values[1:]:
            result = XOREngine.xor(result, value)
        return result
