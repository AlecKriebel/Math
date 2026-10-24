# Kourovka Notebook 21.135 — character-degree multisets and solvable radicals

Source: 21st edition, official October 2026 update 3 (modified 20 October 2026), printed p. 199, PDF index 198. Proposer: A. V. Vasil'ev. The latest official main file gives no solved marker; the updates-only file has no 21.135 solution notice.

## Complete mathematical statement

For a finite group G, chi_1(G) is the multiset containing the degree chi(1) of every irreducible complex character chi of G, retaining all repetitions. For another finite group H with chi_1(H)=chi_1(G), does R(G)=1 imply R(H)=1, where R denotes the largest solvable normal subgroup?

No simplicity, almost simplicity, perfectness, restriction on composition factors, or bound on order is assumed. The conclusion concerns only triviality of the solvable radical, not isomorphism of G and H. The trivial group is included.

Authoritative statement:
https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf
Official updates:
https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21upd-3.pdf

## Equivalent standard formulation

For d>=1 let m_G(d)=|{chi in Irr(G):chi(1)=d}|. Wedderburn's theorem gives

    C[G] ≅ product_{d>=1} M_d(C)^{m_G(d)}.

Consequently equality of the degree multisets is equivalent to an isomorphism C[G] ≅ C[H] of complex associative algebras. Thus the question asks whether the property R(G)=1 is determined by the complex group algebra. No Hopf structure, distinguished group basis, tensor-product rules, or identification of particular character kernels is part of this input. The matrix block's size is d, while its complex dimension is d^2. Every irreducible character contributes once to the multiset; the d-fold occurrence of its representation in the regular representation must not create a different weighting.

The degree multiset determines |G|=sum_d m_G(d)d^2 and k(G)=sum_d m_G(d). An ordinary character table contains this identity-column data together with values on all other classes, and is a stronger input. A degree SET cd(G) discards the numbers m_G(d), and is a weaker input. Character codegrees |G:ker(chi)|/chi(1) are a distinct invariant that cannot be substituted for degrees.

## Primary contemporary open formulation

The proposer restates this exact question as Problem 3.9(ii), with inv=cd, in A. V. Vasil'ev, *Arithmetic invariants for finite simple and related groups*, arXiv:2608.12783v2 (9 September 2026), printed p. 6. In that notation cd^*(G) is the degree multiset. Problem 3.9(i) separately asks preservation of solvability. The known counterexamples there for inv=eo (element-order multisets) do not answer the character-degree question.

https://arxiv.org/abs/2608.12783
https://arxiv.org/html/2608.12783v2

This is preliminary source/priority preparation. General openness is supported by recent primary evidence, not certified by absence of search results. No substantive target research has begun, no new result is claimed, and no publication action is authorized by a solution claim here.
