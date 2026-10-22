# Author attempt 2: global radial interpolation and a coercive midpoint defect

2026-10-03 UTC. Goal: turn equal endpoint perimeter data into a global contradiction without any near-ball assumption. Outcome: exact positive defect, but no contradiction; route blocked at a specified missing implication.

Let ρ_0,ρ_1 be arbitrary positive C¹ radial functions on S². No symmetry or convexity is needed in this calculation. Write ρ_m=(ρ_0+ρ_1)/2. Along any unit-speed great circle, set X=(ρ_0,ρ_0'), Y=(ρ_1,ρ_1'), A=|X|, B=|Y|, and C=|X+Y|. Since the first coordinates are positive, X and Y cannot be opposite nonzero multiples. Direct rationalization gives the exact identity

A+B−C = 2 det(X,Y)² / [(A+B+C)(AB+X·Y)].

This is the pointwise integrand of
D(θ)=P(ρ_0)(θ)+P(ρ_1)(θ)−2P(ρ_m)(θ).
It is nonnegative. It vanishes identically on a given great circle if and only if det(X,Y)=0 there, or equivalently the positive ratio ρ_1/ρ_0 is constant on that circle. Thus if the endpoint perimeters agree, equality D(θ)=0 forces that constant to be 1 and the two radial restrictions to coincide on that whole circle.

For a quantitative form, suppose ρ_i≥r>0 and sqrt(ρ_i²+|∇ρ_i|²)≤Q. Then A,B≤Q,
A+B+C≤4Q, and AB+X·Y≤2Q². Since
det(X,Y)=ρ_0ρ_1 ∂s log(ρ_1/ρ_0),
we obtain
D(θ) ≥ r⁴/(4Q³) ∫_{Cθ}|∂s log(ρ_1/ρ_0)|² ds.

The incidence Fubini identity, using area measure dσ on the normal sphere, is
∫_{S²}∫_{Cθ}|∂s g(u)|² ds dσ(θ)=π∫_{S²}|∇g(u)|² dσ(u).
To see the constant, fix u and integrate (∇g(u)·(θ×u))² over the unit circle θ⊥u. In a tangent orthonormal basis its integral is π|∇g(u)|². The incidence measure is symmetric in θ,u.

Therefore
∫_{S²}D(θ)dσ(θ) ≥ πr⁴/(4Q³)∫_{S²}|∇log(ρ_1/ρ_0)|²dσ.

In particular, the mean section-perimeter functional J(ρ)=∫P(ρ)dσ is strictly convex along radial line segments modulo positive homothety: equality in its midpoint convexity implies ρ_1=cρ_0 globally. If endpoint data are equal, c=1. No nonconstant radial-affine segment can lie entirely in a perimeter-data fiber, and any unequal endpoints in the same fiber have a strictly smaller J at their radial midpoint.

## Why this does not prove global uniqueness
The midpoint is not assumed to have the endpoint perimeter data. Equal endpoint values of a strictly convex functional do not imply equal endpoints; they can bound a sublevel segment. The actual conclusion is that a hypothetical equal-data pair creates a radial midpoint with smaller perimeter data and positive mean defect. There is no hypothesis contradicting that. The same failure occurs for a Euclidean norm on a circle: strict convexity alone does not give injectivity of scalar norm data.

This route is blocked unless an additional global identity forces the radial midpoint to retain the same mean perimeter, or supplies the opposite inequality. No such identity has been established, and imposing it would change the original problem. The defect estimate is retained as an exact partial result, not a global rigidity claim.
