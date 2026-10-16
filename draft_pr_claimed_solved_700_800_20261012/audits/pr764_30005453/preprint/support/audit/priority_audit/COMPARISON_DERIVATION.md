# Independent mathematical comparison

The following calculations establish scope overlap and distinguish mechanisms.
They are a priority auditor's checks, not a substitute for the fresh full PR
mathematical audits. Source identities and exact byte hashes are in the retrieval
receipts. Qin's entire proof was inspected, including local construction,
complete-trajectory coefficient bounds, persistence and countable extraction.

## Boundary construction and normalization

Take the infinite path with unit vertex rates. Give alternating edges weights
two and zero. Every vertex has exactly one positive incident edge. For a positive
edge, each endpoint contribution is `2^alpha/2^alpha = 1`, hence its total
reinforcement is two. For a zero edge each contribution is zero for `alpha > 0`.
All denominators are positive. Thus the array and its one-edge translate are
different fixed points, alongside the all-ones fixed point. The same local
calculation holds on even finite cycles. Normalizing by total vertex rate `n`
gives `2(1,0,...)/n`, the finite-WARM allocation already displayed in the older
cycle literature. This is an explicit deduction valid for every positive
exponent; stability at a strong exponent is a separate question.

## Scope inclusion

Both claims have the same drift

`F_{uv}(x) = -x_{uv} + x_{uv}^alpha[p_u/S_u(x)+p_v/S_v(x)]`,
`S_v(x) = sum_{e incident v} x_e^alpha`.

Qin's parameters `p_*`, `Delta`, `gamma`, `beta` map to the PR's
`P`, `D`, `c`, `alpha/c`. Qin's finite positive real initialization includes
every initial count proved in the PR. No spatial rate lower bound is introduced
by this map. Apply a connected theorem separately on each connected component:
there are at most countably many components, so the intersection of all
coordinatewise probability-one events still has probability one. Equilibria are
unique on each component if and only if their product equilibrium is unique on
the whole graph. Isolated vertices do not affect edges. Thus connectedness does
not leave an unmatched theorem gap.

## Checks on the overlapping analytic route

For `0 < alpha < 1`, put `c=1-alpha`, `beta=alpha/c`, `y_e=x_e^c`.
Direct differentiation gives

`y_e' = c[-y_e + rho_u(y)+rho_v(y)]`,
`rho_v(y) = p_v/sum_{e incident v} y_e^beta`.

Bounded complete solutions admit a past-integral representation. The estimate
`x_e' >= -x_e` implies
`rho_v(y(s-tau)) >= exp(-alpha*tau) rho_v(y(s))`.
Using `c+alpha=1` in that representation yields
`y_e(s) >= c[rho_u(y(s))+rho_v(y(s))]`.
Hence the vertex forcings are uniformly bounded despite vanishing rate infimum.

For two positive complete trajectories, define divided differences
`a_e=(y_e^beta-tilde_y_e^beta)/(y_e-tilde_y_e)`, with derivative at equality.
The elementary inequality

`a_e <= max(1,beta)(y_e^beta+tilde_y_e^beta)/(y_e+tilde_y_e)`

and the preceding forcing bound imply the row estimate

`sum_{e incident v} p_v*a_e/[R_v(y)R_v(tilde_y)] <= max(1,beta)/c`.

This avoids bounding either divided-difference factor separately near zero.
Collecting edge differences into vertex past-integrals produces an extra
diagonal coefficient equal to the nonnegative off-diagonal row sum. For a small
positive Euler step the operator norm is at most `1-c*epsilon`. Norm
differentiability is established through relative derivative bounds before
differentiating the supremum norm; it is not assumed from coordinatewise
smoothness. The resulting comparison decays as
`[1+2 max(1,beta)T]exp(-cT)`.
Sending `T` into the infinite past identifies every bounded positive complete
trajectory with the equilibrium. These checks confirm that the proof's central
step does not silently require a uniform positive rate or coordinate lower
bound. They also do not extend the comparison to arbitrary forward stochastic
paths or establish a uniform stochastic rate.

For persistence, a single edge's local neighboring counts are eventually bounded
linearly; a coupled birth chain of rate `kappa*t^(-alpha)*n^alpha` has count
asymptotic `kappa^(1/c)*t`. The independent exponential holding-time series has
summable normalized variances of order `n^(-2)`. Countably many integer starting
times permit selection of an eventual valid comparison without a common random
time across the graph. For the logarithmic-time passage,
`Z_t=integral_1^t s^(-1)dM_s` has finite expected bracket; its convergence removes
increments uniformly on each shifted finite window. Continuous compensator
approximations justify Arzelà--Ascoli for càdlàg paths. Local finite sums and
positive limiting coordinates identify the ODE, and a countable diagonal
extraction reaches complete limits. No infinite Lyapunov sum or uniform spatial
initialization bound is needed.

## Mechanism distinctness in the frozen PR

The PR instead makes the nonlinear jump transform exact:

`H(n)=sum_{j=1}^{n-1} j^(-alpha)`,
`H(N_e(t))-H(N_e(0)) = Q_e(t)+M_e(t)`,
`<M_e>(t) <= Q_e(t)`.

Its compensated martingale divided by `1+Q_e` tends to zero. Scaled accumulated
vertex forcing then gives
`X_{uv}(t)^c=A_u(t)+A_v(t)+o(1)`.
Complete limiting vertex trajectories obey

`b_v' = c[p_v/sum_{w~v}(b_v+b_w)^beta-b_v]`.

Equilibrium existence comes from strictly convex finite-volume vertex
minimization and a coordinatewise compactness passage. Uniqueness and complete
trajectory rigidity use a modulus of continuity at approximate space-time
extrema, forcing a signed derivative strictly toward the interior and then
contradicting boundedness backwards in time. Neither attainment of an infinite
supremum nor differentiation of that supremum is assumed.

This is a checkable distinction in proof detail. It is not a certificate that
the complete-limit or vertex-incidence strategy itself first originated in this
PR, nor a claim that the full result was unknown to everyone on October 5.
