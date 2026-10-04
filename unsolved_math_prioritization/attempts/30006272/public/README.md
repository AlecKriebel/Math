# Orbit closures of complexes: partial Catalan-formula investigation

ID 30006272 / OWR-14299283-013, rank 554.

**The general question remains unsolved after five substantive approaches.**
The catalogue's Ekedahl–Oort title is a notation error: the original
question concerns canonical-basis elements indexed by orbits of complexes.

- `PROOF.md`: complete partial proofs, scope and remaining gap.
- `SOURCE_GATE.md`: exact target, inspected sources and update checks.
- `ATTEMPT_LOG.md`: five mathematical approaches and their outcomes.
- `verify.py`, `verification.json`: reproducible bounded exact checks.
- `SOURCE_HASHES.json`: hashes/URLs of locally inspected primary PDFs.
- `FROZEN_MANIFEST.json`: SHA-256 binding of this authored packet.

Run with Python 3 and its standard library:

    python3 verify.py

To save a replay independently:

    python3 verify.py --output /tmp/rank554-replay.json

The checks cover 2,460 small profiles, 18,525 rank-drop cases,
12,580 relevant-path comparisons, 55 independent partition/Gaussian
comparisons, and 180 determinantal cases. Counts include overlapping
families of assertions. No large search or IC software is used.

The strongest general partial result is an exact smallness/semismallness
criterion for a specified incidence resolution, with Gaussian-product
formulas where the map is small. A worked non-sparse case is computed by
semismall decomposition. A failure of a chosen resolution is not a
counterexample to the original conjectural extension.

No source PDFs, source corpora, raw tool outputs or private context are
included. Independent review is a separate step; this author packet does
not assert that such a review has passed.
