# Kirby Problem 4.51 (UnsolvedMath 2927)

**Result: unsolved in this attempt; five substantive approaches completed.**

The target asks whether the equivariant intersection form of every closed oriented smooth four-manifold with fundamental group Z is extended from Z. No full solution, smooth counterexample, or novelty claim is made.

Useful outcomes:

- Corrected a source-triage error: the original Hambleton–Teichner example already has a nonsmoothability proof.
- Recorded the exact conflict between the 2026 problem list and published prior splitting claims without treating either bibliographic statement as a proof certificate.
- Supplied a complete algebraic argument for the definite subcase, using Fourier positivity, localization of norm-one vectors, and prime-order deck orbits. The conclusion has prior claims; this is a reconstruction for review.
- Gave an explicit unimodular 5×5 Laurent isometry showing L ⊕ [−1] is extended.
- Verified exact finite-cover obstruction controls for degrees 1–12 and generated extended controls for prime degrees 3, 5, 7, 11.

The remaining gap is extension in the low-indefinite cases min(b₂⁺,b₂⁻)=1 or 2, or verification of the prior finite-cover descent theorem. The definite argument and all publication text require the independent audit recorded separately before promotion.

## Files

- `PROOF.md`: exact scope, complete partial proofs, certificate, and unresolved gap
- `APPROACH_LOG.md`: five substantive attempts and completion estimates
- `PROVENANCE.md`: exact sources, version conflict, and source limitations
- `controls.py`, `controls.json`: exact reproducible controls
- `SHA256SUMS`: frozen public-file hashes

Run `python3 controls.py`, then `sha256sum -c SHA256SUMS` from this directory. The checker uses only the Python standard library. Finite controls do not certify the infinite general theorem or a topological descent argument.
