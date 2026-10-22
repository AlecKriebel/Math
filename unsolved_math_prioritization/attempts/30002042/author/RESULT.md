# Stringy E-polynomials: degree clarification and finiteness boundary

Problem 30002042 / OWR-11783-009. Assessment date: 2026-10-06.

## Outcome

The compound arbitrary-Gorenstein-polytope question is **not solved by this work**. Five substantive approaches were completed. A September 2026 preprint supplies a claimed resolution of the correctly qualified degree half; the general finiteness half is not established here. The proofs below are limited reductions and obstruction examples, with no novelty claim.

### Scope and notation

A lattice polytope P of dimension d is Gorenstein of index r when rP becomes reflexive after an integral translation. Write n=d+1−2r. Reflexive polytopes are the special case r=1. Smoothness, a nef-partition, and a Calabi–Yau complete-intersection realization are extra assumptions, not part of the arbitrary-polytope question. The dual P^× is the support polytope of the dual reflexive Gorenstein cone; for r>1 it must not be replaced by the ordinary polar of P.

Use E_P(u,v) for the standard two-variable stringy E-polynomial. OWR printed pp. 1292–1293 uses the label E_st(P,t) despite giving a formula in u and v. It does not define t or a specialization there. Accordingly, this report does not invent a univariate interpretation. The qualified degree assertion in Nill–Schepers, Conjecture 3.3(2), is E_P=0 or total degree 2n. When nonzero and with nonzero constant coefficient, its degree in each variable is n. The polynomial degree of P in Ehrhart theory is a third quantity, s=d+1−r=n+r.

The general finiteness question concerns nonzero E_P up to nonzero scalar, with n fixed and d,r unrestricted; adjoining the zero polynomial adds at most one case. For integer polynomials, scalar proportionality can equivalently use rational scalars. We do not replace this by exact equality, a fixed-index problem, or finiteness of the polytopes themselves.

### Source-dependent inputs

We use established polynomiality, Hodge symmetry, Poincaré duality, vanishing for n<0, and multiplicativity for integral free joins from Nill–Schepers [NS: Proposition 3.2, Corollary 3.7, Proposition 4.15]. Free joins of Gorenstein polytopes have d=d1+d2+1 and r=r1+r2. In particular n=n1+n2. An ordinary, Cayley, or Gorenstein join alone does not authorize multiplicativity; [NS, Example 4.16] explicitly warns against that extension.

Knupfer–Nill [KN, Theorem 1.5] states that E_P vanishes exactly for thin P and otherwise has total degree 2n. We verified that statement and its application proof, including dependence on Theorem 2.18, in arXiv:2609.18873v1. We have not independently checked the entire decomposition argument in Sections 3–4. The arXiv record inspected lists a preprint and no journal reference; this is a recorded manuscript claim, not an independent acceptance of its full proof.

## 1. What duality alone actually proves

Let E be a polynomial satisfying E(u,v)=(uv)^n E(u^-1,v^-1). Distinct monomials on the right have distinct exponent pairs, so there can be no cancellation that hides a negative exponent. If E is nonzero, every exponent (p,q) obeys 0≤p,q≤n. Thus n≥0. For n=0, E is constant. For n≥0 the coefficient of u^n v^n is the constant coefficient. Hence

    total_degree(E)=2n  if and only if  E(0,0) is nonzero.

In that event deg_u(E)=deg_v(E)=n. Conversely, merely having degree n in each variable does not force a u^n v^n term: u^n+v^n is a counterexample to that formal inference for n>0. This is why the degree issue involves nonvanishing of a specific corner coefficient, not just an upper bound.

The proof is elementary coefficient comparison and needs no unproved finiteness assertion.

## 2. Explicit convention and zero-exception checks

Let T=conv((1,0),(0,1),(-1,-1)). Its dual under the convention <x,y>≥−1 is conv((-1,-1),(-1,2),(2,-1)), so T is reflexive, d=2,r=1,n=1. All edges of T are primitive. Its h*-polynomial is 1+t+t²; that of T^× is 1+7t+t². For a triangle, the local polynomial is h*(T) minus the sum of the three edge h*-polynomials plus 2. Consequently both local polynomials are t+t²; those of the edges of T and its vertices vanish.

Only the empty and whole faces contribute to the defining stringy formula, giving

    E_T(u,v)=(uv)^-1[(uv)+(uv)²−u³((v/u)+(v/u)²)]
             =1−u−v+uv.

Thus total degree is 2, each separate degree is 1, the diagonal specialization has degree 2, and E_T(t,1)=0. These are different conventions. A literal total-degree-n reading is false already here, but this does not refute the qualified standard conjecture.

The zero exception is essential even for n≥0. Let R be a reflexive (n+2)-simplex and let P be its integral lattice pyramid, i.e. its free join with a lattice point. A point has dimension 0 and index 1, so P has dimension n+3 and index 2, and hence CY-dimension n. Its point factor has E=0 (negative CY-dimension −1), whence E_P=0 by free-join multiplicativity. This constructs a zero example for every integer n≥0. No finite degree is assigned to the zero polynomial.

## 3. Cases where finiteness follows

For n<0 every polynomial is zero; for n=0 every nonzero polynomial is constant. Therefore scalar-class finiteness is immediate in both ranges, independently of [KN].

For any fixed n and upper bound R on the index, d=n+2r−1≤n+2R−1, so only finitely many dimensions occur. In each dimension there are finitely many Gorenstein polytopes up to lattice equivalence. One way to see the last deduction from reflexive-polytope finiteness is to write rP−m=Q: for fixed reflexive Q and r, translation classes of m modulo rM supply at most r^d candidates. This gives finiteness of the actual polynomials, and in particular handles reflexive polytopes. The unbounded-index case is not covered.

For smooth Gorenstein polytopes, Lorenz–Nill [LN, Theorem 4.1] reduces d>3n+3 to a smooth polytope with the same E and d≤3n+1. Together with the dimensions d≤3n+3 this proves finiteness for that class. The complete-intersection construction is also much better understood: Borisov–Li [BL, Corollary 5.3] bounds the stringy Hodge numbers of connected Calabi–Yau varieties arising from the Batyrev–Borisov construction in fixed dimension despite unbounded codimension. These geometric hypotheses cannot be silently extended to all Gorenstein polytopes; [BL, Section 6] expressly separates the broader reflexive-Gorenstein-cone question.

## 4. Integral free joins: precise reduction and scalar obstruction

Let I=[−1,1]. It is reflexive and self-dual. Its local polynomial is t, and the two surviving terms in the stringy formula give E_I=2. For the integral free join J_k of k copies of I,

    dim(J_k)=2k−1, index(J_k)=k, CYdim(J_k)=0, E_(J_k)=2^k.

For any Gorenstein Q with nonzero E_Q and CYdim(Q)=n, the free join Q∘J_k has CY-dimension n and polynomial 2^k E_Q. These form infinitely many different polynomials and occur in unbounded dimension, but represent a single scalar class. This is an obstruction to removing the words “up to scalar”, not a counterexample to the actual finiteness question. This scalar phenomenon is already recorded in [BN, Remark 4.22].

Here is a useful exact reduction. Fix N≥1. The following are equivalent:

(a) For every 0≤n≤N, all Gorenstein polytopes of CY-dimension n produce finitely many nonzero scalar classes.

(b) For every 1≤n≤N, Gorenstein polytopes that are indecomposable under nontrivial integral free joins produce finitely many nonzero scalar classes.

Proof. The implication (a)⇒(b) is restriction. Conversely repeatedly split a decomposable polytope into integral free-join factors; dimensions strictly decrease, so the procedure ends. If the original E is nonzero, every factor has nonzero E because their product is nonzero in Z[u,v]. Every factor then has nonnegative CY-dimension by Section 1. Their CY-dimensions add to n. The zero-dimensional-in-CY factors have constant E and disappear upon taking scalar classes. At most n positive-CY factors remain, each with CY-dimension between 1 and n. Under (b) these factors come from a finite union of finite sets of scalar classes; products of at most N members of a finite set form a finite set. Decomposition uniqueness is unnecessary. The n=0 case is Section 3. This proves equivalence.

This is not a dimension bound or a proof of (b). “Indecomposable” here always refers to integral free joins, not the broader Gorenstein-join irreducibility of [NS].

## 5. Even all displayed polynomial identities cannot force finiteness

For every integer m≥0 define the purely formal polynomial

    Q_m(u,v)=(1−u³)(1−v³)+m uv(1−u)(1−v).

It has constant coefficient 1 and total degree 6, degrees 3 in each variable, and coefficients of the form (−1)^(p+q)h^(p,q) with nonnegative integers h. It is symmetric in u,v and obeys both

    Q_m(u,v)=(uv)³Q_m(u^-1,v^-1),
    Q_m(u,v)=−u³Q_m(u^-1,v).

Its boundary is Q_m(u,0)=1−u³, giving the n=3 boundary/Serre identity. Also Q_m(u,1)=0 identically, so Q_m(1,1), its first u-derivative there, and its second u-derivative there are all zero. Thus it obeys both derivative identities displayed in [NS, Conjecture 3.3(4)–(5)] as well, with n=3. These verifications follow immediately by factoring, or by the exact symbolic check over Z[m] supplied here.

The coefficient of uv equals m. If Q_m is a scalar multiple of Q_l, the constant coefficients force the scalar to be 1, then the uv coefficients force m=l. Hence infinitely many scalar classes satisfy all these identities.

**No realization by Gorenstein polytopes is claimed.** This proves only that those identities, positivity, symmetry, and the correct degree cannot by themselves establish finiteness. The missing input must constrain realizability or the coefficients more strongly.

## Remaining gap

A finiteness theorem or an infinite non-proportional realized family for arbitrary Gorenstein polytopes remains missing from this attempt. The retained reduction identifies positive-CY, free-join-indecomposable factors as the obstruction. The formal Q_m family is not a geometric counterexample. The 2026 degree claim does not fill this finiteness gap. No exhaustive current-openness or external peer-review claim is made.

## References

[OWR] Benjamin Nill (joint work with Jan Schepers), contribution in Toric Geometry, Oberwolfach Rep. 9 (2012), printed pp. 1292–1294; https://doi.org/10.4171/OWR/2012/21 .

[BN] Victor Batyrev, Benjamin Nill, Combinatorial aspects of mirror symmetry; https://arxiv.org/abs/math/0703456 .

[NS] Benjamin Nill, Jan Schepers, Gorenstein polytopes and their stringy E-functions; https://arxiv.org/abs/1005.5158 ; journal DOI https://doi.org/10.1007/s00208-012-0792-2 .

[LN] Benjamin Lorenz, Benjamin Nill, On smooth Gorenstein polytopes; https://doi.org/10.2748/tmj/1450798070 .

[BL] Lev A. Borisov, Zhan Li, On complete intersections with trivial canonical class; https://doi.org/10.1016/j.aim.2014.08.013 ; https://arxiv.org/abs/1404.7490 .

[KN] Johannes Knupfer, Benjamin Nill, Decomposing Gorenstein polytopes of large index, arXiv:2609.18873v1, 16 September 2026; https://arxiv.org/html/2609.18873v1 .
