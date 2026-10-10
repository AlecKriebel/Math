# Independent audit of the global statistical embedding proof

Problem 6000001 / AMR-059-0001, queue rank 983.

Audit date: 7 October 2026 UTC.

## Verdict and exact accepted statement

**PASS for the theorem exactly stated below. No mathematical correction is required in the frozen proof.** The construction gives a finite-dimensional global proper statistical embedding, including for noncompact manifolds. The third-jet prescription is coordinate compatible, the coefficient selection is globally smooth, and the ambient Hessian is positive definite in every ambient direction on one open neighborhood of the whole image. Both induced connections have the asserted ordering.

Let M be a smooth Hausdorff second-countable n-manifold without boundary, n >= 1, with a smooth positive-definite metric g and mutually g-dual torsion-free smooth affine connections nabla and nabla-star. For

    N = binomial(2n+4,3),

there are an open U contained in R^N, a smooth Psi on U with positive-definite ordinary Hessian G, and a proper smooth embedding f:M->U such that f^*G=g and G-orthogonal tangential projection of the standard affine connection D and its G-dual D-star gives nabla and nabla-star, respectively. The two ambient connections are torsion-free and curvature-free.

Thus every statistical manifold in this smooth positive-definite sense has the asserted realization. For arbitrary smooth mutually dual pairs, torsion-freeness of both members is necessary and sufficient for realization in a torsion-free dually flat statistical ambient manifold. The necessity assertion must retain its torsion-free ambient qualification.

The audit does not establish novelty, journal acceptance, optimal dimension, completeness, a convex ambient domain, injectivity of the ambient gradient map, or finite-sample probability-model realization. Those conclusions are unnecessary for the theorem and are not silently included in this verdict.

## Frozen object and independence

The inspected proof is the 17,635-byte PROOF.md with SHA-256

    a26c1755bc6f61085db4c01b6579701ff380822f2cc58a3ffbfb4acfa49370a2

The externally identified original manifest has SHA-256

    7df56d745e4c57a30d0303388b1adda3e52d1c99190d2f96fe50b6d616b1cf3f

Both identities were independently recomputed, and every file in that manifest was checked against its actual byte count and digest. The frozen proof and its packet were not modified. No other mathematical review, inherited verification results, or candidate verification script was read or used. The accompanying algebraic controls were written independently and do not import or execute the candidate's verification program. Standard differential-topological existence results are declared dependencies rather than claimed consequences of those controls.

## The historical question and its scope

The full three-page 1998 FMU source was visually inspected. Item 1(a), printed p.125, asks for realization preserving the dual structure in a higher-dimensional dually flat manifold. It defines the target through its affine connections. It does not impose completeness, a convex domain, globally one-to-one dual coordinates, fixed codimension, or a probability-simplex target. Its footnote separately credits Abe with affine-space realization of statistical manifolds. [FMU]

There is especially useful clarification in the original question's own reference [3], Amari's 1997 article. Printed p.84 defines dual flatness using vanishing torsion and curvature, then introduces local affine coordinates. The potential statement on p.85 is local. Page 87 presents compatible statistical embedding as item 1 and affine realization separately as item 2. Its probability-theoretic motivation does not add an exponential-family requirement to the geometric question. These directly inspected passages support the interpretation used in the frozen theorem. [A97]

An affine immersion into affine space, by itself, does not supply the positive ambient metric and both orthogonally induced connections demanded here. Indeed, an immersion into Euclidean space equipped with its standard metric and standard connection always induces the Levi-Civita connection; it cannot realize a prescribed nonzero statistical cubic tensor. The positive Hessian construction is therefore a substantive additional step.

There is a genuine terminology hazard if “flat” is redefined to mean only zero curvature while allowing torsion. For example, on R^2 with g=dx^2+exp(2x)dy^2, the standard connection D is curvature-free and torsion-free. Its g-dual has the sole nonzero coefficient (Gamma-star)^y_xy=2. It too has zero curvature, but its torsion on (partial_x,partial_y) is 2 partial_y. Extending this example by a Euclidean line gives a higher-dimensional curvature-flat dual ambient realization with nonzero induced torsion. Consequently, the necessity claim would fail in that broader category. The frozen statement correctly restricts necessity to torsion-free statistical targets, and Amari's primary definition supports that restriction.

## Reconstruction of the proof

### 1 The statistical tensor and the prescribed third derivative

Let L denote the Levi-Civita connection and write A=nabla-L. The torsion-free condition makes A symmetric in its two vector arguments. Duality gives

    g((nabla-star-L)_X Z,Y) = -g(A_X Y,Z).

Since nabla-star is also torsion-free, g(A_X Y,Z) is symmetric under interchange of X and Z. Together with symmetry under interchange of X and Y, this makes it totally symmetric. Therefore

    C(X,Y,Z) = (nabla_X g)(Y,Z) = -2g(A_X Y,Z),
    Gamma_ijk = L_ijk - C_ijk/2.

In arbitrary coordinates,

    Q_ijk = partial_k g_ij + Gamma_ijk
          = (partial_i g_jk + partial_j g_ik + partial_k g_ij - C_ijk)/2.

This is symmetric in its three indices. It is not a tensor: its inhomogeneous coordinate terms are exactly those required of a scalar third jet with zero first derivative and second derivative g. Confusing Q with C or with a covariant third derivative would be a fatal error; the frozen proof does not do so.

At each p, use the local inverse of exp_p for L and prescribe

    q_p(exp_p v) = g_p(v,v)/2 - C_p(v,v,v)/12

only as a germ at p. The ordinary third derivative in L-normal coordinates is -C/2, because the third derivative of a homogeneous cubic evaluates with factor 6. At a critical point of a scalar,

    (L^3 q)_ijk = partial_i partial_j partial_k q
                 - L_ij^a q_ak - L_ik^a q_aj - L_jk^a q_ai.

With q_ij=g_ij, the three correction terms sum to one half of the three displayed first derivatives of g. This yields precisely Q. Equivalently, Taylor expansion of the inverse exponential map contributes the same three Christoffel terms. Thus the scalar jet prescription is coordinate compatible, with the sign and factor in the cubic term correct.

The exponential map is smooth on an open neighborhood of the zero section of TM even without geodesic completeness. Near each base point, its parameter-dependent local inverse gives a smooth representative of the prescribed germ. These local representatives define one smooth jet section. No global injectivity radius or single globally defined q is required.

The section is generally nonholonomic, meaning it need not equal the jet of one scalar function on M. This causes no integrability obstruction: it is lifted to variable coefficients in a fixed global function space, and derivatives of those coefficients supply the required metric and connection identities later.

### 2 A proper embedding and one finite global jet-spanning family

The proper smooth Whitney theorem gives e:M->R^(2n+1). Compose e with the map consisting of every ambient monomial of total degree at most three, including the constant. There are binomial(2n+4,3) such monomials.

The coordinate functions of degree one recover e by linear projection. Hence the resulting f is injective, immersive, and a topological embedding. If B is compact in R^N, f^{-1}(B) is closed in e^{-1}(pi(B)); the latter is compact by properness of e. Thus f is proper and f(M) is closed in R^N.

At a fixed p, the differential of e is injective, so n linear forms on R^(2n+1) restrict to local coordinates y on M near p. Every scalar third jet at p is represented by a polynomial of degree at most three in y-y(p). Substituting the selected ambient linear forms makes this an ambient polynomial of degree at most three. Its restriction is a linear combination of the same finite list of features.

This proves surjectivity at every p of the smooth vector-bundle map

    E: M x R^N -> J^3(M,R),
    E_p(a) = j^3_p(sum_A a_A f^A),

where a is held constant while taking that jet. The local linear forms may depend on p; they only prove rank. The actual feature family is fixed globally. No finite coordinate cover, compactness, analytic structure, or approximation is hidden in this argument.

### 3 The smooth global coefficient selection

A Hausdorff second-countable smooth manifold is paracompact, so its finite-rank jet bundle admits a smooth positive-definite bundle metric. Let E-dagger be the corresponding fiber adjoint, using the ordinary Euclidean metric on the coefficient space.

For nonzero jet v,

    <E E-dagger v,v> = |E-dagger v|^2 > 0,

because surjectivity of E makes its adjoint injective. Thus E E-dagger is invertible at every point. Its inverse varies smoothly in local trivializations. Consequently

    R = E-dagger (E E-dagger)^(-1)

is a smooth global right inverse. Small singular values tending to zero at infinity merely make its norm large; they do not destroy pointwise smoothness. There is no uniform bound premise.

Lift the jet section with a=R J and set phi=-a. The defining equations become

    a.f = 0,
    a.f_i = 0,
    a.f_ij = g_ij,
    a.f_ijk = partial_k g_ij + Gamma_ijk.

The value equation can be imposed because the constant monomial is present. It is harmless and does not impose a relation between different base points.

### 4 Differentiation yields the correct exact pair

Differentiate a.f_i=0 in direction j. The result is

    f_i.(partial_j phi) = a.f_ij = g_ij.

Differentiate a.f_ij=g_ij in direction k. Substituting the prescribed third derivative gives

    f_ij.(partial_k phi) = Gamma_ijk.

Also phi.df=0 identically. Thus the scalar potential compatibility one-form has zero periods on every loop, even when M is not simply connected. Mere local closedness would not have been enough for a single global potential; the construction supplies the stronger identity actually needed.

Positive definiteness of g ensures that dphi has rank n: a vector in its kernel would pair to zero with every df(X), hence have zero g-pairing with every X. Global injectivity of phi is neither asserted nor used. Calling the construction a Lauritzen-type pair is accurate even though some formulations reserve “pair of embeddings” for a stronger global injectivity condition on each factor.

### 5 Extension from the conormal field to an ambient Hessian

Identify M with its closed embedded image S. The Euclidean tubular-neighborhood theorem supplies a diffeomorphism from an open neighborhood of the zero section in the full normal bundle NS onto an open T in R^N. Its inverse gives smooth maps r:T->S and nu:T->R^N satisfying

    z = r(z)+nu(z),     nu(z) in N_(r(z)) S.

The normal fibers may have arbitrarily small radii. The construction does not require a trivial normal bundle or one global collection of defining functions.

Since phi annihilates TS, define

    Psi_0(z) = phi_(r(z))(nu(z)).

At s in S, the derivative on tangent vectors vanishes, while on normal vectors it equals phi. Hence Psi_0|S=0 and dPsi_0|S=phi as full ambient covectors. Differentiating this ambient-covector identity along S gives

    Hess(Psi_0)(V,df(X)) = (dphi(X))(V)

for every ambient vector V. In particular, the tangent-tangent block is g.

On a fixed normal fiber through s, Psi_0(s+w)=phi_s(w), which is linear in w. Therefore the normal-normal block is zero. Relative to the Euclidean splitting TS plus NS, the Hessian along S is

    H_0 = [ A  B ; B^t  0 ],

with A positive definite. There is no assumption that the mixed block B vanishes.

Use the Euclidean metrics to define

    tau = tr(A^(-1)) ||B||_HS^2,     lambda=1+tau.

Both are smooth, globally defined scalar functions on S. The expression is invariant under changes of orthonormal local tangent and normal frames. Matrix inversion occurs only in a positive-definite block, so lambda stays smooth even when it is unbounded.

For

    Psi = Psi_0 + lambda(r(z)) |nu(z)|^2,

the correction has zero value and first derivative on S. Its Hessian there is exactly twice lambda times the normal Euclidean metric; derivatives of lambda multiply factors that vanish to second order. Thus

    Hess(Psi)|S = [ A  B ; B^t  2 lambda I ].

The eigenvalues of A^(-1) are positive, so its largest eigenvalue is at most its trace. For every normal w,

    <B^t A^(-1) B w,w> <= tau |w|^2.

The Schur complement is therefore at least (2+tau)I. It is positive definite, as is A. Equivalently, completing the square in tangent and normal components gives strict positivity of the full ambient quadratic form. This checks positive definiteness in all N dimensions, not only on TS and not in a split-signature model.

Finally set U to be the open subset of T on which the ordinary Hessian of Psi is positive definite. Since positivity holds at every point of S and is an open condition, U contains all of S. No compactness is used to turn pointwise positivity into a uniform estimate. Smoothness of Psi is already established throughout T, so restriction to this possibly thin and nonconvex U is legitimate.

The map f remains proper into U: a compact subset of U has compact image under the continuous inclusion U->R^N, and its preimage is compact by the original properness. No boundary accumulation issue has been ignored.

### 6 The two ambient connections and their projections

On U, D is the standard torsion-free flat connection and G_AB=partial_A partial_B Psi. The G-dual connection is smooth and has coefficients

    (Gamma-star)^C_AB = G^(CD) partial_A G_BD.

Symmetry of third derivatives of Psi makes these coefficients symmetric in A and B, so D-star is torsion-free.

Define eta_E=partial_E Psi. Its differential matrix is G, which is invertible. The inverse function theorem gives local coordinate charts eta, and

    partial_A partial_B eta_E
       - (Gamma-star)^C_AB partial_C eta_E = 0.

Thus eta consists of local affine coordinates for D-star, proving zero curvature. This is a local tensorial conclusion valid everywhere on one global U. A globally one-to-one eta is unnecessary. The existence of globally defined eta functions does not by itself imply their injectivity.

The normal correction leaves dPsi|S=phi unchanged, so

    G_AB f_k^B = partial_k phi_A.

It follows that f^*G=g. Moreover,

    G(f_ij,f_k) = f_ij^A partial_k phi_A = Gamma_ijk.

The G-orthogonal tangential projection of D therefore induces precisely nabla. Restricting ambient duality to tangent fields shows that the projected D-star is the g-dual of nabla. Uniqueness of the dual connection makes it exactly nabla-star. This verifies both connections, not only the metric or an unordered dual pair.

For necessity, projection of the ambient torsion equation along an immersion gives the induced torsion. If the ambient connection is torsion-free, its projected torsion is zero. Applying this separately to D and D-star proves the stated necessity for statistical ambient targets.

## Adversarial checks on the global argument

- **Noncompactness:** none of the lift, tubular radius, lambda, or smallest eigenvalue is required to have a uniform bound. The final U is defined by the actual positivity locus.
- **Topology:** the pair satisfies phi.df=0, so potential periods vanish without H^1(M)=0. Nontrivial normal bundles are handled with the full Euclidean normal bundle.
- **Completeness:** the exponential map is used only for germs at its zero section. The ambient manifold is allowed to be incomplete.
- **Embedding:** injection and topology come from the retained degree-one coordinates. Rank of dphi or positivity alone is not being mistaken for global embedding.
- **Finite dimension:** a fixed finite polynomial space supplies all jets on all charts. A locally finite construction with an unbounded number of coordinates is not being relabeled finite dimensional.
- **Potential value:** Psi is constant on S, but its full ambient derivative is generally nonzero. A constant restriction does not imply a vanishing ambient Hessian on tangent vectors, because the second fundamental term enters the second derivative of Psi composed with f.
- **Target strength:** a custom positive Hessian metric is materially more flexible than a fixed Euclidean, linear-statistical, or simplex target. The proof does not substitute one for another.
- **Disconnected manifolds:** second countability permits only countably many components. Proper embedding and all bundle constructions remain applicable. No connectedness assumption enters the proof.
- **Dimension zero:** a countable discrete manifold properly embeds as a discrete subset of R and has no nonzero tangent data. The separately stated one-dimensional ambient realization is valid.

## Independent exact controls

The accompanying independent_controls.py and INDEPENDENT_CONTROLS.json contain six passing groups, with 63 asserted algebraic or integrity conditions:

1. A direct cubic feature lift on the line verifies all pair equations for unspecified smooth g(t) and C(t), including the ordering of the dual connection. The 3-jet matrix has determinant 12. Removing the cubic feature drops its rank and supplies a negative control.
2. A nonconstant positive-definite two-dimensional metric and cubic tensor are transformed under x=u+v^2, y=v+u^2. All eight Q entries obey the full scalar-jet chain rule. A nonzero inhomogeneous term rejects a tensor-only treatment of Q.
3. Fifty-six ambient polynomial features of a nonlinear immersion into R^5 produce a rank-ten scalar 3-jet matrix, and its exact Gram right inverse is verified.
4. Exact rational matrix controls verify the Schur estimate and full Hessian positivity. With A(t)=1/(1+t^2), B(t)=t, the variable normal coefficient has determinant t^2+2/(1+t^2)>0, while a fixed coefficient already fails at t=2.
5. A nonconstant positive Hessian potential has a flat torsion-free dual connection by direct symbolic curvature and torsion calculation. The curvature-flat but torsionful example above verifies the scope warning independently.
6. The original proof, manifest, and all original manifest entries match their frozen hashes and byte counts.

These controls are supplemental. Finite computations cannot prove global existence on arbitrary manifolds, and no such inference is made. Those arguments are justified in the reconstruction above.

## Literature boundaries and dependencies

Marugame's definitions use a Riemannian metric and torsion-free statistical connection, and define statistical submanifolds by metric restriction and orthogonal connection projection. Theorem 2.2 establishes a local equivalence with Lauritzen pairs. It supplies useful context, but the candidate does not rely on it to globalize the pair or the potential. [M]

Lê's arXiv version 6, dated 10 March 2016, explicitly places compactness in Theorems 5.1 and 5.6; the version history flags the added compactness. Those results concern a finite linear statistical model and a finite probability simplex. The older Journal of Geometry publisher abstract states a broader finite-set assertion. The full journal text was not obtained in this audit, and the abstract is not treated as proof of the noncompact case. The candidate's custom Hessian target neither removes the corrected hypotheses nor establishes a finite-sample theorem. [L, LJ]

The external differential-topological inputs are proper smooth Whitney embedding, smooth bundle metrics, and the smooth Euclidean tubular-neighborhood theorem. Whitney's printed Theorem 1, p.654, explicitly covers infinite differentiability and points to the properness footnote 32; Lemma 19 and that footnote appear on p.665. These inputs apply to the stated manifold class. [W]

No mandatory correction was found. Two optional citation improvements would make the scope and dependency trail easier to check: add Amari 1997 pp.84-87 to the historical interpretation paragraph, and cite Whitney Theorem 1/p.654 together with Lemma 19/p.665 and footnote 32. These are documentary improvements, not repairs to the mathematical construction.

## References

[FMU] H. Furuhata, H. Matsuzoe, H. Urakawa, Open Problems in Affine Differential Geometry and Related Topics, Interdisciplinary Information Sciences 4(2) (1998), 125-127, item 1(a). https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en

[A97] S.-I. Amari, Information Geometry, Contemporary Mathematics 203 (1997), 81-95, especially pp.84-87. https://bsi-ni.brain.riken.jp/database/file/166/169.pdf

[M] T. Marugame, The Bonnet theorem for statistical manifolds, arXiv:2103.10102v1 (18 March 2021), Sections 2.1-2.4 and Theorem 2.2. https://arxiv.org/abs/2103.10102

[L] H. V. Lê, Monotone invariants and embeddings of statistical manifolds, arXiv:math/0506163v6 (10 March 2016), Theorems 5.1 and 5.6. https://arxiv.org/abs/math/0506163v6

[LJ] H. V. Lê, Statistical manifolds are statistical models, Journal of Geometry 84 (2006), 83-93; publisher abstract and bibliographic metadata only. https://link.springer.com/article/10.1007/s00022-005-0030-0

[W] H. Whitney, Differentiable Manifolds, Annals of Mathematics 37(3) (1936), 645-680; Theorem 1 p.654, Lemma 19 and footnote 32 p.665. https://doi.org/10.2307/1968482
