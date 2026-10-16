# PR195 independent exact reproduction

Run from this directory with standard-library Python 3.10 or later:

```text
python3 -E -S -B -P reproduce_exact.py --verify EXACT_CERTIFICATE.json
python3 -E -S -B -P orthogonal_checks.py --verify ORTHOGONAL_CERTIFICATE.json
```

Each command reconstructs the exact deterministic certificate and requires byte equality with the saved certificate. The orthogonal verifier also checks the frozen primary implementation hash before loading it. No third-party dependencies or external services are used. The original archive is not read or modified by either verifier.

The primary certificate covers ambient differentiation, Euler, compatible restrictions, all five proof-critical ranks, binary degree 9, exact left kernels and nonzero rank minors, a constructive degree-(1,2,3) Hilbert–Burch matrix with all signed minors checked, and the displayed linear syzygy. The orthogonal certificate adds ternary degree 8, full binary Gröbner evidence with all 21 S-pairs and membership representations, exact partial three/four-variable initial-ideal checks at one rational GL4 change, twelve open-flag controls, and excluded characteristic/degeneracy tests. Finite flags do not establish genericity; see the algebraic argument and limits in REPORT.md.

`SAFE_ALLOWLIST.json` is the exact authored public set. `HASH_MANIFEST.json` binds every allowlisted file except itself. `private_work/` is excluded: it contains only the copied archived verifier and its regenerable replay outputs. No downloaded publications, account information, API payloads, original artifacts, or unrelated work are part of this audit package. This folder records a completed assigned review, not a publication, merge, or priority certification.
