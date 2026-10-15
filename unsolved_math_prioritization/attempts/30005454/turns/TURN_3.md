# Substantive turn 3: neighboring sums converge, leaving one neutral phase

2026-10-01 06:44–06:48 UTC. Unit-initialized critical WARM on Z. Unreviewed partial theorem. The full almost-sure pointwise convergence question is still unresolved; estimated completion 50%.

Continue with Z_i=N_i/(t+1), T_i=Z_i+Z_{i+1}, and h(n)=sum_{r=1}^{n-1}1/r.

## Exact harmonic-entropy identity

Define

    A(t)=E h(N_0(t))-log(t+1).

The exact harmonic martingale of turn 1 and translation invariance give

    A'(t)=2 E[1/S_0(t)]-1/(t+1)
         =1/(t+1) E[(T_0(t)-2)^2/(2 T_0(t))].       (1)

The last equality uses E T_0=2 and the elementary identity

    (T-2)^2/(2T)=T/2-2+2/T.

This identity has no Taylor remainder. The expectation is differentiable by the bounded local generator. Since A(0)=0, (1) makes A nondecreasing. If gamma is the Euler constant, h(n)<=log n+gamma, and Jensen gives

    A(t)<=E log N_0(t)-log(t+1)+gamma<=gamma.

Consequently

    integral_0^infinity E[(T_0(t)-2)^2/(2 T_0(t))] dt/(t+1)
       <=gamma.                                    (2)

By Tonelli and translation invariance, for every fixed edge pair, simultaneously almost surely,

    integral_0^infinity (T_i(t)-2)^2/T_i(t) dt/(t+1)<infinity.

## Theorem: every adjacent normalized sum converges to two

The logarithmic-time martingale-tail argument of turn 2 applies to T_i and to the smooth nonnegative function (T_i-2)^2/T_i. Eventually T_i lies in [1/2,4] on each fixed local neighborhood, by the clock bounds. The normalized drifts are bounded and the two count-noise martingales converge. Thus that nonnegative function is asymptotically uniformly continuous in logarithmic time. Its finite integral implies convergence to zero, exactly by the disjoint-fixed-length-interval argument already supplied in turn 2. Therefore

    Z_i(t)+Z_{i+1}(t) -> 2

almost surely for every i.

This rules out all local equilibrium accumulation profiles with nonconstant neighboring sums, without importing a finite-dimensional unstable-equilibrium theorem into the infinite system.

Choose the time-dependent scalar phase a(t)=Z_0(t). Telescoping finitely many adjacent-sum errors shows that for every fixed index i,

    Z_i(t)-a(t) ->0                 if i is even,
    Z_i(t)-(2-a(t))->0              if i is odd.

The remaining problem is precisely to show a(t)->1. The statement above is local in space and does not permit an index growing with t without an additional estimate.

## Exact alternating-flux martingales

For integers l<=r with an even number of edges in the interval, let

    Q_[l,r](t)=sum_(i=l)^r (-1)^i h(N_i(t)).

Its compensator telescopes:

    Q_[l,r](t)=sum_(i=l)^r (-1)^i M_i(t)
       +(-1)^l integral_0^t [1/S_(l-1)(s)-1/S_r(s)] ds.    (3)

The initial harmonic sum is zero. Every interior reciprocal pair cancels exactly. This is a finite sum identity, with no summability assumption on an infinite alternating series.

Different M_i have no common jumps: a vertex clock event increments just one edge, and distinct local clock events are almost surely nonsimultaneous. Hence they are orthogonal square-integrable martingales. In particular for an interval of length L,

    E[(L^(-1) sum_(i=l)^r (-1)^i M_i(t))^2]
       <=pi^2/(6L),                                (4)

uniformly in t, and the same holds for their limits.

Equations (3)–(4) are useful neutral-coordinate controls. They do not prove convergence of the boundary integral in (3). The adjacent-sum theorem only gives reciprocal boundary differences o(1/t); its integral may diverge or oscillate. The squared-error estimates give L2 control in logarithmic time, not L1 control. Treating that remainder as integrable would be an unsupported central step.

## A useful but insufficient boundary-tightness estimate

From 0<=A(t)<=gamma and h(n)<=log n+gamma we get E[-log Z_0(t)]<=gamma. Since (-log z)^+<=-log z+(log z)^+ and (log z)^+<=z, it follows that

    E[(-log Z_0(t))^+]<=gamma+1,
    P(Z_0(t)<=epsilon)<=(gamma+1)/|log epsilon|,  0<epsilon<1.

Thus no weak subsequential one-time law puts positive mass at zero; applying the adjacent-sum limit gives the same exclusion at the opposite phase endpoint two. This is a uniform-in-time probability bound, not a pathwise positive lower bound. It does not rule out rare deep excursions or prove convergence.

## Remaining phase problem

Even though each finite-time configuration is a translation-covariant factor of iid clock data, a weak limit of such laws can be a nonergodic mixture of alternating profiles. The proof in turn 1 uses shift-two ergodicity only **after actual almost-sure limits exist**. It cannot be applied to a random subsequential phase chosen from a time-dependent path.

The next turn should attempt to control the phase through the conservative alternating-flux structure or a genuine parabolic/contraction argument. The formal identities above provide a concrete target: establish convergence of the local neutral coordinate, rather than merely repeat that every cluster profile is an alternating equilibrium. No general theorem or integrability estimate closing that step has been proved here.
