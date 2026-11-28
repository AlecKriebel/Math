# Matroid base weights: exact reductions and partial proofs

Problem 3064 / OPG-369, “Bases of many weights.” Prose edition dated 2026-10-11.

**PARTIAL. The unrestricted conjecture remains unresolved in this investigation. No counterexample to the conjecture is claimed.**

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. No novelty or exhaustive current-openness claim is made.

## Exact target

For a finite matroid M on E, labels w:E→G into any additive abelian group, rank R, base-weight set S, and its actual stabilizer H, the target is

    |S| ≥ |H| (1 − R + Σ_{Q∈G/H} r(w^{-1}(Q))).

Loops, parallel elements, coloops, repeated labels, rank zero, and infinite ambient groups are allowed.

## What the edition proves

- Exact reduction by the true stabilizer to an aperiodic base-weight set.
- Transfer of each instance to a finite abelian group, preserving periods, stabilizer-coset fiber partitions, fiber ranks, and both sides of the bound.
- The inequality when the stabilizer quotient is torsion-free, with a complete rank induction.
- Equality for at most two nonloop quotient-label classes; unrestricted-label rank-zero, rank-one and corank-one boundary cases.
- Direct-sum closure conditional on the bound for every labeling of each fixed summand into every abelian group, using the explicitly imported Kneser theorem.
- A four-element C6 example showing that an intermediate contraction sumset can be periodic even when the final base-weight set is aperiodic. This refutes a tempting proof step, not the conjecture.

The missing general step remains the aperiodic inequality for arbitrary finite matroids in arbitrary finite abelian groups. Known cases in the literature cover many torsion instances; the remaining description does not claim that all cases outside the elementary proofs are unknown.

## Read the full arguments

- PROOF.md: complete reductions, proofs, witness, remaining gap, and public citations.
- AUDIT.md: full independent mathematical review, exact source-inspection limits, and supplementary historical computation scope.
- ACCEPTANCE.md and ACCEPTANCE.json: precise accepted scope and limitations.
- SOURCES.json: titles, public URLs, retained-version byte identities, inspected portions and dependency boundaries.
- VERIFICATION.json: original and distributed identities, historical checks and preparation limits.
- MANIFEST.json: exact eight-member inventory; hashes the other seven files, with its own digest independently pinned in the publication metadata.

## Evidence and prior credit

The original finite scan reported 669,782 normalized instances in each of normal, -O and -OO modes, with matching mathematical outputs and 21 negative controls. It is supplementary and was not rerun by the independent mathematical auditor or by the edition preparer. The universal partial results are proved in prose. The Kneser source proof was not independently audited.

The prime-order contraction mechanism is already in DeVos’s notes. DeVos–Goddyn–Mohar and the ICALP 2025 article distinguish prior cases from the full conjecture. Sources were inspected only in the portions recorded in SOURCES.json; neither those inspections nor bounded literature searches certify novelty or exhaustive current openness.

This edition distributes only authored prose and public verification/source metadata. Programs, full raw scans, datasets, source documents, source-page images and private coordination material are excluded. Historical identity records identify retained material without distributing it. Preparation makes no new scholarly-source inspection, mathematical computation, or literature-survey claim.
