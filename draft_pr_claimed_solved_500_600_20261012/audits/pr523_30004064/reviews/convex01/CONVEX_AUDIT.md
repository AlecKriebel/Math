# Independent adversarial convex-analysis review of PR523

Problem: 30004064 / OWR-16766-003. Review date: 2026-10-13 UTC.

**Verdict: mathematical PASS for the frozen candidate's literal exact-minimizer claim. No required mathematical repair found.** The precise result is that every noiseless box-feasible datum has zero exact back-projected dual optimizer. Thus, with sign(0)=0, exact sign recovery cannot return a nonempty uniquely determined binary image and returns the common-coordinate vector only when every coordinate varies among binary solutions. This does not certify any algorithm-specific, smoothed, auxiliary-variable, or priority conclusion.

The candidate and earlier positive audit were treated as hypotheses. The derivation below does not import their code or depend on their conclusions. All write actions were restricted to this review folder. No remote mutation, candidate edit, branch change, commit, push, release, or external communication was performed.

## 1. Exact claim, assumptions, and falsification targets

Let A be any real m-by-N matrix, C=A[-1,1]^N, and P the orthogonal projection onto range(A), so P=AA-dagger. The candidate studies

\[
F_y(\mu)=\tfrac12\|\mu-y\|^2+\|A^T\mu\|_1,
\quad
G_y(\mu)=\tfrac12\|P(\mu-y)\|^2+\|A^T\mu\|_1.
\]

The recovery convention is sign(0)=0. The noiseless hypothesis is that y=As for at least one binary vector s; the optimizer theorem needs only s in the box. No rank, tomography geometry, or uniqueness hypothesis is needed for that theorem. Counterexamples to the recovery assertions must additionally satisfy the source's geometry and full-row-rank conditions; the frozen 3-by-3 construction does.

The attempted falsifications were: a sign error in the support penalty; a missing factor in the quadratic; a pseudoinverse domain error; confusion between projected and unprojected minimizers; an unjustified strong-duality step for a nonconvex binary primal; the possibility that exact nonzero multipliers exist at a noiseless optimum; and silent passage from objective convergence to sign convergence.

## 2. Stronger exact solution by projection onto a zonotope

For every mu,

\[
\|A^T\mu\|_1=\max_{x\in[-1,1]^N}\langle\mu,Ax\rangle=h_C(\mu).
\]

This identity fixes both the sign and the coefficient of the penalty. C is compact and convex. Let p be its Euclidean projection of y and r=y-p. The projection inequality gives

\[
\langle r,c-p\rangle\leq0\quad(c\in C),\qquad h_C(r)=\langle r,p\rangle.
\]

For any v, direct expansion now gives

\[
F_y(v)-F_y(r)
=\tfrac12\|v-r\|^2+h_C(v)-\langle p,v\rangle
\geq\tfrac12\|v-r\|^2.
\]

Consequently, without any rank assumption,

\[
\boxed{\mu_F^*=y-\Pi_C(y)},\qquad
\boxed{\min F_y=\tfrac12\|y\|^2-\tfrac12\operatorname{dist}(y,C)^2}.
\]

The optimizer is unique, and it is zero **if and only if** y belongs to C. In particular, at y=As with s in the box,

\[
F_y(\mu)-F_y(0)
=\tfrac12\|\mu\|^2+
\sum_j\bigl(|(A^T\mu)_j|-s_j(A^T\mu)_j\bigr)
\geq\tfrac12\|\mu\|^2.
\]

Every scalar summand is nonnegative because |s_j|<=1. Strict positivity of the quadratic excludes every nonzero minimizer, including at box boundary points. This independently verifies the frozen proof's central theorem.

Changing the penalty to lambda times the l1 norm changes C to lambda C; zero is then optimal iff y belongs to lambda C. Thus the coefficient one matters, and it is exactly the coefficient produced by minimizing the binary multiplier term. The candidate has the correct normalization.

## 3. Projected objective and rank-deficient cases

C lies in R=range(A), and A^T annihilates R-perp. Write mu=v+w with v=Pmu and w in ker(A^T). Then

\[
G_y(\mu)=\tfrac12\|v-Py\|^2+h_C(v).
\]

Applying the preceding projection argument on R gives the complete formula

\[
\boxed{\operatorname{argmin}G_y
=Py-\Pi_C(Py)+\ker(A^T)}.
\]

Since projection onto C ignores the orthogonal component of y, Pi_C(Py)=Pi_C(y). Hence the unprojected minimizer and all projected minimizers have the same back-projection for arbitrary y, even though their actual mu values differ when y is not in R. At noiseless box-feasible y,

\[
\boxed{\operatorname{argmin}G_y=\ker(A^T)},\qquad A^T\mu=0
\quad\text{at every projected minimizer}.
\]

The candidate does not incorrectly claim uniqueness for G. Its rank-deficient result is exact.

Boundary checks include A=0: F has unique optimizer y, G is constant, and every optimizer has zero back-projection. At noiseless data y=0 this agrees with both candidate formulas. If N=0, the empty binary image is a harmless exception to the phrase that exact signs cannot recover a unique image; the candidate explicitly restricts that phrase to a positive number of pixels.

## 4. Genuine binary least-squares dual and exact gap

Use a true binary vector t, a real vector z, and the constraint z=t:

\[
p_B(y)=\min_{t\in\{-1,1\}^N}\tfrac12\|At-y\|^2,
\qquad
L(z,t,\nu)=\tfrac12\|Az-y\|^2+\nu^T(z-t).
\]

The binary part has infimum -||nu||_1. For M=A^T A, the real quadratic is bounded below iff nu lies in range(A^T). Outside that space, a kernel direction makes its linear term unbounded below. Inside that space, set ell=A^T y-nu, complete the square on range(M), and obtain

\[
q(\nu)=\tfrac12\|y\|^2
-\tfrac12\langle\ell,M^\dagger\ell\rangle-\|\nu\|_1,
\quad \nu\in\operatorname{range}(A^T),
\]

with q=-infinity otherwise. Substituting nu=A^T mu and using A M-dagger A^T=P yields

\[
q(A^T\mu)=\tfrac12\|y\|^2-G_y(\mu).
\]

The projected solution formula therefore proves, rather than assumes, the dual optimum:

\[
\boxed{d_B(y)=\max_\nu q(\nu)
=\tfrac12\operatorname{dist}(y,C)^2
=\min_{x\in[-1,1]^N}\tfrac12\|Ax-y\|^2}.
\]

Thus this dual's value is exactly the box relaxation's value. The genuine binary gap is

\[
\boxed{p_B(y)-d_B(y)
=\tfrac12\min_{t\in\{-1,1\}^N}\|At-y\|^2
-\tfrac12\operatorname{dist}(y,C)^2\geq0}.
\]

At noiseless binary-feasible data, p_B=d_B=0 and the unique optimal nu is zero. Strong duality here follows immediately from primal feasibility, q(0)=0, and weak duality; a general strong-duality theorem for a nonconvex primal is unnecessary. However, at nu=0 **every binary t** minimizes -nu^T t. The real quadratic requires Az=y, and enforcing z=t still requires finding a binary data-fit. Replacing this tied minimization by sign(0)=0 does not enforce the binary constraint. Zero gap therefore supplies no recovery rule from the multiplier alone.

For nonzero multiplier coordinates and zero gap, any binary primal optimizer must agree with sign(nu_j), by equality in weak duality and minimization of the binary term. That familiar conclusion gives no information at the noiseless optimal nu=0.

The source's sign(phi) parametrization permits zero-valued pixels under its stated convention. Its binary/ternary distinction does not change this dual: both sets have convex hull [-1,1]^N and the same support function. This review used the true binary primal above, so its gap statements do not silently switch to the ternary primal.

## 5. Recovery, subgradients, smoothing, and finite iterates

At an unprojected optimum, the first-order certificate has a box variable x satisfying

\[
x\in\partial\|\cdot\|_1(A^T\mu),\qquad \mu-y+Ax=0.
\]

At noiseless mu=0 this becomes x in [-1,1]^N with Ax=y. Such an x can contain useful information, but it is additional information. In the frozen two-solution example, the common-coordinate vector is itself box-feasible, so it can serve as an auxiliary certificate while the multiplier stays zero. This explains why exact zero-multiplier failure does not refute a separately specified auxiliary-variable method.

Conversely, binary uniqueness alone does not select the right auxiliary variable. For the full-row-rank weighted toy matrix A=(1,2), y=1, the unique binary data-fit is (-1,1). Both (1,0) and (1/5,2/5) are box data-fits. The latter is the minimum-norm data-fit and has sign (1,1), different from the unique binary solution. This is a boundary illustration for arbitrary matrices, not a claim about a particular implementation on unweighted square tomography.

Objective convergence certifies distance to the optimum, not signs. In the scalar noiseless endpoint A=1,y=1,

\[
F(e)-F(0)=e^2/2,\qquad F(-e)-F(0)=2e+e^2/2\quad(e>0).
\]

Both values tend to the optimum, while the signs stay opposite. The candidate's scalar distinction is exactly correct.

Smoothing changes the minimization problem. For example, replace |q| by sqrt(q^2+delta^2), delta>0. In the scalar endpoint y=1 the smoothed minimizer is positive, although it tends to the exact nonsmooth minimizer zero. Thus the limit of signs can differ from the sign at the limit. In the weighted toy example A=(1,2), y=1, the derivative of the smoothed objective is

\[
\mu-1+\frac{\mu}{\sqrt{\mu^2+\delta^2}}
+\frac{4\mu}{\sqrt{4\mu^2+\delta^2}}.
\]

It is strictly increasing, negative at zero, and positive eventually, so its unique zero is positive for every delta>0. The signs are therefore (1,1), which fail to recover the unique binary solution (-1,1). The smoothed minimizer tends to zero: the smoothing error is at most 2delta and strong convexity bounds its squared norm by 4delta. This independently demonstrates why a universal smoothing claim needs a separate statement and proof. It does not undermine the candidate, which expressly excludes such a claim.

## 6. Independent exact checks and actual tomography

`verify_convex.py` uses only Python's standard library and rational arithmetic. It imports no candidate function. Its small box optimizer enumerates faces with linearly independent free columns and solves rational normal equations. This enumeration is sufficient: select an extreme point of an optimal data-fit fiber; its free columns must be independent, since a dependency would give a nonzero feasible two-sided perturbation. More importantly, every returned projection is independently certified by the projection inequality against every binary vertex, whose convex hull is the entire box image C.

The run passed:

- 29 exact box-projection certificates and 29 exact pseudoinverse dual-value checks;
- 177 exact strong-convexity perturbation checks;
- 1,890 exact unprojected noiseless identities and 1,890 projected identities, including fractional box images;
- exact Moore-Penrose identities, zero matrices, rank deficiency, signed matrices, boundary data, and data outside the measurement range;
- enumeration of all 512 binary 3-by-3 images: 328 fibers, 230 singleton fibers, and exactly two images in the frozen target fiber, with exactly five fixed coordinates.

The independent tomography construction measures all three rows and all three columns, and then removes the last column measurement. Both the six-row and five-row matrices have rank five. For every enumerated image the omitted sum equals the sum of row sums minus the first two column sums, so removal preserves the fiber exactly. The target datum (3,1,1,3,1) has the common vector (1,1,1,1,0,0,1,0,0), whereas every exact dual optimizer has zero back-projection. The all-positive datum has one binary solution and fails exact sign recovery as well.

The arbitrary-size family also checks analytically: for k>=3, saturation of the first k-2 rows and columns forces all entries outside the bottom-right 2-by-2 block to one; the residual block has zero row and column sums and exactly two checkerboards. The independent measurement matrix has rank 2k-1 because inspecting its omitted last column first annihilates all row coefficients, and then all measured-column coefficients. The measurement-to-pixel ratio (2k-1)/k^2 tends to zero. No hidden rank or undersampling exception rescues the literal assertion.

The results file also exhibits non-noiseless boundary gaps. For A=(1,2),y=0, the binary optimum is 1/2 while the dual optimum is zero. For A=[[1,2],[2,4]],y=(1,0), the binary optimum is 2, the dual optimum is 2/5, and the unprojected optimizer is (4/5,-2/5); its back-projection is zero. These cases falsify overextensions from zero multiplier to noiseless binary feasibility or from projected to unprojected optimizer equality.

## 7. Primary-source reconciliation and disposition

The [primary manuscript, arXiv:1807.09196v3](https://arxiv.org/pdf/1807.09196v3) was inspected at Sections II-III and Appendix A. Equations (12)-(14) agree with the derived domain and projected/unprojected objectives. Section II explicitly sets sign(0)=0; its sign parametrization consequently permits zero pixels. Section II-A gives the scalar soft-thresholded optimizer and discusses approximate signs; Section II-C discusses a smooth surrogate. Algorithm 2 returns sign of an auxiliary z, and its optimality condition contains mu-y+Az. These facts support keeping exact multiplier recovery distinct from approximate and auxiliary recovery. This source reconciliation is not an exhaustive literature or priority audit.

**Strongest verified result:** the complete optimizer and dual-value formulas in Sections 2-4, with the frozen exact-recovery counterexamples as immediate consequences. The candidate's inequality, unique unprojected zero optimizer, projected optimizer set, binary zero-gap explanation, and approximation caveat all withstand this independent check.

**Exact remaining gaps:** no mathematical gap remains in the candidate's stated exact-minimizer negative result. A specified finite-iterate, smoothing-limit, or auxiliary-variable claim would require its own algorithm, parameters, stopping/selection rule, success criterion, and proof or counterexample. Historical priority and whether this result is a novel contribution are outside this mathematical audit. No inference of a complete priority conclusion is drawn from the source's scalar observation.

**Required repairs:** none to the frozen mathematical proof. Retain its exact-minimizer scope wherever the result is summarized. There is no supported basis here for broadening that scope to all numerical reconstructions.
