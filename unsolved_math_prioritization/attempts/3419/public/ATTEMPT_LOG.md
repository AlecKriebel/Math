# Attempt log: ID 3419 / OPG-37237

All five attempts were made on 3 October 2026. The outcome is unresolved. Literature checking and finite computations are not counted as proof of a solution.

## 1. Lower the higher-dimensional embedding construction

Goal: preserve an embedded undecidable group while obtaining a 2-knot realization.

Work: checked the perfect-container/HNN construction, explicitly computed its two H₂ maps and its normal generator, and proved the necessary homological/peripheral conditions for a 2-knot exterior. Compared the actual genus-zero presentation theorem with the weaker surface-group/Wirtinger criterion.

Result: the known construction reaches 3-knot groups. No connected, unlinked, genus-zero saddled presentation or geometric 2-knot realization was produced. An embedded thickening or the Kervaire conditions alone do not close this gap. See PROOF.md §§1–2.

## 2. Encode an undecidable group in a ribbon presentation

Goal: use labelled-tree Wirtinger presentations to ensure geometric realization from the start.

Work: proved cyclic abelianization, vanishing second homology and weight one by the tree incidence matrix; proved that triangular label dependencies force the group to be Z. Checked every labelled tree up to six vertices as exact controls. Compared the nontriangular BS(1,2) example with its actual word-problem algorithm.

Result: the simplest faithful-encoding proposal collapses; the general cyclic-dependency construction lacks an injectivity/undecidability proof. See PROOF.md §3.

## 3. Prove a general word-problem algorithm via fibering

Goal: extend 3-manifold decidability to all 2-knot complements.

Work: supplied a complete word-scanning algorithm in H⋊Z, including negative stable-letter exponents, and applied it to every fibred 2-knot. Checked exactly which finiteness-to-fibering assertions in Hillman's discussion are conditional.

Result: fibred knots cannot supply a positive example. No theorem reducing every 2-knot to this case is available in the argument. See PROOF.md §4.

## 4. Use finite quotients or a non-residually-finite candidate

Goal: either complete a general dovetailed decision procedure or exploit failure of residual finiteness to obtain a candidate.

Work: proved that the explicit Hillman satellite group has a nontrivial order-three element invisible in every finite quotient. Then gave a terminating Britton-reduction algorithm for its entire word problem using C₃⋊Z normal forms and two decidable edge-membership tests. Implemented the algorithm with deterministic relation-insertion and permutation-representation controls.

Result: the residual-finiteness route fails, but its counterexample is not an undecidable group. See PROOF.md §5.

## 5. Test the September 2026 small undecidable group

Goal: apply the recent three-generator, nine-relator, weight-one construction directly or through knot realization.

Work: read the actual injective HNN decomposition and subgroup proofs. Tracked rational H₂ through all six stages, computing the H₂ dimensions of both non-free edge groups used at the last two stages. Established the lower-bound chain 2,5,7,7,4,2 without assuming the intermediate subgroup Δ is free, without computing unspecified semigroup words, and without inferring group deficiency from one presentation.

Result: dim H₂(Γ₆;Q)≥2 excludes this particular group from every sphere-knot group class. Its H₁=Z and normal generator do not suffice. Killing the remaining homology while preserving undecidability and achieving dimension-four realization remains unproved. See PROOF.md §6.

## Final boundary

No full solution, refutation, geometric example, universal algorithm, or novelty claim is asserted. The five attempts produce reusable reductions, exclusions and one concrete homological obstruction. Independent review must assess the written mathematics; the finite checks alone are insufficient.
