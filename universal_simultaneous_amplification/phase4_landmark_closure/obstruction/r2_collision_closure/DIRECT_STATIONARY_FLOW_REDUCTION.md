# Direct stationary-flow reduction for the actual r=2 sign

Date: 2026-08-08 (America/Los_Angeles)

## Status

This note gives a **PROVED exact cancellation identity** for the only sign
that matters,

\[
                    \mathcal L\le \mathcal V.       \tag{1}
\]

It does not prove (1).  It isolates a precise transport-cost inequality on
the actual stationary dual flow.  The earlier auxiliary split through the
symmetric complete flow is exactly false and is not used here.

A bounded six-vertex hostile search found no graph with `L-V>0`.  This is
**NUMERICAL EVIDENCE ONLY**.  The universal r=2 upper bound remains **OPEN**.

## 1. Event kernels rather than centered generators

Let `T_P(A,B)` be the total rate of dual update events taking `A` to `B`,
including events for which `B=A`.  Each occupied target fires at rate one,
so

\[
 \sum_B T_P(A,B)=|A|.                              \tag{2}
\]

The centered generator is

\[
 Q_P(A,B)=T_P(A,B)-|A|1_{A=B}.                    \tag{3}
\]

Define `T_K,Q_K` analogously for the complete row kernel.  Both event
kernels have exactly the same row mass (2).  Moreover, every actual event is
also an event allowed by the complete kernel.  Thus, whenever `T_K(A,B)>0`,
put

\[
 r_{AB}={T_P(A,B)\over T_K(A,B)},                 \tag{4}
\]

and set no ratio on the common zero entries.  Equation (2) becomes the exact
sourcewise centering

\[
 \boxed{\sum_B T_K(A,B)r_{AB}=\sum_BT_K(A,B)=|A|.}\tag{5}
\]

Let

\[
 c_{AB}=\pi_K(A)T_K(A,B),\qquad
 g(A)={\pi(A)\over\pi_K(A)}.                      \tag{6}
\]

The actual event flow is

\[
 d_{AB}=\pi(A)T_P(A,B)=c_{AB}g(A)r_{AB}.          \tag{7}
\]

Stationarity of `pi` under `Q_P` says that `d` is balanced after its
state-dependent row mass is included:

\[
 \sum_Bd_{AB}=|A|\pi(A)=\sum_Bd_{BA}.             \tag{8}
\]

## 2. Exact compensation of the linear term

Let `psi` solve the verified complete Poisson equation

\[
 Q_K\psi(A)=U_{|A^c|}Z(A).                        \tag{9}
\]

The self-event increments vanish, so the Green linear term is

\[
 \mathcal L
 =\sum_{A,B}c_{AB}g(A)\{\psi(B)-\psi(A)\}.       \tag{10}
\]

On the other hand, actual stationarity (8) gives

\[
 0=\sum_{A,B}d_{AB}\{\psi(B)-\psi(A)\}
  =\sum_{A,B}c_{AB}g(A)r_{AB}\Delta\psi_{AB}.     \tag{11}
\]

Subtracting (11) from (10) yields the direct cancellation

\[
 \boxed{
 \mathcal L
 =\sum_{A,B}c_{AB}g(A)(1-r_{AB})\Delta\psi_{AB}.}\tag{12}
\]

Therefore the exact universal target is

\[
 \boxed{
 \mathcal V-\mathcal L
 =E_\pi[v(A)]
 -\sum_{A,B}c_{AB}g(A)(1-r_{AB})\Delta\psi_{AB}
 \ge0.}                                           \tag{13}
\]

This is not the former `S` split in disguise: (12) uses the actual balanced
event flow directly and retains the full compensation between its symmetric
and circulating parts.

## 3. Minimal remaining obstruction

The local cost `v(A)` is the explicit Green-weighted tangent remainder

\[
 \sum_{x\in A}\sum_{k=1}^{|A^c|}
 c_k{2\over(1+k/(n-1))^2}
 \sum_{\substack{C\subseteq A^c\\|C|=k}}
 {\{P_{xC}-k/(n-1)\}^2\over1+P_{xC}}.            \tag{14}
\]

Thus (13) is a constrained transport-cost inequality:

* `r` has the sourcewise mean-one constraint (5);
* `c g r` has the global flow-conservation constraint (8);
* all ratios `r_AB` arise simultaneously from one row kernel `P`;
* for an undirected graph, that row kernel obeys
  `d_x P_xy=d_y P_yx` for positive vertex degrees `d_x`;
* the cost (14) is built from every subset mass of those same rows.

Dropping any of these couplings leaves signed edge work in (12) and does not
prove (13).  The already certified path witness shows that even the local
state residual

\[
 v(A)-(Q_K-Q_P)\psi(A)                           \tag{15}
\]

can be negative.  Hence the remaining theorem is precisely:

> Prove that the coupled sourcewise centering and global conservation in
> (5), (8), together with vertex reversibility, make the aggregate work in
> (12) no larger than the subset-mass cost (14).

This is the current **MINIMAL OPEN OBSTRUCTION** for the direct r=2 route.

## 4. Bounded hostile search

The direct search used the exact six-vertex counterexample to the discarded
`L<=S` inequality as a seed, then evaluated:

* 400 lognormal perturbations of that seed across five scales;
* 800 complete-support log-uniform six-vertex graphs;
* 900 connected sparse supports with 5--13 edges and log-uniform weights;
* local optimization from the eight best complete or sparse candidates.

No positive `L-V` was found.  The best value was the complete graph, zero to
floating precision.  The strongest nonbaseline local candidate approached
the complete graph with `L-V` approximately `-1.23e-7`.  The exact split
counterexample itself has `L-V` approximately `-0.1084443`.

These figures validate only the hostile-search implementation.  They do not
discharge (13).

## 5. Verification

Run

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B verify_fisher_route.py
```

The exact verifier constructs both uncentered event kernels independently,
checks (2)--(5), checks the actual-flow balance and zero work in (11), and
certifies (12)--(13) on the frozen rational witnesses.  It also replays the
exact undirected six-vertex refutation of the discarded symmetric split.

`search_direct_gap.py` and `search_symmetric_split.py` are floating-point
discovery programs, not proof certificates.
