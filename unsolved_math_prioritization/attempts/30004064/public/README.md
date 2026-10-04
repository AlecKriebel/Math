# Binary tomography: exact-dual recovery fails

Problem 30004064 / OWR-16766-003, rank 550.

**Result:** a complete negative answer to the stated exact-minimizer recovery rule. For every noiseless binary datum, the dual objective in the question has unique optimizer zero. An explicit 3-by-3 row/column tomography instance has exactly two binary solutions and five common pixels, while the prescribed recovery returns all zeros.

This is not a novelty claim. The cited source already recognizes the scalar zero-minimizer obstruction and discusses approximate-iterate signs. Algorithm-specific, smoothed, or auxiliary-primal-variable formulations are outside this result.

- `PROOF.md`: the general theorem, two-solution tomography counterexample, rank-deficient variant, and precise interpretation limits.
- `SOURCE_GATE.md`: primary-source reconciliation, known scalar issue, bounded prior-work checks, and source hashes.
- `ATTEMPT_LOG.md`: one substantive proof attempt, stopped early after complete negative resolution of the exact formulation.
- `verify.py`: dependency-free exact rational and finite checks.
- `verification_results.json`: deterministic output of `python3 verify.py`.
- `FROZEN_MANIFEST.json`: SHA-256 manifest of the frozen authored package.

The proof does not depend on floating-point optimization or exhaustive large-image enumeration. The checks use only 1,044 binary images (two 3-by-3 constraint sets, one 2-by-2 set, two scalar examples) and small rational test vectors. They supplement the proof rather than replace its universal inequality.

Status: candidate negative resolution of the literal formulation; independent review required before any publication. No merger, release, or outreach is implied.
