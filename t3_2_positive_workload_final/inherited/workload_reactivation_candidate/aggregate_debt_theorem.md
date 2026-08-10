# Subcritical aggregate workload debt

Fix a terminal source chart and an integer workload `H(x)=h.x`. At the
beginning of an excursion set `B=H(X_0)` and define

\[
D_t=(H(X_t)-B)^+.
\]

At successive physical service-trial endpoints,

\[
D_{k+1}\le (D_k-S_k)^+ + A_k,
\]

where `S_k` is negative workload delivered by processed source layers and
`A_k` is positive workload delivered by the first unprocessed slower event.

Assume, on `D_k>0`,

\[
P(S_k\ge1\mid\mathcal F_k)\ge p,\qquad
E(A_k\mid\mathcal F_k)\le a<p.
\]

For every integer `d>0` and `s,a>=0`,

\[
(d-s)^++a-d\le-\mathbf1_{\{s\ge1\}}+a.
\]

Therefore

\[
E(D_{k+1}-D_k\mid\mathcal F_k)\le-(p-a).
\]

If `tau_0=inf{k:D_k=0}`, bounded-index stopping gives

\[
E D_{n\wedge\tau_0}+(p-a)E(n\wedge\tau_0)\le D_0.
\]

Consequently,

\[
E\tau_0\le\frac{D_0}{p-a}.
\]

If one trial has conditional mean physical duration at most `T`, then the
mean physical clearing time is at most `TD_0/(p-a)`.

No independence, identical distribution, bounded embedded jump count,
individual reaction credit, or genealogical state is used.

At `D=0`, a strict service trial lowers `H` below `B`. A failed trial may
create at most a bounded debt; that debt is cleared before the next zero-debt
trial. A uniform positive strict-service probability therefore gives genuine
descent below the baseline in finite mean physical time.
