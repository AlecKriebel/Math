# Kourovka 21.139

Updated 2026-10-24T17:02:39.023669+00:00. Research status: **unsolved**. Full-problem discovery estimate: **15%**; this is a planning estimate, not a probability of correctness. No complete proof, counterexample, new paper, DOI or tracker entry is claimed.

## Exact question and current priority evidence

For a hyperbolic virtually compact special group G, suppose the ordinary rational second Betti numbers b2(H;Q) are bounded over **all** finite-index subgroups H. Must G be virtually free or virtually a closed surface group? H. Wilton, official 21st edition, 20 October 2026 update3, printed p.200. Finite and virtually cyclic groups belong to the first alternative. Surface orientation is handled by passing to the orientation cover.

The latest official statement is unchanged and unstarred; the updates-only document contains no solution notice. The dated primary literature audit found restricted solutions, but no complete solution of this quantified question. This is a bounded search assessment, not proof of global openness. Source receipts: `../../sources/latest_20261024_manifest.json`, `priority_20261024.md` and the branch manifests.

## Strongest verified results and exact scope

1. **Known amplification mechanism, with complete quantifier checks.** Rational virtual Betti bounds pass to quasiconvex subgroups via virtual retractions. Positive virtual H2 of a single infinite-index quasiconvex subgroup gives ambient covers of index Cn with b2 at least an, for fixed positive C,a. Fruchter–Morales already use this mechanism; it is not claimed as new. Wilton supplies a one-ended subgroup, not the positive homology needed to start amplification.
2. **Audited equivalence, not a solution.** The full question is equivalent to the assertion (Z2) that a hyperbolic compact special group of rational cohomological dimension at most two with zero H2 in every finite cover is free. A mid-hyperplane cutting hierarchy with free hyperplane groups constructs a finite two-dimensional classifying space. Dimension induction proves the equivalence **assuming (Z2)**, which remains unproved. The 24 October fresh audit accepts the precise midplane convention and both directions. No finite-dimensional model is silently descended through a finite extension.
3. **Restricted families.** Hyperbolic right-angled Coxeter groups, and commensurable groups, satisfy the desired dichotomy by the chordal/induced-cycle argument. The arithmetic simplest-type examples inspected have infinite-index quasiconvex closed surface subgroups and hence unbounded vb2. These are restricted checks, not classification of all compact special groups. Fruchter–Morales already treat residually free and cyclic-edge graphs of free groups.
4. **Exact free-by-cyclic diagnostic.** For F3 with a->b, b->c, c->ab, every cyclic height cover has rational b2=0. A characteristic eight-sheet free-group cover, combined with monodromy powers2 and14, gives ambient subgroups of indices16 and112 with b2=1 and7. Independent spanning-tree homology and direct integer-minor certificates agree. In the degree-seven height cover H2(Z)=0 but H1(Z)=Z plus (Z/2)^3 and b2(F2)=3: integral UCT torsion blocks an automatic coefficient upgrade. This example does not satisfy global rational boundedness and is not a counterexample to the problem.
5. **New explicit finite-action constructions, in an already known class.** For G_q=<a,b,t | t^-1 a t=(ab)^(q-1)b>, connected degree2nq covers have b2=n(q-2)+1, by identifying the actual cellular kernel with the flow space of a connected bipartite q-regular multigraph. The q=2 surface control gives1. A general common-zero sparse finite-action certificate amplifies a class for arbitrary free-factor edge rank, if such a certificate exists.
6. **All abelian and p-group tests can miss homology.** E=<a,b,t | t^-1 a t=ab^2ab^3> has b2=0 in every finite abelian cover and every cover with p-group monodromy, for every prime p. Nevertheless explicit connected degree5n covers have b2=n. A degree-five witness already has solvable monodromy C5 semidirect C4. The p-group proof is the augmentation-unit argument for a primitive exponent-sum vector. It is a statement about the entire monodromy, not just a prime-power degree, and is not extended to mixed-prime nilpotent covers. The generalized primitive-word family has the exact abelian-blindness gcd criterion in the HNN note.

The new cover formulas are independent mathematical deductions, but the examples belong to an already resolved restricted class. Their literature-wide novelty has not been established. They do not advance to the publication pipeline.

## Routes attempted and precise remaining obstructions

- A one-ended quasiconvex subgroup need not have a presently proved finite H2 witness. Replacing this gap by an asserted surface subgroup or positive virtual homology merely restates an equivalent central difficulty.
- L2 vanishing, a selected cyclic tower, all finite abelian covers, and p-group monodromy covers do not replace the all-finite-index hypothesis. The exact diagnostics above must be retained as controls.
- Kielak–Linton reduce the dimension-two zero-L2 case to virtual free-by-cyclic structure, allowing an **infinite-rank free kernel**. The finite-rank Euler-characteristic argument does not cover that remainder. Linton's finite free-base HNN form has both associated subgroups free factors, but these may have arbitrary rank.
- No general finite-action certificate-existence theorem has been proved for those HNN extensions. Killing both associated factors may collapse the whole base; a two-generator edge example with this collapse still has positive H2 in its degree-two height cover. Neither quotient triviality nor failure of the chosen mechanism implies freeness.
- Retractions in torsion-free hyperbolic groups are malnormal (known). This blocks overlapping distinct conjugate retract copies in the same retraction host. It does not block nonconjugate doubles or conjugators outside that host.
- Naively completing a partial free-factor isomorphism adds relations and gives a quotient, not the embedding needed for transferring homology. Unbounded homology in an overgroup alone does not pass to the subgroup.
- Stabilized finite-image coefficient cohomology and the cyclic Alexander formulas give necessary conditions; their converse classification is unsupported.

These are mathematical route blocks, not an operational impasse for the ongoing research program. Reopening a route requires a new mechanism or evidence. After this substantial multi-route attempt, descending work continues at21.138.

## Verification and reproducibility

The theoretical geometry and homology statements received independent adversarial checks. The fresh 24 October geometry report accepts the conditional reduction, amplification, RACG scope, retract obstruction and integral coefficient calculation. A separate fresh finite-action adversary accepts the universal flow proof, common-zero amplification, generalized word identity, abelian gcd criterion, p-group argument, exact E family and category citations. Its independently rebuilt right-action relator-walk matrices pass67 cases with exact rational ranks; these finite checks supplement the universal proofs rather than replacing them.

Primary proof/code/review entry points:

- `approach_geometry.md`, `approach_homology.md`, `homology_adversarial.md`, `approach_counterexamples.md`.
- `root_hnn_slot_flow.md`, `approach_hnn_20261024.md`, `root_hnn_obstructions_20261024.md`, `retract_double_obstruction.md`.
- `root_artifacts/`, `counterexample_artifacts/`, and authored code/results in `source_20261024_hnn/`.
- `reviews/partial_adversary_oct24.md`, `reviews/finite_action_adversary_20261024.md`, and their independent verifiers/certificates.

No independent human peer review or proof-assistant verification is claimed. Publication gate: **closed — no complete original resolution**.
