# A generalized-gradient formulation and its compactness obstruction

This note examines a route different from relative entropy or Hölder continuation. It derives a nonlinear dissipation formulation for the original continuum DMK reaction law. It does not identify that law with the different metric gradient flow in the published transport-energy paper and does not prove existence of a global solution of the original equation. No priority claim is made.

## Exact local dissipation

For a positive regular density m and its elliptic potential u, write g=|∇u|. The first variation of the energy S is

    δS/δm = (1−g²)/2.

For scalar m>0 define the convex dissipation function

    r_m(v)=v²/(2m)+v³/(6m²),  if v≥−m,
    r_m(v)=+∞,               if v<−m.

On the interior, r_m'(v)=v/m+v²/(2m²), and r_m''(v)=(m+v)/m²≥0. The extension is convex, and r_m(v)≥v²/(3m) on its domain. Its subdifferential at v=−m is (−∞,−1/2]. Therefore the pointwise inclusion

    0 ∈ ∂r_m(v)+(1−g²)/2

is equivalent to v=m(g−1), including g=0 at the boundary. Indeed set z=v/m≥−1: z+z²/2=(g²−1)/2 implies (z+1)²=g² and the domain selects z=g−1.

At that velocity, direct calculation gives

    r_m(v) = m(g−1)²(g+2)/6,
    r_m* ((g²−1)/2) = m(g−1)²(2g+1)/6,
    r_m(v)+r_m*((g²−1)/2)=m(g−1)²(g+1)/2.

The sum is exactly the density of −S' in the known Lyapunov identity. Thus the nonlinear dissipation gives an exact generalized-gradient representation on regular solutions. It is not the ordinary L2 or usual Fisher–Rao gradient equation.

## A well-defined frozen-state variational step

Fix 0<τ<1, a bounded smooth connected domain Ω, forcing f∈L∞(Ω) with ∫Ωf=0, and a bounded density m with positive lower bound. These ensure finite energy for the competitor m by Poincaré and elliptic coercivity. Use the convex dual energy

    S_ext(ν)=sup_{φ∈C¹(Ω̄)}[∫fφ−(1/2)∫ν|∇φ|²]+(1/2)∫ν.

Consider minimizing, over ν∈L³ and ν≥(1−τ)m,

    J(ν)=S_ext(ν)+τ∫ r_m((ν−m)/τ).

The competitor ν=m has finite energy. The dissipation is nonnegative, strictly convex, and grows cubically in ν with constants depending on τ and the bounds on m. The dual energy is nonnegative, convex, and weakly lower semicontinuous in L³: each expression inside its supremum is weakly continuous, since the smooth test-function gradient is bounded. The constraint is weakly closed. The direct method in the reflexive space L³ gives a unique minimizer. This one-step existence statement does not assert classical elliptic regularity at that minimizer.

Whenever the minimizer is regular enough for the displayed energy derivative and pointwise optimality conditions, these conditions yield

    ν=(1−τ)m+τm|∇u_ν|.

At an active lower-bound point, the variational inequality forces |∇u_ν|=0, so the same formula applies. This is a consistent semi-implicit approximation, using the old density m in the dissipation. It is not an identity for a finite time step of the continuum solution.

The minimizing inequality implies

    S_ext(ν)+ (τ/3)∫[((ν−m)/τ)²/m] ≤ S_ext(m).

In any chain of steps for which the construction and energy remain defined, this gives weighted square-velocity control. Mass is bounded by twice the initial energy. Cauchy–Schwarz consequently gives a bound on total L1 time variation over a finite interval, but none of these estimates provides spatial compactness or identification of the nonlinear elliptic flux.

The elementary one-step argument is stated with bounded m. The minimizer is only known to lie in L³, so even iteration in that same class would require extra justification. Spatially discretized versions avoid this particular issue; their limiting continuum identification still has the gap below.

## Why weak density compactness alone cannot identify the elliptic limit

Use the exact static states from `continuation.md`: m_n=2+cos(2πnx), u_n'=F/m_n, and fixed nonzero F. Periodic averaging gives

    m_n ⇀* 2,
    1/m_n ⇀* 1/√3,
    u_n' ⇀* F/√3.

The reciprocal average is elementary:

    (1/(2π))∫₀²π [1/(2+cos θ)]dθ = 1/√3.

For example, splitting at θ=π and using t=tan(θ/2) reduces it to the integral of 2/(t²+3) over the real line. Averaging against continuous test functions follows by partition into periods and uniform continuity, then extends to L1 tests by boundedness.

However the potential for the weak limit m=2 satisfies U(2)'=F/2. Hence the elliptic potential map is not continuous under weak-* density convergence, even with 1≤m_n≤3. The products m_nu_n'=F converge, but multiplying the two separate weak limits gives 2F/√3, which is not F. The example is one-dimensional; the dynamic one-dimensional problem itself is explicitly solvable. Its role here is to invalidate an unsupported weak-product passage, not to furnish a dynamical counterexample.

## Exact gap

A global construction for the original reaction law must justify iteration or regularization and provide enough compactness to identify both μ∇u and μ|∇u| in the limit. A formal gradient structure plus energy bounds does not do that. This route does not prove the full target.

## References

- Facca, Cardin, Putti, Towards a stationary Monge–Kantorovich dynamics (2018), https://doi.org/10.1137/16M1098383 ; https://arxiv.org/abs/1610.06325
- Facca, Daneri, Cardin, Putti, Numerical Solution of Monge–Kantorovich Equations via a Dynamic Formulation (2020), https://arxiv.org/abs/1709.06765
- Facca, Piazzon, Putti, L¹ Transport Energy (2022), https://doi.org/10.1007/s00245-022-09880-1 . The metric flow in this source must not be substituted for the original reaction equation.
