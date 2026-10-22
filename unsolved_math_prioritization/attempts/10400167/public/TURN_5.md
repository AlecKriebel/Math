# Turn 5: all colored-link invariants and the remaining reconstruction gap

Timestamp: 2026-10-03T09:39:00Z. Outcome: partial; five-turn budget exhausted without a general resolution.
Completion estimate toward the general converse: 25% (subjective).

## Extend the intrinsic torus reconstruction

Let C and D be unitary fusion categories and suppose their ordinary state-sum TQFTs are isomorphic. Transport the isomorphism through the TV/RT-center comparison, and put B=Z(C), B'=Z(D). Turn 1 constructs a single vacuum-preserving permutation pi of their simple labels such that the torus component of the natural isomorphism satisfies

    alpha_(T^2)(x_i)=x'_(pi(i)).

This one permutation, not a different choice for each link, transports *all* simple-colored framed oriented link invariants in arbitrary closed oriented 3-manifolds.

Proof. Let L have n ordered components in M, with fixed framings. Remove open tubular neighborhoods and parameterize each resulting boundary torus using its meridian and framed longitude. The complement X is an ordinary bordism from a union of n tori to the empty surface, so its TQFT map is a linear functional

    Z_B(X): A^(tensor n) -> C.

Filling a boundary torus by the solid torus whose core has color i inserts the vector x_i. The RT gluing axiom therefore identifies

    Z_B(X)(x_(i1) tensor ... tensor x_(in))

with the RT invariant of (M,L) in the TQFT normalization. Since alpha is monoidal and natural for the undecorated complement X,

    Z_B'(X) (alpha_(T^2)^(tensor n)) = Z_B(X).

Substitute the basis vectors to obtain equality of the two colored invariants under pi. Orientation reversal of a component replaces its simple label by the dual; duality is preserved because the based fusion algebra is preserved. A framing change acts by the twist, also preserved. For n=0 this reduces to ordinary closed-manifold equality. QED.

For link evaluations in S^3 normalized to send the empty link to 1, divide both sides by the common nonzero value Z(S^3)=1/Dim(C). Thus the statement is independent of the customary overall RT normalization.

## Why this is stronger, and why it still stops short

This necessary relation includes the Whitehead and Borromean link tensors, all knots, every number of components, and all ambient closed 3-manifolds. It is stronger than matching the S,T matrices or a bounded collection of low-complexity probes.

To finish by this route, one would need a proof that these transported invariants, together with the remaining ordinary TQFT data, determine the ribbon category. The current argument gives linear functionals on tensor powers of the torus state space. It does not construct coherent identifications of the trivalent multiplicity spaces Hom(k,i tensor j), nor their associators and braidings. Those are exactly the data needed to build a categorical equivalence. A category assigned to a circle or a modular functor on labeled punctured surfaces would supply additional data, but that is not part of the original hypothesis.

Consequently the attempted reconstruction is blocked at a specific step, rather than completed by invoking the classification of theories extended to circles. We have neither proved the needed lifting/reconstruction theorem nor produced two inequivalent centers with isomorphic ordinary TQFTs.

## Current-literature controls

Bonderson, Delaney, Galindo, Rowell, Tran and Wang's [*On invariants of modular categories beyond modular data*](https://arxiv.org/abs/1805.05736) (J. Pure Appl. Algebra 223 (2019), 4065–4088; DOI 10.1016/j.jpaa.2018.12.017) studies additional link invariants and proves the Whitehead data go beyond S,T. Its discussion of completeness must not be silently substituted for a reconstruction theorem.

The primary [Luo–Tian preprint, arXiv:2609.33231v1](https://arxiv.org/abs/2609.33231v1), submitted 2026-09-27, reports inequivalent Dijkgraaf–Witten centers with matching invariants of every framed oriented link in S^3 with at most two components, under one common simple-label bijection, but also a closed oriented 3-manifold partition function separating the family. Its abstract, Main Theorem, and Theorem 7.1 were inspected. This is a recent preprint claim, not independently re-proved here. Even if accepted, it is not a counterexample to the present problem because its ordinary TQFTs are distinguished by that closed-manifold value.

## Final disposition

The exact original target is unresolved after five written attempts. The surviving results are the unitary torus and colored-link transport lemmas, an explicit gauge-versus-Morita control, and affirmative reconstruction in two declared finite-group subcases. No sixth proof-search turn is hidden in subsequent verification, source checking, or packaging. A fresh independent audit may validate or correct these claims without expanding the exhausted search.
