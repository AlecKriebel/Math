# What the existing BKV estimates already yield

Authored audit derivation, 2026-10-12 UTC. This is a priority comparison, not a claim that the following theorem is printed in BKV. The actual primary input is the complete proof of Proposition 6.2, publisher PDF pp. 46–48, especially (100)–(102), (106). The source bytes and complete page-body hashes are frozen in `PRIMARY_COMPARISON_FROZEN.json`. Definition 1.7 is on p. 6 and the minimal graphical definition (19) on p. 17. All these bodies were actually read. The audit's derivation supplies the finite-horizon and common-time bookkeeping absent from the printed proposition.

Suppose a positive, finite integer offspring variable D satisfies BKV Definition 1.7 with tail exponent α>0. Let μ≥0 and α+μ<1. Infection arrows have rate λ/max(d(u),d(v))^μ, independently for the two directions, and recoveries have rate 1. Use only downward arrows and finite paths in (19). Then for every λ>0 there is a finite deterministic τ, depending on λ and an initial threshold K, such that the annealed probability of infinitely many infected vertices at τ is positive.

**Proof from the existing estimates.** Choose 1<s₁<s₂ and ε>0 such that

\[
0<\varepsilon<\frac{\alpha(s_2-s_1)}{s_2+s_1},
\qquad
a=1-(\alpha+\varepsilon)s_1>0,
\qquad \delta=a-\mu s_2>0.
\]

The first inequality is the tail-separation hypothesis preceding BKV (100), pp. 46–47; the other two are (106). Together they are solvable whenever α+μ<1: first choose 1<s₁<s₂ sufficiently close to 1 that 1−αs₁−μs₂>0, then choose ε>0 below both the tail-separation bound and the positive algebraic margins. For a vertex with L offspring, count children whose own offspring lies in [L^{s₁},L^{s₂}]. Equations (100)–(101) give, for sufficiently large L,

\[
\mathbb P(N\le L^a/4\mid L)
\le \exp(-L^a/48).
\]

Take an integer M=⌊L^a/4⌋ of these eligible children. Enlarging K ensures M≥L^a/8. On an eligible edge the actual undirected degrees are L+1 and D_child+1, so its downward rate is at least λ2^{-μ}L^{-μs₂}. Consequently the total arrow rate into the selected children is at least

\[
c_\mu\lambda L^\delta,
\qquad c_\mu=2^{-\mu}/8.
\]

The factor accounts for the integer rounding and the offspring/undirected-degree difference; one does not need to read BKV's use of L as an exact undirected degree.

Set

\[
L_m=K^{s_1^m},\quad
\ell_m=K^{-(\delta/2)s_1^m},\quad
s_0=0,\quad s_m=\sum_{j<m}\ell_j,\quad
\tau=\sum_{j\ge0}\ell_j.
\]

Both ∑ℓ_m and ∑(m+2)ℓ_m are finite. Require the root to have at least K offspring. At stage m, the current vertex has at least L_m offspring. Reveal its children's offspring and select the first M eligible children by a fixed label order. In the deterministic interval [s_m,s_{m+1}], select the recipient of the first downward arrow to one of those children. If no eligible pool or no such arrow exists, this route fails. Otherwise the next vertex has at least L_{m+1} offspring.

Conditional on previous choices, the relevant offspring rows and future outgoing-edge arrow processes are fresh. Selection depends only on the tree and arrows, not on any recovery process. The two stage failures have conditional probabilities at most

\[
e_m(K)=\exp(-L_m^a/48)
+\exp(-c_\mu\lambda L_m^{\delta/2}).
\]

For every fixed λ>0 the series ∑e_m(K) converges and tends to 0 as K→∞. For example s₁^m grows faster than m, hence the exponential terms eventually dominate any geometric series; monotone convergence applied from a fixed sufficiently large K then gives the limit in K. Choose K with ∑e_m(K)<1. Iterated conditional union bounds give a probability of an infinite selected tree/arrow ray at least

\[
\mathbb P(D\ge K)\bigl(1-\sum_m e_m(K)\bigr)>0.
\]

Now independently require no recovery of the root on [0,τ], and no recovery of selected vertex v_m, m≥1, on [s_{m-1},τ]. All selected vertices are distinct. Conditional on the entire selected ray their rate-one recovery clocks are independent. The total forbidden duration is

\[
\tau+\sum_{m\ge1}(\tau-s_{m-1})
=\sum_{j\ge0}(j+2)\ell_j<\infty.
\]

The recovery event therefore has conditional probability exp(−∑(j+2)ℓ_j)>0. On it, every selected vertex is infected by the end of its incoming stage and remains infected at τ. For each selected vertex only a finite initial segment is needed, so (19) or the increasing finite-ball construction includes that vertex at τ. Thus infinitely many are present together at τ, with lower bound

\[
\mathbb P(|X_\tau|=\infty)\ \ge\
\mathbb P(D\ge K)
\bigl(1-\sum_m e_m(K)\bigr)
\exp\!\bigl(-\sum_{j\ge0}(j+2)\ell_j\bigr)>0.
\]

This completes the claimed qualitative deduction.

**Candidate specialization and exact limits.** With P(D≥m)=m^{-1/4}, α=1/4 and μ=0, one may take s₁=3/2, s₂=2, ε=1/64, giving a=δ=77/128. The tail-separation bound is 1/28, so 1/64 satisfies it. The tail satisfies Definition 1.7, D is finite almost surely and D≥1. The displayed deduction proves a positive annealed common-time explosion probability for every λ>0 from existing BKV estimates. It does not reproduce the candidate's fixed τ=1/(2λ), numerical constant 7/30, or its exact quenched all-rates formulation. Those must remain attached to the independently accepted candidate proof.

**Recorded correction.** Root's independent check identified that the earlier audit specialization ε=1/16 violated the tail-separation bound 1/28. This document was corrected to impose that hypothesis explicitly and to use ε=1/64. The primary comparison freeze remains a historical record; neither the accepted candidate proof nor any printed source theorem was changed.

This derivation corroborates the original authors' 2024 and 2026 suggestion that their cited growing-degree ray method gives classical explosion. It makes it untenable to treat the qualitative route as newly discovered. It does not establish that a prior author printed this exact common-time theorem or the present bookkeeping. A source-theorem implication and an audit-supplied proof adaptation are different evidence categories.

**Adversarial checks.** The construction selects on arrows and offspring before inspecting recoveries; otherwise the final independent recovery product would be unjustified. The forbidden recovery windows include the entire incoming interval, so arrival before the stage endpoint is sufficient. Every witness is a finite path, and no post-explosion uniqueness is invoked. The degree offset and floor in the pool size have explicit constants. Failure sums and recovery durations converge because degree thresholds grow faster than exponentially. Survival alone, or infinitely many visited sites alone, is not used as a substitute for the simultaneous configuration event.
