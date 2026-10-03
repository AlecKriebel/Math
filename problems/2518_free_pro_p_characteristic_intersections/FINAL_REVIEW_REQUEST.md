# Full independent review request:2518 / KOU-21.9

Review all five frozen author turns, the exact sources and all checks. Recommended original disposition:unsolved5/5. No sixth author search is authorized by this packet. Publication requires the parent gate.

Public bytes are defined by FINAL_AUTHOR_MANIFEST.json. Read SOURCE_GATE.md, FINAL_RESULT.md, TURN_1.md through TURN_5.md, and all scripts/manifests. Source files are local-only in /workspace/shared/math-2518/sources. Run `python REPLAY_ALL.py --source-dir /workspace/shared/math-2518/sources`; omit the option in a clean public checkout.

## Primary anchors

- Current Kourovka21st edition, October2026 full PDF, printed/PDF177, exact unannotated21.9. Image printed177.png. Updates-only PDF has no21.9entry. https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt.pdf
- Barnea–Ershov–Le Boudec–Reid–Vannacci–Weigel, arXiv:2507.04120v3,22September2026: exact Question4 and distinctions from Proposition12.2 on p53 (comm-p53.png); discrete-only Observation6.10 pp27–28; finite-index characteristic-core counting Lemma2.21; Frattini and Schreier/basis facts p18; pro-p Hall Theorem3.11 on p18 (comm-p18.png); natural Aut(F)->GL_d(Z_p) epimorphism in Notation7.8 p30. https://arxiv.org/abs/2507.04120v3
- Nikolov–Segal, Annals165(2007),171–238, Theorem1.1 printed172 (ns-p172.png) for strong completeness; Theorem1.4/consequence printed174 for closed lower-central terms. The pro-p special case is credited there to Serre. https://annals.math.princeton.edu/2007/165-1/p05

## High-risk obligations

1. T1: classify GL_r(Z_p)-invariant additive subgroups without assuming closedness; retain r>=2. Equality of actual images under U_ab->F_ab and the nonscalar lattice contradiction. The Schreier inclusion has one p-scaled coordinate and repeated unscaled coordinates. Aut(F)-transitivity proves redundancy of all index-p choices, not triviality of their common core.
2. T2: strong completeness removes the abstract/continuous ambiguity. The limiting subgroup is characteristic in each U_i by a cofinal subsequence, not by a single cycle. Each finite step uses only finitely many subgroup images. Verify Aut(G)->Aut(G/Phi^eG) lifting using freeness and the basis criterion. The finite quotient construction gives a finite step, not a halting procedure for the source problem. Strictly increasing indices must not replace the exact forall-depth/exists-stage cofinality condition.
3. T3: conjugation by x_1 on the Schreier block is a p-cycle modulo U'; the terminal wrap is inner by x_1^p. Verify the integral augmentation-ideal identity T^{p-1}=pB, invertibility of B, saturation of the ideal, and exact valuation floor((k-1)/(p-1)), including p=2. The finite-modulus threshold has n=k+1. Do not reverse the containment quantifier when excluding lower-central terms or finite-class nilpotent quotients.
4. T4: the Hall theorem applies to the closed finitely generated container, not the hypothetical infinitely generated normal subgroup. Its free-factor retraction and the finite P wr C_p separator prove the contradiction without assuming an abstract normal-form theorem. Distinguish ordinary topological generation from finite normal generation.
5. T5: arbitrary open subgroups of the p-adic Heisenberg group have center equal to their intersection with its procyclic center; prove this using two deep coordinate elements and torsion-freeness of Z_p. The finite quotient's displayed index-p subgroup is elementary abelian even at p=2, and the explicit theta swaps it to a distinct subgroup. No statement that all maximal subgroups are elementary abelian at p=2 is made. The nonlifting automorphism of that finite subgroup does not imply a result about the source free-pro-p group.

All historical bytes must be preserved; identify any required correction precisely for an additive correction workflow. The final WIP binding will be supplied separately after exact backup. No raw source files or private coordination belong in a publication.
