# Acceptance: prior five-divisor construction for EP887 / 2366

Accept the core of Theorem 1 in M. Czech's pinned July 2026 manuscript, with the ancillary corrections retained in PROOF.md and AUDIT.md. This is an attributed prior-result audit.

For every positive integer solution z²−56x²=65 with x≥37, the integer
n=(x²−1)(x²−4)(x²−16)(x²−49) has five explicitly given distinct divisors in the strictly open right interval (√n,√n+31 n^(1/4)). The recurrence (x,z)↦(15x+2z,112x+15z), starting from (37,277), supplies infinitely many distinct n. Therefore any constant K in the uniform one-sided formulation must satisfy K≥5. The five cofactors lie in the corresponding left window.

The complete analytical proof retains all factor identities, positivity and distinctness arguments, strict window bounds, shifted-polynomial coefficients, finite base inequalities, and the infinitude argument. It uses no general Pell existence theorem or external upper-bound result. The exact small-parameter inequalities are public; no omitted census is a premise.

## Accepted corrections

- 31 is the least integer window constant that works for all five displayed divisors at every admissible parameter. It is not the least real constant: 30.5 works for the entire admissible family. Every fixed C>30 works eventually; C≤30 never contains all five displayed divisors.
- Pell necessity is restricted to the fifth pair with its prescribed midpoint. It does not prohibit other near-square factorizations off the Pell conic.
- The original question is one-sided. The symmetric reformulation changes the numerical normalization of K and does not imply same-window counting equivalence.
- The balanced-split method is shared with the consecutive-factor construction; the weight sets are not literal affine recenterings. Exhaustive split maximality is not needed or asserted in this edition.
- The nonsquareness argument is retained. Complete sample divisor counts and eventual exact-five behavior are not conclusions of this edition.

Acceptance excludes the incomplete secondary family, speculative sixth-pair and generic geometric discussions, historical priority or record claims, formal-conjectures references as proof evidence, and the complete chains of cited upper-bound proofs. No literal C=1 result is credited to this C=31 construction.

This AI-assisted authored reconstruction is unrefereed. Acceptance means an independent internal AI audit of the pinned prior construction. No external human peer review, journal acceptance, formal proof-assistant certification, novelty, priority, or exhaustive current-literature status is claimed. The general EP887 target remains unresolved by this work.

This edition retains the complete self-contained analytical proof, including the finite inequalities needed at small parameters. It is not a computational reproduction package: executable programs, raw census certificates, copied source documents, and images are not distributed. Historical aggregate checks are supporting metadata; the proof does not depend on access to omitted code or census outputs. Edition preparation performed no new proof search, scholarly-source retrieval, or visual source inspection, and did not execute or import the original mathematical checker.
