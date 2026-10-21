# Adjoint-free recovery: scoped partial results

Problem ID 30006081; queue row 1855. **UNSOLVED after five scoped approaches.**

This authored package records five accepted narrow results: the sharp minimax expected cost pn (not a pointwise lower bound), known-row-subspace recovery and squared-additive tails, r-query EP reconstruction, a known-range rank-one candidate ball, and constant-real-drift Dirichlet PDE bounds. The broad asymmetric geometry and general PDE questions are not resolved. No novelty or priority is claimed.

The existing bounded-query result is Theorem 5.1 of the arXiv preprint *Transpose-free linear algebra*, with real m-by-n inputs, n >= m, 1 <= k <= m, Frobenius error and gamma > 1. Field, aspect-ratio, expected-cost, and norm extensions here have separate proofs. See source_gate.md and theorem_scope_audit.md.

Read research_report.md, independent_review.md (stopping-time proof), structural_scope_review.md, and mathematical_acceptance.md. The latter records acceptance of the original mathematical artifacts and discloses editorial transformations; it is not an independent package audit.

## Reproduction

Python 3 and NumPy are required. From this directory run:

    python3 -B verify_package.py
    python3 -B sanity_checks.py
    python3 -B -O sanity_checks.py
    python3 -B mutation_checks.py
    python3 -B -O mutation_checks.py

The explicit numerical guards remain active with Python optimization. Numerical checks are sanity diagnostics, not proofs, continuum certification, stability guarantees, or bit-complexity results. The recorded full output is sanity_results.json; exact float-output replay may depend on NumPy/BLAS versions. Proofs do not depend on bitwise numerical replay.

package_manifest.json recursively binds all other package files, their byte counts, and SHA-256 hashes. Only that exact root manifest is excluded from its own inventory. Unexpected nested files (including nested manifests), symlinks, unsafe manifest paths, missing files, and altered bytes are rejected. The manifest itself must be independently anchored by its externally recorded hash; a mutable self-contained manifest is not an authenticity signature. The private freeze receipt independently binds every file including the root manifest.

Only authored mathematical writing/checks/audits and sanitized public-source metadata are included. No third-party source documents or datasets are included.
