# Independent adversarial audit: adaptive coding, row 1842

## Scope and provisional verdict

The proposed Bernoulli obstruction is correct. It refutes a universal affirmative assertion over arbitrary collections of source classes having nontrivial minimax redundancy. It does not refute exact or constant-factor adaptation for the specific collection of regularly varying envelope classes. The recovered workshop discussion introduces the generic adaptation framework and then studies envelopes; it must not be represented as explicitly proposing the unrestricted assertion as a theorem or precisely formulated conjecture.

This audit initially inspected the recovered OWR report and arXiv:1608.08367v2 text. The supplemental manuscript audit and final reconciliation below provide the completed verdict.

## Complete verification of obstruction

Use logarithms to base b>1 consistently. Put P_p=Bernoulli(p), p in (0,1/2), and C_p={P_p,P_(1-p)}. For each n, Q_n is an arbitrary probability distribution on binary strings of length n. It need not be consistent in n. Allowing it instead to live on a larger common alphabet makes no difference to the argument.

1. For the equal mixture M_(p,n)=(P_p^n+P_(1-p)^n)/2, pointwise domination gives max D_b(P^n||M_(p,n)) <= log_b 2. In fact the two divergences are equal by bit-complement symmetry, and for every Q the identity

   (D_b(P_p^n||Q)+D_b(P_(1-p)^n||Q))/2 = JS_b(P_p^n,P_(1-p)^n)+D_b(M_(p,n)||Q)

   proves that this mixture attains the minimax value, equal to the Jensen–Shannon divergence. The identity is valid in the extended sense when Q has zeros. Equivalently this divergence is I_b(J;X^n) with a fair binary label J. The empirical-frequency test at 1/2 has error tending to zero (the strict inequality p<1/2 is essential). Binary Fano then gives I_b(J;X^n) >= log_b 2-h_b(error), tending to log_b 2. Thus R(C_p^n) tends to log_b 2 and is positive for every n>=1.

2. Fix an arbitrary finite set F of distinct parameters. Choose disjoint open intervals about its parameters, with a common sufficiently small positive radius. Let A_(p,n) be the empirical-frequency event in the p interval. These events are disjoint for every n, and a_(p,n)=P_p^n(A_(p,n)) tends to 1. If q_(p,n)=Q_n(A_(p,n)), binary data processing yields

   D_b(P_p^n||Q_n) >= a_(p,n) log_b(1/q_(p,n))-h_b(a_(p,n)).

   The inequality follows by dropping the nonnegative term -(1-a)log_b(1-q). Cases q=0, q=1 follow by the usual extended conventions; eventual finite divergence excludes problematic cases when 0<a<1.

3. Define L_p=limsup_n D_b(P_p^n||Q_n). If L_p is finite, the displayed bound gives liminf_n q_(p,n) >= b^(-L_p). Since the events are disjoint, finite-sum liminf gives sum_(p in F) b^(-L_p) <= 1. In particular, for S_M={p:L_p<=M}, every finite subset has size at most b^M; hence S_M itself has size at most floor(b^M). Taking the union over nonnegative integer M proves that {p:L_p<infinity} is at most countable. No uniform onset time across infinitely many parameters was used.

4. Any asymptotic bound R(Q_n,C_p^n) <= (K_p+o_p(1))R(C_p^n), with K_p finite for each p, implies L_p<=K_p log_b 2. Therefore no single Q_n can satisfy such a bound for every p in (0,1/2). Since R(C_p^n)=O(1)=o(n), these classes meet the source's definition of nontrivial redundancy. This is stronger than ruling out one common constant, and avoids singleton classes with zero benchmark.

The conclusion is infinite limsup outside a countable set, not necessarily convergence to infinity. Do not replace limsup by liminf in the countability assertion. Do not claim finite constant-factor failure for all p: Q_n tailored to one pair succeeds on that pair.

## Source precision

- The recovered arXiv v2 introduction explicitly uses base-2 logarithms; the benchmark limit is then 1 bit, and |S_M|<=2^M. Natural logs are acceptable if declared, with limit ln 2 and |S_M|<=e^M.
- The same introduction defines nontrivial minimax redundancy as o(n), which includes the bounded Bernoulli-pair benchmarks.
- OWR report, printed p.1922, defines exact adaptation and permits a larger factor depending on the class label.
- OWR report, printed pp.1923–1924, restricts the proposed construction to envelope classes: f is nonincreasing, positive, summable, and has sum greater than 1. The regular variation assumption concerns the counting function t -> nu_f(1/t), with index in [0,1), rather than automatically the sequence f itself.
- OWR Theorem 1 and arXiv v2 Theorem 6 give an O_f(log log n) redundancy ratio. That theorem is not a constant-factor or exact-adaptivity theorem. The normalizing integral R_f(n) has class-dependent positive comparability constants.
- No global current-literature completeness claim follows from these two recovered sources.

Public source URLs: https://doi.org/10.4171/owr/2016/33 and https://arxiv.org/abs/1608.08367 .

## Checks required for auxiliary arguments

A countable mixture with weights w_j>0 gives R(Q_n,C_j^n)<=R(Q_(j,n),C_j^n)+log_b(1/w_j). Exact adaptation requires that this fixed overhead, and any approximation error in the component code, are negligible relative to the benchmark. Divergence R(C_j^n)->infinity suffices for a fixed O(1) approximation error. Nontriviality o(n) alone does not suffice.

For n-dependent finite covers or grids, the overhead is the actual negative log weight of the selected component. A covering argument must control the target class's full worst-case redundancy uniformly. Mere pointwise KL proximity of sources is not a substitute: KL has no triangle inequality. A diagonal argument also needs explicit control on approximation error and grid size at the same n; pointwise convergence for each fixed class is not a uniform bound over an expanding grid.

## Supplemental manuscript audit

Inspected `RESEARCH.md` after it became available. Mathematical verdict: all three propositions and auxiliary calculations PASS within their stated scopes.

- Proposition 1: mixture domination and the +1 approximate minimax argument are valid. For literal precision, when only eventual finiteness is assumed, choose approximate optimizers for finite-benchmark n and arbitrary coding distributions at any earlier infinite-benchmark n. The displayed extended-real bound remains valid. This is a clarity amendment, not a flaw in the asymptotic theorem.
- Proposition 2: both minimax limit and countability argument are valid, including all class-dependent constants and starting times. Natural-log convention is explicit and coherent. The interval (0,1/2) removes p=1/2 degeneracy and identifies distinct unordered pairs.
- Proposition 3: strict increase of j_m ensures unbounded j_m and hence positivity of h at every finite coordinate. The tail-sum argument proves j g_m(j)->0, so all selections are possible. Since j_m>=3 and sum a_m=1, h(j)<=1/3, so f(1)=f(2)=1 while f(j)=h(j) for j>=3. Tonelli gives sum h=1; therefore 2<sum f<=3. Each f(j_m)>g_m(j_m). This is a valid coordinatewise-cofinality obstruction only. It is not a claim about all coding strategies or the regularly varying subclass.
- Power-tail and exponential calculations are correct in nats. For f(j)~c exp(-bj), inversion has O(1) counting error, and integration gives (ln n)^2/(4b)+O(ln n). Finite initial modifications from the associated envelope distribution do not change these asymptotics.
- The fixed smaller power exponent has a polynomially diverging rate ratio. The manuscript correctly does not infer failure of n-dependent approximation.
- Integer prefix coding lower-overhead barrier follows immediately from Kraft and the harmonic series. The explicit warning against inferring necessity of the PC log-log redundancy loss is essential and present.
- The report correctly separates expected KL from regret, pointwise-in-class guarantees from uniform guarantees, and generic source classes from envelope classes.
- PC Theorems 5–6 and the index-zero equivalence were directly checked against the recovered arXiv v2 text. The source's log(e) conversion disappears in nats, as used in the manuscript.

One source-evidence item remains outside this audit's supplied files: the direct import attributed to arXiv:1202.0258. Its independently recovered statement or inspection record should be checked before treating that citation as directly verified. This does not affect any authored proof. No current exhaustive-literature or novelty claim has been certified.

This audit concerns the mathematics and source attribution only.

### Final reconciliation

The author correctly pointed out that iid class minimax redundancy is nondecreasing in n: for N>=n, marginalization of any Q_N and KL data processing give R_n(C)<=R_N(C). Eventual finiteness therefore implies finiteness at every earlier n as well. The earlier finiteness clarification is unnecessary; there is no actual missing assumption in Proposition 1. The manuscript has added this explanation.

The newly available recovery SOURCE_GATE.md records the AC restricted theorem and its primary conference source, https://dmtcs.episciences.org/2995/pdf . The author additionally reports checking https://arxiv.org/abs/1202.0258 . This is adequate attribution for a clearly labeled known import; this audit does not independently reprove that imported theorem. No outstanding mathematical correction remains.

FINAL VERDICT: ACCEPT the three authored propositions and auxiliary calculations as scope-limited partial results. ACCEPT the recommendation not to claim resolution of the intended envelope adaptation question. Do not label these standard arguments novel without a separate novelty investigation.
