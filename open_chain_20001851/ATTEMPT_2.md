# Attempt 2 of 5: direct rigid-bar straightening inside an ordered core

## Goal and result

Attempt a constructive proof that an ordered middle subchain can pull arbitrary
end bars clear and then straighten. The argument succeeds under precisely the
endpoint inequalities from Attempt 1. It gives a self-contained rigid-bar motion
for the scalar-certificate class, without invoking the simple-projection theorem.
It does not prove that an arbitrary equilateral chain can reach that class.

Fix a unit vector `u`. Put `x_i=u·p_i` and suppose `n>=4` and

    x_1<...<x_{n-1},  x_0<x_2,  x_n>x_{n-2}.             (1)

Lengths `ell_i>0` may be arbitrary.

## Step 1: send the first bar below the entire core

Keep `p_1,...,p_n` fixed and move `p_0` on the sphere
`p_1+ell_1 S²`, within its open cap

    u·p_0 < x_2.                                        (2)

The starting point lies in this cap, as does `p_1-ell_1 u` because `x_1<x_2`.
Every nonadjacent stationary bar has all its points at height at least `x_2`:
the middle ones do by (1), and the last one does because both its endpoints
have height greater than `x_{n-2}>=x_2`. Thus the rotating first bar cannot
meet any nonadjacent bar while (2) holds.

An intersection with the adjacent second bar beyond `p_1` occurs exactly
when `p_0-p_1` has the direction `d_2=p_2-p_1`. This excludes at most one point
of the endpoint sphere. An open spherical cap containing the south pole, with
at most one other point removed, is path connected: if it is not the full sphere
it is a topological disk (or a punctured disk), and the full-sphere case is also
path connected after removing a point. The south pole is not the forbidden
point since `u·d_2>0`. Hence `p_0` can be moved to `p_1-ell_1 u` through
strict-simple configurations with all bar lengths unchanged.

For equilateral first and second bars, the forbidden point lies on the boundary
`u·p_0=x_2`, so it is already absent from the open cap. For unequal lengths,
the explicit removal above is necessary. This is a reason to state the
adjacent-overlap test rather than assume nonadjacent clearance is sufficient.

## Step 2: send the last bar above the core

Keep all other vertices fixed and move `p_n` on `p_{n-1}+ell_n S²`, within

    u·p_n > x_{n-2}.                                    (3)

Every nonadjacent bar now lies at height at most `x_{n-2}`; the first bar's
new low endpoint causes no exception. The only possible adjacent overlap is
the single direction `-d_{n-1}`. The same punctured-cap argument moves `p_n`
to `p_{n-1}+ell_n u`. This gives strict simplicity throughout.

## Step 3: straighten all positively directed bars simultaneously

At this stage every directed bar has positive dot product with `u`. Set
`v_i=d_i/ell_i` and, for `0<=t<=1`, define

    v_i(t)=((1-t)v_i+t u)/| (1-t)v_i+t u |,
    p_0(t)=p_0,
    p_j(t)=p_0 + sum_{i=1}^j ell_i v_i(t).              (4)

The denominator is nonzero: its numerator has positive `u`-dot-product.
Every length is exactly preserved, and every edge continues to have positive
height increment. Consequently the height along the whole parameterized
polygonal chain is strictly increasing. Two different chain points cannot
coincide, since their heights differ. At `t=1`, every directed bar equals
`ell_i u`, giving the desired straight configuration.

This is a continuous path of rigid bars. It never subdivides a bar or permits
its bending. Only the vertices and joint angles change.

## Boundary cases and scope

For three bars, choose the sign of a strict separating axis so that
`max(x_0,x_1)<min(x_2,x_3)`. The same first-cap construction uses the threshold
`min(x_2,x_3)`, then the last-cap construction uses `x_1`. The middle direction
is positive and (4) finishes. The one- and two-bar cases are immediate.

This is a configuration-by-configuration path construction. No continuous
choice of a cap path over the entire configuration space is asserted, so no
deformation-retraction or contractibility theorem follows from it.

## Where the attempted general proof stops

The crucial first-step clearance is `x_0<x_2`; if it fails, the moving endpoint
may hit a nonadjacent bar before reaching the lower cap. Similarly the final
bar needs `x_n>x_{n-2}`. We have not shown how to manufacture such inequalities
from an arbitrary configuration. Even existence of a common positive axis for
the middle edges can fail, as tested next. Thus this direct motion independently
recovers the supplied sufficient unlockability theorem, but does not resolve
the original all-equilateral-chain problem.
