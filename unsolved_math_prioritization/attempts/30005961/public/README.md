# Primitive positive-entropy automorphisms of strict Calabi–Yau threefolds

Problem 30005961 / OWR-14298581-008. Research checkpoint: 2026-10-03.

**Outcome: unresolved after five substantive attempts. No new threefold is constructed.**
This package is an obstruction and verification note, not a claimed solution or a
new classification theorem. The known varieties (X_3) and (X_7) are not counted
as new examples, even when an additional automorphism on either is exhibited.

The exact target is a smooth simply connected projective complex threefold (X)
with (K_X\simeq\mathcal O_X), not isomorphic to (X_3) or (X_7), and a
biregular automorphism (f) with positive topological entropy that preserves no
dominant rational fibration onto a positive-dimensional lower-dimensional variety.

## Contents

- [PROOF.md](PROOF.md): exact calculations and rigorously delimited obstructions.
- [RESEARCH_LOG.md](RESEARCH_LOG.md): five attempts, outcomes, and remaining gaps.
- [SOURCE_GATE.md](SOURCE_GATE.md): primary-source provenance, definitions, and novelty limits.
- [check_exact.py](check_exact.py): standard-library exact arithmetic checks.
- [exact_results.json](exact_results.json): reproducible checker output.

Run `python3 check_exact.py` in this directory. The computations check only the
specified algebra; they do not certify any construction, primitivity theorem,
crepant-resolution classification, or current literature completeness.

## Strongest established conclusions

1. An explicit integral matrix family gives primitive positive-entropy maps on
   the already known (X_3). It does not vary the threefold.
2. The cited (X_7) map has (d_2>d_1>1); exact cyclotomic identities verify this.
3. The isolated abelian-quotient route is already exhausted by the published
   classification when smoothness, projectivity, and simple connectedness hold.
4. Product-induced maps preserve a rational fibration. Picard-number at most two
   excludes positive-entropy biregular automorphisms in dimension three.
5. Any genuinely new target example must have no nonzero semiample divisor
   orthogonal to (c_2). Turning a real nef eigenclass into such a divisor is
   precisely an unproved step, not a solution.

These results are established facts or elementary deductions; no originality
claim is made for them. A fresh independent audit is required before promotion.
