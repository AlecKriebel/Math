# Function Theory 6.40 checkpoint

- Numeric target: 2306040 / AMR-022-6040, queue rank 583.
- Classification: unsolved; five substantive approaches recorded.
- Main artifact: PARTIAL.md, with full proofs of the stated partials and
  the precise remaining gap. No full-target proof or counterexample.
- Source/status audit: PROVENANCE.md.
- Exact verification: `python3 verify.py` (Python 3.10+, standard library).
- Optional diagnostics: run the three Python scripts in exploratory/ in
  order search_loewner.py, search_two_switch.py, recheck_minima.py.
  They need NumPy, SciPy, mpmath; versions and bounds are in
  exploratory/ENVIRONMENT.json. Search output can vary across versions.
- CHECKS.json contains the exact finite certificates. The numerical
  optimizations and 80-digit evaluations are not interval certificates.
- MANIFEST.json binds the frozen files by SHA-256, excluding itself.

No downloaded source PDF, source corpus, credentials, or private
coordination material is part of this package. No novelty or expert
peer-review claim is made.
