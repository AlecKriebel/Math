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

## 3. Exact hit-probability cost and rank collapse

There is a useful exact simplification of the cost which is invisible in
the raw row-mass variable.  Put

\[
 h(x)={2x\over1+x},\qquad a={k\over n-1},\qquad
 p=h(x),\quad p_0=h(a).
\]

The tangent remainder in each atom of `V` is exactly

\[
 \boxed{
 {2(x-a)^2\over(1+a)^2(1+x)}
 ={(p-p_0)^2\over2-p}.}                          \tag{14}
\]

Thus `V` is a Green-weighted one-sided chi-square cost of the burst-hit
probabilities.  Moreover, the same algebra gives

\[
 {(p-p_0)^2\over2-p}-{2(x-a)\over(1+a)^2}=p_0-p.\tag{15}
\]

For a dual state `A`, target `v in A`, and `k`-set `C subset A^c`, let

\[
 p_{vC}=h(P_{vC}),\qquad p_k^0=h(k/(n-1)).
\]

Summing (15) over all atoms gives the **statewise identity**

\[
 \boxed{
 v(A)-U_{|A^c|}Z(A)
 =\sum_{v\in A}\sum_{k=1}^{|A^c|}c_k
   \sum_{\substack{C\subseteq A^c\\|C|=k}}
       (p_k^0-p_{vC}).}                          \tag{16}
\]

Consequently the direct sign also has the exact hit-deficit form

\[
 \boxed{
 \mathcal V-\mathcal L
 =E_\pi\sum_{v\in A}\sum_kc_k
   \sum_{\substack{C\subseteq A^c\\|C|=k}}
       (p_k^0-p_{vC}).}                          \tag{17}
\]

This expression collapses further under stationarity.  Define

\[
 B_k(A)=\sum_{v\in A}\sum_{\substack{C\subseteq A^c\\|C|=k}}p_{vC},
 \qquad M_j(A)=|A|{ |A^c|\choose j},\qquad B_0=0.
\]

Stationarity of the number of `k`-subsets of holes gives

\[
 E_\pi(B_k+B_{k-1})=E_\pi M_{k-1},               \tag{18}
\]

and hence

\[
 E_\pi B_k
 =E_\pi\sum_{j=0}^{k-1}(-1)^{k-1-j}M_j.         \tag{19}
\]

Substitution of the exact complete Green coefficients gives, for every
integer `1<=a<=n-1`,

\[
 \begin{split}
 &a\sum_{k=1}^{n-1}c_k\left[
 {2k\over n-1+k}{n-a\choose k}
 -\sum_{j=0}^{k-1}(-1)^{k-1-j}{n-a\choose j}
 \right]\\
 &\hspace{35mm}=\rho_{\rm dB}(K_n,2)-{a\over n}. \tag{20}
 \end{split}
\]

Equations (17)--(20) prove the invariant collapse

\[
 \boxed{
 \mathcal V-\mathcal L
 =\rho_{\rm dB}(K_n,2)-{E_\pi|A|\over n}.}       \tag{21}
\]

This is consistent with the coverage representation of fixation, but (20)
shows explicitly that the entire transport cost and work reduce, with no
slack, to one rank statistic.  The universal theorem is therefore also
exactly the stationary-size inequality

\[
 \boxed{
 E_\pi|A|\le
 { (n-1)2^{n-2}\over2^{n-1}-1}.}                 \tag{22}
\]

The right side is the mean size under the complete dual.  Inequality (22)
remains **OPEN**.

## 4. Why a full event-KL charge cannot close

Normalize the event rows by

\[
 \tau_A(B)={T_P(A,B)\over|A|},\qquad
 \kappa_A(B)={T_K(A,B)\over|A|}.
\]

The natural rowwise event entropy is

\[
 \mathscr K=E_\pi\{|A|D(\tau_A\Vert\kappa_A)\}.
\]

Pinsker gives the exact rational lower bound

\[
 \mathscr K\ge \mathscr P
 :=E_\pi {2\over|A|}
 \left\{ {1\over2}\sum_B|T_P(A,B)-T_K(A,B)|\right\}^2.       \tag{23}
\]

Already on the two frozen rational witnesses,

\[
\begin{array}{c|cc}
 &\mathscr P&\mathcal V\\ \hline
\text{path }(1,2)&8051/18000&8/135\\
\text{regular weighted }K_4&65753/774900&247/22960.
\end{array}                                                     \tag{24}
\]

In both rows `P>V` exactly.  Hence a log-sum argument which first charges
the *entire* event KL to `V` cannot close.  A successful entropy argument
would have to retain the signed compensation in (12), or project the event
law to the particular hit marginals in (14); a generic Pinsker or full-KL
absorption loses far too much.

Even inserting one graph-independent scalar cannot repair the analogous
full event chi-square sandwich.  If

\[
 \mathscr X=E_\pi\sum_{A,B}{(T_P(A,B)-T_K(A,B))^2\over T_K(A,B)},
\]

then the regular weighted `K4` would require

\[
 \alpha\ge {\mathcal L_{K_4}\over\mathscr X_{K_4}}
 \simeq0.042318852,
\]

whereas the exact six-vertex split witness would require

\[
 \alpha\le {\mathcal V_6\over\mathscr X_6}
 \simeq0.025064992.
\]

The verifier checks the strict crossing by rational arithmetic.  Thus no
universal `L<=alpha X<=V` proof exists.  This does not exclude a
state-dependent or genuinely compensated divergence.

## 5. Minimal remaining obstruction

The local cost `v(A)` is the explicit Green-weighted tangent remainder

\[
 \sum_{x\in A}\sum_{k=1}^{|A^c|}
 c_k{2\over(1+k/(n-1))^2}
 \sum_{\substack{C\subseteq A^c\\|C|=k}}
 {\{P_{xC}-k/(n-1)\}^2\over1+P_{xC}}.            \tag{25}
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
 v(A)-(Q_K-Q_P)\psi(A)                           \tag{26}
\]

can be negative.  Hence the remaining theorem is precisely:

> Prove that the coupled sourcewise centering and global conservation in
> (5), (8), together with vertex reversibility, make the aggregate work in
> (12) no larger than the subset-mass cost (25).

Equivalently, after the exact rank collapse, the current **MINIMAL OPEN
OBSTRUCTION** is (22): show that reversibility of the underlying vertex
kernel prevents the stationary geometric-union dual from having larger mean
cardinality than the complete dual.  The transport formulation retains more
local information, while (22) is the sharpest scalar invariant statement.

## 6. Bounded hostile search

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

An additional broad pass evaluated 1,200 complete-support and 1,000 sparse
six-vertex graphs, followed by local optimization, and 1,000
complete-support plus 700 sparse seven-vertex graphs, followed by three
local optimizations.  Again no positive direct gap appeared.  The strongest
random seven-vertex value was about `-7.08e-4`; every polished full-support
candidate converged to the complete graph with gap at floating roundoff.
This remains **NUMERICAL EVIDENCE ONLY**.

The deterministic exact screen independently checks all 54 connected
three-vertex graphs with weights in `{0,1,2,5}`, all 624 connected
four-vertex graphs with weights in `{0,1,2}`, 48 fixed seeded sparse/extreme
five-vertex integer graphs, and the frozen six-vertex split witness.  No
`L>V` graph occurs in that finite list.  This is **EXACTLY COMPUTED FINITE
VALIDATION**, not a universal theorem.

## 7. Verification

Run

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B verify_fisher_route.py
```

The exact verifier constructs both uncentered event kernels independently,
checks (2)--(5), checks the actual-flow balance and zero work in (11), and
certifies (12)--(17) and the exact Pinsker lower bounds (24) on the frozen
rational witnesses.  It also replays the exact undirected six-vertex
refutation of the discarded symmetric split.

Run

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B verify_direct_flow_screen.py
```

for the deterministic exact finite screen described above.

`search_direct_gap.py` and `search_symmetric_split.py` are floating-point
discovery programs, not proof certificates.
