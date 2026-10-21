# A closed-concordance retract at a cylindrical Lie end

## Scope and status

This is an authored partial theorem for one explicitly defined Lie structure. It is not a solution of OWR-15579-004. It separates controlled end data from compactly supported changes and supplies an actual endpoint-class law on a product-representable sector. No claim of novelty is made for the underlying conformal quotient construction.

Let Y be a closed smooth manifold of dimension d >= 2. Put X = R x Y and compactify the R factor at both ends using boundary coordinates x_+ = exp(-r), x_- = exp(r). Let A = bT(bar X). A compatible metric means a smooth positive-definite metric on A. Require its Lie scalar curvature to be strictly positive on the entire compact base bar X. Thus it has a uniform positive lower bound on X.

Define a b-PSC concordance from g_0 to g_1 to be a smooth metric G on A direct-sum T[0,1] with scalar curvature strictly positive on bar X x [0,1], equal to g_i + ds^2 in temporal collars. There is NO fixed metric requirement at the spatial infinity faces. Denote the resulting endpoint-metric concordance set by C_b(X). Let C(Y) be the ordinary PSC concordance set on Y. These definitions are explicit choices for this theorem; the OWR question did not specify them.

## 1. Translation-invariant normal metric and scalar identity

At either infinity face, the restriction of A is the central-line extension R direct-sum TY. In a boundary coordinate, a smooth b-metric restricts to the translation-invariant metric

    q = f^2 (dr + alpha)^2 + H

on R x Y, where f > 0, alpha is a one-form on Y, and H is a metric on Y. This is just the Schur-complement decomposition of a positive-definite block matrix. More generally it applies over a base B of dimension m >= 2, possibly with boundary.

Write F = d alpha. Use Delta = div grad, and define |F|_ten^2 = sum_{i,j} F(e_i,e_j)^2 in an H-orthonormal frame (twice the usual differential-form norm). The invariant-metric curvature identity is

    scal(q) = scal(H) - (f^2/4)|F|_ten^2 - 2 f^{-1} Delta_H f.       (1)

The coefficient of the F term is tied to this stated norm convention. Formula (1) follows from the scalar-curvature formula for a one-dimensional Riemannian submersion with connection alpha and variable fiber length f; it can also be computed in the coframe f(dr+alpha), e^1,...,e^m. The expression is local, so compactness of the R fiber is irrelevant. Quotienting r modulo a fixed period yields the same identity for a free isometric circle action.

Set u = log f and H_hat = f^{2/(m-1)} H. The conformal scalar formula gives

    f^{2/(m-1)} scal(H_hat)
      = scal(H) - 2 Delta_H u - ((m-2)/(m-1)) |du|_H^2
      = scal(q) + (f^2/4)|F|_ten^2 + (m/(m-1))|du|_H^2.            (2)

Consequently scal(q)>0 implies scal(H_hat)>0. This is the circle-quotient conformal construction recalled in Wiemeler, Theorem 2.2, and attributed there to Berard-Bergery.

For a smooth b-metric, its scalar curvature at the compactification face equals scal(q): in a product frame x partial_x, partial_{y_i}, every normal derivative x partial_x of a smooth coefficient vanishes at x=0, and the remaining structure functions and derivatives are exactly those of the r-invariant model. The same reasoning applies at a spatial face of a concordance, with base Y x [0,1]. Strict positivity at the face is indispensable.

## 2. Normal metrics deform through invariant PSC metrics to products

Assume scal(q)>0 over a compact B. First replace alpha by (1-t)alpha while keeping f,H fixed. Equation (1) shows that scalar curvature does not decrease. At the end alpha=0.

Next keep H_hat fixed and define, for 0 <= t <= 1,

    f_t = f^{1-t},       H_t = f^{2t/(m-1)} H,
    q_t = f_t^2 dr^2 + H_t.

Using (2) and the conformal change of the gradient norm,

    scal(q_t) = f^{-2t/(m-1)} [
      f^{2/(m-1)} scal(H_hat)
      - (m/(m-1))(1-t)^2 |d log f|_H^2 ].                         (3)

The bracket at t=0 is scal(f^2 dr^2+H)>0. Since (1-t)^2 <= 1, the bracket remains positive. The endpoint is dr^2+H_hat. Smoothing the junction and flattening parameter endpoints does not change the image of this path and preserves positivity. All coefficients, inverse metrics and parameter derivatives are uniformly bounded, and the scalar lower bound is positive by compactness.

This path yields an R-invariant PSC concordance between q and dr^2+H_hat: slow its parameter on a sufficiently long temporal interval. The scalar-curvature error is O(L^{-2}), uniformly on the compact quotient B. Equivalently perform the slow-concordance construction on S^1 x B and lift to R x B. No averaging of arbitrary PSC metrics is used.

## 3. End map and the dimensional subtlety

For either chosen infinity face define

    E(g) = [ f^{2/(d-1)} H ] in C(Y),

where f,H come from its normal metric. This definition is unchanged by replacing a defining function x by a(y)x: r changes by a function of y, alpha changes by an exact form, while the fiber-length f and quotient metric H are unchanged.

**Claim.** E descends to a well-defined map C_b(X) -> C(Y).

**Proof.** Let G be a b-PSC concordance. Its normal metric at the selected infinity face is an R-invariant uniformly PSC metric Q on R x (Y x [0,1]), with temporal end metrics q_0 and q_1. Apply Section 2 on the compact d-dimensional manifold Y to obtain invariant PSC concordances from q_i to dr^2+H_hat_i, where H_hat_i=f_i^{2/(d-1)}H_i. Reverse the first as necessary and attach both to Q using their exact temporal products. The resulting invariant PSC metric Q' on R x (Y x J), for a compact interval J, has product endpoints

    dr^2 + H_hat_i + ds^2.

Now apply (2) with base B=Y x J, of dimension d+1. Its quotient conformal metric is a PSC metric on Y x J. At either temporal collar the fiber coefficient is exactly 1 and the connection is 0, so the quotient metric is exactly H_hat_i+ds^2. It is therefore a PSC concordance between the two E-values. Reparametrize the finite interval preserving temporal product collars. QED.

**Important:** Applying (2) directly to the original Q would use exponent 2/d, not the endpoint exponent 2/(d-1), and would generally produce a non-product temporal lapse. The normalization-and-attachment step is essential; it is not legitimate to ignore this dimension mismatch.

## 4. Product inclusion is a section; actual law on its image

Define

    j: C(Y) -> C_b(X),         j([h]) = [dr^2+h].

This is well-defined: take the product with R of an ordinary PSC concordance on Y. Its scalar curvature is unchanged and it is smooth in the b-compactification. At either end, f=1, alpha=0 and H=h, so

    E composed with j = identity on C(Y).

Thus j is injective and the closed PSC concordance set is a retract of C_b(X). This statement concerns the complete ambient b-concordance relation, not only concordances constrained to be spatial products.

Now assume Y is connected, closed, spin, dim Y=d>=5 and h_0 is a PSC metric. The verified closed theorem gives C(Y) a basepoint-dependent abelian group law via the free transitive action of R^{spin}_{d+1}(B pi_1(Y)). No simply-connected or torsion-free assumption is needed. Hence the image j(C(Y)) has the actual law

    j(a) star j(b) = j(a +_{h_0} b).

This law is well-defined, associative, commutative, has unit [dr^2+h_0], and has inverses. All assertions follow from injectivity and the corresponding closed theorem. The operation is natural under spin diffeomorphisms of Y carrying the chosen reference metric/class along, and under the product identifications used here. A surgery realization is obtained by taking the ordinary compact surgery cobordism for the closed group law and multiplying it by R, then applying the b-compactification. This is not cylinder concatenation between arbitrary endpoint classes.

There is no claim that j is onto, or that these classes constitute a subgroup of some already-existing group C_b(X). No such ambient group law has been constructed.

## 5. Fixed-end reduction genuinely misses classes

Suppose h_1 is not PSC-concordant to h_0 on Y. Then dr^2+h_1 is not b-PSC-concordant to ANY compatible metric g which agrees with dr^2+h_0 near the chosen infinity face. Otherwise E would identify [h_1] with [h_0]. In particular it is not concordant to any compactly supported modification of the reference product metric.

This situation occurs in the verified closed theory: for Y=S^7, Xie--Yu--Zeidler Corollary 1.2 gives rank P(S^7)>=1 (take Gamma trivial, k=2, p=0; the H_0 contribution has dimension one, and the trivial-group assembly map is an isomorphism). Thus such h_1 exist. This uses an established existence theorem, not an explicit metric formula. The example is an 8-dimensional spin b-Lie manifold and satisfies the uniform positivity condition.

## 6. What this does not resolve

The fiber E^{-1}([h_0]) may contain compact/interior information not classified here. A candidate a star b = j(E(a)+E(b)) on all of C_b(X) would forget this information; its purported unit sends a to j(E(a)), so the unit law would require the UNPROVED identity jE=identity. It is not a solution of the full problem.

Pushing a compact PSC defect to r=infinity is not a valid automatic proof of that identity: a family whose defect moves toward infinity can fail joint b-smoothness at the spatial/temporal corner. Uniform smoothness on bar X x [0,1], not pointwise convergence on X, is required. Nor is this b-product argument available for arbitrary Lie algebroids, where the normal algebra may be more complicated than one central line.

## Sources and checks

- Xie--Yu--Zeidler, *On the range of the relative higher index and the higher rho-invariant for positive scalar curvature*, arXiv:1712.03722v3, introduction, Corollary 1.2 and Proposition 4.1: https://arxiv.org/abs/1712.03722v3
- Wiemeler, *Circle actions and scalar curvature*, arXiv:1305.2288, Theorem 2.2 and proof: https://arxiv.org/abs/1305.2288
- Ebert--Frenck, *The Gromov--Lawson--Chernysh surgery theorem*, arXiv:1807.06311, Lemmas 2.4--2.5: https://arxiv.org/abs/1807.06311
- verify_curvature_identities.py independently checks a full nonzero-connection coordinate model, the conformal coefficient, and the warped-cylinder specialization. CURVATURE_CHECKS.json records PASS. These are sanity checks, not substitutes for the general proof.
