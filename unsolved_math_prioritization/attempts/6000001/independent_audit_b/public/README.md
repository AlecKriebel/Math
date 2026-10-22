# Independent audit B of the statistical embedding proof

**Verdict: PASS for the exact frozen theorem, with no required mathematical patch.**

The accepted author PROOF.md has SHA-256 `a26c1755bc6f61085db4c01b6579701ff380822f2cc58a3ffbfb4acfa49370a2`; its author manifest has SHA-256 `7df56d745e4c57a30d0303388b1adda3e52d1c99190d2f96fe50b6d616b1cf3f`.

The theorem gives a global proper embedding of every smooth positive-definite statistical n-manifold without boundary into a positive Hessian domain in dimension binomial(2n+4,3). Both ordered torsion-free dual connections are induced. The target may be nonconvex and incomplete, and its dual affine coordinates need only be local.

## Contents

- `FULL_REPORT.md`: complete independent mathematical review and scope verdict
- `ACCEPTANCE.json`: machine-readable verdict tied to the exact author freeze
- `SOURCE_METADATA.json`: public source titles, URLs, inspection history, hashes and byte counts
- `AUTHOR_FREEZE_VERIFICATION.json`: authenticated author inventory and corroborating author test output
- `INDEPENDENT_CHECKS.json`: output of the independent exact checks and negative controls
- `independent_checks.py`: reproducible independent checks; Python 3, SymPy and NumPy required
- `CITATION_SCOPE_NOTE.md`: optional primary-source citation clarification; no original file is changed
- `verify_audit.py`: audit integrity and optional exact-author-packet verification
- `MANIFEST.json`: complete audit inventory, excluding itself

Run `python independent_checks.py` with assertions enabled to reproduce the independent finite checks. They corroborate the mathematics and do not prove its global arguments.

Run `python verify_audit.py --expected-manifest HASH --author-dir PATH`, supplying this audit manifest's SHA-256 from an independent channel and the directory containing the original author manifest and proof. The author argument is optional; omitting it verifies only the audit bytes and recorded binding.

This packet contains authored review and public verification metadata only. It contains no copied papers, copied source extracts, datasets, private-source files, or private coordination records. PASS is an independent mathematical assessment of the stated candidate, not journal acceptance or a novelty claim.
