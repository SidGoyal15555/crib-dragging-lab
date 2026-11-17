from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.express as px

from core.demo import ensure_demo_state, reset_demo
from core.xor_engine import XOREngine
from core.crib_dragger import CribDragger
from core.key_recovery import KeyRecovery
from core.attack_runner import AttackRunner
from scoring.adjacent_difference import AdjacentDifferenceScorer

st.set_page_config(
    page_title="Crib Dragging Lab",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
.stApp { background: linear-gradient(135deg,#fff8f4 0%,#f4f8ff 48%,#f8f2ff 100%); }
.block-container { padding-top: 1.5rem; max-width: 1450px; }
.hero {
  padding: 1.7rem 2rem; border-radius: 22px;
  background: linear-gradient(115deg,#263d70,#5668b8 55%,#b45b9b);
  color: white; margin-bottom: 1rem;
  box-shadow: 0 12px 30px rgba(48,55,110,.16);
}
.hero h1 { color: white; margin: 0; font-size: 2.55rem; }
.hero p { color: #edf1ff; margin: .5rem 0 0 0; font-size: 1.05rem; }
.info-card {
  background: rgba(255,255,255,.88); border: 1px solid #e5e9f5;
  padding: 1rem 1.15rem; border-radius: 16px; height: 100%;
  box-shadow: 0 5px 18px rgba(40,55,95,.05);
}
.metric-card {
  background: white; border: 1px solid #e8eaf4; border-radius: 14px;
  padding: .9rem 1rem; box-shadow: 0 4px 14px rgba(30,45,80,.05);
}
.small-muted { color: #64748b; font-size: .88rem; }
code { color: #7045a6 !important; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

ensure_demo_state()

st.sidebar.title("🔐 Crib Dragging Lab")
st.sidebar.caption("Interactive two-time-pad cryptanalysis")
page = st.sidebar.radio(
    "LAB MODULES",
    [
        "🏠 Overview",
        "🔑 Encryption Lab",
        "⊕ XOR Visualizer",
        "🎯 Crib Dragging Lab",
        "⚙️ Automated Attack",
        "🗝️ Key Recovery",
        "💻 Code Architecture",
    ],
)
st.sidebar.divider()
st.sidebar.caption("Demo messages")
st.sidebar.code("The cat sat on the mat.\nHello, cruel old world.")
if st.sidebar.button("↻ Reset demonstration", use_container_width=True):
    reset_demo()
    st.rerun()

m1 = st.session_state.message1.encode("utf-8")
m2 = st.session_state.message2.encode("utf-8")
key = st.session_state.key
c1 = st.session_state.cipher1
c2 = st.session_state.cipher2
z = XOREngine.xor(c1, c2)

def hero(title: str, subtitle: str):
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )

def bytes_table(data: bytes, label: str):
    frame = pd.DataFrame({
        "Position": list(range(len(data))),
        "Decimal": list(data),
        "Hex": [f"{b:02X}" for b in data],
        "Character": [chr(b) if 32 <= b <= 126 else "·" for b in data],
    })
    st.caption(label)
    st.dataframe(frame, use_container_width=True, hide_index=True, height=260)

if page == "🏠 Overview":
    hero("CRIB DRAGGING LAB", "Break the Two-Time Pad — explore the mathematics, inspect the bytes, and recover the key.")
    st.subheader("What are we demonstrating?")
    st.write(
        "When two messages are encrypted with the same XOR keystream, XORing their "
        "ciphertexts cancels the keystream and reveals the XOR of the two plaintexts. "
        "A guessed plaintext fragment (a **crib**) can then be moved across the result "
        "to reveal candidate fragments of the other message."
    )
    cols = st.columns(4)
    for col, value, label in zip(
        cols, ["01", "02", "03", "04"],
        ["Encrypt twice", "Cancel the key", "Drag a crib", "Recover key bytes"],
    ):
        col.markdown(
            f'<div class="metric-card"><h2 style="color:#7956bd">{value}</h2>'
            f'<b>{label}</b></div>', unsafe_allow_html=True
        )
    st.subheader("The central equation")
    st.latex(r"C_1 \oplus C_2 = (M_1 \oplus K)\oplus(M_2\oplus K)=M_1\oplus M_2")
    a, b = st.columns(2)
    with a:
        st.markdown('<div class="info-card"><b>Message 1</b>', unsafe_allow_html=True)
        st.code(st.session_state.message1)
        st.markdown("</div>", unsafe_allow_html=True)
    with b:
        st.markdown('<div class="info-card"><b>Message 2</b>', unsafe_allow_html=True)
        st.code(st.session_state.message2)
        st.markdown("</div>", unsafe_allow_html=True)
    st.info("Use the sidebar to move through the lab. The built-in example uses equal-length ASCII messages so byte positions align clearly.")
    st.warning("Educational demonstration only. Never reuse a one-time pad or a nonce where the encryption mode requires uniqueness.")

elif page == "🔑 Encryption Lab":
    hero("Encryption Lab", "Create two ciphertexts with one shared key and inspect the result.")
    st.write("Edit the messages below. For this byte-aligned demonstration, use equal-length ASCII messages.")
    col1, col2 = st.columns(2)
    with col1:
        new_m1 = st.text_area("Plaintext M1", st.session_state.message1, height=100)
    with col2:
        new_m2 = st.text_area("Plaintext M2", st.session_state.message2, height=100)
    st.caption(f"Byte lengths: M1 = {len(new_m1.encode())}, M2 = {len(new_m2.encode())}")
    if st.button("Encrypt both messages with the same random key", type="primary"):
        if len(new_m1.encode()) != len(new_m2.encode()):
            st.error("The two messages must have equal byte lengths for this visual demonstration.")
        elif not new_m1 or not new_m2:
            st.error("Messages cannot be empty.")
        else:
            st.session_state.message1 = new_m1
            st.session_state.message2 = new_m2
            reset_demo(preserve_messages=True)
            st.success("Both messages encrypted with the same randomly generated key.")
            st.rerun()
    st.subheader("Ciphertext inspection")
    x, y = st.columns(2)
    with x:
        st.markdown("**Ciphertext C1 (hex)**")
        st.code(c1.hex(" ").upper())
    with y:
        st.markdown("**Ciphertext C2 (hex)**")
        st.code(c2.hex(" ").upper())
    st.caption("The same random key is used for both encryptions. The key is available in this teaching simulator so the demonstration can be verified.")

elif page == "⊕ XOR Visualizer":
    hero("XOR Visualizer", "Watch the shared key disappear from the ciphertext relationship.")
    st.latex(r"C_1=M_1\oplus K")
    st.latex(r"C_2=M_2\oplus K")
    st.latex(r"C_1\oplus C_2=M_1\oplus M_2\oplus K\oplus K")
    st.latex(r"K\oplus K=0 \quad\Longrightarrow\quad C_1\oplus C_2=M_1\oplus M_2")
    st.subheader("Byte-level view")
    idx = st.slider("Choose a byte position", 0, len(z)-1, min(4, len(z)-1))
    rows = [
        ("M1 byte", m1[idx]), ("Key byte", key[idx]),
        ("C1 = M1 XOR K", c1[idx]), ("M2 byte", m2[idx]),
        ("C2 = M2 XOR K", c2[idx]), ("C1 XOR C2", z[idx]),
        ("M1 XOR M2", m1[idx] ^ m2[idx]),
    ]
    df = pd.DataFrame([
        {"Value": name, "Decimal": val, "Hex": f"{val:02X}", "Binary": f"{val:08b}",
         "Character": chr(val) if 32 <= val <= 126 else "·"}
        for name, val in rows
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.success(f"At byte position {idx}, C1 XOR C2 = {z[idx]:08b} and M1 XOR M2 = {m1[idx] ^ m2[idx]:08b}. They are identical.")
    st.subheader("Combined plaintext relationship")
    st.code(z.hex(" ").upper())

elif page == "🎯 Crib Dragging Lab":
    hero("Crib Dragging Lab", "Move a guessed plaintext fragment across Z = C1 XOR C2.")
    st.markdown("**Attacker's available data:** the combined bytes `Z`. The actual plaintexts are shown only as instructor-side verification in this simulator.")
    crib_text = st.text_input("Your guessed crib", value=" the ")
    crib = crib_text.encode("utf-8")
    if not crib:
        st.warning("Enter a non-empty crib.")
    elif len(crib) > len(z):
        st.error("Crib is longer than the combined ciphertext.")
    else:
        offset = st.slider("Drag the crib — choose starting offset", 0, len(z)-len(crib), min(14, len(z)-len(crib)))
        result = CribDragger.drag_at(z, crib, offset)
        left, right = st.columns([1, 1])
        with left:
            st.metric("Current offset", offset)
            st.metric("Crib length (bytes)", len(crib))
        with right:
            st.metric("Candidate output", result.decode("utf-8", errors="replace"))
            st.caption("A readable fragment is evidence of a promising alignment, not proof by itself.")
        st.subheader("Alignment view")
        positions = list(range(len(z)))
        crib_start, crib_end = offset, offset + len(crib)
        alignment = pd.DataFrame({
            "Index": positions,
            "Z byte (hex)": [f"{b:02X}" for b in z],
            "Crib window": [
                chr(crib[i-offset]) if crib_start <= i < crib_end and 32 <= crib[i-offset] <= 126
                else ("·" if crib_start <= i < crib_end else "")
                for i in positions
            ],
            "Candidate byte": [
                f"{result[i-offset]:02X}" if crib_start <= i < crib_end else ""
                for i in positions
            ],
        })
        st.dataframe(alignment, use_container_width=True, hide_index=True)
        st.subheader("Byte operation at this offset")
        st.code(
            f"Z[{offset}:{offset+len(crib)}] = {z[offset:offset+len(crib)].hex(' ').upper()}\n"
            f"crib         = {crib.hex(' ').upper()}\n"
            f"XOR output   = {result.hex(' ').upper()}\n"
            f"text         = {result.decode('utf-8', errors='replace')}"
        )
        st.caption("Try crib = ' the ' at offset 14, then try 'world' at offset 17, and finally 'cat sat on the mat' at offset 4.")

elif page == "⚙️ Automated Attack":
    hero("Automated Attack", "Evaluate every possible crib offset and rank candidate outputs.")
    crib_text = st.text_input("Crib to scan", value=" the ", key="auto_crib")
    if st.button("Run multithreaded offset scan", type="primary"):
        if not crib_text:
            st.error("Enter a crib first.")
        else:
            runner = AttackRunner(AdjacentDifferenceScorer())
            results = runner.scan(z, crib_text.encode("utf-8"), max_workers=4)
            st.session_state.scan_results = results
            st.success(f"Scanned {len(results)} candidate offsets using ThreadPoolExecutor.")
    results = st.session_state.get("scan_results", [])
    if results:
        df = pd.DataFrame([
            {
                "Rank": rank + 1,
                "Offset": item.offset,
                "Score (lower is better)": round(item.score, 3),
                "Candidate": item.output.decode("utf-8", errors="replace"),
            }
            for rank, item in enumerate(results)
        ])
        st.dataframe(df, use_container_width=True, hide_index=True)
        chart = px.bar(
            df.sort_values("Offset"), x="Offset", y="Score (lower is better)",
            color="Score (lower is better)", color_continuous_scale="Purples",
            title="Crib candidate score by offset",
        )
        st.plotly_chart(chart, use_container_width=True)
        st.info("The adjacent-byte score is a simple heuristic, not Shannon entropy. A low score can still be a false positive.")
    else:
        st.info("Run the scan to see all candidate offsets ranked by their heuristic score.")
    with st.expander("How multithreading is used"):
        st.code(
            "with ThreadPoolExecutor(max_workers=4) as executor:\n"
            "    results = list(executor.map(score_offset, offsets))\n"
            "results.sort(key=lambda item: item.score)"
        )
        st.write("Each offset is evaluated as an independent task. Threads demonstrate concurrent task scheduling; CPU-bound Python work may not become faster because of the GIL.")

elif page == "🗝️ Key Recovery":
    hero("Key Recovery", "Use a known plaintext fragment to recover the corresponding key bytes.")
    st.write("Enter a plaintext fragment and the offset where it is believed to occur in message 1.")
    known_text = st.text_input("Known plaintext fragment", value="cat sat on the mat")
    max_offset = max(0, len(c1) - len(known_text.encode("utf-8")))
    offset = st.slider("Plaintext starting offset", 0, max_offset, min(4, max_offset))
    known = known_text.encode("utf-8")
    if known and offset + len(known) <= len(c1):
        recovered = KeyRecovery.recover_fragment(c1, known, offset)
        recovered_other = XOREngine.xor(c2[offset:offset+len(recovered)], recovered)
        st.subheader("Recovered key fragment")
        st.code(recovered.hex(" ").upper())
        st.subheader("Decrypt corresponding bytes of message 2")
        st.code(recovered_other.decode("utf-8", errors="replace"))
        st.metric("Matches actual demo key", "YES" if recovered == key[offset:offset+len(recovered)] else "NO")
        st.caption("This works because K = C XOR M. The fragment only recovers key bytes at the known plaintext positions.")
    else:
        st.error("The known plaintext does not fit at this offset.")

elif page == "💻 Code Architecture":
    hero("Code Architecture", "A modular Python design using OOP, type hints, dataclasses and concurrency.")
    st.subheader("Project layers")
    architecture = [
        ("Presentation", "app.py", "Streamlit pages, controls and visualizations"),
        ("Cryptographic core", "core/xor_engine.py", "Byte-wise XOR operations"),
        ("Attack logic", "core/crib_dragger.py", "Crib alignment and candidate generation"),
        ("Scoring", "scoring/", "Pluggable plaintext scoring strategies"),
        ("Concurrency", "core/attack_runner.py", "ThreadPoolExecutor offset scanning"),
        ("Verification", "tests/", "Pytest unit tests"),
    ]
    st.table(pd.DataFrame(architecture, columns=["Layer", "Module", "Responsibility"]))
    st.subheader("Key design decisions")
    st.markdown("""
    - **Single responsibility:** encryption, XOR, dragging, scoring and UI are separate.
    - **Encapsulation:** cryptographic operations are exposed through small classes.
    - **Abstraction and polymorphism:** scoring strategies share a common interface.
    - **Dataclasses:** each candidate has a clear structured result.
    - **Concurrency:** each crib offset can be evaluated independently.
    - **Testing:** algebraic properties are checked automatically.
    """)
    st.info("Open the source files in the project folder. The README contains setup instructions, module explanations and suggested presentation talking points.")
