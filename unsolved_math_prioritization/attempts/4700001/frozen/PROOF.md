# Exact reductions, partial proofs, and remaining gap

## 1. Target and return-map domain

Let a,b,c,d,e be arbitrary real numbers and put

    B(theta) = b cos(theta) + c sin(theta),
    C(theta) = d cos(theta)^2 + e cos(theta) sin(theta).

Away from the origin the target system is exactly

    theta' = 1,
    dr/dtheta = f(theta,r) = a r + B(theta) r^2 + C(theta) r^3.       (1)

The origin is the only equilibrium: the matrix acting on (x,y) has determinant 1+F(x,y)^2. A finite periodic orbit cannot pass through it. Scalar uniqueness implies the positive solutions of (1) never cross. The time-2*pi map P, on its open interval of finite-time existence, is strictly increasing. An increasing scalar map has no nontrivial periodic points of higher period. Thus the finite planar periodic orbits correspond exactly to positive fixed points of P, and limit cycles correspond to isolated fixed points. Neither all solutions' global existence nor a return map on the whole positive half-line is assumed.

For any fixed point s, its multiplier is P'(s)>0. Multiplier less than 1 means asymptotically stable; greater than 1 means unstable; multiplier 1 requires separate analysis. The target includes such nonhyperbolic cycles. A family of periodic orbits is not a family of limit cycles.

## 2. Approach 1: Schwarzian bound for the non-sign-changing case

Suppose e=0 and d is nonzero. Then C has a fixed nonzero sign apart from its isolated zeros. Extend the scalar equation to negative r as an auxiliary device. If r(theta) is a positive periodic solution, then -r(theta+pi) is a negative periodic solution of the same equation. Distinct positive solutions give distinct negative partners. Zero is always a solution.

For the scalar solution R(theta;s), let w=R_s>0 and write the Schwarzian of a differentiable map as

    S(P) = P'''/P' - (3/2)(P''/P')^2.

Differentiating the three variational equations in s gives

    S(P)(s) = integral_0^(2*pi) f_rrr(theta,R(theta;s)) w(theta;s)^2 dtheta
            = 6 integral_0^(2*pi) C(theta) w(theta;s)^2 dtheta.       (2)

The initial map is the identity, whose Schwarzian vanishes. Equation (2) is verified symbolically in the supplied check. Its sign is strictly the sign of d. Consequently h(s)=1/sqrt(P'(s)) satisfies

    h''(s) = -(1/2) S(P)(s) h(s),

so h is strictly convex or strictly concave on the relevant domain interval. It cannot take the value 1 at three distinct points. If P had four distinct fixed points, Rolle's theorem would give three such points with P'=1, a contradiction. Thus there are at most three distinct real fixed points. Two positive cycles would yield two negative partners and zero, or at least five fixed points. Therefore there is at most one positive cycle.

If the positive fixed point were nonhyperbolic, the negative partner, zero, and this point give two interior Rolle points with P'=1, while the positive endpoint itself also has P'=1. This again contradicts strict convexity/concavity. The cycle, if present, is hyperbolic. The interval used in Rolle's theorem exists: solutions starting between two finite solutions remain between them and cannot blow up on the intervening compact time interval.

If d=e=0, a periodic positive solution instead satisfies, with u=1/r,

    u' = -a u - B(theta).

Its period integral implies a integral u = 0. Since u>0, there are no positive periodic solutions when a is nonzero. When a=0, u(theta)=u(0)-b sin(theta)-c(1-cos(theta)); any positive periodic solution belongs to a nearby continuum obtained by shifting u(0). There are no limit cycles here either.

**Unclosed part:** e nonzero makes C indefinite. The weighted integral in (2) need not have a fixed sign. This proof then supplies no global count.

## 3. Approach 2: exact solution of the homogeneous nonlinear sector

Assume b=c=0, with a,d,e otherwise arbitrary. Put z=r^(-2). A positive finite radial solution corresponds to a strictly positive finite solution of

    z' = -2a z - 2 C(theta).                                    (3)

For a nonzero, its unique 2*pi-periodic solution is

    z_*(theta) = -d/(2a)
       + (e-ad) cos(2theta)/(2(1+a^2))
       - (d+ae) sin(2theta)/(2(1+a^2)).                          (4)

Substitution verifies (4). Uniqueness follows from the nonunit homogeneous monodromy exp(-4*pi*a). The oscillatory amplitude is

    sqrt(d^2+e^2)/(2 sqrt(1+a^2)).

Therefore z_* is strictly positive everywhere exactly when

    -d/a > 0 and d^2 > a^2 e^2.                                (5)

When (5) holds, r_*=1/sqrt(z_*) gives the unique finite planar limit cycle. Its multiplier, invariant under the smooth transverse coordinate change, is exp(-4*pi*a). It is stable when a>0 and unstable when a<0. If equality d^2=a^2e^2 occurs with positive mean, z_* touches zero; r_* is not finite at that angle. This is not an extra finite cycle or a semistable boundary cycle. If z_* fails positivity, there is no positive finite periodic radius.

For a=0, integrating (3) over a period requires d=0. If d is nonzero there is no periodic orbit. If d=0, then

    z(theta) = K + (e/2) cos(2theta),  K > |e|/2,

is a continuum of finite periodic solutions. None is isolated, so there is no limit cycle. This also handles e=0.

**Unclosed part:** nonzero B prevents the linearization; it introduces the term -2B sqrt(z) into (3).

## 4. Approach 3: two hyperbolic cycles by a controlled small-parameter expansion

Take the following subfamily of the exact target, with epsilon>0:

    a=-alpha epsilon^4, b=c=e=1, d=beta epsilon^2,
    alpha=1/2, beta=2.                                         (6)

Set r=epsilon R. The equation becomes

    R' = epsilon B R^2 + epsilon^2 C0 R^3
         + epsilon^4(-alpha R + beta cos(theta)^2 R^3),
    B=cos(theta)+sin(theta), C0=cos(theta)sin(theta).             (7)

On any compact positive R interval, solutions over [0,2*pi] exist and depend analytically on (epsilon,R(0)) for sufficiently small epsilon. This follows from local analytic ODE dependence and a uniform compact containment bound as the right side of (7) tends to zero. All expansions below, including one R derivative, are uniform on such compact intervals.

For initial value R, expand the solution as R+epsilon u1+epsilon^2 u2+epsilon^3 u3+epsilon^4 u4+O(epsilon^5). Define

    H=sin(theta)+1-cos(theta), J=(1/2)sin(theta)^2,
    K(theta)=integral_0^theta C0(t) H(t) dt.

Then H'=B, J'=C0, and direct coefficient comparison gives

    u1 = R^2 H,
    u2 = R^3(H^2+J),
    u3 = R^4(H^3+2HJ+K).

At theta=2*pi, H=J=K=0; hence the first three return coefficients vanish. For order four, the pure R^5 coefficient in the derivative is

    B(4H^3+6HJ+2K)+C0(6H^2+3J).

Integration by parts, using the zero endpoint values, reduces its period integral to integral C0 H^2 = -pi/2. The additional order-four terms integrate to -2*pi*alpha*R+pi*beta*R^3. The rescaled return map therefore satisfies

    P_epsilon(R)-R = epsilon^4 Q(R)+O(epsilon^5),
    Q(R)=pi R(-2alpha+beta R^2-R^4/2).                          (8)

This derives the needed coefficient rather than inferring it from a truncated numerical fit. `check_symbolic.py` verifies the moment identities.

For alpha=1/2,beta=2, the two positive simple zeros are

    R_- = sqrt(2-sqrt(2)), R_+ = sqrt(2+sqrt(2)).

After analytically dividing the displacement by epsilon^4, the implicit-function theorem gives two distinct positive fixed points R_-(epsilon),R_+(epsilon) for every sufficiently small positive epsilon. They yield finite isolated planar cycles at

    r_-(epsilon)=epsilon sqrt(2-sqrt(2))+O(epsilon^2),
    r_+(epsilon)=epsilon sqrt(2+sqrt(2))+O(epsilon^2).

At a root with z=R^2, Q'(R)=2*pi*z(2-z), positive at R_- and negative at R_+. Their multipliers are 1+epsilon^4 Q'(R_+/-)+O(epsilon^5). Thus the inner cycle is hyperbolic and unstable; the outer is hyperbolic and stable. The origin has a<0 and is stable. This proves **at least** two cycles, not that those are all the cycles of (6). The proof does not specify a rigorous numerical epsilon cutoff.

**Unclosed part:** this local expansion has no control over cycles outside the small-radius region, or elsewhere in parameter space. A local cyclicity calculation cannot establish the proposed global maximum.

## 5. Approach 4: global variational and pairwise identities

Let r(theta)>0 be any finite periodic solution, not necessarily hyperbolic. Period integration of the logarithmic and reciprocal equations gives

    2*pi*a + integral B r + integral C r^2 = 0,
    a integral (1/r) + integral C r = 0.                        (9)

Its characteristic exponent is exactly

    log P'(r(0)) = integral [a+2Br+3Cr^2]
                = -2*pi*a + integral C r^2.                    (10)

For two distinct ordered positive periodic solutions r1<r2, subtracting their equations gives

    d/dtheta log((r2-r1)/(r1 r2)) = -a+C r1 r2,
    integral C r1 r2 = 2*pi*a.                                 (11)

For three ordered solutions r1<r2<r3, (11) would force

    integral C r2(r3-r1)=0.                                    (12)

All integrals here run from 0 to 2*pi. The weight in (12) is positive, so (12) is impossible for fixed-sign nonzero C, but is entirely compatible with an indefinite C. Equations (9)-(12) neither supply a contradiction nor assert the existence of three cycles.

For completeness, the trace parameter is genuinely monotone: if w=partial R(theta;s,a)/partial s>0, variation of a gives

    partial P(s,a)/partial a = w(2*pi) integral_0^(2*pi) R(theta;s,a)/w(theta) dtheta > 0

on the finite positive-flow domain. This orders return maps as a varies but does not bound the number of intersections of one such map with the identity. Merely appealing to a rotated-family parameter transfers, rather than solves, the central counting problem.

**Unclosed part:** prove a uniform two-cycle bound for all e nonzero with nonzero (b,c), including all nonhyperbolic cycles and return-domain boundaries; or provide a rigorous parameter example with at least three cycles. No sign or oscillation control needed to do this has been established here.

## 6. Approach 5: numerical falsification controls and their limits

`check_numeric.py` uses the radial and first variational ODE with DOP853. It retains incomplete flows rather than reporting them as absent cycles. The exact homogeneous control a=0.1,b=c=0,d=-1,e=0.5 has section radius 0.4344940123050857 and log multiplier -1.2566370614359164. A center control checks zero displacement, and the equality boundary in (5) checks a zero reciprocal-square radius.

The two-cycle controls for (6), at epsilon 0.12,0.10,0.07, each have two bracketed roots with opposite multiplier signs. At epsilon=0.10, the approximate radii are 0.07081517178465 and 0.15290666127132; the characteristic exponents are approximately 0.0005235854841 and -0.0031406332684. Repeating the control with a 100-fold smaller tolerance preserves these values closely.

A seed-4700001 probe of 24 indefinite-C parameter vectors on 31 logarithmically spaced radii from 0.005 to 5 had at most one bracketed root per vector, with 227 incomplete sampled flows. This search is deliberately recorded as weak empirical evidence only. Sign-change bracketing can miss even-multiplicity roots, closely spaced roots, cycles outside the radius window, and behavior near return-domain endpoints. The |r|=100 cutoff is a computational event, not a proved blow-up certificate. No interval arithmetic or rigorous integration-error enclosure was used.

## 7. Conclusion

The full target remains **unsolved** in this attempt. The lower bound two and several exact subclasses are rigorously supported; no global upper bound or three-cycle counterexample has been obtained. This packet claims neither a new theorem settling the target nor a verified later resolution.
