# Author verification

Environment: Python 3.12.14, SymPy 1.14.0. The code uses explicit exceptions for all checks; it does not depend on Python `assert` statements.

- Mathematical diagnostics: 85,363 exact checks, predominantly componentwise algebraic Bianchi identities, plus five rejected mathematical negative controls. The detailed result is `results.json`.
- The general tangency identity is independently checked on two deterministic, non-diagonal algebraic curvature examples, in dimensions four and five. This is a regression check, not a proof by sampling.
- Symbolic identities cover endpoint formulas and width formulas. Finite diagonal model checks cover dimensions 4 through 16. The all-dimensional proofs are the written calculations in the five approach files.
- At dimension 12, the entire diagonal-Weyl linearization has an exact characteristic-polynomial check. Four specified non-diagonal pencils have exact polynomial and positivity certificates. Neither check covers all Weyl tensors.
- Normal and `python -O` mathematical replays reproduce the saved output byte for byte.
- Package verification uses an externally supplied SHA-256 of `MANIFEST.json`, exact member names, regular-file and symlink checks, byte sizes, SHA-256 hashes, and an exact mathematical replay/output comparison.
- The integrity harness verifies original and relocated copies under normal and optimized Python. It rejects 11 actual package corruptions and one wrong external-anchor control per mode, 24 rejections total. See `integrity_results.json`.

Reproduction commands, from any working directory:

```
python -B /path/to/math_check.py
python -O -B /path/to/math_check.py
python -B /path/to/verify_package.py --expected-manifest EXTERNAL_SHA256
python -O -B /path/to/verify_package.py --expected-manifest EXTERNAL_SHA256
python -B /path/to/test_integrity.py --expected-manifest EXTERNAL_SHA256
```

The expected SHA-256 must be obtained from the separate trusted handoff receipt. The integrity harness mutates only temporary copies, not the source package. These are accidental-corruption/tamper diagnostics, not a claim that an attacker controlling the Python interpreter or replacing the verifier can be defeated without an independent trusted verifier. An independent auditor must establish the transport anchor separately and review the mathematics.

No remote files were changed and no public release, PR, DOI, or outreach was performed. Independent adversarial audit has not yet occurred. The original mathematical problem remains unresolved by this work.
