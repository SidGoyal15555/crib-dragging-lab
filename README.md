# Crib Dragging Lab — Interactive Python Project

An interactive educational website demonstrating a reused XOR keystream (two-time pad) vulnerability and crib dragging.

## Features

- Encrypt two equal-length messages with one randomly generated key.
- Visualise `C1 XOR C2 = M1 XOR M2`.
- Inspect individual bytes in decimal, hexadecimal and binary.
- Drag a guessed plaintext fragment using an interactive offset slider.
- Scan and rank every possible crib offset.
- Demonstrate concurrent offset evaluation with `ThreadPoolExecutor`.
- Recover key bytes from known plaintext.
- Run unit tests for the mathematical properties and example attack.

## Requirements

- Python 3.11 or newer recommended.
- pip.

## Windows setup (PowerShell)

```powershell
cd crib_dragging_lab
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks virtual-environment activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Linux / macOS setup

```bash
cd crib_dragging_lab
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

The app normally opens at `http://localhost:8501`.

## Run tests

```bash
pytest -q
```

## Project structure

```text
crib_dragging_lab/
├── app.py
├── core/
│   ├── __init__.py
│   ├── xor_engine.py
│   ├── cipher.py
│   ├── crib_dragger.py
│   ├── key_recovery.py
│   ├── attack_runner.py
│   └── demo.py
├── scoring/
│   ├── __init__.py
│   ├── base.py
│   └── adjacent_difference.py
├── tests/
│   └── test_crypto.py
├── requirements.txt
└── README.md
```

## Architecture and OOP concepts

### Encapsulation
`XOREngine`, `ReusedKeyEncryptor`, `CribDragger`, and `KeyRecovery` keep related operations together.

### Abstraction and polymorphism
`PlaintextScorer` is an abstract base class. New scoring strategies can implement the same `score()` interface and be passed into `AttackRunner` without changing the runner.

### Dataclasses
`CiphertextPair`, `CribCandidate`, and `ScoredCandidate` provide structured, immutable result objects.

### Multithreading
`AttackRunner` uses `ThreadPoolExecutor` to evaluate crib offsets as independent tasks. This demonstrates concurrent scheduling. Since this scoring workload is CPU-bound Python code, threads may not make it faster because of the CPython Global Interpreter Lock (GIL). For CPU-bound scaling, a process pool or native/vectorised implementation may be more suitable.

### Separation of concerns
The Streamlit UI is in `app.py`; cryptographic primitives and attack logic are in `core/`; scoring strategies are in `scoring/`; tests are in `tests/`.

## Built-in example

```text
M1 = The cat sat on the mat.
M2 = Hello, cruel old world.
```

Both are 23 ASCII bytes long.

Useful crib experiments:

| Crib | Offset | Candidate output |
|---|---:|---|
| ` the ` | 14 | `ld wo` |
| `world` | 17 | `e mat` |
| `cat sat on the mat` | 4 | `o, cruel old world` |

## Security note

This project intentionally reuses a key to demonstrate the vulnerability. It is a teaching simulator, not a secure encryption application. Never reuse a one-time pad. For real encryption, use a vetted authenticated-encryption library and follow the algorithm's key and nonce requirements.

## Suggested live presentation

1. Open Overview and explain the two-time-pad equation.
2. Open Encryption Lab and show both ciphertexts.
3. Open XOR Visualizer and move the byte-position slider.
4. Open Crib Dragging Lab. Try ` the ` at offset 14.
5. Try `cat sat on the mat` at offset 4 and show `o, cruel old world`.
6. Run Automated Attack and explain the ranked offsets and heuristic limitation.
7. Open Key Recovery and show that the recovered fragment matches the demo key.
8. Open Code Architecture and explain OOP, scoring abstraction, tests and thread pool.
