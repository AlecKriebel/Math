# Supplemental exact checks

The mathematical proof in PROOF.md is self-contained and uniform in n. These checks corroborate implementation-level details; no finite check or sampled assignment is used to establish the universal quantifier.

Run with Python 3 (standard library only):

    python verify_exact.py

The resulting exact_checks.json records:

- 60 explicit integer-coordinate drawings: m in {3,4}, n from 3 through 32. Integer orientation predicates check every crossing pair and every edge-vertex incidence; rational intersection coordinates check that no two crossing pairs share a point. Every independent-pair total and exact q(n) / 2q(n) crossing count matches.
- 1,650 induced K(3,3) restrictions, across m in {3,4}, n from 3 through 10. Each baseline count is 1 or 3, and direct symbolic coefficient counting gives exactly 36 relevant incidence variables, each with coefficient 2 in the total p-sum.
- 1,792 deterministic seeded complete assignments for n from 3 through 16. These are explicitly samples, not exhaustive verification. They satisfy the claimed weight inequality and the optional two-class parity identity.
- Complete enumeration of the distinct switching-image coset for K(3,3) only. Its 36 input variables span a 17-dimensional subspace of the 18-bit independent-pair space; all 131,072 distinct switched vectors have odd weight, and the exact minimum weight is 1. The program enumerates the image, not the 2^36 original assignments. This check is not needed by the proof.

No network request, nonstandard package, private source, or third-party text is required by the checker. It performs no remote mutation.
