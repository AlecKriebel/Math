# Surgery and actual-knot construction routes

These are the fourth and fifth bounded approaches. Neither provides a full solution. All known results are used with attribution; no novelty is claimed.

## 4. Surgery, spin parity and the missing functorial bridge

The Arf invariant can be recovered as the Rokhlin invariant of +1 surgery. This suggests comparing A with a spin/Floer invariant of the surgery, then using finite concordance order. However, a knot connected-sum relation cannot simply be passed through +1 surgery as an additive homology-cobordism relation.

Here is a concrete failure of that shortcut. Let T be the right-handed trefoil. Its staircase has two degree-zero cycles p,q at bifiltrations (0,1),(1,0), and a degree-one generator r at (1,1) with ∂r=p+q. Multiplication by U lowers the bifiltration by (1,1) and the degree by two.

For this complex, V_0(T)=1: a representative of U times the tower generator lies in the nonpositive quadrant, whereas no degree-zero generator does. For T#T, the cycle U(p⊗q) lies at (0,0) and represents U times the tower generator, so V_0(T#T)≤1. In degree zero, the possible terms are pp,pq,qp,qq and Urr, at filtrations (0,2),(1,1),(1,1),(2,0),(1,1); none lies in the nonpositive quadrant. Thus V_0(T#T)=1 as well. The verifier independently checks these finite chain equations and the tower augmentation.

The surgery correction-term identity d(S^3_1(K))=−2V_0(K), together with additivity of d under three-manifold connected sum, now gives

    d(S^3_1(T#T))=−2,
    d(S^3_1(T)#S^3_1(T))=−4.

These manifolds are not smoothly integral-homology cobordant. Therefore the operation K↦S^3_1(K) is not a group homomorphism from all of smooth knot concordance to integral homology cobordism. This example does not itself rule out a special torsion-only construction; it rules out using general additivity without a proof.

There is a second information gap. For the figure-eight, the ordinary V_0 is zero while Arf and A are one. Thus the ordinary surgery correction term already loses the bit needed here. The involutive correction terms supply additional information, but do not become additive merely by being concordance invariants. A general identification of the relevant involutive surgery parity with A on all torsion knots is not established by this argument.

Hendricks–Mallick's 2025 cabling formulas concern underline(V_0) and overline(V_0). They do not identify the Kang–Park A invariant with Arf. Their Section 4 also treats long-box local-equivalence models, so the elementary long-box tests in FORMAL_COMPLEX_AUDIT.md should not be presented as a newly discovered model family.

Exact gap: an actual construction or formula preserving the necessary involutive structure and spin parity on every smooth torsion class, with all functorial hypotheses proved. Neither a surgery slogan nor numerical correction terms provide it.

## 5. Symmetric satellite search on certified two-torsion knots

An actual-knot counterexample is more informative than a formal complex. A concrete testing family is the two-band family K_(J,n) of Hedden–Kim–Livingston: the bands are tied in J and −J with opposite n twists. Their Proposition 1.1 certifies negative amphichirality and hence 2[K_(J,n)]=0. Their branched-cover calculation gives determinant 4n^2+1. The untied knot K_(U,n) is the corresponding two-bridge knot and is quasi-alternating. These are existing constructions, not new knots proposed here.

The determinant gives an exact target value:

    4n^2+1 ≡ 1 (mod 8) when n is even,
    4n^2+1 ≡ 5 (mod 8) when n is odd,
    Arf(K_(J,n)) = n mod 2.

In particular, the companion J cannot change Arf in this family. By the already known quasi-alternating case, A(K_(U,n))=n mod 2. Consequently, for

    L_(J,n)=K_(J,n)#K_(U,n),

we have 2[L_(J,n)]=0, Arf(L_(J,n))=0, and

    A(L_(J,n))=A(K_(J,n))+(n mod 2).

An independently computed value A(K_(J,n))≠n mod 2 would therefore be an actual counterexample. A(L)=1 would itself certify that L is nonslice, so a separate proof of *exact* order two would not be needed after that computation. Hedden–Kim–Livingston obtain infinite families of nonslice, topologically slice examples of this general form using Whitehead-double companions. Ordinary branched-cover correction terms detect their nonsliceness, but that calculation does not supply the knot involution needed to compute A.

There is a precise finite certificate for the missing computation. Suppose the horizontal complex of an actual torsion knot has been reduced to a homogeneous F_2[U] basis x,y_i,z_i with

    ∂x=∂z_i=0,   ∂y_i=U^(n_i)z_i,   n_i>0,

where x is the normalized free generator. In the hat vector space put

    Z=span{z_i},   W=im(1+iota).

The argument in Kang–Park's Theorem 2.11 gives

    A(K)=0  ⇔  x∉Z+W,
    A(K)=1  ⇔  x∈Z+W,

under the essential hypothesis that K is genuinely torsion. To see the map test directly, a local chain map to O must send x to 1 and every torsion cycle z_i to zero; hat-equivariance makes it vanish on W. If x is outside Z+W, choose a separating functional supported in bidegree (0,0) and extend it F_2[U]-linearly. It is the required local chain map. For a torsion class, the only alternatives are O and E, and E admits no such map. Thus the membership test determines the bit.

This reduces the proposed family computation to a rank test once correct chain and involution matrices are available. It does not manufacture those matrices. No involutive bordered computation for K_(J,n), nor any replacement geometric invariant computing the same bit, was completed in this bounded approach. Reusing the ordinary CFK complex or the three-manifold involution of its branched cover would leave precisely the missing datum unspecified. No member of this family is claimed as a counterexample.

## Disposition

Five distinct mechanisms were investigated: additive characters, Euler-parity descent through horizontal equivalence, tensor-power descent, surgery/spin comparison, and an actual two-torsion satellite family. The exact target is unresolved in this work, with no complete proof or actual-knot counterexample. The proof-search budget is exhausted at 5/5. The saved material is a partial audit package, not a candidate full solution or an assertion of worldwide openness.

## References

- S. Kang and J. Park, *Torsion in the knot concordance group and cabling*, JEMS 28 (2026), 3011–3047. https://doi.org/10.4171/JEMS/1520
- K. Hendricks and C. Manolescu, *Involutive Heegaard Floer homology*, Duke Math. J. 166 (2017), 1211–1299. https://arxiv.org/abs/1507.00383 ; author preprint https://web.stanford.edu/~cm5/hfi.pdf (preprint numbering may differ from the journal).
- Y. Ni and Z. Wu, *Cosmetic surgeries on knots in S^3*, J. Reine Angew. Math. 706 (2015), 1–17, Proposition 1.6. https://arxiv.org/abs/1009.4720
- K. Hendricks and A. Mallick, *A note on cables and the involutive concordance invariants*, Bull. London Math. Soc. 57 (2025), 1593–1604. https://doi.org/10.1112/blms.70050 ; https://arxiv.org/html/2409.02192v2
- M. Hedden, S.-G. Kim and C. Livingston, *Topologically slice knots of smooth concordance order two*, J. Differential Geom. 102 (2016), 353–393, Proposition 1.1 and Section 2.1. https://arxiv.org/html/1212.6628v2
