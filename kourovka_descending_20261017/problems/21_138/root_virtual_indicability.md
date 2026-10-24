# The virtually indicable case and the FAb remainder

Checkpoint: 2026-10-24T17:02:39.023669+00:00. This is a restricted deduction from established theorems, not a solution of 21.138 or a first-priority claim. Full-problem discovery estimate: **12%**. Fresh independent review has passed within the restricted scope. No publication package is proposed.

An infinite group has property IF if every subgroup of infinite index is free, including infinitely generated subgroups. A finitely generated group is FAb if the abelianization of each finite-index subgroup is finite. A group is virtually indicable if some finite-index subgroup maps onto Z.

## Exact deduction

**Proposition.** Every infinite finitely generated virtually indicable IF group is isomorphic to a free group or to the fundamental group of a closed aspherical surface. Finite presentation is not needed in this restricted proposition.

The free kernel of a homomorphism onto Z is permitted to have infinite rank. Replacing it silently by a finite-rank free group would invalidate the proof.

### Established inputs, with their separate roles

1. Gardam–Kielak–Logan, *The Surface Group Conjectures for groups with two generators*, [arXiv:2202.11093v2, Proposition 3.5](https://arxiv.org/html/2202.11093v2): a finitely generated indicable IF group is hyperbolic or a surface group. This proposition is not restricted to one-relator groups, although several other theorems in that paper are.
2. Linton, *Embedding finitely generated free-by-cyclic groups in {finitely generated free}-by-cyclic groups*, [arXiv:2510.10178v2, Corollary 1.5](https://arxiv.org/html/2510.10178v2): a hyperbolic free-by-cyclic group is virtually compact special. The paper explicitly allows infinite-rank free kernels in its introduction. Corollary 1.4 obtains a quasiconvex embedding in a hyperbolic mapping torus with finite-rank free kernel; it is not a quotient-completion argument.
3. Wilton, *Surface groups among cubulated hyperbolic and one-relator groups*, [arXiv:2406.02121v3, Theorem A](https://arxiv.org/html/2406.02121v3): a cubulated hyperbolic group that is neither free nor surface has a one-ended quasiconvex subgroup of infinite index.
4. A torsion-free virtually free group is free. A torsion-free group virtually isomorphic to a closed aspherical surface group is itself a surface group; the latter is recorded as GKL Theorem 3.4, with the Nielsen realization/Eckmann–Müller references. The torus and Klein bottle cases are included.

### Proof with all finite-index passages

First, an infinite IF group is torsion-free, because a nontrivial finite cyclic subgroup would have infinite index and would not be free. IF is hereditary: if L has infinite index in H <= G, it has infinite index in G as well.

Choose a finite-index subgroup H <= G and an epimorphism h:H -> Z. H is finitely generated and IF. Its kernel K has infinite index, so it is free by the full IF hypothesis. Choose t with h(t)=1. Conjugation by t is an automorphism of K, and the extension splits over Z. Thus H is a finitely generated free-by-Z group K semidirect Z; K is not assumed finitely generated.

Apply GKL Proposition 3.5 to H. If H is already a surface group, torsion-freeness and the surface-extension theorem give the same conclusion for G. Otherwise H is hyperbolic. Linton Corollary 1.5 then supplies a compact special finite-index subgroup S <= H. This passage preserves hyperbolicity and IF. S is torsion-free and has a compact nonpositively curved cubical classifying space.

If S were neither free nor surface, Wilton Theorem A would supply a one-ended subgroup L of infinite index in S. The hereditary IF property makes L free. No free group is one-ended: a nontrivial finite-rank free group has two or infinitely many ends, and the subgroup supplied by Wilton is finitely generated (quasiconvex in a hyperbolic group). This is a contradiction. Hence S is free or surface. It has finite index in G; applying the torsion-free finite-extension statements in input 4 proves the proposition.

No assertion is made that the original G itself is compact special, or that a finite-dimensional classifying space automatically descends through a finite extension.

## Consequence for the unrestricted problem

An actual counterexample to 21.138 must be **FAb**. Indeed, if a finite-index subgroup H had infinite abelianization, that abelianization is a finitely generated infinite abelian group and admits an epimorphism onto Z. H would be indicable, so the proposition would classify G.

For a finitely generated group the alternatives are exact: failure of FAb is equivalent to virtual indicability. This reduction is stronger than merely saying b1(G;Q)=0. A finite abelianization of G alone does not rule out an indicable finite-index subgroup.

The conclusion excludes, among other cases, every infinite virtually locally indicable IF group: any infinite finitely generated locally indicable finite-index subgroup itself maps onto Z. It also excludes all groups of positive virtual first Betti number. These are consequences of the same proposition, not additional new discovery claims.

## Attempts to remove FAb and exact gaps

- Finite presentation gives a finite presentation complex, not an aspherical complex of dimension two. No Euler-characteristic or Poincare-duality inference is available without additional work.
- Coherence follows from IF and finite presentation, but coherence alone has not produced an infinite cyclic quotient of a finite-index subgroup.
- Every nonfree subgroup must have finite index. Finding a surface subgroup would therefore settle the group under study, but asserting its existence is an unsupported subgroup-existence problem.
- Residual finiteness alone does not provide virtual retractions or virtual positive first Betti number. Replacing a finite quotient by a retraction to a free subgroup would add a missing hypothesis.
- In a residually finite FAb group, a residual normal-chain first-Betti approximation, when its hypotheses apply, gives first L2-Betti number zero. That vanishing supplies neither freeness nor a surface subgroup; surface groups of negative Euler characteristic would in fact have positive first L2-Betti number. No classification follows from a zero limit.

These routes are blocked at their stated unsupported assertions. They should reopen only with a new mechanism. The FAb finite-presentation remainder, including groups not known to be hyperbolic or cubulated, is the remaining full-scope problem.

## Validation status

Root checked the exact three primary theorem statements and their hypotheses on 24 October 2026. The construction and structure agents were initially kept independent, then received this proposed deduction as a new input. The fresh nonauthor review in `reviews/virtual_indicability_adversary.md` independently checked the primary statements, both finite-extension upgrades, flat surface boundaries, and the FAb equivalence; it passes with no substantive objection. This is an accepted partial deduction, not a full solution or originality certification. No computational evidence is needed for this theoretical deduction.

Checkpoint 2026-10-24T17:12:40.273563+00:00: restricted review100%complete, full-problem discoveryestimate12%; publicationgateclosed. The separate structure/construction routes retain the FAb finite-presentation gap.
