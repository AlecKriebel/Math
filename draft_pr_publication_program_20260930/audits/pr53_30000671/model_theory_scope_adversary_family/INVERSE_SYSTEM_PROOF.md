# Independent inverse-system and model-theory audit

## Exact quantifiers and functorial restriction

Let A and B be commutative complete Noetherian local rings with maximal ideals m and n. Assume for each r ≥ 1 that I_r = Iso_ring(A/m^r, B/n^r) is nonempty. This statement is ∀r ∃f_r, with no compatibility condition. The desired compatible family is a single sequence (f_r) with every reduction square commuting. These are different quantifiers.

Every quotient A/m^r is local, with unique maximal ideal m/m^r. A ring isomorphism preserves this ideal and its powers. Hence f in I_(r+1) canonically induces an element of I_r, and further restrictions compose. There is no reason in the hypothesis for every chosen element of I_r to lift to I_(r+1).

Suppose a compatible family exists. For a = (a_r) in lim A/m^r, the sequence (f_r(a_r)) belongs to lim B/n^r. This defines a ring homomorphism. The inverse maps f_r^(-1) are compatible: reduction of f_(r+1)^(-1)(b) equals f_r^(-1) of the reduction of b, by applying f_r to both sides of the original commuting square. They induce the inverse homomorphism. Completeness and separatedness identify the limits with A and B. Thus compatibility suffices. This is not a deduction that compatibility can always be selected.

## A proved positive boundary: finite residue fields

Assume in addition that k = A/m is finite. Since the r = 1 quotients are isomorphic, B/n has the same finite cardinality. For every i ≥ 0, m^i/m^(i+1) is a finitely generated A-module by Noetherianity, is annihilated by m, and is therefore a finite-dimensional k-vector space. It is consequently a finite set. The filtration of A/m^r has these r factors; by repeated use of the exact sequences of additive groups, A/m^r is a finite set. The same argument applies to B/n^r. The case m = 0, including fields, is included.

It follows that I_r is finite, since it is a subset of the set of all functions between two finite sets. Build a rooted tree whose depth-r nodes are compatible chains (f_1,...,f_r). For each r there is a node at depth r: take any element of I_r and all its restrictions. Each node has finitely many children, because its children are parametrized by a subset of I_(r+1).

Here is the selection argument without assuming surjectivity of the restriction maps. Call a node persistent when descendants of arbitrarily large depth occur below it. The root is persistent. A persistent node has finitely many children; if every child had a bounded descendant depth, their finitely many bounds would give a bound for the node. Thus it has a persistent child. Inductively choosing such children gives an infinite compatible branch. The preceding inverse-limit construction yields A ≅ B.

This proof establishes the finite-residue-field boundary only. It does not prove the broader historical result for residue fields algebraic over their prime field. Such a field may be infinite; Q itself is already an example. The cited broader theorem uses further approximation arguments which are not supplied by the finite-tree proof.

## Finite length is not finite cardinality

For an infinite field k, the local ring k has module length one and infinitely many elements. More directly relevant to isomorphism sets, k[ε]/(ε²) has length two and admits a distinct k-algebra automorphism ε ↦ aε for every a in k^×. The inverse is ε ↦ a^(-1)ε. These automorphisms preserve the relation because (aε)² = 0. Therefore even a finite-length quotient can have infinitely many isomorphisms. Taking k = Q makes this entirely explicit.

The topology from the maximal ideal on such a quotient does not supply the missing compactness: the quotient is discrete, since a sufficiently high power of its maximal ideal is zero. An infinite discrete space is not compact, as its cover by singleton open sets has no finite subcover. There may be additional topologies useful under additional hypotheses, but none is specified by the unrestricted question.

## A logical countermodel to the selection inference, not a ring example

For r ≥ 1 define X_r = {N in the positive integers: N ≥ r}, with transition X_(r+1) → X_r the inclusion. Every level is nonempty, and every finite initial subsystem has a compatible chain: choose N equal to its largest level. The full inverse limit is empty. Compatibility forces every coordinate to equal one fixed integer N, while membership would require N ≥ r for every r, contradicted by r = N + 1.

This inverse system disproves the abstract implication that nonempty levels alone imply a nonempty inverse limit. It does not realize these X_r as quotient-ring isomorphism sets, and it is not Gabber's construction or a new ring counterexample. Surjective transition maps would be a sufficient different assumption for a countable system with nonempty levels, since a lift can be chosen recursively; the target has no such assumption.

## Model-theoretic compactness does not automatically descend to the given rings

The same obstruction can be expressed as the type {x ≥ r : r ≥ 1} in the standard positive integers with order and constants for the standard integers. Every finite subset is realized in that structure, but the complete type is not. First-order compactness can produce a model satisfying the constraints together with the elementary diagram, allowing nonstandard elements; it does not force realization in the original standard structure.

Likewise, an appeal to logical compactness for maps between all quotient levels needs an explicit language and axioms and a proof that the resulting objects live in the original quotient rings. Naming every original element and its algebraic diagram does not exclude new elements from infinite sorts by first-order axioms; the infinite disjunction asserting that every element is named is not a first-order sentence. No compactness invocation without this realization/descent step fills the target's compatibility gap. This audit does not assert that every proposed encoding is finitely satisfiable, or build an isomorphism in an elementary extension of A and B. It isolates the invalid general inference.

## Limits of the new evidence

The bounded computation checks explicit finite rings and finite inverse systems only. The universal proofs above establish their stated boundary and logical facts. The historical unrestricted negative answer is imported from the original report and the institutional abstract. Neither these proofs nor the computation reconstructs the historical non-domain counterexamples, proves the full algebraic-residue-field theorem, or decides the current domain-restricted problem.
