# Substantive turn 5: deterministic almost-sure homogenizing subsequences

2026-10-01, fifth substantive author turn, begun 07:10 UTC. Unit-initialized critical WARM on Z. **Complete candidate partial theorem; full temporal convergence remains unresolved after 5/5.** Estimated full-target completion: 65%. Independent review required; no novelty claim.

## Theorem

There exists a deterministic sequence t_n increasing to infinity such that, almost surely, simultaneously for every fixed edge i,

    N_i(t_n)/t_n -> 1.

The sequence is chosen from the law of the process, not from a realized sample path. This is stronger than identifying alternating accumulation profiles, but does not assert convergence between the selected times.

## 1. Deterministic dissipation function and reciprocal bound

Write tau=log(t+1), and use Z_i=N_i/(t+1), T_i=Z_i+Z_(i+1). Define the deterministic function

    D(tau)=E[(T_0(exp(tau)-1)-2)^2/(2 T_0(exp(tau)-1))].

Turn 3 proves

    integral_0^infinity D(tau) dtau <= gamma,        (1)

where gamma is Euler's constant. Translation invariance makes the same expectation valid at every index, including indices in a growing deterministic window.

A useful bound holds uniformly in physical time:

    E[1/T_i(t)] <= 1.                              (2)

Indeed S_i>=2+P_(i+1), with P a rate-one Poisson process. For t>0,

    E[1/(2+P(t))]=(t-1+exp(-t))/t^2.

Multiplying by t+1 gives a value at most one because (t+1)exp(-t)<=1. At t=0 the reciprocal T equals 1/2. This proves (2).

Cauchy–Schwarz, E T_i=2 and (2) now give

    E|T_i-2| <= 2 sqrt(D(tau)),
    E|1/T_i-1/2| <= sqrt(D(tau)/2).                 (3)

No spatial independence of T_i is required.

## 2. Three finite-block error estimates

For an even positive integer L, define

    C_L(t)=L^(-1) sum_(i=0)^(L-1) (-1)^i h(N_i(t)).

The exact telescoping identity of turn 3 splits this as

    C_L(t)=A_L(t)+B_L(t),
    A_L=L^(-1) sum_(i=0)^(L-1) (-1)^i M_i(t),
    B_L=L^(-1) integral_0^t [1/S_(-1)(s)-1/S_(L-1)(s)] ds.

Orthogonality of the harmonic martingales gives

    E A_L(t)^2 <= pi^2/(6L).                       (4)

After the logarithmic time change, the expectation of the absolute boundary integrand is at most sqrt(2D(sigma)), by (3). Consequently

    E|B_L(t)| <= sqrt(2 gamma tau)/L.              (5)

This uses Cauchy–Schwarz over the time interval and (1). It improves the crude logarithmic-time boundary estimate and is the important balance in this turn.

Let a=Z_0(t), and define z_i^a=a on even i and 2-a on odd i. Adjacent-sum telescoping gives the pathwise bound

    delta_L(t):=max_(0<=i<L)|Z_i(t)-z_i^a|
       <=sum_(i=0)^(L-2)|T_i(t)-2|.

Hence

    E delta_L(t) <=2L sqrt(D(tau)).                (6)

The window may grow here because (6) is an explicit uniform estimate derived at each deterministic time. It does not invoke the fixed-window convergence theorem uniformly without a rate.

## 3. Choose times and lengths so all errors are summable

A nonnegative integrable function satisfies liminf_(tau->infinity) tau D(tau)=0; otherwise it would eventually dominate a positive multiple of 1/tau. We can therefore choose deterministic increasing times tau_n, for n>=2, with

    tau_n>=n^2,
    tau_n>tau_(n-1)+1,
    tau_n D(tau_n)<=n^(-16).

Set t_n=exp(tau_n)-1. Let L_n be the smallest even integer at least n^3 sqrt(tau_n). Then

    n^3 sqrt(tau_n)<=L_n<n^3 sqrt(tau_n)+2.

Equations (4)–(6) yield summable bounds:

    E A_(L_n)(t_n)^2 <= const/n^4,
    E|B_(L_n)(t_n)| <= sqrt(2gamma)/n^3,
    E delta_(L_n)(t_n) <= 2/n^5+4/n^9.

Tonelli implies that the squares in the first bound and the nonnegative quantities in the other two bounds have finite sums almost surely. In particular, on one probability-one event,

    C_(L_n)(t_n)->0,
    delta_(L_n)(t_n)->0.                           (7)

This is a simultaneous growing-space/time estimate, not an interchange of two uncontrolled limits.

## 4. The block harmonic average pins the phase to one

For positive integers m,

    0<=h(m)-log m<=gamma,
    h(m)-log m->gamma as m->infinity.               (8)

Let a_n=Z_0(t_n). First (7) prevents a_n from approaching the endpoints zero or two along this sequence. For example take epsilon=1/10. If a_n<=epsilon and delta_(L_n)<=epsilon, every even Z_i is at most 2epsilon and every odd Z_i is at least 2-2epsilon. Pairing neighboring terms of C_L and using (8) gives

    C_(L_n)(t_n) <= (1/2)[log(epsilon/(1-epsilon))+gamma] <0.

The right side is a fixed negative number. Likewise, if a_n>=2-epsilon and delta_(L_n)<=epsilon, the harmonic average is bounded below by the opposite fixed positive number. Since C_(L_n)(t_n)->0, neither endpoint event can occur infinitely often. Thus eventually a_n lies in [epsilon,2-epsilon].

For all sufficiently large n the whole window then has normalized weights at least epsilon/2. Its unnormalized counts are therefore at least (t_n+1)epsilon/2, which tends to infinity **uniformly over that window**. The convergence in (8) is consequently uniform there. The logarithm is Lipschitz on the relevant compact positive interval. Pairing terms again and using delta_(L_n)->0 gives

    C_(L_n)(t_n) - (1/2)log(a_n/(2-a_n)) ->0.

By (7), log(a_n/(2-a_n))->0, and hence a_n->1 almost surely.

Finally the adjacent-sum theorem of turn 3 propagates this limit to every fixed positive or negative index. Its probability-one event already includes all countably many fixed indices. Replacing t_n+1 by t_n does not alter the limit. This proves the theorem.

## 5. Why the original limit is still not established

The construction selects very low-dissipation times. Their gaps can be arbitrarily large; no bound on tau_(n+1)-tau_n or t_(n+1)/t_n is proved. Monotonicity of N_i therefore cannot squeeze the normalized process between nearby selected times. Finite local energy, vanishing drift, deterministic envelopes and an almost-sure homogenizing subsequence still allow, on the present estimates alone, excursions between those times.

The missing original step remains convergence of the local alternating phase, equivalently the boundary-flux integral isolated in turn 4. This proof neither supplies its L1 integrability nor proves conditional convergence of that integral. It does not use ergodicity of a weak limit or assume uniform spatial ellipticity.

## Five-turn disposition

The original critical-line almost-sure limit conjecture remains **unsolved after five substantive author turns** in this attempt, even under the explicitly chosen standard unit initialization. The stronger ambiguity about arbitrary unspecified initial counts in the OWR wording is also not silently resolved.

Completed candidate partials are exact harmonic martingales and growth bounds; conditional homogenization of any actual limit; finite local dissipation and asymptotic stationarity; almost-sure adjacent-pair convergence to two; deterministic phase envelopes and conservative-flux reductions; and the deterministic almost-sure homogenizing subsequence above. All require independent review before publication as reviewed partial mathematics. No sixth author search turn or reset is taken.
