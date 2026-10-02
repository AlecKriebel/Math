# Turn 3: the complete center algebra can miss the commutator pencil

Problem 30006345. Third substantive author turn. **Original unresolved, 3/5.** This gives two explicit class-two exponent-three groups with isomorphic center algebras over every characteristic-three field, but nonisomorphic full group algebras over every such field. It is a limitation of the center route, not a modular-isomorphism counterexample.

## 1. Explicit groups

All coefficients in this section are in F_3. Put

    T_0 = [[0,2],[1,0]],       T_1 = [[0,1],[1,2]],
    A_T(u,v)=u I_2−vT,
    M_T(u,v)=[[0,A_T(u,v)], [−A_T(u,v)^T,0]].

These last matrices are alternating 4×4 matrices. Define alternating 8×8 pencils

    P(u,v)=diag(M_(T_0)(u,v), M_(T_0)(u,v)),
    Q(u,v)=diag(M_(T_0)(u,v), M_(T_1)(u,v)).

Write P=uP_0+vP_1, Q=uQ_0+vQ_1. For B=P or Q let V=F_3^8, W=F_3² and define

    beta_B(x,y)=(x^T B_0 y, x^T B_1 y),
    (x,z)(y,w)=(x+y,z+w+(1/2) beta_B(x,y)).                    (1)

Here 1/2=2 in F_3. Denote the resulting groups by G_P,G_Q.

Bilinearity proves associativity directly; alternation gives inverse(−x,−z) and (x,z)^j=(jx,jz). The commutator ghg⁻¹h⁻¹ is (0,beta_B(x,y)). Hence the groups have order 3^10, exponent 3, and class at most two. The following calculation gives derived subgroup and center both equal to W, so their class is exactly two.

## 2. Every noncentral class is a full central coset

The determinant polynomials of the 2×2 matrices are

    det A_(T_0)=u²+v²=:q_0,
    det A_(T_1)=u²+uv+2v²=:q_1.                               (2)

Both are irreducible homogeneous quadratics over F_3: setting v=1 gives discriminant2, a nonsquare, and neither has a root at infinity. Therefore P(u,v) and Q(u,v) are nonsingular for every nonzero(u,v)∈F_3². In particular B_0 is nonsingular, so beta_B has zero common radical.

For any nonzero x∈V, the contraction y↦beta_B(x,y) is onto W. Otherwise a nonzero functional(u,v) on W would annihilate its image, giving x^T B(u,v)=0, contradicting nonsingularity. Thus the commutator image spans W, the center is W, and every noncentral conjugacy class is exactly (x,z)W, of size 9.

The calculation of turn 2 now applies with center rank 2 and quotient dimension 8. As a unital k-algebra, for every field k of characteristic3,

    Z(kG_P) ≅ Z(kG_Q) ≅ R⊕U,
    R=k[s,t]/(s³,t³),    dim_k U=3^8−1=6560,
    U²=0,    r u=epsilon(r)u.                                (3)

To be explicit, the vector space U is spanned by noncentral conjugacy-class sums. Each is gN with N the sum of the 9 central elements. Then N²=9N=0 and (z−1)N=0, proving (3) independently of the commutator pencil. The center dimension is 6569 and its radical Hilbert polynomial is

    1+6562 t+3 t²+2 t³+t⁴.                                   (4)

Thus even the complete abstract center multiplication, not just center dimension or its radical Hilbert series, is identical in this pair.

## 3. Geometric pencil ranks separate the groups

Over an algebraic closure of F_3, q_0 and q_1 each have two distinct projective roots and share none. Separability follows from their nonzero discriminants. A common root would have v≠0, and subtracting q_0 from q_1 would give v(u+v)=0, hence u=−v; but q_0(−v,v)=2v²≠0.

At a root of q_i, the matrix A_(T_i) has rank 1, not 0, since T_i is nonscalar and v≠0. Elsewhere it has rank 2. The matrix M_T has twice the rank of A_T: its two blocks send the two coordinate summands into separate target summands.

It follows that P has rank 4 at exactly the two roots of q_0 and rank 8 at every other projective point. The pencil Q has rank 6 at the four roots of q_0q_1 and rank 8 elsewhere. In particular P has a nonzero projective parameter of rank 4, whereas Q has none, over the algebraic closure.

A group isomorphism between class-two exponent-p groups induces invertible F_p-linear maps on the abelianization and derived subgroup, intertwining the alternating commutator maps. Such maps act on a pencil by simultaneous congruence and an invertible change of the two parameters. These operations preserve matrix ranks and projective rank loci over every extension field. Therefore G_P and G_Q are not isomorphic.

## 4. Why their full group algebras are also different

We supply the algebraic bridge rather than assuming that group nonisomorphism implies group-algebra nonisomorphism. For a group defined by (1), over any characteristic-three field k the radical associated graded algebra has generators X_1,…,X_8 of degree 1 and Z_1,Z_2 of degree 2, with central Z's, relations

    [X_i,X_j]=sum_l (B_l)_(ij) Z_l,
    X_i³=Z_l³=0.                                            (5)

This is the special Jennings–Quillen presentation already proved by the ordered-monomial argument in turn 1. Here is its dimension check in the current size. The corresponding presented algebra is spanned by ordered monomials with each of ten exponents 0,1,2, so has dimension at most3^10. Sending the generators to augmentation leading terms gives a surjection onto gr_J(kG_B): the commutator coefficients pass to degree 2, the central generators belong to J², and the eight group generators generate all of G_B because the commutator map is onto W. The latter graded algebra has dimension 3^10, as J is nilpotent. The surjection is an isomorphism, proving (5), with no extra relations or hidden collapse of the two Z directions.

In this graded algebra, its degree-one space is canonically V_k. The subspace spanned by brackets of degree-one elements inside degree two is canonically W_k=span(Z_1,Z_2). Multiplication therefore canonically recovers beta_B over k. Any graded algebra isomorphism must intertwine these spaces and this bracket map; a Hopf-algebra isomorphism is not assumed.

An isomorphism kG_P≅kG_Q would preserve the Jacobson radical and all its powers, giving a graded algebra isomorphism and consequently equivalent pencils over k. Extending to an algebraic closure of k gives a contradiction to the rank 4 distinction of Section 3. The root calculation is valid in every algebraically closed field of characteristic3. Hence

    kG_P ≄ kG_Q for every field k of characteristic3.         (6)

Equations (3) and (6) demonstrate that the center algebra alone cannot support a general positive solution. Turn 1 separately showed that the scalar-extended graded algebra alone cannot recover the prime-field group. Neither example satisfies the original hypothesis of isomorphic full group algebras.

## 5. Credit, checks and remaining route

The alternating-form/Baer construction and the use of determinantal rank loci are classical. They are explicitly described in O’Brien–Stanojkovski, *Geometric invariants for p-groups of class 2 and exponent p*, https://arxiv.org/abs/2411.19555 , Section 2.1 and Theorem 2.3; the relevant complete sections were read. Published version: Journal of Algebra 703 (1 October 2026),266–278, DOI https://doi.org/10.1016/j.jalgebra.2025.08.029 . That work treats group invariants; the graded-algebra bridge needed here is justified separately in Section 4. No downloaded code was run, and no historical novelty is asserted for the explicit pair or method.

The supplementary exact checker verifies both determinant identities, all projective pencil ranks over F_3 and F_9, all 6560 nonzero contraction vectors for each group, the center polynomial and bounded group-law controls. The all-field/nonisomorphism conclusion follows from the symbolic rank argument, not a scan over two fields. It does not search all elements of either 3^10-dimensional group algebra.

The remaining challenge is descent: a full algebra isomorphism supplies commutator-tensor equivalence over an extension field, but recovering an F_p-equivalence is not automatic. The next turn investigates a precise connected-stabilizer condition under which descent is valid, with that condition retained as a hypothesis.

Subjective completion estimate for the original question: 2%. Author turns completed: 3/5.
