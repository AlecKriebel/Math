# A finite-dimensional Hessian realization of a smooth statistical manifold

Problem 6000001 / AMR-059-0001, queue rank 983.

**Manuscript status:** authored proof candidate, frozen for independent mathematical review. No novelty claim, journal acceptance claim, or assertion that the independent review has passed is made here.

## 1. Statement, interpretation, and scope

Let M be a smooth, Hausdorff, second-countable manifold without boundary, of finite dimension n >= 1. Let g be a smooth positive-definite metric, and let nabla and nabla-star be smooth affine connections dual with respect to g:

    X g(Y,Z) = g(nabla_X Y,Z) + g(Y,nabla-star_X Z).

The 1998 question [FMU, item 1(a), printed p. 125] defines a dually flat space by flatness of its two affine connections. It asks for realization as a higher-dimensional submanifold with the induced dual structure. It does not require a complete ambient metric, a convex ambient domain, globally injective dual coordinates, a probability simplex, or a prescribed codimension. These additional requirements are not imposed below.

**Theorem.** If both connections are torsion-free, there exist

* N = binomial(2n+4,3),
* an open set U in R^N,
* a smooth function Psi: U -> R whose ordinary Hessian G is positive definite everywhere on U, and
* a proper smooth embedding f: M -> U

such that f pulls back G to g and the G-orthogonal tangential projections of the standard flat connection D and its G-dual D-star are nabla and nabla-star, respectively. Both D and D-star are torsion-free and flat.

Consequently, under the usual smooth positive-definite definition of a statistical manifold, finite-dimensional realization in the sense stated in [FMU] needs no additional invariant. Among smooth mutually dual connection pairs not assumed torsion-free, torsion-freeness of both connections is necessary and sufficient for realization in a torsion-free dually flat statistical manifold.

The target U is allowed to depend on (M,g,nabla). It can be nonconvex and need not be complete. The assertion concerns a global embedding of all of M into a finite-dimensional target, not merely a germ at each point. Its global dual connection is flat, but the map x -> dPsi(x) need not be globally injective. No assertion is made for indefinite metrics, nonsmooth metrics, manifolds with boundary, or a dimension-minimizing target.

## 2. Definitions and the connection tensor

Write L for the Levi-Civita connection of g and put

    C(X,Y,Z) = (nabla_X g)(Y,Z).

Duality and torsion-freeness of both connections imply that C is totally symmetric. Moreover,

    g(nabla_X Y,Z) = g(L_X Y,Z) - C(X,Y,Z)/2,          (2.1)
    g(nabla-star_X Y,Z) = g(L_X Y,Z) + C(X,Y,Z)/2.

For completeness, A = nabla-L is symmetric in X,Y because both connections are torsion-free. Duality expresses nabla-star-L as the negative g-adjoint of A in its last slot. Torsion-freeness of nabla-star then makes g(A_X Y,Z) symmetric in all three entries. Therefore C(X,Y,Z) = -2g(A_X Y,Z), proving (2.1).

In a coordinate chart x^1,...,x^n set

    Gamma_ijk = g(nabla_{partial_i} partial_j,partial_k).

Then

    Q_ijk = partial_k g_ij + Gamma_ijk                 (2.2)

is symmetric in i,j,k. Indeed, with L_ijk denoting the lowered Levi-Civita coefficients,

    Q_ijk = (partial_i g_jk + partial_j g_ik
             + partial_k g_ij - C_ijk)/2.              (2.3)

Q is not being asserted to be a tensor by itself; it will be the third ordinary derivative of a scalar jet whose second derivative is g and whose first derivative vanishes.

## 3. Polynomial features span all scalar 3-jets

Use the proper smooth Whitney embedding theorem to choose

    e: M -> R^K,                 K = 2n+1.

Only this standard differential-topology theorem and the tubular-neighborhood theorem are external existence inputs to the proof. Whitney [W, printed p.665, Lemma 19 and footnote 32] gives the embedding and its proper version. Their roles are stated explicitly in Section 9.

Let P_3(R^K) be the vector space of real polynomials of total degree at most three. Choose the monomial basis p_1,...,p_N, including the constant monomial, where

    N = dim P_3(R^K) = binomial(K+3,3).

Define the feature map

    f(p) = (p_1(e(p)),...,p_N(e(p))).                  (3.1)

Because degree-one monomials are included, projection onto those coordinates recovers e. Thus f is an injective immersion and is a topological embedding. It is proper: for a compact B in R^N, f^{-1}(B) is a closed subset of the compact set e^{-1}(pi(B)), where pi is the degree-one-coordinate projection. Its image S=f(M) is therefore a closed embedded submanifold of R^N.

Let J^3(M,R) be the vector bundle of scalar 3-jets. Define a smooth bundle map

    E_p: R^N -> J^3_p(M,R),
    E_p(c) = j^3_p(sum_A c_A f^A).                   (3.2)

Every E_p is surjective. To see this, choose n linear functions on R^K whose differentials, after restriction by e, are linearly independent at p. These restricted functions give local coordinates y near p. Any scalar 3-jet is represented in those coordinates by a polynomial of degree at most three in y-y(p). That polynomial is the restriction of an element of P_3(R^K), since the chosen y are linear functions of the ambient coordinates. Thus it lies in the range of (3.2).

This argument is pointwise and uses the same finite global polynomial space at every p. It does not invoke a finite chart cover, a boundedness condition, a convergent infinite sum, or compactness of M.

Choose any smooth positive-definite bundle metric on J^3(M,R) and the standard Euclidean metric on M x R^N. If E^dagger denotes the fiberwise adjoint, then

    R_p = E_p^dagger (E_p E_p^dagger)^{-1}             (3.3)

is a smooth global right inverse. Surjectivity makes E_p E_p^dagger positive definite on the jet fiber; matrix inversion is smooth on invertible matrices. No uniform lower singular-value bound is needed. Formula (3.3) gives a smooth bundle map even when its norm is unbounded on a noncompact M.

## 4. A globally compatible prescribed jet

We now specify a smooth section J of J^3(M,R). At p, use the Riemannian exponential map of L merely as a local coordinate construction near the zero vector of T_pM. Require that J_p be the jet at v=0 of

    q_p(exp_p v) = g_p(v,v)/2 - C_p(v,v,v)/12.        (4.1)

This specifies a coordinate-independent smooth jet section: changing the basis of T_pM acts linearly on v and leaves the displayed contractions invariant, and the local exponential map depends smoothly on p and v. Completeness of g is unnecessary because only a germ at zero is used.

In arbitrary coordinates, the jet has

    q_p(p) = 0,
    (partial_i q_p)(p) = 0,
    (partial_i partial_j q_p)(p) = g_ij(p),
    (partial_i partial_j partial_k q_p)(p) = Q_ijk(p). (4.2)

To verify the last line, in L-normal coordinates the third derivative in (4.1) is -C_ijk/2. For a scalar with vanishing first derivative and Hessian g at p, conversion from its L-covariant third derivative to ordinary third derivatives adds

    L_ij^a g_ak + L_ik^a g_aj + L_jk^a g_ai.

The sum equals (partial_i g_jk + partial_j g_ik + partial_k g_ij)/2. Combining this with -C_ijk/2 gives exactly (2.3). This also verifies the coordinate compatibility of the prescribed jet directly.

Apply the global right inverse and define

    a(p) = R_p J_p,              phi(p) = -a(p).      (4.3)

Treat phi(p) as a covector in (R^N)^*. From (3.2) and (4.2), with a held constant when evaluating the x-derivatives of the scalar jet, we obtain

    a_A f^A = 0,
    a_A f_i^A = 0,
    a_A f_ij^A = g_ij,
    a_A f_ijk^A = partial_k g_ij + Gamma_ijk.          (4.4)

All a and f in these identities are evaluated at the same point of M. Subscripts on f denote ordinary coordinate derivatives; repeated A is summed.

## 5. The metric and the connection are both encoded

Differentiate the second line of (4.4):

    (partial_j a_A) f_i^A + a_A f_ij^A = 0.

Using phi=-a and the third line gives

    f_i^A partial_j phi_A = g_ij.                    (5.1)

Differentiate the third line of (4.4):

    (partial_k a_A) f_ij^A + a_A f_ijk^A
      = partial_k g_ij.

The fourth line yields

    f_ij^A partial_k phi_A = Gamma_ijk.              (5.2)

Finally,

    phi_A df^A = 0                                  (5.3)

by the second line of (4.4). This is stronger than closedness: the potential-compatibility one-form is identically zero and hence has no period obstruction. Positive definiteness in (5.1) also implies that dphi has rank n, but global injectivity of phi is not needed anywhere.

These identities are often formulated as a Lauritzen-type pair. Here they have been constructed globally from finite jets; they are not assumed from a local embedding theorem.

## 6. Global Hessian extension with pointwise positivity

Identify M with the closed embedded submanifold S=f(M). Let T be a tubular neighborhood of S in R^N with smooth Euclidean normal projection r:T->S. Write

    z = r(z) + nu(z),       nu(z) in (T_{r(z)}S)^perp.

The tubular radius may vary with the base point. A uniform radius is not required.

The covector field phi along S annihilates TS by (5.3). Define on T

    Psi_0(z) = phi_{r(z)}(nu(z)).                    (6.1)

It is smooth and satisfies

    Psi_0|S = 0,             dPsi_0|S = phi.          (6.2)

Indeed, along S the tangential derivative is zero, while on a normal fiber the function is linear with derivative phi. Let H_0 be its ordinary Euclidean Hessian. Differentiating dPsi_0(f(p))=phi(p) in a tangent direction shows

    H_0(f_i,f_j) = f_i^A partial_j phi_A = g_ij.      (6.3)

On two normal vectors based at the same point, H_0 is zero, since (6.1) is linear on that normal fiber. Relative to the Euclidean orthogonal decomposition TS plus NS, its block form along S is therefore

    H_0 = [ A  B ; B^t  0 ],                        (6.4)

where A is positive definite. Regard A as a positive self-adjoint endomorphism of TS using its Euclidean metric. Let

    t = tr(A^{-1}) * ||B||_HS^2,
    lambda = 1 + t.                                 (6.5)

These are smooth scalar functions on S, independent of the choice of orthonormal tangent and normal frames. In particular, no global frame of the normal bundle is required. The trace and Hilbert-Schmidt norm in (6.5) are finite at each point; they need not be bounded globally.

Set

    Psi(z) = Psi_0(z) + lambda(r(z)) |nu(z)|^2.       (6.6)

The added term has zero value and first derivative along S, and its Hessian there is twice lambda times the Euclidean normal metric. Thus

    Hess(Psi)|S = [ A  B ; B^t  2 lambda I ].         (6.7)

For every normal vector w,

    w^t B^t A^{-1} B w
      <= ||A^{-1}||_op ||B||_HS^2 |w|^2
      <= t |w|^2.

Consequently the Schur complement is bounded below, pointwise, by

    2 lambda I - B^t A^{-1} B >= (2+t) I > 0.

Together with A>0, this proves positivity of (6.7). Now take

    U = { z in T : Hess(Psi)_z is positive definite }. (6.8)

Positive definiteness is an open condition. Therefore U is an open neighborhood of all of S. This definition, rather than an asserted uniform neighborhood or uniform lower Hessian bound, is what handles the noncompact case. Restrict Psi to U and put G=Hess(Psi). The original f remains a proper embedding into U, since every compact subset of U is also compact in R^N.

## 7. Flatness and the induced dual pair

Let D be the standard coordinate connection on U. It is torsion-free and flat. Since G_AB=partial_A partial_B Psi, the tensor DG is totally symmetric, so its dual D-star is torsion-free. In these global x-coordinates its coefficients are

    (Gamma-star)^C_AB = G^{CD} partial_A G_BD.

This connection is flat: locally the functions eta_A=partial_A Psi are coordinates, since their Jacobian is G and G is invertible. Moreover,

    partial_A partial_B eta_E
      - (Gamma-star)^C_AB partial_C eta_E = 0,

so the eta_A have zero covariant Hessian for D-star and are local affine coordinates. Flatness is a local tensorial property; global injectivity of eta is unnecessary.

Along f(M), (6.2) is unchanged by the correction in (6.6), so

    G_AB(f(p)) f_k^B = partial_k phi_A.              (7.1)

Equations (5.1) and (7.1) imply f^*G=g. If nabla-induced is the G-orthogonal tangential projection of D, then

    g(nabla-induced_{partial_i} partial_j,partial_k)
      = G_AB f_ij^A f_k^B
      = f_ij^A partial_k phi_A
      = Gamma_ijk,                                  (7.2)

by (5.2). Since g is nondegenerate, nabla-induced=nabla.

Let nabla-induced-star similarly be the tangential projection of D-star. Restricting the duality identity for D,D-star gives

    X g(Y,Z) = g(nabla_X Y,Z)
               + g(Y,nabla-induced-star_X Z).

The g-dual of nabla is unique, so nabla-induced-star=nabla-star. Thus both connections, with their specified ordering, are induced correctly. This proves the theorem.

For necessity of the torsion condition, the tangential projection of a torsion-free ambient connection along an immersion is torsion-free: the projected difference D_XY-D_YX equals the tangent bracket [X,Y]. Apply this separately to D and D-star.

## 8. Scope checks and non-consequences

1. **Global versus local.** One proper f and one open U contain the image of all of M. The only locality is that a nonconvex Hessian domain's dual affine coordinates may require multiple charts.
2. **Embedding versus immersion.** Injectivity, topology, and properness come from the degree-one coordinates recovering e. They are not inferred from metric positivity alone.
3. **Positive versus split signature.** The full N-dimensional Hessian is positive definite on U by the Schur-complement estimate. A split-signature pairing on R^N x (R^N)^* is not used as the final ambient metric.
4. **Noncompact M.** There is no uniform estimate for the jet right inverse, normal radius, or Hessian lower bound. Only smoothness and pointwise invertibility/positivity are used, with the open set selected in (6.8).
5. **Ambient dimension.** The count is for all monomials of degree at most three in K=2n+1 variables, including the constant. N>n. No optimized bound is claimed.
6. **Riemannian flatness.** Flatness here refers to D and D-star. The Levi-Civita curvature of G need not vanish.
7. **Probability models.** A finite Hessian target with custom potential is not automatically a finite probability simplex. The theorem does not strengthen the compactness hypotheses in corrected finite-sample statistical-model theorems.
8. **Convexity and completeness.** Neither a globally convex target domain nor complete affine or metric geometry is established. Imposing one of these is a different problem.
9. **Zero-dimensional case.** A second-countable zero-dimensional manifold is countable and discrete. It properly embeds in R, and both its metric and connections have no nonzero tangent data. Thus it has a trivial one-dimensional realization separately.

## 9. Dependencies and credited literature

The proof above depends on the proper smooth Whitney embedding theorem, existence of smooth bundle metrics, the smooth tubular-neighborhood theorem for a closed embedded submanifold of Euclidean space, and elementary linear algebra/calculus. These are standard differential-topological inputs, not assertions proved by the symbolic verification script. The jet-surjectivity, jet compatibility, global right inverse, Hessian construction, and induced-connection computations are proved above.

The earlier local realization result and statistical submanifold definitions are credited to the literature. Marugame [M, Introduction and Sections 2.1-2.4] explicitly credits Lê for unrestricted local embedding and proves a local Lauritzen-pair/Hessian equivalence. The present argument supplies a particular global exact pair and a nonuniform global tubular extension; it does not attribute that additional construction to Marugame.

Lê's corrected arXiv version [L, v6, Theorems 5.1 and 5.6] gives compact smooth statistical embeddings into a finite-dimensional linear statistical model and into a finite probability simplex. Its revision history expressly adds compactness. The older Journal of Geometry abstract [LJ] asserts an unrestricted finite-set result; that abstract is not used as a proof of the noncompact case here. This distinction prevents an unjustified literature-only closure.

No claim is made that the authored proof is historically new. Its purpose is a complete checkable argument for the exact flat-connection interpretation of the original question.

### References

[FMU] H. Furuhata, H. Matsuzoe, H. Urakawa, *Open Problems in Affine Differential Geometry and Related Topics*, Interdisciplinary Information Sciences 4(2) (1998), 125-127, item 1(a), p.125. https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en

[M] T. Marugame, *The Bonnet theorem for statistical manifolds*, arXiv:2103.10102v1 (18 March 2021), especially Sections 2.1-2.4 and Theorem 2.2. https://arxiv.org/abs/2103.10102

[L] H. V. Lê, *Monotone invariants and embeddings of statistical manifolds*, arXiv:math/0506163v6 (10 March 2016), especially Theorems 5.1 and 5.6; original volume publication in *Advances in Deterministic and Stochastic Analysis*, World Scientific (2007), 231-254. https://arxiv.org/abs/math/0506163v6

[LJ] H. V. Lê, *Statistical manifolds are statistical models*, Journal of Geometry 84 (2006), 83-93. Publisher abstract and publication metadata. https://doi.org/10.1007/s00022-005-0030-0

[W] H. Whitney, *Differentiable Manifolds*, Annals of Mathematics 37(3) (1936), 645-680. https://doi.org/10.2307/1968482

