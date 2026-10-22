# Problem 2302069: characteristic growth under differentiation

Status: **partial, 5/5 substantive approaches; no full resolution.**

The question is whether some positive order threshold forces
liminf T(r,f)/T(r,f′) ≤ 1 for every transcendental entire f below that
threshold. Any such threshold is at most 1/2 by established prior work.

The packet contains complete proofs of auxiliary comparisons, the real-zero
subclass, an explicit finite-radius obstruction, and ramification identities.
It identifies the missing angular-loss estimate without claiming that this
reformulation resolves the problem. There is no novelty or priority claim.

- `PROOF.md`: exact target, hypotheses, proofs, and limitations
- `ATTEMPT_LOG.md`: five substantive approaches and their precise gaps
- `SOURCE_GATE.md`: primary-source and actual prior-attempt checks
- `SOURCE_MANIFEST.json`: source URLs, scope, and local-copy hashes
- `STATUS.json`: intended own-row status and turn count
- `verify.py`, `checks.json`: reproducible supplementary controls
- `FROZEN_MANIFEST.json`: SHA-256 binding of all other author artifacts

Run `python3 verify.py` from this folder. No dependencies beyond the Python
standard library are needed. Exact controls check identities and algebra;
quadrature is explicitly illustrative and is not the proof of an infinite
statement. No papers, source corpora, or page images are included.

OpenAI tools were used extensively in research and writing. This is an
unrefereed partial investigation, not a human-reviewed or formally certified
solution. Publication requires a separate independent audit of the frozen
packet.
