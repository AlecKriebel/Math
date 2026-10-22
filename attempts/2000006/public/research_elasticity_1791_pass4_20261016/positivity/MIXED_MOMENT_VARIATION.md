# A one-sided mixed inverse-Jacobian moment from minimality

E-6322, shared pass 4, 16 October 2026.

## 1. New comparison theorem

Let y be a global minimizer in the exact frozen class, and let v belong to W^{1,6} with the same complete boundary trace. Assume

rank(Dv-Dy)<=1 almost everywhere, and J_v=det Dv>=0 almost everywhere.       (1)

The endpoint v is not required to have finite inverse-determinant energy. In particular it may have J_v=0 on a set of positive measure. One-component replacements, or differences in any one fixed target direction, satisfy the rank hypothesis; arbitrary competitors do not.

Write H(F)=a|F|^6+b|cof F|^3+c(det F)^2, B_y=dJ_y^{-2}, and

L_y(v)=DH(Dy):(Dv-Dy).

Then L_y(v) is integrable, the genuinely new mixed moment is finite,

integral J_v J_y^{-3}<infinity,                                           (2)

and

2d integral J_v J_y^{-3}
 <= integral L_y(v)+2 integral B_y
 <= integral [H(Dv)-H(Dy)]+2 integral B_y.                                (3)

All integrals are over the original domain. This is an unconditional consequence of minimality for every endpoint meeting the explicit comparison hypotheses (1). The theorem does not assert that a uniformly positive-Jacobian endpoint satisfying (1) exists for an arbitrary minimizer.

The case v=y gives only the already known inverse-square integrability. The new content is the weighted moment when an admissible rank-one-connected direction increases the determinant substantially on a low-J region.

## 2. Admissibility before differentiation

For 0<=t<1, define y_t=(1-t)y+tv. At almost every point the gradient difference has rank at most one, so every minor is affine along the line:

cof Dy_t=(1-t)cof Dy+t cof Dv,
J_t=(1-t)J_y+tJ_v >=(1-t)J_y>0.

The positive minor terms satisfy H(Dy_t)<infinity after integration. Indeed they are convex along this rank-one line and are bounded by (1-t)H(Dy)+tH(Dv). The barrier obeys

J_t^{-2}<=(1-t)^{-2}J_y^{-2}.

Thus y_t is an actual full-class competitor for every t<1, even if v itself is not one. In particular I(y_t)>=I(y). No claim of admissibility is made for an arbitrary additive variation.

## 3. The derivative calculation is noncircular

The derivative DH has growth at most C|F|^5, so

|L_y(v)|<=C|Dy|^5|Dv-Dy|

is integrable by Holder. Difference quotients of the H term converge in L^1, using the degree-six growth bound along the segment.

For the barrier put

q_t=[J_t^{-2}-J_y^{-2}]/t.

Convexity of s -> s^{-2} makes q_t decrease pointwise as t decreases to zero. For 0<t<=1/2, on the region J_v<J_y,

0<=q_t<=([(1-t)^{-2}-1]/t)J_y^{-2}<=6J_y^{-2}.

On J_v>=J_y it is nonpositive. Hence 6J_y^{-2}-q_t is nonnegative and increases as t decreases to zero. Monotone convergence, allowing an infinite limit, therefore gives

lim_{t down to 0} integral q_t
=integral [2J_y^{-2}-2J_v J_y^{-3}],                      (4)

with the possibility of negative infinity on the right. If the mixed moment in (2) were infinite, the right derivative of I(y_t) at zero would consequently be negative infinity, since the H derivative is finite. This contradicts I(y_t)>=I(y). Thus (2) holds, and the nonnegative right derivative proves the first inequality in (3).

Finally, along a rank-one gradient line the positive minor variables are affine, so convexity gives

L_y(v)<=H(Dv)-H(Dy)

pointwise. This proves the second inequality. Ordinary Piola equilibrium or integrability of the full stress DW(Dy) has not been used.

## 4. Quantitative repair consequences

If an endpoint meeting (1) also has J_v>=j_0>0, then

integral J_y^{-3}
 <= [integral H(Dv)+2 integral B_y]/(2d j_0).             (5)

More locally, on any measurable set A on which J_v>=j_0, the same bound controls integral_A J_y^{-3}. These are inverse-cube conclusions obtained from a feasible repair, not from a regularity assumption. Constructing such a repair under the baseline hypotheses remains open.

If v=y outside a measurable set E, cancellation in (3) gives the exact localized budget

integral_E H(Dy)+2d integral_E J_v J_y^{-3}
 <= integral_E H(Dv)+2 integral_E B_y.                   (6)

In particular every such nonnegative-endpoint truncation satisfies

integral_E H(Dy)<=integral_E H(Dv)+2 integral_E B_y.       (7)

If one additionally arranges J_v>=kappa J_y on E, 0<=kappa<=1, then

integral_E H(Dy)<=integral_E H(Dv)
                   +2(1-kappa) integral_E B_y.           (8)

Thus the precise comparison quantity needed to reduce the inverse-barrier source is relative determinant preservation on the changed set. Merely making the new determinant nonnegative leaves a source with coefficient 2. No estimate here constructs the required high-level truncation or closes a reverse-Holder iteration.

If kappa=1 and v=y outside E, the null-Lagrangian determinant integral and J_v>=J_y force J_v=J_y almost everywhere: a full-trace repair cannot increase the determinant everywhere without compensating somewhere else.

## 5. Taking a smaller step does not remove the barrier source

The coefficient in (7) cannot be made arbitrarily small just by taking t smaller. At a point where J_v=0, the finite-step barrier increase divided by t is exactly

B_y [(1-t)^{-2}-1]/t
=B_y(2-t)/(1-t)^2 >=2B_y,

and tends to 2B_y as t decreases to zero. The positive energy's first-order change is also proportional to t. Dividing the minimizer inequality by t therefore retains the coefficient 2; it does not yield a small parameter for absorption.

This endpoint degeneration is compatible with the comparison class, not merely formal matrix algebra. Take the actual identity minimizer on a smooth ball. Choose a compactly supported horizontal cutoff 0<=eta<=1 and a smooth nondecreasing scalar f equal to the identity outside an interior interval, with f'=0 on a smaller interval. Such f is obtained by choosing a smooth nonnegative derivative q, equal to one outside the interval and zero inside the smaller interval, adding a nonnegative compensating bump so integral(q-1)=0, and integrating. Define

v=(x_1,x_2,x_3+eta(x_1,x_2)[f(x_3)-x_3]).

Choose the product support inside the ball. Then v has the identity complete trace, is smooth, differs from y in one component, and

J_v=1+eta(f'-1)>=0.

It vanishes on an open box where eta=1 and f'=0. The endpoint energy is infinite, but every y_t with t<1 is a genuine finite-energy competitor. The pointwise barrier cost there is exactly the expression above. This verifies the sharp obstruction to the stated small-step absorption mechanism; it is not a singular minimizer.

## 6. Outcome

This pass gains a weighted inverse-cube moment for every feasible rank-one-connected nonnegative endpoint and a precise localized energy budget. It enlarges the usable endpoint class beyond pass 3's finite-energy endpoints. It neither supplies the crucial uniformly positive repair nor proves an unconditional inverse-cube moment for every minimizer, a gradient higher-integrability gain, or the frozen global positivity assertion.
