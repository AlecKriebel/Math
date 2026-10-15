# Substantive turn 2: finite local dissipation and asymptotic stationarity

2026-10-01 06:29–06:34 UTC. Unit-initialized critical WARM on Z. Unreviewed partial results; existence of almost-sure pointwise limits remains unresolved. Completion estimate: 35%.

Use Z_i(t)=N_i(t)/(t+1), T_i=Z_i+Z_{i+1}, and

    g_i=1/T_{i-1}+1/T_i-1,    b_i=Z_i g_i.

The harmless t+1 normalization avoids the origin; it has the same limits as N_i/t.

## 1. Pair sums stay linearly positive

Every clock ring at vertex i+1 increments exactly one of e_i,e_{i+1}. Thus pathwise

    2+P_{i+1}(t) <= S_i(t) <= 2+P_i(t)+P_{i+1}(t)+P_{i+2}(t).

Consequently almost surely 1<=liminf T_i<=limsup T_i<=3. These are local statements simultaneous over countably many i; they are not a uniform-in-space law of large numbers. Individual Z_i can still approach zero.

## 2. Every count has logarithmic growth exponent one

The exponent lower bound from turn 1 can be improved to

    lim log N_i(t)/log t = 1     almost surely for every i.

Let M_i be the convergent harmonic martingale of turn 1 and set

    R_i(t)=exp(h(N_i(t))-M_i(t))
          =exp(integral_0^t [1/S_{i-1}+1/S_i] ds).

It is positive and absolutely continuous. Since h(n)-log n is bounded and M_i converges, there are pathwise positive constants c,C with c R_i<=N_i<=C R_i for all sufficiently large t.

Given epsilon>0, the two neighboring counts are eventually at most (2+epsilon)t by the two-clock upper bound. Therefore

    R_i' >= 2R_i / [C R_i+(2+epsilon)t]

almost everywhere for sufficiently large t. Fix beta<2/(2+epsilon). A sufficiently small positive K makes z(t)=K t^beta a subsolution on [T,infinity): choose z(T)<=R_i(T) and

    C K T^(beta-1)+2+epsilon < 2/beta.

The inequality persists because beta<1. Scalar differential comparison gives R_i(t)>=K t^beta. Taking epsilon down to zero through a countable sequence and using the linear upper bound proves the exponent-one assertion. This does **not** prove a positive limit or a positive lower linear rate: t/log t also has logarithmic exponent one.

## 3. A finite entropy-dissipation integral

Translation invariance of the unit-initialized law gives E lambda_i=1. Indeed the two incident-vertex contributions have expectations summing to one after one spatial shift. Hence E N_i(t)=1+t and E T_i(t)=2.

Put

    ell(t)=E log T_0(t),
    D(t)=E [Z_0(t) g_0(t)^2].

The jump rate of S_0 is lambda_0+lambda_1<=3. Differentiating the expectation by its bounded local jump generator gives the exact identity

    ell'(t)=D(t)/(t+1)-rho(t),

where

    rho(t)=E[(lambda_0+lambda_1)(1/S_0-log(1+1/S_0))]

satisfies 0<=rho(t)<=3 E[S_0(t)^(-2)]/2.

To verify the drift identity, translation invariance gives

    E[(lambda_0+lambda_1)/S_0]
       =E[N_0(1/S_{-1}+1/S_0)^2].

Also E Z_0=1 and E[Z_0(g_0+1)]=E lambda_0=1. Expanding the square in D leaves exactly the preceding drift minus 1/(t+1), which is the derivative of the normalization logarithm. No global infinite sum of entropy is used.

Since S_0>=2+P_1 and P_1 is a rate-one Poisson process, Tonelli and its successive mean-one holding times yield

    integral_0^infinity E[(2+P_1(t))^(-2)] dt
      =sum_(n>=0) 1/(n+2)^2 = pi^2/6-1.

On the other hand Jensen gives ell(t)<=log(E T_0)=log 2=ell(0). Integrating the exact drift identity therefore proves

    integral_0^infinity D(t)/(t+1) dt
      <= (3/2)(pi^2/6-1) < infinity.

By Tonelli, almost surely for each edge, simultaneously,

    integral_0^infinity Z_i(t) g_i(t)^2 dt/(t+1) < infinity.   (**)

This is a pathwise local weighted-dissipation statement obtained from the stationary law; it is not a finite-volume approximation or an unjustified infinite Lyapunov sum.

## 4. The local stationarity defect vanishes

The compensated count A_i=N_i-1-integral lambda_i is a martingale with bracket rate lambda_i<=2. The martingale

    B_i(t)=integral_0^t dA_i(s)/(s+1)

has expected total bracket at most 2 and therefore converges almost surely. With tau=log(t+1), the exact normalized equation is

    Z_i(tau)=1+integral_0^tau b_i(s) ds+B_i(exp(tau)-1).

For each finite set of neighboring indices, the clock laws eventually bound all Z_i by 3 and relevant T_i below by 1/2. Thus b_i is bounded there, and Z_i g_i^2 is a Lipschitz function of its three local weights on that domain. Convergence of the finitely many B_i implies that their entire tail oscillations tend to zero. It follows that Z_i g_i^2 is asymptotically uniformly continuous in tau: on a sufficiently late interval, increments are bounded by C times the interval length plus an arbitrarily small martingale-tail term.

Together with (**) this forces

    Z_i(t) g_i(t)^2 -> 0,
    b_i(t)=Z_i(t)g_i(t) -> 0

almost surely for every i. Explicitly, if a fixed positive defect recurred at arbitrarily late times, the asymptotic continuity bound would keep at least half that defect on infinitely many disjoint intervals of one fixed positive length, contradicting finite integral. This argument accommodates the vanishing jumps; it does not assert literal continuity of the jump paths.

Consequently every product-topology accumulation point of the normalized configuration is an equilibrium in the compact coordinate range 0<=z_i<=2 with every neighboring sum at least one. Such accumulation points exist by a diagonal compactness argument. Equilibrium follows by continuity of b_i on neighboring sums bounded away from zero.

## Remaining obstruction

Vanishing drift and finite squared-velocity-type energy do not alone imply convergence of a bounded trajectory on an infinite time interval. Even a scalar bounded function can have a derivative tending to zero and square-integrable derivative while failing to converge. The critical alternating equilibrium family also supplies a neutral direction. A proof must exclude repeated movement among different local equilibrium profiles or other boundary equilibria, not simply invoke stationarity of accumulation points.

The first turn proves that an actual full pointwise limit must be identically one in the unit model. This second turn proves asymptotic stationarity and finite local dissipation, but does not yet bridge that existence gap. No claim that weak subsequential limits remain ergodic is made. Further work must control the boundary/neutral modes or produce a valid counterexample for this exact initialized process.
