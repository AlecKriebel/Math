# Substantive turn 5: the initial-tangent regularity gap

**Final substantive turn; unreviewed partial.** Date: 2026-10-01. The original question is still unresolved. This turn tests whether the broad arrival-ordered admissible class supplies the initial tangent needed to formulate either A1 convention. It does not: an explicit admissible Lipschitz prefix has neither a limiting tangent nor a limiting secant direction at its starting point, even though every sufficiently early tangent lies in the acute cone for both coordinate axes.

## 1. An explicit admissible prefix with no initial tangent

For 0<theta<=1/10 put

    h(theta)=theta*(1+sin(log(theta))/10),
    r(theta)=exp(h(theta)),
    z(theta)=r(theta)(cos(theta),sin(theta)),
    z(0)=(1,0).                                         (1)

The derivatives satisfy

    h'=1+(sin(log(theta))+cos(log(theta)))/10,
    4/5<=h'<=6/5,
    9 theta/10<=h(theta)<=11 theta/10.                    (2)

Thus r is strictly increasing, the curve is outside the initial unit disk, and the distinct polar angles make it simple. Its derivative is bounded on (0,1/10], so it extends to a Lipschitz curve at zero. Reparametrize by arc length s; the result is a unit-speed Lipschitz simple prefix and is smooth at every positive parameter.

As in Turn 1, each radial ray reaches its sole barrier endpoint without meeting another barrier point. The unit-disk arrival trace is exactly u=r-1 and is strictly increasing. Moreover

    (ds/du)^2=1+1/(h')^2<=41/16<4.

Integrating gives s<2u away from the starting point. Hence the ordered curve is admissible at construction speed sigma=2, with strict slack at every positive point. No confinement or optimality is asserted.

## 2. Neither tangent notion exists at zero

The unit tangent angle at theta>0 is

    theta+arctan(1/h'(theta)).                           (3)

Along theta_n=exp(-2*pi*n) it tends to arctan(10/11). Along eta_n=exp(-(2*pi*n+pi)) it tends to arctan(10/9). These are distinct. The one-sided limit of the unit tangent, which local convexity would supply in the later source, therefore does not exist. Its variation is infinite on every initial interval: interlacing these sequences gives infinitely many angle changes bounded away from zero.

There is not even a limiting secant direction. Uniformly as theta decreases to zero,

    [z(theta)-(1,0)]/theta
       = (1+sin(log(theta))/10, 1)+O(theta).             (4)

Taking log(theta)=pi/2-2*pi*n and log(theta)=3*pi/2-2*pi*n produces the distinct limiting directions (11/10,1) and (9/10,1). The arc length is bounded above and below by positive constants times theta, so a right derivative of the arc-length parametrization could not be zero. The absence of a secant direction thus also rules out a right derivative at zero.

This is not caused by tangents pointing into the initial fire or to the wrong side of an axis. For theta<=1/10, (2) gives

    0 < theta+arctan(1/h') <= 1/10+arctan(5/4) < pi/2.

Thus all positive-parameter tangents lie in the first quadrant. Both acute-angle inequalities hold for each such tangent individually, but neither has the required limiting initial vector.

## 3. What genuine optimality would still have to do

The example's signed-curvature factor is

    1+(h')^2-h'',
    h''=(cos(log(theta))-sin(log(theta)))/(10 theta).

It is negative along the first tangent sequence for all sufficiently large n and positive along the second sequence. Hence this prefix is not a local length minimizer in the radial fixed-endpoint class: any sufficiently small negative-curvature interval away from zero admits the budget-preserving shortening from Turn 2. This explains exactly where that partial theorem can use optimality to exclude the oscillation.

For an optimal complete winding strategy, however, such a local shortening must be converted into a competitor for the actual global objective, with its later construction still feasible and its required closing geometry preserved. Turn 4 proves that retaining an arbitrary saturated suffix does not accomplish this. Neither the conditional local argument nor the feasibility example settles whether a true optimizer can have the displayed oscillations.

Bressan–Chiri's nowhere-denseness theorem does not fill this gap: a compact finite-length single arc already has empty interior. Its arrival-time continuity results likewise do not prove a one-sided tangent or the signed quantitative splice bound. No stronger regularity theorem is being inferred from these credited results.

If an initial right tangent does exist and the curve stays outside the initial disk, elementary feasibility implies its e1 component is nonnegative. The OWR e2 condition additionally needs the chosen orientation. In a reflection-invariant problem one can reflect a candidate to select that sign, but this changes an arbitrarily weighted objective or a fixed oriented endpoint problem in general, and does not prove that every specified optimizer already has that sign. It also does not create a missing tangent. The two printed source conventions remain distinct.

## Final outcome after five turns

The five-turn packet contains feasibility obstructions, conditional local shape theorems, a causal arrival lemma, and an explicit failure of the natural unchanged-suffix comparison. It contains neither a proof that all optimal source strategies are locally convex with A1 nor an optimal confining counterexample.

A complete resolution still requires a precise global meaning of “optimal” in the OWR passage and an argument valid for that objective which simultaneously controls later arrival times, closing geometry, and initial tangent regularity. The later preprint's optimizer theorem is inside a class that already assumes convexity and its own initial-angle condition, so it cannot be used to remove those assumptions.

`turn_5_check.py` verifies the derivative and curvature identities, the speed inequality and the distinct phase values exactly. The absence of limiting tangents and the admissibility proof are analytic, not numerical sampling claims.

Substantive author turns: **5/5**. Proposed original-target status: **unsolved**, with independent review required for every retained partial before a result PR. Estimated completion toward a full original resolution: **10%**. No novelty claim or sixth proof-search turn is included.
