# Bicanonical connectedness and finite covers of numerical Godeaux surfaces

Problem 30000515 / OWR-1276-008. Authored note, 10 October 2026.

**Status: PARTIAL. The topological simple-connectivity question is not settled.**

This note reconstructs established consequences in a self-contained argument and makes the residual obstruction explicit. No novelty is claimed for the torsion or algebraic-fundamental-group conclusions. Reid already states the torsion implication in the original question; the established finite algebraic fundamental group of a numerical Godeaux surface is cyclic of order at most five. We do not need that sharper classification below.

## 1. Exact question and conventions

Let S be a smooth, connected, minimal complex projective surface of general type with p_g(S)=q(S)=0 and K_S^2=1. The question asks whether pi_1(S)=1 under both of the following hypotheses:

1. The complete bicanonical pencil |2K_S| has four distinct base points (the usual finite, reduced base-locus condition).
2. Every divisor C in |2K_S| is 2-connected: for every expression C=A+B with nonzero effective divisors A and B, including expressions with repeated or overlapping components, A.B >= 2.

All divisors and intersection numbers below are on the smooth minimal surface, not silently on its singular canonical model. Write K=K_S and Tors Pic(S) for the finite-order subgroup of Pic(S). Linear equivalence is denoted by ~, and numerical equivalence by =_num.

## 2. The exact torsion criterion

**Theorem 1.** For every numerical Godeaux surface S, the following conditions are equivalent:

(a) Every member of |2K| is 2-connected.

(b) Tors Pic(S)=0.

The four-distinct-base-points hypothesis is unnecessary for this equivalence.

### Proof of (a) implies (b)

Suppose that tau is a nontrivial torsion line bundle. A nontrivial numerically trivial line bundle L has no nonzero global section: its effective zero divisor, if nonempty, would have positive intersection with an ample divisor, whereas L has intersection zero; a nowhere-vanishing section would trivialize L.

Thus h^0(-tau)=h^0(tau)=0. Riemann–Roch and Serre duality give

    chi(K+tau)=chi(O_S)+(K+tau).tau/2=1,
    h^2(K+tau)=h^0(-tau)=0.

Consequently h^0(K+tau)=1+h^1(K+tau)>=1. Applying the same argument to -tau produces effective divisors D_+ in |K+tau| and D_- in |K-tau|. Both are nonzero because their intersection with K is one. Their sum C=D_++D_- belongs to |2K|, but

    D_+.D_-=K^2=1.

This contradicts (a). If tau has order two, the two divisors may coincide; that remains a valid decomposition, so this case is not omitted.

### Proof of (b) implies (a)

The canonical divisor K is nef and K^2=1. Suppose C=A+B in |2K| with A,B nonzero and effective. Set k=K.A. Since K.B=2-k and K is nef, k is one of 0,1,2.

If k=0, A is not numerically zero because an ample divisor intersects a nonzero effective divisor positively. The Hodge index theorem says that the intersection form on K-perp is negative definite, so A^2<0. The parity identity A.(A+K)=2p_a(A)-2 shows A^2 is even. Hence

    A.B=A.(2K-A)=-A^2>=2.

If k=2, the same argument applied to B gives A.B>=2.

If k=1, Hodge index gives A^2 <= (K.A)^2/K^2=1. The same parity identity shows that A^2 is odd. Suppose A.B<2. Since A.B=2-A^2, necessarily A^2=1 and A.B=1. Then

    K.(A-K)=0,    (A-K)^2=0.

Negative definiteness on K-perp implies A=_num K. On a surface with p_g=q=0, a numerically trivial line bundle is torsion. Here is a justification of that last step: the exponential sequence gives Pic(S) isomorphic to H^2(S,Z), since H^1(O_S)=H^2(O_S)=0. Divisor classes therefore span H^2(S,R); numerical triviality and the nondegeneracy of the intersection pairing imply zero real cohomology class, so the integral class is torsion. Thus A-K is torsion. Under (b), A~K. Its effectiveness would imply h^0(K)>=1, contradicting p_g=0.

All possibilities give A.B>=2. This proves (a). QED.

**Useful sharper formulation.** A failure of 2-connectedness is necessarily an intersection-one decomposition with A=_num B=_num K and nontrivial opposite torsion classes A-K and B-K. This argument covers nonreduced members and negative curves. It never replaces “every member” by “general member.” If K is ample and the torsion is trivial, the same proof actually gives A.B>=3, because the cases k=0 and k=2 cannot occur.

**Source credit.** Reid's 2006 report, printed p.1645, states (a) implies (b). The torsion decompositions and Hodge-index mechanism also occur in Catanese–Pignatelli and in Schreyer–Stenger, arXiv:2201.12065, Lemma 2.1 and its proof, stated there using the canonical model. The proof above gives the precise 2-connectedness equivalence on S directly; it is an exposition of standard geometry, not a claimed new theorem.

## 3. Integral first homology vanishes

**Corollary 2.** Under either equivalent condition in Theorem 1, H_1(S,Z)=0, and therefore pi_1(S) is perfect.

**Proof.** The group H_1(S,Z) is finitely generated, and its rank is b_1(S)=2q(S)=0. It is thus finite. The universal-coefficient exact sequence identifies the torsion of H^2(S,Z) with Ext^1(H_1(S,Z),Z), which is isomorphic, noncanonically, to H_1(S,Z) for a finite abelian group. By the exponential-sequence isomorphism above, torsion in H^2(S,Z) is exactly torsion in Pic(S), and hence is zero. Thus H_1(S,Z)=0. The degree-one Hurewicz theorem identifies H_1(S,Z) with the abelianization of pi_1(S). QED.

Perfectness by itself does not prove triviality. The next argument excludes all finite quotients, rather than mistakenly stopping at abelian quotients.

## 4. Every finite cover is trivial

**Lemma 3.** If f:Y->S is a connected finite unramified topological cover of a numerical Godeaux surface, and d is its degree, then d<=6.

**Proof.** The cover inherits a complex structure making f holomorphic and unramified. It is compact and projective: the pullback of a positive ample line bundle on S is positive, so Kodaira's embedding theorem applies. Its canonical divisor is f^*K and is nef; in particular Y is minimal. It is of general type, and

    K_Y^2=d K_S^2=d,
    chi(O_Y)=d chi(O_S)=d.

The second identity also follows directly from Noether's formula, since both c_1^2 and the topological Euler characteristic multiply by d. Noether's inequality for a smooth minimal surface of general type gives

    K_Y^2 >= 2 chi(O_Y)-6.

Thus d>=2d-6 and d<=6. This weaker form follows as well from K_Y^2>=2p_g(Y)-4 and q(Y)>=0. QED.

**Theorem 4.** If every member of |2K_S| is 2-connected, pi_1(S) has no nontrivial finite quotient. Equivalently, S has no nontrivial connected finite topological cover, its profinite completion is trivial, and its algebraic fundamental group is trivial.

**Proof.** Let Gamma=pi_1(S), and suppose Gamma surjects onto a finite group G. The kernel gives a connected regular cover Y->S of degree |G|, so Lemma 3 gives |G|<=6. By Corollary 2, Gamma is perfect, and any quotient of a perfect group is perfect: G=[G,G].

No nontrivial group of order at most six is perfect. Groups of order 2,3,5 are cyclic. Groups of order four are abelian. For order six, Sylow's theorem gives a unique subgroup of order three because its number is congruent to one modulo three and divides two. The quotient by that normal subgroup has order two, so the abelianization is nontrivial. This accounts for every possible order 2 through 6. Therefore G=1.

For completeness, a nontrivial nonregular finite connected cover would correspond to a proper finite-index subgroup H of Gamma. The action on the finite set Gamma/H would give a nontrivial finite quotient, already excluded. Thus the assertion covers non-Galois covers as well. The comparison between finite étale covers and finite topological covers over C identifies the algebraic fundamental group with the profinite completion. QED.

**Corollary 5.** Under the question's hypotheses, if pi_1(S) is finite or residually finite, then S is simply connected. A counterexample must have an infinite, finitely presented, perfect fundamental group with no nontrivial finite quotient and no proper finite-index subgroup.

The finite-presentation assertion follows because S is a compact smooth manifold. These are necessary conditions on a hypothetical counterexample, not a construction of one and not evidence that it exists.

**Source credit.** The finite-cover method is the standard Noether-inequality argument in the geography of algebraic fundamental groups. Noether's inequality in exactly the needed form appears in Mendes Lopes–Pardini, arXiv:math/0512483v3, introduction. The sharper established result pi_1^alg(S)=Z/m, m<=5, is reported in the primary Godeaux literature; Theorem 4 is compatible with it and is not claimed as a new algebraic simple-connectivity result.

## 5. Why this does not settle the requested conclusion

Theorem 4 gives trivial profinite completion, not trivial topological fundamental group. The argument in Lemma 3 cannot be applied to an infinite-sheeted universal cover: that cover is not compact and the projective-surface form of Noether's inequality does not apply to it. Neither residual finiteness nor finiteness of pi_1(S) has been proved here.

Theorem 1 also shows that the 2-connectedness condition is precisely the absence of Picard torsion. Consequently it supplies no additional unproved monodromy-generating statement. With four simple base points one can blow up to a genus-four fibration with four sections. Adjunction computes p_a(2K)=4. This geometric setup alone does not compute the normal subgroup killed in the fundamental group of a smooth fiber. We have no uniform van Kampen or vanishing-cycle proof that this subgroup is the whole fiber group.

Schreyer–Stenger construct an eight-dimensional locally complete family whose surfaces are simply connected, including the Barlow deformation class. A smooth proper deformation into that family would suffice. Their later paper leaves unclassified special-line loci in the construction of marked surfaces. No argument here shows that every torsion-free marked Godeaux surface lies in the known smooth deformation class, or that every remaining special-line solution is singular, reducible, or deforms into it.

Thus the exact residual is to rule out an infinite fundamental group with trivial profinite completion for every torsion-free numerical Godeaux surface with the stipulated four distinct bicanonical base points, or to exhibit one and verify all hypotheses. Neither has been achieved here.

## 6. Public primary references

1. Miles Reid, “Attempt to construct the general simply connected Godeaux surface,” Oberwolfach Report 27/2006, printed pp.1645–1647. https://doi.org/10.4171/OWR/2006/27
2. Frank-Olaf Schreyer and Isabel Stenger, “An 8-dimensional family of simply connected Godeaux surfaces,” arXiv:2009.05357v2, §§1,5–6; especially Remark 1.8, Lemma 1.9, Corollary 5.2 and Proposition 5.6. https://arxiv.org/abs/2009.05357v2
3. Frank-Olaf Schreyer and Isabel Stenger, “Marked Godeaux surfaces with special bicanonical fibers,” arXiv:2201.12065v1, Lemma 2.1, Theorem 2.2, §4 and Summary. https://arxiv.org/abs/2201.12065v1
4. Fabrizio Catanese and Roberto Pignatelli, “On simply connected Godeaux surfaces,” Complex Analysis and Algebraic Geometry (2000), 117–153. https://doi.org/10.1515/9783110806090-007 ; author copy: https://pignatelli.maths.unitn.it/papers/godeauxdg.pdf
5. Margarida Mendes Lopes and Rita Pardini, “On the algebraic fundamental group of surfaces with K^2<=3chi,” arXiv:math/0512483v3; Journal of Differential Geometry 77 (2007), 189–199. https://arxiv.org/abs/math/0512483
6. Eduardo Dias and Carlos Rito, “Z/2-Godeaux surfaces,” arXiv:2009.12645v3 (28 April 2026), introduction; Journal of Algebra 701 (2026), 340–357. https://arxiv.org/abs/2009.12645v3 ; https://doi.org/10.1016/j.jalgebra.2026.04.035

These references support the stated dependencies and scope. The bounded literature review does not certify present global openness or priority.
