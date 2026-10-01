# 3413: five-turn partial outcome

**Original status: unsolved5/5. Independent review pending.**

The original [Budney realization problem](https://www.openproblemgarden.org/op/realisation_problem_for_the_space_of_knots_in_the_3_sphere) asks for the representations of the **full** finite cyclic, ambient-orientation-preserving and oriented-distinguished-component symmetry group of a hyperbolic link L=L0 union U, where U is an unlink. Realizing a chosen cyclic subgroup on an unlink is not enough.

## Established scoped claims, all awaiting independent review

1. Every negative component cycle has length exactly half the domain order. Hence a signed realization with a negative cycle is faithful. Explicit faithful abstract actions are excluded by this necessary condition.
2. A free ambient cyclic action preserving an unlink has only full-length positive cycles and at most one positive singleton. The converse holds for the ambient problem, by explicit disk/ball models. A fixed-point-free generator alone does not suffice for the free-action hypothesis.
3. Fixed-axis and branched-cover linking arguments give further signed obstructions, including the constraints associated with a positive singleton.
4. Classical Myers theory gives a connected hyperbolic completion for any prescribed free ambient cyclic action on an unlink, preserving the action as a subgroup. Separately, if a hyperbolic completion contains a signed C_m action with k negative cycles, its full source group has index q dividing k. An exact positive-cycle multiplicity test lists the algebraically possible indices; with one negative cycle no enlargement is possible.
5. The fixed-boundary equivariant Dehn lemma sharpens the axis argument to a **complete characterization at the ambient cyclic-unlink level**. Both signed and unsigned cases, including trivial and order-two cases, have explicit smooth constructions and disjoint spanning disks. See Turn5 Theorem5.2 for the complete arithmetic list.

These are consequences of classical inputs with proofs and exact controls; no historical novelty is claimed. The free and nonfree cases have deliberately different scope.

## Original gap

There is no proved general construction adding a **single** distinguished component to each nonfree ambient model so that the complement is hyperbolic. The attempted local-tangle construction leaves global gluing incompressibility and fixed-stratum compatibility unverified. The valid conditional gluing certificate in Turn5 does not assert its existence. Also, the free-action completion only gives subgroup inclusion; it does not suppress every possible additional source symmetry. The arithmetic extension test handles specified signed cases, not every pattern.

Thus the complete ambient characterization must not be promoted to a complete answer to the source. Five substantive author turns are consumed, with timestamps in TURN_STATE.json and RESEARCH_LOG.md. No author proof search continues after freeze. Separate adversarial review is required before any result PR.

## Checks and reading

Read PROOF_COLLECTION.md, then turns/TURN_1.md through TURN_5.md. Their five scripts and saved receipts give20,320;93,882;580,616;34,527;1,496 finite exact controls. These counts concern finite algebra/model bookkeeping. The topological arguments depend on the written proofs and the stated classical theorems, not on exhaustive computation of links.

The original source and seven supporting PDF hashes are in source_manifest.json. The additional Edmonds fixed-boundary theorem was read in its author's public full-text rendering; its PDF retrieval limitation is explicitly recorded in SOURCE_READING_NOTES.md. Full copyrighted reading copies are excluded from the public packet. Estimated completion50% is a heuristic, not a theorem or review grade.
