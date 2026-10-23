# Nonpolyhedral Monge–Ampère obstacles: audit and five approaches

Target: row 1887, ID 30004758, OWR Problem 5. Date: 2026-10-21.
Disposition: partial results and proof-scope corrections; NOT a full resolution or novelty certification. No publication or QUEUE modification.

## Source scope

The original OWR 35/2021, printed pp.1884–1886, Problem 5 asks to investigate analogues of preceding questions for obstacles whose graphs are not necessarily convex polytopes. The antecedents include high-dimensional construction, persistence under perturbation, the geometry/topology of a singular-solution locus, and tangent behavior. A construction alone does not discharge that program. Moreover, the older setting distinguishes the support of singular MA measure from the generally larger nonsmooth locus. A curved boundary carrying singular MA measure is not automatically an answer about singularities away from that measure.

Sources inspected: https://ems.press/content/serial-article-files/46911 ; https://doi.org/10.4171/owr/2021/35 ; https://arxiv.org/html/2204.11365v1 ; https://doi.org/10.3934/mine.2023083 ; https://arxiv.org/html/2605.19142v3 . The saved v3 PDF has an internal October 20 date, whereas arXiv HTML/version metadata says October 19; distinguish version date from internal manuscript date.

Mooney–Rakshit (2023) supplies polyhedral constructions and stability. Its general lower-semicontinuous-obstacle existence proposition is not a general geometric regularity theorem. Rakshit–Sen v3 states a construction on the boundary of an open convex C1 set, with positive bounded surface density and smoothness off that boundary; its §4.4 is a one-sentence reduction. It is preprint prior art, not a proved comprehensive answer to OWR Problem 5.

## Initial gate audit

1. The unqualified convex-set wording includes unbounded sets. Earlier small-support scaling and radial barriers do not extend automatically to these. The cited exterior regularity theorem explicitly requires a bounded excluded convex set. This is a gap in the supplied reduction, NOT a counterexample to the stated existence theorem.
2. The claim that any smooth convex boundary obstacle works needs qualifications. In the unbounded case take K={x_n<0} and obstacle zero on the full boundary hyperplane. Any finite convex u bounded above by zero there has constant trace there. Its boundary subgradients all have zero tangential component, so their union is contained in one normal line. In n≥2 this has zero n-dimensional volume, hence MA assigns zero to every boundary patch, contrary to uniformly positive surface density. This refutes the unrestricted obstacle parenthetical, not the theorem with a quadratic obstacle. Indeed q+a(x_n)_+ is a valid halfspace example.
3. A bounded-body constant boundary obstacle is NOT a counterexample: a quadratic bowl on a ball has constant boundary values. An initial speculative objection on that ground was withdrawn before use.
4. The phrase “fixing the quadratic polynomial gives a unique solution” requires fixing the MA right-hand side as well. Varying the shell mass below, in n≥3, gives distinct solutions with the same normalized quadratic asymptote. The cited exterior smoothness statement alone does not prove uniqueness. In n=2 a logarithmic term must be included in the asymptotic specification.
5. A C1 limit of smooth convex boundaries need not retain a bounded surface density. Uniform curvature/density estimates are missing from a naive approximation argument. The compact C2 repair below therefore cannot be labeled a proof of the full C1 statement.

## Approach 1: close the compact smooth construction gap

Let K be a bounded convex body with C2 boundary; translate so that 0 lies in its interior and quadratically rescale it into B_epsilon. Write q(x)=|x|²/2 and W(r)=integral_0^r (1+s^n)^(1/n) ds. Let D(x)=W(|x|)-W(epsilon). Choose epsilon much smaller than rho, and rho much smaller than 1. Then D≤0 on K, and D≥rho/2 on the sphere of radius rho after sufficiently small choices.

For a fixed small a>0, set Phi=q+a dist(x,K). This is convex, equals q in K, and has Alexandrov MA at least Lebesgue measure: its Hessian is at least I wherever twice differentiable, with any additional singular measure nonnegative. On the radius-rho sphere, Phi≤rho²/2+a(rho+epsilon)<D. Thus max(Phi,D) inside B_rho, continued by D outside, is a globally convex admissible lower barrier. It is important that Phi is a subsolution/barrier, not itself an exact det=1 solution outside K.

Solve the finite-ball upper-obstacle problem with obstacle q on ∂K and +infinity elsewhere, lower MA bound dx, and outer upper data W+10. The radial D is admissible. The spliced barrier is admissible and forces u_R=q on ∂K. Comparison with q inside K then gives u_R=q throughout K. A comparison with W+10 outside the origin gives a uniform upper bound; at the origin the interior value is already q. Local convex compactness gives a global limit u, with MA=dx off ∂K. The cited exterior regularity theorem, applied with excluded K, gives smoothness outside K, while the interior is explicitly q.

At x∈∂K the tangential derivatives equal those of q. Interior contact gives the subgradient x, and the spliced barrier gives x+[0,a]nu(x)⊂∂u(x). Consequently

  ∂u(x)=x+[0,T(x)]nu(x), with a≤T(x)≤M,

where M is a uniform local gradient bound near compact ∂K. The normal map F(x,t)=x+t nu(x), t≥0, is injective, because x is the nearest-point projection to K. Its Jacobian is product_i(1+t kappa_i(x)). The area formula yields

  MA_u=dx+f H^{n−1}|∂K,
  f(x)=integral_0^{T(x)} product_i(1+t kappa_i(x)) dt.

In particular a≤f≤M(1+M kappa_max)^{n−1}. Thus the bounded-C2 case is repaired with an explicit positive-density mechanism. Scaling back preserves the equation det=1: if the scaled coordinates are y=lambda x, set U(x)=lambda^(-2)u(lambda x). The surface density rescales by lambda^(-1), so positivity and boundedness survive.

What this achieves: a verified restricted construction and a formula for its surface mass. What it does not: C1 rough-curvature bounds, unbounded domains, prescribed f, classification, or persistence under general perturbation. This is a repair of a stated prior construction, not a novelty claim.

## Approach 2: exact spherical and ellipsoidal families

For R>0 and C>0 define a radial u by

  u(r)=r²/2 for r≤R,
  u(r)=R²/2+integral_R^r (s^n+C)^(1/n) ds for r≥R.

Inside, det D²u=1. Outside, writing p=u', det D²u=p'(p/r)^{n−1}=1 because p^n=r^n+C. At r=R the subgradient shell runs from radius R to beta=(R^n+C)^(1/n). Its volume is omega_n C, so the density on the sphere is

  f=C/(n R^{n−1}).

There is no mass at the origin, because the interior is q. The solution is smooth off the sphere and strictly convex everywhere. The density is constant and positive.

For n≥3, u(r)=r²/2+A−C/[n(n−2)]r^{2−n}+o(r^{2−n}); for n=2 the correction is (C/2)log r+O(1). Additive shifts can normalize A in n≥3, showing why the asymptotic quadratic alone cannot select C when f is not fixed.

For det A=1, v(y)=u(A^{-1}y) has MA density 1 off the ellipsoid A∂B_R. Since dS_y=|A^{-T}nu|dS_x, its singular density is f/|A^{-T}nu|. Translations and affine additions give further explicit covariance, not new singular geometry.

Outcome: exact nonpolyhedral test solutions, mass normalization, finite-dimensional stability under changes of R,C,A, and a benchmark for all claims. Limitation: affine images of spheres are not arbitrary shapes; parameterized continuity is not a classification of the full moduli space.

## Approach 3: shape perturbation and a transmission formulation

For a smooth K with quadratic trace and interior q, the preceding density formula rewrites the problem as an exterior det=1 solution with boundary q, unknown outward normal jump T, and prescribed surface mass condition

  integral_0^T product_i(1+t kappa_i) dt=f.

For fixed smooth curvature and f>0 the left side is strictly increasing in T. Thus it determines T pointwise. This is useful local algebra, but Dirichlet trace plus prescribed normal derivative overdetermines the exterior MA equation unless f, K, and infinity data obey a compatibility condition. One cannot simply select arbitrary f and declare that the Perron solution realizes it.

A possible local deformation theorem would linearize det D²u=1 to cof(D²u):D²w=0 separately on the smooth sides, with shape derivatives of trace and jump conditions. The unproved steps are invertibility in suitable weighted spaces at infinity, boundary regularity uniform under shape changes, and control of the resulting nonlinear compatibility map. None follows from weak Alexandrov convergence alone.

Outcome: an explicit scalar transmission law and identification of the missing analytic theorem. Residual: no general local moduli manifold, smooth dependence, or arbitrary-shape persistence theorem established here.

## Approach 4: approximation and what weak stability actually proves

Given locally uniformly convergent finite convex potentials u_j→u, their Alexandrov measures converge weakly. If K_j→K and the measures are dx+f_j dS_j with enough uniform geometric and density control, this supports a route to existence for a limiting obstacle. It does not automatically identify a limit density in L-infinity or preserve the whole nonsmooth locus.

A direct diagnostic is the spherical family with fixed R and C_j down to zero: each u_j is nonsmooth on ∂B_R and carries positive singular mass there, yet u_j→q locally uniformly and the limiting singular set is empty. Thus mere positivity for each j is insufficient; uniform lower mass and geometric controls are essential. Conversely, C_j→C>0 within this family preserves the full sphere and gives a completely verified special stability result.

For C1 approximation of a general convex body, curvature may concentrate. The integrand product(1+t kappa_i) in the compact smooth repair then has no uniform bound. An argument that declares its densities uniformly bounded merely from C1 convergence is invalid. Nor does weak convergence rule out an additional singular component relative to surface measure.

Outcome: a valid weak compactness tool plus a concrete failure mode for singular-set stability. Residual: uniform geometric estimates and a theorem identifying the limiting surface measure in the desired class.

## Approach 5: tangents and the distinction from Hessian asymptotics

For any finite convex u at x0, the first directional blow-up

  [u(x0+r z)−u(x0)]/r

converges locally uniformly as r decreases to zero to the support function of ∂u(x0). This is elementary convex analysis, not a new MA classification. At a smooth boundary point of the compact quadratic-trace construction the segment formula gives exactly

  x0·z+T(x0) max(nu(x0)·z,0).

For the sphere T=beta−R. The exterior Hessian eigenvalues at the boundary are (R/beta)^{n−1} in the normal direction and beta/R in tangent directions; the interior Hessian is I. This supplies an explicit one-sided second-order benchmark, not a universal second-order expansion.

The universal first-order wedge only records a normal slope jump. It does not determine how the Hessian behaves near a general boundary, nor tangent geometry at junctions, endpoints, higher-codimension singular supports, or singularities away from the support of MA. The OWR Dirac-mass tangent question also cannot be replaced by this different shell-support computation.

Outcome: rigorous tangent statements for the constructed class and exact radial second-order data. Residual: quantitative asymptotics for general geometry and the relevant stratified/junction models.

## Adversarial checks and final disposition

The construction was independently checked against the source hypotheses by a second mathematical worker. In particular: boundedness is used rather than silently omitted; q+a dist is never called an exact solution; the barrier contact is established before transferring subgradients; the upper density uses C2 curvature control; the halfspace affine-obstacle obstruction is not mislabeled a counterexample to Theorem1.5; and the radial density includes the factor n R^{n−1}.

No full resolution of the original broad problem has been established. Valid output consists of a compact-C2 proof repair, exact shell/ellipsoid examples and limited stability, a transmission identity, a weak-stability warning with an exact family, and first-order tangent computations. General stability/moduli/tangent questions remain unproved in this investigation. Do not mark solved, do not certify novelty, and do not convert five approaches into five successful general theorems.

### Additional adversarial finding: a concrete C1 barrier failure

The C1 issue is more than lack of an estimate. In dimension two, for a convex C1 boundary the singular boundary measure of q+a dist(·,K) is

  a ds + (a²/2) dtheta,

where ds is arclength and dtheta is the turning/curvature measure. C1 ensures continuous normals but does not ensure that dtheta is absolutely continuous with respect to ds. A convex C1 closed curve can have a nonzero singular continuous turning measure. For example, prescribe its tangent angle on an arclength interval using a continuous Cantor staircase spanning angle pi, and complete with its centrally symmetric copy. This gives a closed convex C1 curve whose turning is concentrated on an arclength-null set E. The normal tube over E then has positive area, namely (a²/2)dtheta(E).

If a Perron lower barrier of this form touches q on all of ∂K, its subgradients on E transfer to the solution, forcing positive MA(E). This contradicts a boundary measure of the form f ds alone. Thus the fixed-positive-width distance-barrier repair genuinely cannot be extended from C2 to all C1 bodies. This finding challenges the advertised proof reduction, not the existence of some other solution under Theorem 1.5 with a different trace or mechanism. It does not justify marking that theorem false.
