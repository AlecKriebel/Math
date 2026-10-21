# Replay

The independent verifier requires Python 3 and its standard library. It imports no original submission code or certificates. Run `python3 independent_check.py` from any working directory after making a writable copy of this read-only audit folder. It writes `independent_certificate.json` next to the copied script and prints the compact verification outcome. The original replay is preserved as `replay_stdout.txt`.

All arithmetic deciding the result is rational or integer. Root enclosures use binary search on integer eighth powers on a 10^36 lattice. Boundary roots use 128 exact bisections from [-8,8]. Five sign brackets use 100 exact bisections each. The last coarse endpoint is independently bounded by concavity, with u=100 exactly at s=10^16.

`AUDIT_REPORT.md` contains the mathematical justification for treating these finite interval checks as a proof of existence. A passing script alone does not assert uniqueness within the root brackets or exhaustiveness of their count.
