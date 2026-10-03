# Kirby Problem 4.21 (ID 2897)

**Status: partial progress; the general closed 4-manifold question is unresolved here.**

This investigation records five substantive approaches to decomposing a closed topological 4-manifold into a smoothable piece and an acyclic piece along an integral homology 3-sphere.

- `PROOF.md`: proved special cases, precise punctured-smoothing gap, exact lattice obstruction calculation, and a proof that the compact obstruction can embed in a positive closed example.
- `SOURCE_GATE.md`: primary theorem locations, source fingerprints, scope checks, and retrieval limits.
- `RESEARCH_LOG.md`: five distinct attempts and the exact obstruction to extending each.
- `verify.py` and `verification.json`: reproducible standard-library exact-arithmetic checks.
- `STATUS.json`: machine-readable scope, with no full-solution or novelty claim.
- `SHA256SUMS`: checksums of the authored files.

## Verification

Run from this directory with Python 3:

```sh
python3 verify.py > verification.reproduced.json
cmp verification.json verification.reproduced.json
sha256sum -c SHA256SUMS
```

The program checks finite lattice instances and elementary integral chain-map calculations. It is not a formal verification of the topological arguments or a decision procedure for the conjecture. The all-n lattice calculation is proved symbolically in `PROOF.md`.

Original source PDFs and full extracted texts are not included. Follow the primary links in `SOURCE_GATE.md` for the papers. No novelty is claimed for these deductions or known positive cases.
