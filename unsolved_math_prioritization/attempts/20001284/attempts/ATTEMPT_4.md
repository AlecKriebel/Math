# Author attempt 4: exact invisible perturbations for every finite plane set

2026-10-03 UTC. Goal: replace the full data by finitely many measurements while allowing increasing harmonic bands, as a possible route to global reconstruction. Outcome: explicit even, analytic, strictly convex counterexamples to that finite-data reduction. They do not refute the all-plane problem.

Fix N≥1 central planes with unit normals θ₁,…,θ_N. Repetitions cause no difficulty. Put
h(u)=∏_{i=1}^N(u·θ_i)², u∈S²,
ρ_ε(u)=R+ε h(u), ε>0.
The function h is nonnegative, even, real analytic, and not identically zero because a finite union of proper planes cannot cover S². On each measured great circle C_{θ_i}, h is identically zero, so its tangential derivative is zero there too. Consequently
K_{ρ_ε}∩θ_i^⊥ = R B³∩θ_i^⊥
exactly for every i. In particular every measured perimeter is exactly 2πR, despite K_{ρ_ε}≠RB³. This is equality of the measured sections themselves, stronger than scalar-data equality.

## A quantitative convexity certificate
The homogeneous polynomial h(x)=∏(x·θ_i)² has degree d=2N. Treat it as a product of d unit linear forms. On S²,
0≤h≤1, ||∇_{R³}h||≤d, ||D²_{R³}h||op≤d(d−1).
Euler's identity gives u·∇h=d h. For tangent vectors,
Hess_{S²}h=P_u D²h P_u−d h I,
so ||Hess_{S²}h||op≤d²=4N².
For a positive radial function ρ define the tangent quadratic form
Q_ρ=ρ²I+2∇ρ⊗∇ρ−ρ Hessρ.
Here ρ_ε≥R and ||Hessρ_ε||op≤4εN², whence
Q_{ρ_ε}≥ρ_ε(ρ_ε−4εN²)I>0
provided 0<ε<R/(4N²). For example ε<R/(8N²) leaves a strict margin at least R²/2.

For completeness, Q_ρ>0 implies convexity as follows. Put s=1/ρ. Then
Hess s+sI=ρ^(−3)Q_ρ>0.
The positive homogeneous degree-one extension H(x)=|x|s(x/|x|) has nonnegative Hessian away from the origin (the radial direction is its null direction); it is convex, including across the origin by positivity and homogeneity. Its unit sublevel set is precisely K_ρ={x:H(x)≤1}, so K_ρ is convex. The strict tangent inequality also gives positive curvature of the smooth radial boundary. Thus these finite-data collisions occur among origin-symmetric, real-analytic, strictly convex bodies.

## Arbitrarily close and finite-band nature
For every prescribed C^k-neighborhood of RB³, with finite k, ε can be chosen sufficiently small to put ρ_ε in that neighborhood, since h is a fixed smooth polynomial. Its spherical-harmonic expansion contains only even degrees at most 2N. Therefore a fixed finite list of planes cannot work simultaneously for all harmonic cutoffs, even arbitrarily near the ball. Nor can the finite-dimensional local inverse argument itself supply arbitrary-function reconstruction from the same finite data.

## What this says about the original problem
The original asks equality for EVERY central plane. The construction matches only the prescribed finite set, and some unmeasured plane has larger perimeter: choose u with h(u)>0 and a plane through u. Its section strictly contains the disk, so by strict perimeter monotonicity for nested planar convex bodies its perimeter exceeds 2πR. Hence this is not an all-plane counterexample.

A dense infinite set of plane normals would determine the continuous perimeter function, so this finite invisibility obstruction does not apply to equality on dense/all normals. The attempted finite-data reduction is disproved, while the source global uniqueness question remains open.
