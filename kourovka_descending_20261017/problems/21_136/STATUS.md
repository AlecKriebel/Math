# Kourovka 21.136

Research label: **unsolved**. Full-problem discovery estimate: **12%**, a planning estimate, not confidence in a theorem. No complete proof, counterexample, preprint, DOI, or tracker entry has resulted from this attempt.

## Exact target and source status

For an arbitrary profinite group G with fewer than 2^{aleph_0} ambient conjugacy classes of infinite-order elements, must every element have finite order? John S. Wilson; 21st edition, official 20 October 2026 update 3, printed p.199. Finite generation and metrizability are not hypotheses. Strictly fewer than the actual continuum is required, without CH. The conclusion does not require a uniform exponent.

The current official entry has no solution marker, and Wilson's 2023 primary paper proves the finitely generated case rather than the full question. The apparent omission of finite generation in its Corollary3.1 cannot be used to settle the problem: its context requires that hypothesis, and an infinite elementary abelian pro-p group refutes the unqualified finiteness conclusion. The NCC literature counts procyclic subgroup classes, a different invariant. Preliminary and independent priority notes preserve dated sources and limits; no complete prior solution was identified.

## Strongest reviewed deductions

1. Every counterexample has a countably based quotient retaining an infinite-order element and the class bound. Its conjugacy-class space is compact metrizable, and its infinite-order part is Polish. The strict continuum bound therefore makes that part countable, and an infinite-order class is relatively isolated. No CH or hereditary claim for arbitrary closed subgroups is used.
2. Infinite-order conjugacy classes have empty interior. In the countably based reduction the infinite-order set is meagre, torsion is comeagre, and interiors of finite-exponent sets have dense union. Dense torsion or one bounded-exponent coset alone is inadequate.
3. The normalizer action on every infinite procyclic subgroup has open image in its automorphism group. Any abelian torsion subgroup of unbounded exponent forces continuum many ambient infinite-order classes by exact binary power coding in finite quotients, even if that subgroup is not closed.
4. A relatively isolated infinite-order element survives quotienting by any closed normal kernel that is torsion or virtually abstract locally nilpotent. The finite-index locally nilpotent subgroup need not be open or closed. The proof uses a torsion centralizer in the quotient and a terminating ordinary-integer iterated commutator. Thus groups with a finite closed ambient-normal series of these factors cannot be counterexamples; virtually soluble groups are included. Pronilpotence and infinite prosoluble derived depth are not included.
5. Under the weaker property P0 that every open subgroup contains some open bounded-exponent coset, a virtually metabelian pro-p group has finite exponent and is locally finite. The proof uses commuting finite-order operators and a finite Fourier decomposition; no finite-dimensional representation assumption is made. This is a restricted locality theorem, not an extension to all pro-p groups.
6. A relatively isolated infinite-order element has finite prime support, torsion of unbounded orders in every neighborhood, and a procyclic closure with infinite-index normalizer. For a Z_p closure, small normalizer actions force small-conjugator relations. These relations have not yielded a contradiction.

The local quotient lemma was independently extended and then checked by a fresh nonauthor. Source, proof, boundary, and scope artifacts are in root_class_space.md, root_isolated_quotients.md, approach_constructions.md, approach_lie.md, approach_isolated_classes.md, and reviews/. The review's distinction between sequences and nets in nonmetrizable groups applies throughout.

## Distinct approaches and verified failure controls

Finite-quotient power coding excludes standard rooted-tree/upper-unitriangular constructions containing unbounded abelian torsion. Root independently reproduced 170 tree permutations; the separate checker also verified word-action/support certificates. Compact affine quotients and compact coordinate-action restrictions exclude other proposed examples.

Dense locally finite torsion plus an open exponent-p coset does not imply torsion without finite generation: explicit products of cyclic-permutation modules semidirect C_p give nontorsion pro-p controls for every p. Their continuum many infinite-order classes are acknowledged; they are not target counterexamples. Nonopen Zassenhaus terms and weighted-filtration completion prevent a naive Lie-algebra density argument. A Q8 representation prevents exporting the abelian exponent-drop step to arbitrary nonabelian actions.

The local isolated-class route supplies the quotient-persistence theorem, but transferring P0 or the ambient class bound to its closed two-generator metabelian subgroup is invalid. A single conjugate power-conjugation relation is compatible with profiniteness, as a cited generalized Higman-group control shows. Iterated commutators converging to1 in a pro-p group cannot replace actual termination: the explicit Z_3 semidirect Z_3 example has a^h=a^4 and nontrivial a^(3^j) for every j.

## Exact unresolved obstruction

No mechanism proved here forces an arbitrary relatively isolated infinite-order class to meet a permitted normal kernel after finitely many steps. In particular nonabelian pro-p groups and infinite prosoluble derived depth remain. A closed subgroup does not automatically inherit the global class bound, dense bounded-torsion interiors, or P0. Assuming any of those transfers, or assuming the nonexistence of relatively isolated infinite-order classes in all profinite groups, merely replaces the central difficulty with an unsupported assertion.

No actual target counterexample has been constructed. These routes are blocked at their specified mathematical gaps; the continuing descending research program is not operationally blocked. Reopen a route only for a materially new mechanism or evidence.

## Verification and publication

Fresh adversarial reports accept the stated partial deductions, including arbitrary cardinality, all-prime power coding, finite-series scope, and boundary controls. Independent reviewers actively checked hidden finite-generation, metrizability, finite-dimensionality, and subgroup-inheritance assumptions. No literature-wide originality, formal proof-assistant verification, or independent human peer review is claimed. AI tools were used extensively.

Publication gate: **closed — no complete original solution**. The next eligible descending problem is21.135, selected from the official Notebook and current primary literature.
