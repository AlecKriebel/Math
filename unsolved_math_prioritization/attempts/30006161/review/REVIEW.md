# Independent audit of 30006161: exceptional-surface chains

**Verdict: PASS_SCOPED_THIN_CHAINS_AND_CYCLE_COVER_OBSTRUCTION.** No mandatory correction. The two original comeagre-orbit questions remain unresolved; retain `unsolved 2/5`.

Reviewed artifact: `PARTIAL_RESULT.md`, SHA-256 `59d2c74070b32a7e8e7926a836b72e6d6bc7743d21f349bd25250456e42dba63`. This audit is separate AI review, not human peer review or certification of novelty.

## Source and hypothesis verification

I inspected the complete original OWR report, printed pp.89–92, and the full BCV accepted manuscript arXiv:2403.08667v3, including its definitions, Theorems 1.2, 5.6 and 7.7, Definition 7.3, Question 1.4, and Proposition 6.13. The source asks about the full homeomorphism groups of the sphere and real projective plane acting on the double-Vietoris space of maximal chains of nonempty subcontinua. It is not an ergodic-theory chaining question. The arXiv record identifies v3 as the accepted Duke version; its DOI resolves to Duke Mathematical Journal volume174 issue14. The journal PDF was not independently compared line by line.

The complete published Gutman2008 PDF was available and read in the relevant sections; printed p.198 was also visually inspected. Its Theorem5.3 states density of ray-induced chains in M(X), rather than merely density of arcs in C(X). Its proof gives a uniform double-Hausdorff approximation to a prescribed chain. Definition5.1 requires a continuous injective ray with dense image. Theorem6.5 gives minimality for the locally transitive group under the strongly arcwise-inseparable Peano hypothesis; LemmaA.1 applies that hypothesis to every closed surface. Examples3.1 cover Homeo(X). Gutman's M(X), not his larger Phi(X), is the chain space used here. These published inputs are credited and are adequate for both exceptional surfaces.

## Independent check of residual thinness

The central topological argument is valid. Given convergence C_n->C in the second Hausdorff metric and K_n->K in the first, with K_n in C_n, the distance from K to C tends to zero, so K belongs to C. This proves the closed incidence relation. The disk-containment and avoidance constraints are separately Hausdorff-closed. Compactness of the two hyperspaces makes projection of their joint constraint compact and hence closed; a mere projection-of-closed argument without compactness would not suffice, but compactness is present.

The disks may be chosen with their entire closed closures inside any specified nonempty open subset of the surface. A proper compact member has a nonempty open complement, so an avoidance witness U_j exists. Thus the countable family F_ij exactly covers the bad chains, with no missing proper-member or root case.

Each finite ray segment is a compact embedded interval. It cannot contain an open surface disk: otherwise a circle inside that disk would embed into an interval, contradicting the topology of a circle. The last member X cannot avoid the nonempty U_j. Hence every F_ij avoids the dense set of ray-induced chains. Its closedness implies nowhere density. Baire's theorem then supplies a dense G_delta of thin chains, and invariance under homeomorphisms puts every orbit of a thick chain inside the meagre complement.

The round-ball examples are indeed maximal connected chains. If a nonempty compact K is comparable with all balls, it contains their common root. Let r_0 be the supremum of radii whose balls are contained in K. For radii below r_0, the balls lie in K; for radii above r_0, comparability forces K inside the corresponding ball. Hausdorff continuity on both sides gives K=B(r_0), including endpoints. On the standard sphere the parameter endpoint is pi; on the standard projective plane it is pi/2. Proper positive-radius balls are disks. Consequently these orbits are meagre despite the credited minimality making them dense.

No implication from residual thinness to existence or absence of a comeagre thin-chain orbit has been smuggled in. If a comeagre orbit existed, it would meet the invariant residual set of thin chains and therefore lie in it, exactly as claimed.

## Independent check of the circular-cover lemma

The closure-intersection pattern in the artifact matches BCV's definition; the extra connected-core hypothesis is not needed for the necessary condition proved here. The cycle has length at least four, so there are no triangles. If adjacent closures meet at p, a cover element containing p either is one of those two or would form a triangle in the closure nerve. In the former case openness forces an actual adjacent overlap. Thus there are points p_i in O_i intersect O_{i+1}, and no triple intersections.

The normalized distance-to-complement functions are positive exactly on their respective open sets. Their sum is strictly positive by the covering property. The resulting nerve map therefore sends O_i into the open star of vertex i, and p_i into the interior of the edge (i,i+1). Connected open sets in a locally path-connected space are path-connected, so the specified paths exist. Each path image can be homotoped relative to its endpoints to the route through the star's central vertex, because the star is contractible. Concatenation winds once around the cycle. This gives a genuine surjection of fundamental groups onto Z, with a basepoint chosen at one p_i. The cover itself also forces X to be connected.

Neither the trivial fundamental group of S² nor the order-two fundamental group of RP² admits this quotient. This excludes this particular sufficient obstruction and agrees with BCV Proposition6.13; it does not prove a generic chain. A locally one-sided curve in RP² should not be confused with a curve contained in the planar open set required by BCV's separate hypothesis. The artifact retains the planar-open-set condition and does not use one-sidedness to overextend that theorem.

## Remaining quantifiers and turbulence

The artifact accurately records Rosendal's quantifiers: one must prove the local mixing statement for every identity neighborhood and nonempty open set, with an open refinement on which every pair of subopens can be reconciled. Excluding one orbit, including the disk chains, is insufficient. BCV's finite graph condition is only used as a necessary condition. Definition7.3 deliberately separates local turbulent points from generic turbulence, the latter including absence of a comeagre orbit. The transitive circle action is a valid diagnostic counterexample to conflating these notions.

## Reproduction and limitations

All 3,447 submitted exact assertions replayed with a byte-identical receipt. The independent standard-library checker separately tests triangle-free closure nerves, lifted winding coordinates in both orientations, finite incidence-witness encodings, and the torsion-to-Z obstruction. The exact independent count is in `independent_results.json`. These finite checks support the mechanisms; they do not prove ray density, Baire category, or the existence of a generic orbit. Those conclusions are justified by the mathematical arguments and specified published inputs.

Copy only the publication files listed in `review_summary.json`. Source PDFs and rendered pages are audit-only and are excluded.
