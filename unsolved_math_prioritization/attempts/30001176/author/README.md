# Problem 30001176: canonical-filtration counterexample

Read `PROOF.md` first. It supplies a complete infinite W*-algebraic counterexample to the claim that the canonical filtration of every minimal exchangeable, tail-trivial sequence is a noncommutative factorization. It also proves that no factorization preserving the sequence's given singleton image algebras exists.

The report's phrase “gives rise” is not a definition of an alternative enlargement procedure. This packet does **not** assert impossibility when arbitrary enlargement or an unrelated factorization is allowed; the constructed example itself has an enlarged factorization. The source-scope interpretation and this substantive qualification require independent review.

Author disposition: **claimed solved in the canonical/singleton-preserving sense; 1/5 substantive approaches used; early stop for a complete candidate counterexample.** No independent acceptance, historical novelty, human peer review, or formal certification is claimed at this author checkpoint.

## Reproduction

Run from any working directory, with Python 3.10 or newer:

    python3 -B /path/to/release/verify_package.py
    python3 -B -O /path/to/release/verify_package.py
    python3 -B /path/to/release/test_package.py

No third-party package or network is required. The release directory must contain exactly the manifested regular files and `MANIFEST.json`; even empty extra directories, `__pycache__`, symlinks and FIFOs are rejected. Run outputs should be redirected **outside** this directory.

`CODE_PINS.json` was written before the first execution of the three Python files. `verify_package.py` checks the full inventory, all file hashes, and the code pins before executing the finite controls; then it requires byte-exact reproduction of `CONTROL_RESULTS.json`. The external freeze receipt authenticates the manifest and ZIP. Hashing is an integrity check, not a proof of mathematical correctness or protection against an attacker who replaces the entire packet and its trust anchor.

The finite controls contain 2,900,842 explicit checks, including two independently implemented group products, all associativity triples of the two-site group, all three-site cocycle triples, all three-site permutations and products, generated subgroup identities, disjoint trace-basis tests, and the strict meet witness. They supplement the written infinite proof; they do not verify tail triviality by finite extrapolation.

## Files

- `PROOF.md`: full argument, exact source interpretation, qualifications, and public references
- `SOURCE_PROVENANCE.json`: public source titles, URLs, PDF hashes, inspection locations, and bounded public-repository checks
- `DATA_BINDINGS.json`: full input byte-count/hash checks and matching review/statement hashes; no dataset contents
- `APPROACH_LOG.md`: authored mathematical approach, outcome, and rejected overclaims
- `check_controls.py`, `CONTROL_RESULTS.json`: exact finite supplementary controls
- `verify_package.py`, `test_package.py`, `CODE_PINS.json`, `MANIFEST.json`: portable integrity and negative-control tools

No source PDF, source extract, corpus record, private source, personal information, or private coordination material is part of this release.
