# Function Theory 5.60: partial results

**Unsolved, 5/5 turns.** No complete proof or counterexample is claimed.

The packet proves the requested implication for polynomial φ of degree at most 2α and reconstructs the known integer-α case. It also reduces any hypothetical analytic counterexample to a robust polynomial one with rational parameters and Gaussian-rational coefficients. Five distinct routes, their exact gaps, and a bounded heuristic search are documented. No novelty is claimed for these observations.

- `PROOF.md`: exact target, full proofs of partial results, obstructions and remaining gap
- `ATTEMPT_LOG.md`: five substantive routes and completion estimates
- `SOURCE_GATE.md`, `SOURCE_MANIFEST.json`: sources, checks and access limits
- `verify.py`, `CHECKS.json`: 208 exact rational algebra controls, standard library only
- `search.py`, `SEARCH.json`: nonexhaustive floating-point search and its limits
- `STATUS.json`: machine-readable disposition
- `SHA256SUMS.json`, `verify_manifest.py`: frozen-packet integrity

From this directory:

    python3 verify.py
    python3 verify_manifest.py

Optional heuristic reproduction requires NumPy (recorded run: 2.3.5, Python 3.12.14):

    python3 search.py --output SEARCH-replay.json

The optional search covers 1,152 fixed-seed samples and ten denser angle-grid repeats. Numerical outputs may differ slightly by platform. Neither exact algebra tests nor floating-point sampling verify the analytic proofs or resolve the open target. Independent review of the written arguments is required. Original source PDFs and full dataset corpora are not included.
