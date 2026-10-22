# Approach 2: construct a shrinking-radius counterexample, then test all centers

This construction is an exact negative control for exchanging limits. It is a genuine sequence of smooth radial metrics, but **not a counterexample to the conjecture**: it fails the curvature hypothesis away from its central point.

## Prescribed central volume profiles

Fix n >= 2 and 0 <= r <= 1/2. Set

h(t) = (t^2-1)/(t^2+1),
W_j(r) = r^n [1+r^2 h(jr)],
W_infty(r) = r^n(1+r^2).

The factor omega_n is suppressed. Then W_j(r) < r^n precisely for 0 < r < 1/j. Every j therefore has a positive central comparison radius, while W_infty(r) > r^n for every r > 0.

The convergence is uniform, since

0 <= W_infty(r)-W_j(r) = 2r^(n+2)/(1+j^2 r^2) <= 2r^n/j^2.

Moreover

A_j(r) := W_j'(r)/(n r^(n-1))
 = 1 + ((n+2)/n)r^2 h(jr) + 4j^2 r^4/[n(1+j^2 r^2)^2].

Since h >= -1 and the last term is nonnegative,
A_j >= 1-((n+2)/n)r^2 >= 1/2.
Thus these are strictly increasing positive volume profiles, not oscillating signed functions.

## Exact realization by smooth metrics

Define f_j(r) = r A_j(r)^(1/(n-1)) and

g_j = dr^2 + f_j(r)^2 g_S^(n-1)

on the open Euclidean-radius-1/2 ball, using the usual smooth structure at r=0. Because A_j is positive, smooth and even in r with A_j(0)=1, f_j/r is smooth and even with value one at zero. In Cartesian coordinates the tangential factor is 1+O(r^2), so g_j extends smoothly and positively through the center. Radial distance from the center is exactly r: every path has length at least its total radial displacement, and a radial segment attains that lower bound. Its central ball volume is therefore

n omega_n integral_0^r f_j(s)^(n-1) ds = omega_n W_j(r).

Put A_infty=1+((n+2)/n)r^2 and define f_infty and g_infty similarly. With y=j^2r^2,

A_j-A_infty
 = [-2(n+2)y/(1+y)+4y^2/(1+y)^2]/(n j^2).

Hence A_j -> A_infty uniformly, with error at most [2(n+2)+4]/(n j^2). Smooth powers are uniformly Lipschitz on the resulting compact positive range, so (f_j/r)^2 -> (f_infty/r)^2 uniformly. The Cartesian tensors g_j thus converge uniformly to g_infty, including at the center. They converge with every derivative on compact annuli r >= a > 0.

## Why the apparent counterexample fails

The central small-ball expansion gives

Sc(g_j)(0) = 6(n+2),
Sc(g_infty)(0) = -6(n+2).

These signs also follow directly from the warped scalar formula

Sc = (n-1)[(n-2)(1-f'^2)/f^2 - 2f''/f].

For completeness, in an orthonormal frame the sectional curvatures of radial planes are -f''/f and those of tangential planes are (1-f'^2)/f^2. There are n-1 radial planes and (n-1)(n-2)/2 tangential planes; scalar curvature is twice their sum, giving the displayed formula. Substituting f=r(1+b r^2+O(r^4)) gives Sc(0)=-6n(n-1)b. Here b is respectively -(n+2)/(n(n-1)) and +(n+2)/(n(n-1)).

The smooth limit has negative scalar curvature on some punctured central neighborhood by continuity. Choose a fixed point with radial coordinate r0 in that neighborhood. Smooth convergence on an annulus around r0 implies Sc(g_j)(r0) -> Sc(g_infty)(r0) < 0. Thus, for all sufficiently large j, g_j violates every nonnegative volumic lower bound at that noncentral point. The construction only verifies a central ball comparison, whereas the conjecture requires the condition at all centers.

This provides an explicit and rigorous warning: even uniform convergence of actual smooth tensors, positive central scalar curvature, increasing volume profiles, and a positive comparison interval at the chosen center do not justify interchanging j -> infinity and r -> 0. It does not show that the full all-centers hypothesis allows those radii to collapse in a harmful way.

## Residual obstruction

To turn this into a true counterexample one would have to keep the volumic condition at every center while retaining the bad limit. The radial construction demonstrably fails that test. No metric satisfying the full target hypothesis and violating the conclusion was obtained.
