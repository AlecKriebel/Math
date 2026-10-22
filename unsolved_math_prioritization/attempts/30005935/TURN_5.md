# Turn 5: logarithmic bounded-Lipschitz weak convergence in one dimension

Fifth and final author turn. The superlinear mean-square half-order claim is refuted by Turns1–3. Here the same unmodified scheme is shown to have a specified bounded-test weak rate in dimension one. This is not a claim of weak order1, an optimal rate, or a higher-dimensional result. Independent review is required.

Let u0 be the fixed nonzero nonnegative smooth compactly supported profile used above, T>0, M≥2 and tau=T/M. Let V_tau denote the continuous heat/geometric-Brownian interpolation from Turn4, with the original g(v)=v_+^(5/4). Let

X=C([0,T];C_0([0,1]))

with the supremum norm over time and space. Every numerical interpolation is an almost surely finite continuous X-valued random variable, as is the exact solution u from Turn2. Define d_BL using real test functionals Psi on X with ||Psi||_infinity≤1 and Lipschitz constant≤1.

**Theorem.** For a constant C depending on T and u0 but not M,

d_BL(Law(V_tau),Law(u)) ≤ C [log(eM)]^(-2).

In particular the same rate holds for the laws of the final fields in C_0([0,1]) and for any fixed bounded Lipschitz cylindrical observable. No spatial discretization or CFL condition is introduced.

## 1. Keep all dependence on the cutoff explicit

For the tangent-linear cutoff g_K in Turn4, with K≥max(1,2||u0||_infinity), its Lipschitz bound is L_K=(5/4)K^(1/4). The maximal cutoff error estimate therefore gives constants C0,C1 independent of K,M such that

E||V_tau^K-u^K||_X² ≤ B_K tau^(1/2),

B_K≤C0(1+K)exp(C1 sqrt(K)).

This uses L_K²=(25/16)sqrt(K) and L_K⁴=(625/256)K. The constants are independent of higher derivatives of g_K; otherwise the optimization below would not be justified.

Let G_K be the event that sup_(t≤T)Y_t≤K/2 and ||V_tau^K-u^K||_X≤K/2. On G_K the exact solutions agree, u=u^K, and the numerical grid values never exceed K. The original and cutoff schemes therefore agree at every input and every subsequent substep. Hence V_tau=V_tau^K as entire interpolated paths on G_K, even if an intermediate geometric-Brownian substep exceeds K: its coefficient was frozen at a grid value where the two coefficients agree.

By Turn4 and Markov's inequality,

P(G_K^c)≤2||u0||_infinity/K + 4 B_K tau^(1/2)/K².

For a normalized bounded-Lipschitz test,

|E Psi(V_tau)-E Psi(u)|
≤ E||V_tau^K-u^K||_X + 2P(G_K^c)
≤ sqrt(B_K) tau^(1/4) + 4||u0||_infinity/K + 8B_K tau^(1/2)/K².

This is uniform over the test class and does not require any integrable norm of the original superlinear approximation.

## 2. Optimize the proof cutoff, without changing the algorithm

Put ell=log(eM). Choose a positive kappa so small that C1 sqrt(kappa)≤1/8, and set K=kappa ell² for sufficiently large M; then K also exceeds the fixed lower bound required above. Consequently

B_K≤C(1+ell²)M^(1/8),

sqrt(B_K)tau^(1/4)≤C(1+ell)M^(-3/16),

and B_Ktau^(1/2)/K²≤C(1+ell²)M^(-3/8)/ell⁴.

Each term except K^(-1) decays faster than ell^(-2). This proves the theorem for large M. Increasing C handles the finitely many smaller M≥2, because d_BL≤2. The cutoff is only an analysis device; no coefficient of the actual numerical scheme was modified.

For completeness, the elementary dominance can be made quantitative: writing M=exp(ell-1), the function ell³exp(-(3/16)(ell-1)) is bounded on ell≥1. Thus even the slowest extra term is bounded by a constant times ell^(-2).

## 3. What this says about the source questions

- Positivity: the intended scheme is pathwise nonnegative and finite, with strict interior positivity from nonzero initial data
- Claimed superlinear mean-square half-order: false for this admissible one-dimensional case; the coupled mean-square error is infinite at every grid index≥2
- Weak error for unbounded linear mass: finite but bounded away from zero at fixed T, uniformly in M
- Bounded-Lipschitz weak error: converges at least as [log(eM)]^(-2) in the stated one-dimensional path/field topology

These statements are compatible. The weighted numerical masses converge in probability but cannot be uniformly integrable: their means are fixed at the heat value, while the exact limiting mean is strictly smaller. Bounded tests suppress the rare extreme tails that invalidate the unbounded tests and strong moments.

The source's broader weak-rate question is underspecified as to test class and does not restrict to d=1. This packet does not prove a positive algebraic weak order, does not establish optimality of the logarithmic rate, and does not settle all higher-dimensional bounded-test variants. The reconstructed conjunction demanding mean-square half-order is false, but that fact is not labeled a complete solution of every weak question in the source contribution. Five author turns are exhausted; no sixth search is included.

## 4. Exact checks

`verify_turn5.py` checks the cutoff exponent arithmetic, logarithmic-vs-polynomial bounds and test-class bookkeeping using rational arithmetic. The Hilbert/Sobolev estimates supporting B_K are in Turn4 and must be reviewed as analysis; numerical controls cannot replace them.
