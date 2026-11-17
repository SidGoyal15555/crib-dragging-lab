from __future__ import annotations
import streamlit as st
from core.cipher import ReusedKeyEncryptor

DEFAULT_M1 = "The cat sat on the mat."
DEFAULT_M2 = "Hello, cruel old world."

def reset_demo(preserve_messages: bool = False) -> None:
    if not preserve_messages:
        st.session_state.message1 = DEFAULT_M1
        st.session_state.message2 = DEFAULT_M2
    pair = ReusedKeyEncryptor.encrypt_pair(
        st.session_state.message1.encode("utf-8"),
        st.session_state.message2.encode("utf-8"),
    )
    st.session_state.key = pair.key
    st.session_state.cipher1 = pair.ciphertext1
    st.session_state.cipher2 = pair.ciphertext2
    st.session_state.scan_results = []

def ensure_demo_state() -> None:
    if "message1" not in st.session_state:
        st.session_state.message1 = DEFAULT_M1
    if "message2" not in st.session_state:
        st.session_state.message2 = DEFAULT_M2
    if "key" not in st.session_state:
        reset_demo(preserve_messages=True)
