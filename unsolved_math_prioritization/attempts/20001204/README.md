# Quartic binary hierarchical models: restricted classifications

AIM Computational Algebraic Statistics Problem 28: problem 20001204 / AIM-COMPUTATION-0042, rank 1275. Accepted restricted partial result, substantive attempt 1 of 5. The general classification remains unresolved by this work. No global novelty or priority claim is made.

## What is proved

The full [mathematical report](MATHEMATICAL_REPORT.md) proves three restricted statements.

- Theorem A: a binary hierarchical complex has Graver degree at most two exactly when, after removing ghosts, it is a simplex or has precisely two facets with one exclusive side a singleton. Equivalently, it is flag and its missing-edge graph is a star together with isolated vertices, including the edgeless case.
- Theorem B: when a facet contains all but one actual vertex, Markov degree at most four is characterized by Theorem A applied to the link on its full specified ground set. Exactly two facets give degree two; exactly three facets with the stated singleton-exclusive-side condition give degree four. Every other case requires degree at least six.
- Theorem C: with exactly three facets and pair-only overlap sizes a,b,c, quartic generation holds precisely when one size is zero or at least two sizes are one. The all-positive quartic case has degree exactly four; when at least two sizes are at least two, degree is at least six. If a=1 and b,c≥1, the exact degree is 2^(1+min(b,c)). At most two facets give degree at most two.

All proofs are included. In particular, the report retains the full analytic obstruction table, all ordered cells and elimination systems, empty/ghost/saturated cases, the exact Lawrence identity and two-point fibers, degree-preserving simplex attachments with both bounds, cone reductions, valid grouped-state fiber restrictions and the complete transportation-cycle degree argument. These finite authored certificate tables and equations are proof reasoning, not redistributed program output.

## Prior work and scope

The original question is in Seth Sullivant’s section of the AIM problem document. Bernstein–O’Neill, Bernstein–Sullivant, Engström–Kahle–Sullivant and the classical Lawrence theorem discussed by Petrović–Stokes supply established mechanisms that are explicitly credited. Král’–Norine–Pangrác already resolve the graphical subcase. Theorems A/B/C may be direct corollaries or short syntheses of known results. No unrestricted graph-minor criterion, or replacement of Graver degree by Markov degree, normality or unimodularity, is asserted.

The [mathematical audit](MATHEMATICAL_AUDIT.md) and [acceptance report](ACCEPTANCE.md) accept exactly these restricted statements. This AI-assisted, unrefereed edition makes no external human peer-review, journal-acceptance, formal proof-assistant certification, priority or exhaustive current-openness claim. Acceptance rests on written mathematical arguments and their stated primary inputs.

## Distributed files

[STATUS.json](STATUS.json) records partial attempt 1/5. [SOURCE_METADATA.json](SOURCE_METADATA.json) records public citations, retained source identities where available, and historical retrieval/inspection limits. Edition preparation claims no fresh scholarly retrieval, source-file rehash, source inspection or literature search. [MANIFEST.json](MANIFEST.json) lists exactly seven files and hashes the other six; the draft pull-request body independently pins the manifest. These identities certify packaging integrity, not mathematical correctness.

Supplemental programs, raw computational outputs, JSON fixtures, datasets, third-party source copies or extracted source text/images, and private coordination/version identities are excluded. Unavailable-checker references and supplementary enumeration/determinant outcomes are removed; the complete analytic proof is retained. This addition-only edition leaves QUEUE.md and unrelated repository content unchanged, adds no substantive proof turn and does not reset attempt accounting.
