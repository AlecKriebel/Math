# Kourovka21.138

Updated 2026-10-24T17:15:03.955143+00:00. Research label: **unsolved**. Full-problem discovery estimate: **12%** (planning estimate, not confidence in a conjecture). No unrestricted proof, counterexample, preprint, new DOI or tracker row.

## Original quantified target and status evidence

An infinite finitely presented group G has every infinite-index subgroup free, including infinitely generated subgroups. Must G itself be free or a closed aspherical surface group? H. Wilton, official21st edition,20October2026update3, printedp200. The exact conclusion is an isomorphism classification, not merely a virtual classification. The torus and Klein bottle are permitted surface groups.

The official entry is unstarred and has no update-only solution notice. Wilton's current Question0.1 and the2026Kreuzer–Moldenhauer–Rosenberger paper retain the unrestricted question; checked positive results concern additional hypotheses. The preliminary priority audit found no full resolution through24October2026. This is dated bounded evidence, not a certificate of global openness.

## Accepted partial deductions

- **Virtually indicable classification.** Every infinite finitely generated virtually indicable IF group is free or surface. IF makes a height kernel free, with no finite-rank assumption. GKLProp3.5 gives hyperbolicity or surface; LintonCor1.5 covers the infinite-rank free-by-cyclic hyperbolic case by virtual compact specialness; WiltonA applied to a compact special finite-index subgroup contradicts IF unless it is free or surface. Torsion-free finite-extension theorems give the exact isomorphism conclusion for G. A fresh nonauthor independently checked all inputs, finite-index passages and flat-surface boundaries. This is a synthesis of existing theorems, not an asserted new complete solution. Hence a counterexample must be **FAb**, with every finite-index abelianization finite.
- **General structural filters.** Infinite IF groups are torsion-free, and finitely presented IF groups are coherent. A nonfree finitely generated IF group is one-ended. A subgroup Z² forces the torus/Klein alternative. Full IF directly implies power balance: conjugate nonzero powers of one infinite-order element have equal absolute exponents. The free kernel of the commensurator modular map proves this without a virtual-indicability theorem.
- **Normal-subgroup obstruction.** A nonabelian finitely generated free normal subgroup of infinite index forces virtual indicability: its centralizer vanishes, the quotient embeds Out(F_r), virtual torsion-freeness supplies an infinite-order quotient element, and the preimage-free normal-subgroup theorem forces a cyclic subgroup of finite index. Thus such a normal subgroup cannot occur in a counterexample. Finite normal generation is not substituted for subgroup finite generation. A cyclic normal subgroup inverted by an element produces an embedded Klein bottle group; in a counterexample it must instead be central.
- **Two-branch remainder.** A hypothetical counterexample is cyclic-CSA (cyclic maximal abelian subgroups are malnormal), or it has a nontrivial central cyclic subgroup Z with G/Z an infinite finitely presented torsion group all of whose infinite-index subgroups are finite cyclic. The latter is an Adian-extension mechanism, explicitly credited to prior terminology and results. Conversely, a torsion-free central Z-extension of an actual quotient with these properties would be finitely presented and full IF, giving a counterexample. No such quotient and extension have been constructed. The two branches are reductions, not classifications of their members.

## Construction attempts and decisive gates

1. A finitely generated non-finitely-presented monster cannot embed in a finitely presented IF group, by coherence. Recent Fournier-Facio–Sun high-dimensional monsters also fail FP2(Q), with infinite-dimensional rational H2; they do not meet the finite-presentation hypothesis.
2. An epimorphic sequence on a fixed finite generating set with finitely presented limit stabilizes, because the terminal relation kernel is finitely normally generated. An endlessly strict quotient limit cannot repair this gate. A finitely presented lacunary hyperbolic limit would be hyperbolic, which alone still leaves the general hyperbolic problem open.
3. Strictly ascending HNN extensions of finite-rank free groups fail IF: their infinite-index height kernel is a strictly increasing union of groups with bounded generator number and cannot be free. The proof uses a basis retraction, not false rank monotonicity. A noninjective finite-free endomorphism reduces to an injective stable quotient by rank stabilization and Hopficity, so it provides no escape. The automorphism case is covered by virtual indicability.
4. Finite classical C'(1/6) constructions fall under Wise cubulation and Wilton. Other small-cancellation notions are not included automatically.
5. Standard density-model random groups with1/3<d<1/2 fail IF with probability tending to1, using surface subgroups and property(T) in the same strict model. This excludes neither exceptional individual groups nor every property(T) group.
6. Higman/Baumslag–Gersten have infinite-index nonfree dyadic subgroups; the inspected finitely presented simple homeomorphism examples have infinite-index Z². Torsion examples fail IF immediately. No checked simple or monster construction survives all original hypotheses.

## Precise unresolved obstructions

The FAb cyclic-CSA finite-presentation branch has no proved virtual indicability, cubulation or surface-subgroup mechanism. Coherence, absence of Z², power balance and malnormal cyclic subgroups do not supply those missing properties. The central branch transfers the task to an actual infinite finitely presented torsion quotient with the specified subgroup property and a torsion-free extension; neither its existence nor its impossibility is established. A finite presentation complex cannot be treated as an aspherical two-dimensional complex. Substituting these assertions as lemmas would simply transfer the original difficulty.

These are route blocks, not a claim that the overarching research goal is operationally blocked. Substantial independent structure, construction and theorem-synthesis approaches were attempted. Descending research now skips the already solved21.137 and starts21.136.

## Verification, priority and publication

`root_virtual_indicability.md`, `approach_structure.md`, and `approach_constructions.md` give the proofs and source roles. Fresh reviews `reviews/virtual_indicability_adversary.md`, `reviews/structure_adversary.md`, `reviews/ascending_kernel_adversary.md` and `reviews/construction_gate.md` check the separate mechanisms and boundaries. Root caught an erroneous Klein-abelianization sentence: the final proof correctly retains an infinite-order generator in the quotient by a central power. The corrected argument and all-subgroup central-extension converse passed adversarial checking.

These are theoretical results and source checks; no finite computation is offered as a substitute for the unrestricted subgroup quantifier. Previously known mechanisms and modern restricted theorems receive credit. Literature-wide novelty of the partial deductions has not been established. AI tools were used extensively. No independent human peer review or formal proof-assistant verification is claimed.

Publication gate: **closed — no complete original resolution**.
