# Attempt 5: odd support functions and antipodal cancellation

2026-10-03 08:21 UTC. Substantive author turn 5/5. Outcome: a further all-dimensional sufficient condition and an exact obstruction to a tempting shortcut. **The source problem remains unsolved, 5/5.** Estimated full-target progress: 30% (subjective, not a solved fraction).

## Support-function formulation

For a constant-width-1 body and any choice of origin, write its support function as

    h(u)=1/2+f(u),        f(-u)=-f(u).

For the orbit's reflection normals and weights from Attempt 4,

    L=sum_i a_i h(n_i)=A/2+sum_i a_i f(n_i).           (S)

Let mu=sum_i a_i delta_(n_i). If this weighted atomic measure is antipodally symmetric, meaning mu(E)=mu(-E) for every set E, the odd term cancels exactly. Hence L=A/2>=2. Equality forces a two-bounce trajectory: the equality case A=4 in the radius/perimeter argument is a degenerate unit-direction polygon on a segment, with only the two antipodal directions and one passage each after redundant segments are removed. Because all reflection differences are nonzero, A=4 then gives precisely two changes of unit direction.

For clarity about that equality case, choose p to be a vertex of the unit-direction polygon and q the point halfway around its arclength. A=4 gives an enclosing ball of radius 1 centered at (p+q)/2. The positive weights from the original edge lengths have mean zero, so a radius-1 enclosing ball must have center zero (their weighted mean squared distance from a center z is 1+|z|^2). Thus q=-p and p!=q. For every unit vertex v, equality is necessary in |v| <= (|v-p|+|v-q|)/2 <=1. Equality in the vector triangle inequality forces v,p,q to be collinear. All direction vertices are therefore +/-p. Every nonzero change contributes 2 to A, so A=4 permits exactly two changes.

Thus **any realizable genuinely higher-period orbit with antipodally symmetric weighted reflection normals has length strictly greater than 2**, in every dimension. No claim is made that all minimizing orbits have this symmetry.

## Balance alone does not cancel an odd function

The reflection identity provides only sum_i a_i n_i=0. This annihilates linear functions of n, not arbitrary odd functions. An exact smooth planar example demonstrates the distinction.

Take the support function

    h(theta)=1/2-(1/32) cos(3 theta).

It has constant width 1 because h(theta+pi)=1-h(theta). Its curvature radius is

    h(theta)+h''(theta)=1/2+(1/4) cos(3 theta),

which stays between 1/4 and 3/4, so it defines a smooth strictly convex planar body. At theta=0,2pi/3,4pi/3, h'=0 and h=15/32. The three boundary points are x_i=(15/32)n_i and form an equilateral billiard triangle. Their normals balance, each reflection weight is sqrt(3), and A=3sqrt(3). However,

    sum_i a_i f(n_i)=-3sqrt(3)/32 != 0,
    L=45sqrt(3)/32 > 2.

This is not a counterexample to the original problem; it is an exact counterexample to the proposed shortcut replacing weighted balance by antipodal symmetry. The same failure already in dimension two means no dimension-independent proof can make that replacement.

## Endpoint and remaining target

The five approaches leave the exact finite inequality unresolved: show that every primitive polygon with diam({x_i,x_i-n_i})<=1 has perimeter >2 unless it is two-bounce, or construct one with perimeter <=2. We have not established symmetry of the weighted normal measure, excluded all low-turn nonplanar configurations, or proved a global four-orbit bound. Numerical failures to find a witness are not proofs. The literal disposition is **unsolved, 5/5**; no complete solution, new theorem of historical priority, or human peer review is claimed.
