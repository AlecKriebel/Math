# Exact weak-coupling refutation of active-rank PCDF

Date: 2026-08-08 (America/Los_Angeles)

## Result

The residual active-rank conjecture

\[
 \Pr_q\{K\le j+1\}\ge
 \Pr_{q^K}\{K\le j+1\},\qquad j\ge1,               \tag{PCDF}
\]

is **EXACTLY FALSE**, even for connected loopless reversible kernels coming
from undirected rational edge weights.  The counterexample is a singularly
coupled graph on fifteen vertices.  Its strict limiting defect is

\[
 \Pr_{q_*}\{K\le2\}-\Pr_{q^{K_{15}}}\{K\le2\}
 =-{6530729\over10532745216}<0.                    \tag{1}
\]

Consequently `c_1<0` in the factorization `D(t)=(1-t^2)sum c_jt^j` for
every sufficiently small positive coupling.  This closes proposed lemma
`(17a)` in `UNIFORM_PGF_REFUTATION_AND_INTEGRATED_REDUCTION.md`; it cannot be
used with the mean--singleton sign to prove the collision theorem.

## 1. The connected rational graph family

Let `H` be the weighted path

```text
       10       1
  0 -------- 1 --- 2
```

and call vertex `2` its portal.  Take five labelled copies `H_a`,
`1<=a<=5`.  Retain all internal weights and join every pair of portals by an
edge of weight `epsilon`.  Call the resulting graph `G_epsilon`.

For every rational `epsilon>0`, `G_epsilon` is a connected, loopless,
undirected rational weighted graph on `n=15` vertices.  The construction and
all weights are independent of any mutant fitness parameter.

## 2. Exact isolated-module law

At fitness two, when an occupied target rings, delete it and replace it by
the distinct values in `J` independent samples from its replacement row,
where `Pr(J=j)=2^{-j}`.  Build this chain directly on the six nonempty proper
subsets of `H`.  Its exact stationary probabilities are

\[
\begin{array}{c|rrrrrr}
A&\{0\}&\{1\}&\{2\}&\{0,1\}&\{0,2\}&\{1,2\}\\ \hline
\Pi_H(A)&5/12&121/252&1/42&5/252&5/126&5/252.
\end{array}                                           \tag{2}
\]

Thus its rank PGF, mean, and active size-biased PGF are

\[
 H(z)={58\over63}z+{5\over63}z^2,
 \qquad m_H={68\over63},                              \tag{3}
\]

\[
 Q_H(z)={zH'(z)\over m_H}
        ={29\over34}z+{5\over34}z^2.                 \tag{4}
\]

For the portal `p=2`, put

\[
 \alpha=\Pi_H\{p\in A\}={1\over12},
 \qquad s=\Pi_H\{A=\{p\}\}={1\over42}.            \tag{5}
\]

## 3. First-order module chain

At `epsilon=0`, the closed classes are indexed by a nonempty set `S` of
occupied modules.  Conditional on `S`, the occupied modules are independent
with law `Pi_H`.  States containing a full local module are transient at
zero coupling and carry no limiting stationary mass.

Fix one occupied source module and one empty destination module.  Write
`delta` for the one-sample probability of that specified destination portal;
`delta=epsilon+O(epsilon^2)` because the portal has internal weighted degree
one.  If the source portal is occupied and its local set is not the portal
singleton, the probability of hitting the destination is

\[
 1-E(1-\delta)^J={2\delta\over1+\delta}
 =2\delta+O(\delta^2).                               \tag{6}
\]

If the local set is the portal singleton, both an internal sample and the
specified external portal are needed to colonize without losing the source.
Inclusion--exclusion gives coefficient `3/2`.  Hence the averaged
colonization coefficient is

\[
 b=2(\alpha-s)+{3\over2}s=2\alpha-{s\over2}.         \tag{7}
\]

Conversely, a portal singleton is lost into one specified already occupied
module when every sample is external.  Since

\[
 E\delta^J={\delta\over2-\delta}
 ={\delta\over2}+O(\delta^2),                        \tag{8}
\]

the corresponding loss coefficient is `d=s/2`.  Thus the reduced odds are

\[
 R={b\over d}={4\alpha\over s}-1=13.                \tag{9}
\]

For `S` of size `k` and a module `x notin S`, the first-order rates between
`S` and `S union {x}` are proportional to `k b` and `k d`, respectively.
Therefore the reduced module chain is reversible with stationary weights

\[
                         \widehat\Pi(S)\propto R^{|S|}.              \tag{10}
\]

The remaining first-order moves replace one portal-singleton module by one
empty module.  Their forward and reverse coefficients are both `d`, so they
also satisfy detailed balance for (10).

Equivalently, modules are iid occupied with probability `13/14`, conditioned
on at least one being occupied.  Write

\[
                         a={1\over14}                              \tag{11}
\]

for the vacancy probability.

For completeness, (10) is also the standard finite-state singular
perturbation conclusion.  It follows directly here by expanding the exact
transition matrix as `P_epsilon=P_0+epsilon L+O(epsilon^2)`, averaging `L`
between the finitely many closed classes of `P_0`, and using the detailed
balance calculation above.  The zero-coupling reduced chain is irreducible
on nonempty module sets.  Hence the unique stationary law of
`G_epsilon` converges to (10), with independent `Pi_H` laws inside occupied
modules.

This conclusion can alternatively be read from the Markov-chain tree
formula: retain the lowest nonzero power of `epsilon` in every rooted tree.
Both arguments also prove continuity of every stationary rank probability
at the displayed limit.

## 4. Exact active-CDF defect

Let

\[
 g(z)=a+(1-a)H(z).
\]

The limiting proper-subset PGF is

\[
 {g(z)^5-a^5\over1-a^5}.
\]

Size biasing by the total rank cancels the conditioning factor and gives the
limiting active PGF

\[
                         Q_*(z)=Q_H(z)g(z)^4.         \tag{12}
\]

Extracting its first two coefficients using (3)--(4) and `a=1/14` gives

\[
 \Pr_{q_*}\{K\le2\}
 ={44803\over41143536}.                              \tag{13}
\]

For the complete graph on fifteen vertices, the active law is
`1+Bin(13,1/2)`, so

\[
 \Pr_{q^{K_{15}}}\{K\le2\}
 ={1+13\over2^{13}}={7\over4096}.                   \tag{14}
\]

Subtracting (14) from (13) proves (1).  In the coefficient normalization of
the earlier PGF note,

\[
 \lim_{\epsilon\downarrow0}c_1(G_\epsilon)
 =-{6530729\over21065490432}<0.                     \tag{15}
\]

The defect is strict.  Stationary probabilities for every positive
`epsilon` are rational functions of `epsilon` (by Cramer's rule or the tree
formula), and their one-sided limits are (12).  Therefore there is an
`epsilon_0>0` such that (15) remains negative for every
`0<epsilon<epsilon_0`.  In particular, choosing any rational epsilon in
that interval gives a finite connected rational counterexample.  This is an
exact existence proof, not a sampled-fitness or floating-point inference.

## 5. What remains

This example does **not** refute the separate mean--singleton inequality

\[
                         N+\pi_1-2m\ge0.             \tag{MS}
\]

Indeed, its exact zero-coupling limit is

\[
 14+\pi_{*,1}-2m_*
 ={1151848\over289597}>0.                           \tag{16}
\]

Thus the status after this refutation is:

- stationary uniform PGF order: **EXACTLY REFUTED**;
- derivative/likelihood-ratio shortcuts: **EXACTLY REFUTED**;
- active PCDF away from the singleton cut: **EXACTLY REFUTED**;
- mean--singleton sign `(MS)`: **OPEN**;
- the weighted integrated collision sign: **OPEN**.

The next useful statement must control the weighted aggregate in the exact
collision identity, not each active CDF cut separately.

## 6. Replay

Run

```text
.venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/r2_pgf_order/verify_weak_module_pcdf_refutation.py
```

The verifier independently constructs (2) from the update rule, checks its
stationarity, checks the reduced detailed balance, derives (12), certifies
the exact negative numerator in (1), and checks (16).
