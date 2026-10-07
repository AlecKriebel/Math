# Turn 4: symplectic scattering and reflection exchanges

The fourth substantive approach investigated whether area preservation obstructs exact reversal through a finite aperture. It gives a local affine constraint but no contradiction for general multi-branch scattering.

## Coordinates and exact identity

Take a horizontal aperture I=(0,L)×{0}, with the hollow below it. Write an entering unit velocity as (p,−sqrt(1−p²)), −1<p<1, and an exiting velocity as (P,+sqrt(1−P²)). Let

    S(x,p)=(X(x,p),P(x,p))

be a C² local scattering branch whose finite sequence of mirror collisions is regular and transverse. Taking the mirror arcs C³ is sufficient for the differentiations used here. The travel length ℓ along the branch satisfies the first-variation identity

    dℓ = −p dx + P dX.

Indeed, differentiation of each straight segment contributes its unit tangent dotted with the displacement of each endpoint. At an interior collision, the two segment contributions cancel for tangent displacement of the mirror point by the specular reflection law. Only the two aperture endpoints remain. Exterior differentiation then gives

    dX∧dP = dx∧dp.

This is the usual billiard symplectic identity, derived here to fix its sign.

Exact retroreflection means P=−p in these physical tangential-momentum coordinates. It follows that

    ∂X/∂x=−1,
    X(x,p)=A(p)−x,
    dℓ=−p A′(p) dp

on any subchart with connected horizontal slices. Thus a perfect regular branch is a reflection of entrance position, with an angle-dependent center; its travel length is independent of x on that branch.

## A limited global consequence

If, additionally, a single such formula were valid for every (x,p) in the full aperture strip and always had 0<X<L, then A(p)=L. To see this, let x tend to 0 and L in the inequalities 0<A(p)−x<L; the two limits give A(p)≤L and A(p)≥L. Hence X=L−x and ℓ is constant on the connected strip.

Those global hypotheses are extra. Scattering can have many itinerary branches, each covering only subintervals of x at a fixed p. An involution made from interval reflections preserves the required measure and is fully compatible with the local constraint. Therefore “p reverses, so phase area changes sign” is a false obstruction: reversal of x compensates exactly.

## Concrete consistency control

For a genuine two-reflection branch in perpendicular lines intersecting at (c,−h), h>0, unfolding gives

    A(p)=2c−2h p/sqrt(1−p²),
    ℓ(p)=2h/sqrt(1−p²).

They satisfy ℓ′(p)=−p A′(p) exactly. The allowed branch occupies only incidence data for which both mirror segments are hit and the outgoing ray exits through I. The formula is a local consistency example, not a perfect bounded hollow or body.

The remaining obstacle is geometric realization and compatibility of all branches. Symplecticity and reversibility alone do not forbid such branching and do not supply a realizable body either.
