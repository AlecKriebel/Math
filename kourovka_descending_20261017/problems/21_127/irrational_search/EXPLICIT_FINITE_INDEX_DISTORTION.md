# An explicit finite-index RAAG inclusion is not automatically scl-isometric

2026-10-24 UTC. This is a concrete application of the prior Calegari--Walker nongeometric-cover theorem, not a new theorem or a 21.127 solution.

Let F=F(a,b), and let H be the kernel of the homomorphism F->Z/3 sending a->1, b->0. A Schreier basis is

A=a^3, B_0=b, B_1=a b a^{-1}, B_2=a^2 b a^{-2}.

Both groups are finite RAAGs (free groups), and H has index three in F. Take

w=[A,B_0][B_1,B_2].

The rank-four free group H is the fundamental group of a genus-two surface Sigma with one boundary component, with w its oriented boundary word. Hence scl_H(w)=3/2. For instance this is the standard surface-boundary computation used in Calegari--Walker, Proposition 2.9.

This realization of H is not geometric with respect to its inclusion in F. If it were realized as a finite covering of a compact oriented surface S realizing F, the normal deck group F/H would preserve the algebraic intersection form Omega on H_1(Sigma;Z). In the ordered basis (A,B_0,B_1,B_2), this form has Omega(A,B_0)=Omega(B_1,B_2)=1, their skew-symmetric partners, and all other entries zero. Conjugation by a fixes A and acts on homology by B_0->B_1->B_2->B_0 (the last conjugate is A B_0 A^{-1}, so its homology class is B_0). It does not preserve Omega, because Omega(A,B_0)=1 whereas Omega(A,B_1)=0. Reversing all surface orientations changes both signs and cannot repair this failure; an orientation-preserving cover has orientation-preserving deck maps.

There is also a direct independent boundary-count obstruction. A compact connected oriented surface realizing F_2 is either a once-punctured torus or a pair of pants. A cover of a pair of pants has at least three boundary components. For a once-punctured torus the boundary word is a commutator, whose image in the abelian deck group F/H=Z/3 is trivial. It therefore has three degree-one lifts, again at least three boundary components. Our genus-two Sigma has only one boundary component, so no such covering realization exists. This excludes an overlooked boundary-degree exception without using the symplectic-form calculation.

Calegari--Walker, *Isometric endomorphisms of free groups*, arXiv:1101.4055v1, Example 2.7 and the proof of Proposition 2.9, show that for any such nongeometric realization,

scl_F(w)<scl_H(w)=3/2.

The exact smaller value is not computed here. It is rational by free-group rationality, but the strict drop already proves the needed logical point: being a finite-index free/RAAG subgroup does not make inclusion scl-isometric on each commutator-subgroup element. A virtual-special embedding route cannot silently identify the two values.

This conclusion depends on the cited prior nongeometric-cover theorem; the explicit Schreier basis, deck action, and intersection-form obstruction are the computations supplied here. The word is in [H,H] and is nontrivial. It is not proposed as an irrational-scl example.
