import pytest
from core.xor_engine import XOREngine
from core.crib_dragger import CribDragger
from core.key_recovery import KeyRecovery

def test_xor_is_reversible():
    a, b = b"hello", b"12345"
    assert XOREngine.xor(XOREngine.xor(a, b), b) == a

def test_xor_self_is_zero():
    data = b"crib dragging"
    assert XOREngine.xor(data, data) == bytes(len(data))

def test_two_time_pad_relation():
    m1 = b"The cat sat on the mat."
    m2 = b"Hello, cruel old world."
    key = bytes(range(len(m1)))
    c1 = XOREngine.xor(m1, key)
    c2 = XOREngine.xor(m2, key)
    assert XOREngine.xor(c1, c2) == XOREngine.xor(m1, m2)

def test_crib_drag_example():
    m1 = b"The cat sat on the mat."
    m2 = b"Hello, cruel old world."
    z = XOREngine.xor(m1, m2)
    assert CribDragger.drag_at(z, b"cat sat on the mat", 4) == b"o, cruel old world"

def test_key_recovery():
    plaintext = b"The cat sat on the mat."
    key = bytes(range(len(plaintext)))
    ciphertext = XOREngine.xor(plaintext, key)
    assert KeyRecovery.recover_fragment(ciphertext, b"cat sat on the mat", 4) == key[4:22]

def test_xor_length_mismatch():
    with pytest.raises(ValueError):
        XOREngine.xor(b"short", b"longer")
