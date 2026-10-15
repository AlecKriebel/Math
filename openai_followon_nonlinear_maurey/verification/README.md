# Verification and reproduction

The mathematical certificate is the proof in publication/main.tex. Independent detailed audits are in agent_notes/. No Lean formalization is claimed.

Run `python3 check_finite_identities.py` from this directory to reproduce the finite rational checks extracted from the cut auditor's executed code. Python 3.14.6 produced 242 cubic/quartic grid cases (observed maximum ratio 196/25), 500 deterministic rational finite-cut tuples, and all checks passed. These finite checks detect algebra/sign/tie errors; they do not prove the theorem in arbitrary dimension or measures. The proof establishes the general claims.

Run `../publication/build.sh` to build the standalone manuscript; standard packages and Tectonic 0.16.9 suffice. Clean extraction/build receipts are in receipts/. Package hashes identify reviewed bytes; a rebuilt PDF is not guaranteed byte-identical because PDF creation dates differ.
