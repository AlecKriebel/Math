# Route 1: stability mass, superlevel geometry, and the radial bridge

This route proves only the statements explicitly delimited below. The radial conclusion is prior work, not a new resolution. Write V = lambda* f'(u*) and assume B_(2r)(z) is compactly contained in Omega.

## 1. Exact cutoff bound

For eta(y) = 1 on B_r(z), eta(y) = (2r-|y-z|)/r on B_(2r)(z) minus B_r(z), and eta=0 elsewhere, stability gives

    integral_(B_r(z)) V <= omega_n (2^n-1) r^(n-2).                 (1)

Here omega_n is the unit-ball volume. The Lipschitz test is allowed by bounded smooth approximation, dominated convergence against V in L^1_loc, and convergence of gradients in L^2. Its gradient has norm 1/r almost everywhere on the annulus, which proves the displayed constant. In particular, the average of V on the annulus B_r minus B_(r/2) is at most

    [(2^n-1)/(1-2^(-n))] r^(-2) = 2^n r^(-2).

At an isolated singularity, V is continuous off zero under the differentiable-convex convention. Thus for every sufficiently small r there is a point x_r in that annulus with |x_r|^2 V(x_r) <= 2^n (or the same with an arbitrarily small positive error). This proves the liminf upper statement. It does not bound the annular supremum.

## 2. A precise sufficient nonconcentration hypothesis

Suppose there are constants c,theta>0, independent of x near zero, such that

    |{y in B_(|x|/4)(x): V(y) >= c V(x)}| >= theta |B_(|x|/4)|.    (2)

Use (1), centered at x with radius |x|/4. All these balls avoid zero and lie inside Omega for small |x|. Then

    |x|^2 V(x) <= 16(2^n-1)/(c theta).                           (3)

Indeed, the left side of (1) is at least c V(x) theta omega_n (|x|/4)^n, and division gives (3). A potential counterexample to the full target must violate every such uniform thickness estimate along its high points. Mere continuity gives thickness depending on x and is insufficient.

## 3. Known radial case, with an independent short proof

If u is radial and radially nonincreasing and f is differentiable convex, then V is radially nonincreasing. For 0<r<R and the positive first Dirichlet eigenfunction phi_r on B_r, stability and V(y)>=V(r) for |y|<r give

    V(r) integral phi_r^2 <= integral V phi_r^2
                               <= integral |grad phi_r|^2
                               = lambda_1(B_1) r^(-2) integral phi_r^2.

Density justifies phi_r as a test. Hence r^2 V(r) <= lambda_1(B_1). For the extremal branch on a ball, rotational invariance and minimality give radial symmetry; radial monotonicity follows either from the classical branch and its limit or from the radial equation. The bound is precisely the upper estimate in Villegas, Theorem 1.1 and its proof.

Source: Salvador Villegas, “Behavior near the origin of f'(u*) in radial singular extremal solutions,” arXiv:2005.14334, https://arxiv.org/abs/2005.14334 ; primary PDF https://arxiv.org/pdf/2005.14334 .

## Exact remaining gap

On an arbitrary smooth domain, isolation of the singularity does not furnish radial monotonicity of V or the uniform superlevel-volume property (2). Replacing the annular supremum by an average, or importing the radial eigenfunction argument without radial ordering, is invalid. This route does not establish (2) from the source hypotheses.

Status: partial; the full target is unresolved.
