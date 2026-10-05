# SIS 30003676: auditable partial investigation

General verdict: **NO RESOLUTION**. No novelty claim. No counterexample to the original conjecture is asserted.

- REPORT.md: recovered target, interpretation, bounded literature and prior-work checks, five approach outcomes.
- PROOFS.md: complete proofs for each retained result and explicitly scoped shortcut obstructions.
- verify.py: exact rational finite-state replay; Python 3.10 or later, no packages required.
- verification_results.json: captured expected replay output, 436 checks.
- sources.json and retrieval_history.json: public source metadata and inspection history; no copied source files.
- attempts.json: five substantive approaches and the remaining gap for each.
- MANIFEST.json and verify_manifest.py: closed-payload SHA-256/byte verification and two integrity negative controls.

From this directory run:

    python3 verify.py > /tmp/sis-replay.json
    cmp verification_results.json /tmp/sis-replay.json
    python3 verify_manifest.py

There are five deliberate wrong-formula rejection tests: missing immigration, scaling recovery by θ, treating the mean-field product law as exact, omitting the susceptible-count factor in birth rates, and using ε rather than ε|A| in dual killing. Two additional checks certify the setup of the mean-field and positive-mean/lower-tail logical controls. None of these finite checks substitutes for reading the asymptotic proofs.

Only these authored/metadata payload files belong in the safe package. Downloaded PDFs, source extracts, raw catalog data, and private research coordination are excluded. The manifest excludes its own hash; the external freeze receipt records that hash.
