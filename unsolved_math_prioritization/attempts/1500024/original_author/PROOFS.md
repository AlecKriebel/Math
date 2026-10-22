# Exact scope, credited progress, and five bounded deductions

## 1. Target and notation

Work over **C**, with characteristic zero, and standard grading. Write E_n = Λ(C^n) and S_n = C[x_1,...,x_n]. The target is Conjecture 4.3 in [FLOS18]. Its exterior generators f,g have degree two; its polynomial generators consist of the n coordinate squares and squares of two general linear forms. “Generic” means that coefficients can be chosen mutually algebraically independent over Q; for the finite-dimensional graded quotients here, the same Hilbert function holds on a nonempty Zariski-open set of coefficients.

For s ≥ 0, let a(n,s) count walks of length n+2 from 0 to w=n+2−2s, with increments ±1, staying in the integer interval [0,w]. Set the count to zero when w≤0 and n+2>0. Equivalently these are the rectangle paths in the problem statement. The conjecture asks that both quotient Hilbert functions equal a(n,s). For s=0 the count is one. No positive-characteristic assertion is made.

References used below are identified by public URLs in `SOURCES.json`.

### Credited literature facts

[CLN18], Theorems 1, 3 and 5 and Propositions 4, 6 and 7, supplies the pencil normal forms, the exterior upper bound h(n,s)≤a(n,s), the equivalence between the commutative formula for all n and the exterior formula for all even n, and sharp low/top coefficients. Its odd cases through n=19 are reported as Macaulay2 computations, not independently replayed here. The sharp low range is s≤floor(n/3)+1; the odd top coefficient is h(2k+1,k+1)=1, with higher coefficients zero.

[BL26], Theorem 5.5, proves the commutative formula in characteristic zero. Consequently the even exterior case is covered by prior work. Its displayed Conjectures 5.1–5.2 use floor(n/2), but Theorem 5.5 uses ceil(n/2). The former truncation is incorrect in odd dimension. The elementary n=3 and n=5 computations below verify this distinction without relying on typography or numerical experiments.

These are attributed uses of the cited results. This report does not independently reprove the fat-point interpolation theorem underlying [BL26]. Nor does finding no newer odd-case solution establish an exhaustive negative literature theorem.

## 2. Approach 1: applying the current literature with exact scope

[BL26] uses the quotient by the squares of n+2 general linear forms L_1,...,L_(n+2). To apply its Theorem 5.5 to the target polynomial quotient, the first n forms must be independent. This is a nonempty Zariski-open condition: their coefficient determinant is not the zero polynomial. Use y_i=L_i as coordinates for i≤n. The last two forms then become general linear forms in y_1,...,y_n, and the ideal becomes

    (y_1²,...,y_n², ℓ_1², ℓ_2²).

Conversely, the target normal form is obtained by precisely this coordinate change. No extra generic quadratic relation is substituted for a square, and no characteristic assumption is dropped. Thus the commutative theorem is applicable to the target's polynomial side.

Applying [CLN18, Theorem 1] to this all-n commutative result gives the exterior formula for all even n. This implication is a credited theorem input, not a newly authored proof of that theorem. Its conclusion only covers even n. Neither a specialization nor an additional-variable argument extending it to odd n is part of the cited implication.

The next three approaches test concrete ways of closing that parity gap. They provide complete elementary reductions, but not the missing general odd-case rank calculation.

## 3. Approach 2: the odd pencil is a sign-free path model

For n=2k+1 the generic normal form from [CLN18] can, after swapping or scaling generators, be written

    f = Σ_(i=1)^k a_i b_i,       g = Σ_(i=1)^k a_i b_(i+1).

Regard these as alternating bilinear forms on the dual space. The first radical is the line dual to b_(k+1); the second is the line dual to b_1. Their intersection is zero for k≥1. In contrast, any simultaneous decomposition into k paired blocks with one unused variable has a common radical containing the unused coordinate. Congruence and invertible recombination of f,g preserve the common radical. Thus an odd generic pencil cannot be obtained by merely appending an unused coordinate to the paired even model.

There is nevertheless an exact simpler model. Order the variables along the chain

    z_1=b_1, z_2=a_1, z_3=b_2, ..., z_(2k)=a_k, z_(2k+1)=b_(k+1).

Replacing f by −f gives generators

    F = z_1 z_2 + z_3 z_4 + ... + z_(2k−1) z_(2k),
    G = z_2 z_3 + z_4 z_5 + ... + z_(2k) z_(2k+1).

Let B_n=C[x_1,...,x_n]/(x_1²,...,x_n²), and let F_c,G_c denote the same adjacent-edge sums in B_n.

**Proposition 3.1.** For every degree s, the monomial identification z_J↦x_J induces a vector-space isomorphism

    (E_n/(F,G))_s  ≅  (B_n/(F_c,G_c))_s.                   (3.1)

**Proof.** A product z_j z_(j+1) z_J is zero if J meets {j,j+1}. Otherwise the two adjacent generators pass precisely twice the number of elements of J below j when the product is sorted. The sign is therefore +1. Consequently monomial identification intertwines multiplication by every adjacent pair, and in particular by F and G. The degree-s ideal is the sum of the images of those two multiplication maps from degree s−2. Taking cokernels proves (3.1). This holds in every degree and requires no matrix-rank computation. ∎

The map in (3.1) is a graded vector-space identification of the quotients; it is **not** asserted to be an algebra isomorphism. Anticommuting degree-one generators have not become commuting generators by an algebra homomorphism. Also, F_c and G_c are sparse sums of adjacent products, not squares of general linear forms. Identifying their Hilbert function with that of the latter quotient remains a genuine problem.

## 4. Approach 3: hyperplane reduction isolates missing homology

Let A=E_(n+1)/(F,G), where F,G are generic quadrics, and let ℓ be a general nonzero linear form. Then

    A/(ℓ) ≅ E_n/(f,g)                                      (4.1)

with f,g generic. Indeed, for a fixed nonzero ℓ, the restriction map on pairs of quadrics is surjective. The preimage of the generic locus in n variables is a nonempty open set and meets the generic locus in n+1 variables. A change of basis handles varying ℓ.

Write b_s=dim A_s, q_s=dim(A/(ℓ))_s, and r_s=rank(ℓ:A_s→A_(s+1)). Since ℓ²=0, multiplication by ℓ is a cochain differential. If η_s is its degree-s homology dimension, then

    q_s = b_s − r_(s−1),
    η_s = b_s − r_(s−1) − r_s
        = q_s + q_(s+1) − b_(s+1).                         (4.2)

These equalities are rank-nullity, with r_−1=0. In particular they prove η_s≥0 and give exact constraints on any proposed odd Hilbert function. Once η_s is known, q_0=1 and the recurrence

    q_(s+1) = b_(s+1) − q_s + η_s                          (4.3)

determines every coefficient. For odd n the b_s are supplied by the known even case, but η_s is not supplied by that result. Equations (4.2)–(4.3) exhibit the missing datum explicitly.

A usual commutative maximal-rank/Lefschetz shortcut is invalid here. For any nonzero ℓ∈A_1, the vector ℓ lies in the kernel of multiplication A_1→A_2. In the even generic quotient with N≥4 generators, dim A_2=binom(N,2)−2≥N=dim A_1. Maximal rank would require injectivity, which is impossible.

For N=4, choose the generic normal-form quotient A=Λ(a,b,c,d)/(ab,cd). It has Hilbert series 1+4t+4t². If ℓ=a+b+c+d, the images of a,b,c,d in the basis ac,ad,bc,bd are respectively

    −ac−ad,  −bc−bd,  ac+bc,  ad+bd.

The first three are independent, and the four sum to zero. The rank is exactly three, and A/(ℓ) has series 1+3t+t². Replacing this map by a hypothetical rank-four map would erase an actual coefficient. This is an obstruction to that shortcut, not a counterexample to the target conjecture.

## 5. Approach 4: the remaining problem is an exact syzygy count

For any pair of quadrics f,g in E_n, let K be their Koszul complex. In total degree s it is

    0 → E_(s−4) → E_(s−2) ⊕ E_(s−2) → E_s → 0,
        w ↦ (−gw,fw),                    (u,v) ↦ fu+gv.

The composition is zero because degree-two forms commute. Put h_s=dim(E_n/(f,g))_s and κ_s=dim H_1(K)_s. The perfect top-wedge pairing gives

    dim H_2(K)_s = h_(n−s+4).                              (5.1)

To verify this, H_2(K)_s consists of w∈E_(s−4) annihilated by both f and g. Under the nondegenerate pairing with E_(n−s+4), that subspace is exactly the annihilator of fE_(n−s+2)+gE_(n−s+2), whose codimension is the dimension of that ideal component. Its dimension is thus the quotient dimension in (5.1).

Euler characteristic now gives the universal exact identity

    h_s − κ_s + h_(n−s+4)
      = binom(n,s) − 2 binom(n,s−2) + binom(n,s−4).         (5.2)

Binomial coefficients outside 0,...,n and graded pieces outside the algebra's support are zero.

For the generic odd pencil n=2k+1, h_d=0 for d>k+1. Here is a proof requiring only the first quadric. On W=span(a_1,b_1,...,a_k,b_k), let L be wedge multiplication by Σ a_i b_i and let Λ be its Hermitian adjoint for the standard orthonormal exterior basis. On degree d the elementary creation/contraction relations give [Λ,L]=(k−d)·Id. Thus

    ||Lα||² = ||Λα||² + (k−d)||α||².

For d<k this makes L injective. Top-wedge duality makes L surjective onto degrees greater than k. Consequently Λ(W)/(f) has no degree above k; adjoining the remaining b_(k+1) raises the last possible degree by at most one. Further quotienting by g cannot increase it.

For s≤k+1, the reflected term in (5.2) is therefore zero. With

    P(n,s)=binom(n,s)−2 binom(n,s−2)+binom(n,s−4),

we have the exact formula

    h_s = P(2k+1,s) + κ_s.                                 (5.3)

The desired formula is equivalent to

    κ_s = a(2k+1,s) − P(2k+1,s)       for 0≤s≤k+1.        (5.4)

This is a precise unsolved rank/syzygy condition; (5.4) is not assumed or established here. The inequality h_s≥P(2k+1,s) alone is insufficient. In the n=5 model below, (z_2,−z_4) is a degree-three syzygy because Fz_2=Gz_4=z_2z_3z_4. It cannot be a Koszul boundary, since E_(3−4)=0. Thus κ_3≥1. This directly explains why blindly treating the two quadrics as a regular sequence loses a real term.

## 6. Approach 5: straightening obstruction and exact small controls

In the path model with odd n≥5, order squarefree monomials lexicographically by z_1>z_2>...>z_n. The displayed quadrics have leading monomials z_1z_2 and z_2z_3. Consider

    R = z_1 G − z_3 F.

The common z_1z_2z_3 term cancels. The remaining leading term is z_1z_4z_5, with coefficient one. Subsequent terms involving z_1 have larger indices, and terms from z_3F not already canceled do not contain z_1. Neither quadratic leading monomial divides z_1z_4z_5. Therefore {F,G} is not a Gröbner basis for this order. The same argument works in the commutative squarefree path model by Proposition 3.1.

This proves only failure of this two-generator basis for this order. It does not exclude a larger Gröbner basis, a different order, or a successful straightening argument.

### A complete hand proof for n=5

Take F=z_1z_2+z_3z_4 and G=z_2z_3+z_4z_5. The two relations are independent in degree two, so h_2=10−2=8. The following nine distinct degree-three monomials belong to the ideal:

    134 = Fz_1,        234 = Fz_2,        123 = Fz_3,
    124 = Fz_4,        345 = Gz_3,        125 = Fz_5−Gz_3,
    145 = Gz_1−Fz_3,   245 = Gz_2,        235 = Gz_5.

Here 134 abbreviates z_1z_3z_4, and likewise for the others. These identities have the displayed signs because every quadratic term is an adjacent pair. The remaining monomial 135 cannot occur in a multiple of F or G: each term of such a product contains an adjacent edge, whereas {1,3,5} does not. Thus h_3=1. Every degree-four monomial contains a degree-three subset other than {1,3,5}, so h_d=0 for d≥4. The exact Hilbert series is

    1 + 5t + 8t² + t³.                                    (6.1)

The monomial quotient defined only by the two leading quadrics instead has Hilbert series

    (1+3t+t²)(1+t)² = 1+5t+8t²+5t³+t⁴.

It would therefore overcount four degree-three classes and one degree-four class.

For n=3 the path model is simply (z_1z_2,z_2z_3), giving 1+3t+t². In both odd examples the coefficient in degree ceil(n/2) is one, contradicting a floor(n/2) truncation but agreeing with the original conjecture. More generally, for n=2k+1 the monomial b_1...b_(k+1) survives: every term of (f,g) has positive degree in the a variables. Combined with the cited upper bound h≤a and the unique width-one path, this also recovers the known top coefficient one.

## 7. Exact endpoint

The original all-n conjecture remains unresolved by this package. Even n and the commutative side are credited prior results. The odd path model, hyperplane homology formula, Koszul identity, and explicit straightening obstruction are complete bounded deductions. They do not supply the missing ranks.

After the cited low-degree and top-degree results, the potentially undetermined odd coefficients lie in

    floor((2k+1)/3)+2 ≤ s ≤ k.

The cited finite computations cover odd n≤19, but this report does not certify their computation. The first dimension beyond that cited finite range is n=21, where the remaining degrees are 9 and 10. Settling (5.4) in those degrees or in general requires additional mathematics; no unsupported lower-bound equality or basis-independence assertion is made.
