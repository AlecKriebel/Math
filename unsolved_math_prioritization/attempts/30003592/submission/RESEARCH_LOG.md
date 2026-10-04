# Research log for problem 30003592

All times are UTC on 4 October 2026. This log records the source gate and five substantive approach families, not a sequence of five numerical experiments. The approaches share some diagnostic examples, explicitly identified below. They are not claimed as five independent discoveries.

## Source and repository gate

At 14:13 the catalogue URL was attempted. The pinned problem identity was checked against the supplied corpus SHA-256. The original OWR report was retrieved and its precise question located. At 14:14 live queue, state, related groups, prior report, code/PR/branch searches and repository policies were checked. At 14:19 the original printed statement was visually checked. The source paragraph treats divisor/curve cases as known; the reported 2025 polyhedrality paper has a different dimensional meaning for its indices. Full-target completion estimate: 0 percent.

## Attempt 1  Torus degeneration

Mechanism: use the finite fan to turn effective cycles into nonnegative sums of invariant orbit closures, then attempt to inherit a finite generating set for movable classes.

Substantive work: reconstructed the F_1 effective and movable cones from their intersection matrices and explicit moving curves. Compared a fixed invariant representative with a movable class, including the coordinate-line example. Proved the convex-cone warning using the rank-one boundary of y^2 <= xz.

Outcome: the effective-cone reduction is valid, but it lacks a criterion on numerical classes that both detects movement and has finitely many generators. Degenerating a family does not supply that step. Detailed proof is in PARTIAL.md, Approach 1. Full-target completion estimate: 0 percent.

## Attempt 2  Boundary intersections

Mechanism: replace an unsupported general duality by the necessary requirement that intersection with every effective divisor remain pseudoeffective in one lower dimension.

Substantive work: constructed the rational polyhedral cone P_d(X) from finite invariant divisor tests. Proved Mov_d subset P_d using proper intersection of a general family member. Computed P_2, Eff_2, Eff_1, Nef_2 and Mov_2 on P(O^2 + O(1)^2) over P^1, and constructed the covering surface families explicitly. Calculated the negative intersection -1 against the effective subscroll P(O^2).

Outcome: a finite outer bound and a complete known special case. The example directly invalidates higher-dimensional Mov=dual-Eff. The general sufficiency of the boundary tests is not proved. This scroll case is prior art in Fulger-Lehmann, not a novel contribution. Full-target completion estimate: 0 percent.

## Attempt 3  Birational positivity

Mechanism: exploit a finite nef divisor cone, then use birational flattening to recover movable classes missed by fixed-model complete intersections.

Substantive work: proved the finite-monomial generation of the fixed-model complete-intersection cone. On the scroll it equals cone(xi^2,xi f) and misses the explicit movable class xi^2-xi f. Checked the birational BPF theorem and analyzed the quantifiers: the flattening model depends on the family, and neither a finite toric list nor finite-generation of all relevant BPF images follows. Checked the published toric Nef/BPF separation to guard against that replacement.

Outcome: fixed-model CI does not suffice, and the valid all-models theorem has an unresolved finiteness gap. The scroll witness is shared with Attempt 2; this is a different proposed mechanism, not a second discovery. Full-target completion estimate: 0 percent.

## Attempt 4  Irreducible cycle obstructions

Mechanism: seek nonpolyhedrality via Hodge-type or nonlinear representability restrictions on individual moving subvarieties.

Substantive work: checked the 2025 surface representability paper. Constructed the sum of two complementary coordinate surfaces on (P^1)^4, verified both move, and calculated its divisor-intersection matrix. Two positive eigenvalues forbid every positive multiple being represented by an irreducible surface, while its class remains in the movable cone.

Outcome: this mechanism cannot use the nonconvex irreducible-representability set as the convex target cone. A separating condition that survives sums/limits is missing. Tropical realization constraints were considered as the same type of source of obstructions; no Mov conclusion was drawn from them. Full-target completion estimate: 0 percent.

## Attempt 5  Product decomposition

Mechanism: build examples or a reduction by taking products with projective space and extracting numerical coefficients through nef intersection and projection.

Substantive work: proved the exact direct-sum formula for Mov_d(X x P^m) and its rational-linear inverse. Deduced rational polyhedrality for products of a toric surface with projective spaces and the orthant description for products of projective spaces. Applied it to the fourfold in Attempt 4.

Outcome: products preserve known cone factors and therefore do not generate a new counterexample from a polyhedral factor or reduce an arbitrary toric variety. This is a partial deduction; no novelty claim is made. Full-target completion estimate: 0 percent.

## Verification checkpoint

At 14:24 the complete five-approach note and machine-readable approach records were written. At 14:26 the exact-arithmetic verifier passed 1,877 controls, including negative controls for the tempting false cone equalities. Those checks supplement the written proofs and do not certify the universal statement. No sixth proof-search approach has been undertaken.

The five-approach research allocation is complete. The mathematical question remains unsolved. A fresh independent audit of the recorded packet is pending. Remote publication, if any, is a separate gated step and is not performed by this attempt.
