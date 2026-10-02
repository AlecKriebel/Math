# Author turn 4: finite projective monodromy and rationally split abelian monodromy

**Substantive turn 4/5.** This turn combines a determinant-root construction, normalization at a rational point, Hodge–Tate rigidity, and the preceding tensor identities. It treats smooth **proper** geometrically connected X over a finite extension K/Q_p. It does not settle arbitrary semisimple geometric monodromy.

## 1. Main restricted theorem

**Theorem.** Suppose that after a finite étale surjective cover of X the rational local system V=L[1/p] has a filtration by arithmetic-invariant local subsystems such that the geometric fundamental group acts through scalar matrices on each successive quotient. Then for every i>=2,

    ell_i(V)=0,                 W_i(V)=0.

In particular the target formula holds in these degrees. This includes:

1. every Hodge–Tate local system with finite geometric **projective** monodromy;
2. every rank-one Hodge–Tate local system;
3. systems with commuting, rationally split geometric monodromy as specified in §4.

The first case allows an infinite scalar geometric character. It is strictly a different sufficient condition from the finite geometric image in turn 1. We do not claim the scalar-filtration hypothesis for arbitrary local systems.

## 2. Scalar geometric action: an actual character can be removed

Let V have rank r and suppose its geometric image is scalar. We may pass to finite étale covers and finite extensions of the field of constants throughout: both sides descend by the injective pullbacks proved in turn 1, and properness is preserved.

First pass to a finite étale cover on which det rho_V takes values in a sufficiently small subgroup 1+p^N Z_p. Choose N so that division by r followed by the p-adic exponential converges there, including when p divides r or p=2. For example any N with N−v_p(r)>1/(p−1), enlarged to lie in the usual logarithm/exponential domains, suffices. Define the continuous Q_p-valued character

    lambda_0(g)=exp((1/r) log(det rho_V(g))).                    (1)

The determinant is multiplicative and the small-unit logarithm is additive, so (1) is a homomorphism, and lambda_0^r=det rho_V. The image is compact and has a stable Z_p lattice.

Choose a closed point and then extend the field of constants to its residue field, obtaining a rational point x. It gives a section of the arithmetic fundamental-group sequence, up to conjugacy; evaluation of a character is independent of that conjugacy. Let (lambda_0)_x be the corresponding character of G_K and set

    lambda = lambda_0 tensor f^*((lambda_0)_x^{-1}),             (2)

where f:X->Spec K is the structure morphism. The stalk lambda_x is exactly trivial.

By Petrov's Hodge–Tate rigidity theorem (arXiv:2012.13372v3, Proposition 7.2 and Corollary 7.3), lambda is Hodge–Tate. Its only weight is zero: the generalized weights are constant by Proposition 3.5(ii), and the stalk at x has weight zero. This use of rigidity is essential; a fractional determinant root would not by itself be Hodge–Tate.

Set

    W = V tensor lambda^{-1}.

Both factors are Hodge–Tate, so W is Hodge–Tate. If h is geometric and rho_V(h)=c(h) I_r, the arithmetic character in (2) is trivial on h and therefore

    (c(h)/lambda(h))^r = c(h)^r / det rho_V(h) = 1.

Thus the geometric image of W lies in the finite scalar group mu_r(Q_p). Turn 1 applies to W and gives ell_i(W)=W_i(W)=0 for i>=2.

For lambda, the higher primitive regulator classes vanish: its monodromy is abelian of Lie dimension at most one, and the alternating trace cocycle of degree >=3 restricts to zero. Also W_i(lambda)=0 for every i because its only Hodge–Tate weight is zero. On the proper base, turn 2's tensor identities applied to V=W tensor lambda now give

    ell_i(V)=ell_i(W)+r ell_i(lambda)=0,
    W_i(V)=W_i(W)+r W_i(lambda)=0.

This proves the scalar-action case. All auxiliary characters and covers exist inside the given continuous representation setup; no extraction of a global algebraic r-th root of a vector bundle is assumed.

## 3. Filtrations and finite projective image

For the theorem's filtration, each subquotient is Hodge–Tate. Apply §2 to the subquotients, choosing further finite covers as needed, and use exact-sequence additivity from turn 1. A common cover exists by taking a component of the finite fiber product and, if needed, all components to retain surjectivity. Pullback injectivity descends the conclusion.

For finite projective geometric image, let Gamma be the image of the arithmetic representation in PGL_r(Q_p), and H the finite image of the geometric subgroup. A sufficiently small open subgroup U of the compact group Gamma satisfies U intersection H={1}. The corresponding finite étale cover has trivial geometric projective image, hence scalar geometric linear image. This is exactly the case handled in §2.

The rank-one case is immediate from this argument. Alternatively, for rank one the unweighted Chern-character vanishing of turn 2 makes all positive Chern components zero, and the single weight is constant; the higher odd class is zero by the alternating-trace calculation.

## 4. A precise abelian-monodromy corollary

Assume the geometric image commutes. Let A be the finite-dimensional commutative Q_p-subalgebra of End_Qp(V) generated by that image. Suppose its semisimple quotient is split:

    A / rad(A) ~= Q_p^t.                                      (3)

No assumption about arithmetic commutativity is made. Then the theorem applies.

Indeed, A has its canonical product decomposition into local Artinian algebras A_1,...,A_t. The arithmetic group normalizes A because the geometric group is normal, and therefore permutes the finitely many central primitive idempotents. After passing to a finite-index subgroup, it preserves each component V_j=e_j V. On A_j the unique residue map A_j->Q_p is preserved by all Q_p-algebra automorphisms. Its radical J_j is nilpotent and preserved by arithmetic conjugation. The finite filtration

    V_j superset J_j V_j superset J_j^2 V_j superset ... superset 0

is therefore arithmetic-invariant. On every successive quotient, each geometric element acts by its residue scalar in A_j/J_j=Q_p. These are exactly the scalar geometric quotients required by the theorem.

Condition (3) is explicit. We have not proved the same corollary for arbitrary nonsplit coefficient fields by silently replacing a Q_p-linear characteristic class with an E-linear one. Such a coefficient-extension argument requires its own compatibility treatment. Nor does commuting geometric image follow for a general fundamental group.

## 5. Limits of the result

This turn proves the full higher-degree formula on the stated proper-base classes, but not the complete source question. In particular:

- arbitrary noncommuting semisimple geometric monodromy remains;
- properness is used in turn 2's unweighted vanishing/tensor argument;
- degree one is not addressed by these zero arguments;
- no claim is made that the ambient kernel classes in turn 3 are realized by local systems.

The determinant-root and point-normalization proof is useful precisely because it avoids assuming that every projective representation has an arbitrary prescribed Hodge–Tate lift. The constructed lambda has an actual trivial stalk, and the published rigidity theorem supplies admissibility.

**Next and final author route:** derive the exact extent of numerical detection by smooth complete-intersection restrictions from the credited top-degree theorem, and test whether that reaches the remaining de Rham class or leaves a primitive cohomology component. A sixth author search will not follow the fifth freeze.

## 6. Controls

The exact verifier checks finite truncations of the determinant-root formal identity, validates the needed p-adic convergence inequalities for a range including p|r and p=2, checks a split commuting radical-filtration example under a noncommuting arithmetic normalizer, and checks the rank/scalar tensor identities. These support the algebra. They do not replace Petrov's rigidity theorem or certify the existence of a local system for an abstract matrix example.
