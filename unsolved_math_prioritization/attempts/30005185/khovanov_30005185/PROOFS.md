# Exact formulation, elementary reductions, and the unresolved parity

## 1. Formulation and conventions

Let K be a smooth knot in S³. Write

    r_F(K) = sum over h,q of dim_F reduced Kh^{h,q}(K;F).

This is the total dimension, not an Euler characteristic or an individual grading. Over Z, rank means the rank of the free part, so r_Z=r_Q. Normalize the reduced unknot group in bidegree (h,q)=(0,0). The delta grading is δ=q/2-h. Reduced knot quantum degrees are even in this normalization.

[Marengon's report, OWR 34/2022, printed p.1976](https://ems.press/content/serial-article-files/46971) first states modulo-eight conjectures for coefficients Z or F_p, then explicitly weakens its Khovanov assertions to modulo four. Thus the target is

    r_F(R) ≡ 1 (mod 4) for every ribbon knot R,

for F=Q or F_p, with the equivalent integral-free-rank interpretation. A ribbon knot is obtained by banding an unlink to one component, equivalently bounds a smooth disk having no radial local maxima. The associated concordance assertion concerns ordinary smooth concordance of all knots, with multiplication in (Z/4Z)^×. It is not a claim only about pairs already related by a ribbon concordance, nor a claim about unreduced or odd Khovanov homology. No slice-ribbon conjecture is assumed.

The 2023 [Dunfield–Gong–Hockenhull–Marengon–Willis paper](https://arxiv.org/abs/2303.04233), Conjecture 1.3(b), retains this question. Its Theorem 1.5 proves the concordance equivalence, and Theorem 1.8 credits Lipshitz–Sarkar with the fusion-number-one result over Q and F_p for odd p. Its modulo-eight counterexamples do not refute the modulo-four target. It reports checks on 2.4 million ribbon knots over F2, F3 and F211; these were not independently replayed here.

## 2. Rank parity and connected sums

For any field, the reduced Jones Euler-characteristic identity at q=1 gives

    sum_h,q (-1)^h dim_F reduced Kh^{h,q}(K;F) = V_K(1) = 1.

Reducing modulo two removes all signs, proving r_F(K) is odd. This also follows directly from the integral chain complex, whose Euler characteristic is unchanged on reduction to a field.

The reduced connected-sum formula over a field and the Künneth theorem give

    r_F(K#J)=r_F(K)r_F(J).

Mirror duality gives r_F(-K)=r_F(K), with -K denoting the concordance inverse. Consequently every rectangular ribbon knot K#(-K) has rank r_F(K)²≡1 mod 8: if r=2m+1, then r²-1=4m(m+1), divisible by eight. This is a complete argument for this known family, not a statement that all ribbon knots are rectangular.

For clarity about the concordance reduction, the standard stable-ribbon lemma says that for each smoothly slice S there is a ribbon R such that S#R is ribbon (the precise input used in the cited Theorem 1.5). Assuming the target for ribbon knots, multiplicativity yields r_F(S)r_F(R)≡1 and r_F(R)≡1, so r_F(S)≡1. If K and J are smoothly concordant, K#(-J) is slice. Thus r_F(K)r_F(J)≡1; because every odd residue squares to one modulo four, r_F(K)≡r_F(J). Conversely a concordance-invariant residue must equal the unknot residue for every ribbon knot. This is the credited known equivalence, not a new topological lemma.

## 3. A general normal-form parity lemma

This section is a direct algebraic derivation. Its input is the familiar lifted-Lee description, not a new theorem asserting a geometric restriction on ribbon knots.

Let F have characteristic different from two and A=F[X], with deg(X)=(0,-2). Use the reduced quantum normalization, shifted down one from the unreduced lifted-Lee convention. For a knot, the lifted-Lee chain complex is a finite free graded A-complex. Up to graded chain homotopy and removal of contractible pairs it has one free summand and two-generator summands

    C ≃ A·z ⊕ direct_sum_i [A·u_i --X^{a_i}--> A·v_i],  a_i≥1.

The differential has bidegree (1,0). The free generator z has bidegree (0,s_F(K)). These facts follow from the graded Smith-normal-form decomposition in [Schütz, Section 2.1](https://maths.dur.ac.uk/users/dirk.schuetz/d40.pdf) and the graded torsion description in [Sarkar, Section 5](https://arxiv.org/abs/1903.11095): the free module is in quantum degree s_F(K)+1 before the reduced shift, and every torsion elementary divisor is a power of X. Reduction X=0 recovers the reduced Khovanov complex, up to this conventional shift. For a slice knot, s_F(K)=0.

Put k=# {i}, E=# {i:a_i even}, and δ_i=δ(u_i). Homogeneity gives

    h(v_i)=h(u_i)+1,
    q(v_i)=q(u_i)+2a_i,
    δ(v_i)-δ(u_i)=a_i-1.                         (3.1)

Every differential in this normal form vanishes at X=0, so

    r_F(K)=1+2k.                                  (3.2)

The delta-graded signed sum of the reduced homology equals V_K(-1), the signed determinant D(K). For a slice knot the free contribution is +1. The pair indexed by i contributes

    (-1)^{δ_i} [1+(-1)^{a_i-1}].                 (3.3)

Thus even a_i contribute zero, while odd a_i contribute +2 or -2. Set

    S = sum over odd a_i of (-1)^{δ_i}.

Then D(K)=1+2S. For a slice knot the Fox–Milnor factorization, with the symmetric normalization Δ_K(1)=1, gives D(K)=Δ_K(-1)=f(-1)², an odd square. Therefore D(K)≡1 mod 8, so S≡0 mod 4. Modulo two the signs in S disappear. Hence the number O of odd a_i is even. Since k=O+E, equation (3.2) proves

    r_F(K) ≡ 1+2E (mod 4).                       (3.4)

In particular, for slice knots in characteristic different from two:

    r_F(K)≡1 mod 4  if and only if  E is even.

All a_i odd is a sufficient condition. In particular a_i=1 for all i gives the familiar extortion-order-one conclusion. Sarkar's ribbon-distance bound makes this apply to nontrivial fusion-number-one ribbon knots. The unknot is handled separately by rank one. This rederives the algebra behind the credited Lipshitz–Sarkar special case and isolates what it does not show for larger extortion order.

[Dunfield–Gong, Section 2.8](https://arxiv.org/abs/2512.21825) reports 582 ribbon knots with X-torsion order two in its computations over Q, F3 and F5. Thus even exponents cannot simply be excluded from ribbon knots; the needed condition is their parity. These source computations were not independently rerun.

**Exact gap:** neither the PID decomposition nor the determinant constrains the parity of E. Proving that E is even for all ribbon knots would settle the odd-characteristic/rational target. This package does not prove that condition.

## 4. A formal countermodel to the insufficient hypotheses

Over F[X], take C⁰=A·z⊕A·u and C¹=A·v, with

    deg z=(0,0), deg u=(0,0), deg v=(1,4),
    d(z)=0, d(u)=X²v, d(v)=0.

The differential has bidegree (1,0), d²=0, and C has a literal free direct summand A·z. Inclusion and projection are chain maps whose composition is the identity. After inverting X the u,v pair is acyclic. After setting X=0 it contributes two homology classes, so the reduced rank is three. Their delta gradings are 0 and 1; adding z gives signed determinant 1. The free generator lies in the slice-compatible degree, but E=1 and rank≡3 mod 4.

This example rigorously refutes the implication “split rank-one summand + these grading/normal-form conditions + square determinant implies rank 1 modulo four.” It does not refute a theorem about knots: no realization of C as a knot's complex, ribbon or otherwise, is claimed. In particular it need not satisfy every additional functorial, integral, or geometric constraint of an actual knot complex.

## 5. Coefficient transfer and its independent obstruction

Let C_Z be the reduced integral Khovanov complex, a bounded complex of finitely generated free abelian groups. Let t_p be the total number of p-primary cyclic summands in its integral homology, counting one for each Z/p^a factor, not a copies. Universal coefficients give a tensor contribution and an adjacent-degree Tor contribution for each such summand. Summing over all degrees yields exactly

    r_{F_p}(K)=r_Q(K)+2t_p(K).                    (5.1)

The integral free rank equals r_Q. Therefore a rational modulo-four assertion transfers to F_p precisely when t_p(K) is even. An odd p-torsion count changes the residue by two. Equality for a large prime such as 211 does not by itself certify equality over Q; one needs exact rational calculation or a torsion exclusion.

For a formal negative control, take a free Z-generator z and the two-term complex Z --p--> Z in disjoint summands. Its rational homology rank is one and its F_p homology rank is three. This establishes the logical need for the torsion hypothesis without pretending to realize a knot. Characteristic two is included in (5.1), but is deliberately excluded from the lifted-Lee argument of Section 3.

## 6. Local-move and actual knot controls

The authored program `cube_verify.py` builds the reduced cube over Z, using A=Z[x]/(x²), marked-circle label x, multiplication and comultiplication, and the standard cube sign. It checks d²=0 over Z and then performs exact sparse elimination over Q or the selected prime field. It omits orientation grading shifts; these do not affect total rank. A braid-to-PD builder constructs the diagrams, rather than shipping a source census.

For the unknot, the complex is one generator. For trefoil and mirror, it computes rank three. It constructs the square-knot diagram by joining a trefoil diagram and its mirror, and computes rank nine. The standard untwisted symmetric-double construction supplies its ribbon disk; rank multiplicativity gives an independent expected answer 3²=9.

The explicit four-strand braid (-1,-1,-2,1,3,-2,3) represents stevedore 6_1, and the three-strand braid (-1,-1,-1,2,-1,2) represents 6_2, up to the harmless global mirror convention of the builder. These identifications and a stevedore ribbon diagram are recorded by the [Knot Atlas 6_1 entry](https://katlas.org/wiki/6_1) and [6_2 entry](https://katlas.org/wiki/6_2). The calculated ranks are respectively 9 and 11 over Q,F2,F3,F5. The first is a credited ribbon positive control; the second is a nonslice negative control. The program verifies ranks, not the source's knot identifications or the ribbon movie.

Dunfield and collaborators' Proposition 7.1 exhibits 6_2 as an obstruction to an induction using only their local ribbon-singularity tangle move: the same oriented local move unknots 6_2, although it is not ribbon. The computation here independently checks the numerical rank 11≡3 mod 4. The implication fails when the global ribbon disk is discarded. No claim is made to have encoded or replayed the four diagrammatic unknotting movies from their Figure 10.

## 7. What remains

There is no full proof, no knot counterexample, and no novelty claim. For odd characteristic, the unresolved task is the geometric parity constraint on even X-exponents. Across characteristics, integral p-torsion parity is a separate unresolved issue. The exact small examples and algebra controls cannot replace either missing theorem.
