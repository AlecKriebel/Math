# The feasible two-active gate: promotion versus a closed fast phase

## 1. Scope and exact result

This note classifies every affine-stoichiometrically feasible failed tier
descriptor having exactly two divergent coordinates in the residual
two-linkage table.  It does **not** infer recurrence from the words
"promotion" or "closed phase."  Those words identify the next analytic
mechanism and the precise uniform estimate it still needs.

There are

\[
 2388
\]

such pair--descriptor incidences, carried by 1036 support pairs (996 from
the positive-invariant table and 40 from the signed table).  The disjoint
incidence split is

\[
\begin{array}{l|r|r|r|r}
\text{mechanism}&\text{incidences}&\text{pairs}&\text{positive}&\text{signed}\\ \hline
\text{proper top set with an enabled top seed}&963&584&552&32\\
\text{proper top set wholly dormant}&453&367&333&34\\
\text{closed rank-one top phase}&930&310&308&2\\
\text{coupled rank-two top phase}&42&14&14&0
\end{array}                                                \tag{1.1}
\]

The pair columns overlap because one support pair can fail at several
descriptors.  The union has 1036 pairs; the flat-phase and promotion unions
overlap in 91 pairs.  The fingerprint of all incidences, including pair,
weight, caps, and category, is

```text
908c15311c0d1240a8c79b0fb4b922ec1d33b9a497ffb7484be258a19d136273
```

The classification is exact support geometry.  It is evaluated only after
the affine feasibility filter, so an impossible flag is not counted here.

## 2. Definitions

Fix a feasible two-active descriptor with primitive weight

\[
 w=(w_1,w_2,w_3),\qquad w_i,w_j>0,\quad w_k=0,             \tag{2.1}
\]

where coordinate \(k\) is the nominally bounded coordinate.  Let
\({\cal T}\) be the network-restricted top D-tier.  For a linkage support
\(L\), put \(K_L=L\cap{\cal T}\).

Here and below, “realizes a descriptor” means the **exact D-tier
partition**, not only convergence of normalized logarithmic coordinate
weights.  Thus, for complexes \(y,z\) in one displayed tier,

\[
 { (x_n\vee1)^y\over (x_n\vee1)^z}\longrightarrow c_{yz}
 \quad\text{for some }c_{yz}\in(0,\infty),                \tag{2.2}
\]

and ratios between ordered tiers tend to zero or infinity in the displayed
direction.  For example, \(A_n=n/\log n\), \(B_n=n\) does not realize the
flat tier containing \(2A,A+B,2B\): its ratio
\(AB/(A)_2\sim\log n\) splits that tier and belongs to a proper-top
descriptor.  This distinction is load-bearing in the occupation estimates.

There are two mutually exclusive support modes.

1. **Proper-top mode.**  Some \(K_L\) is nonempty and proper in \(L\).
   The incidence is *seeded* if at least one complex in one such \(K_L\)
   is enabled at the descriptor cap, and *dormant* otherwise.
2. **Flat-top mode.**  Each linkage is either wholly in \({\cal T}\) or
   disjoint from it.  The finite certificate proves that exactly one
   linkage is wholly in \({\cal T}\).  Call it \(L_*\), and classify the
   incidence by the rank of its stoichiometric difference space.

All 1416 proper-top incidences have bounded-coordinate cap zero.  In the
972 flat incidences, each of caps zero, one, and two occurs 324 times.

## 3. The exact promotion path

The word promotion has the following limited, rigorous content.

> **Lemma 3.1 (carried support path).**  Give a proper-top linkage \(L\)
> any strongly connected orientation.  Suppose its top set \(K_L\) has an
> enabled vertex \(u\), and suppose the oriented network has no enabled
> top-tier source with an edge from \(K_L\) to \(L\setminus K_L\).  Then
> an oriented path from \(u\) to \(L\setminus K_L\) contains, before its
> first exit, a target whose bounded-coordinate requirement exceeds the
> original cap.  If the path reactions occur consecutively, each target is
> an actual physical source for the next reaction and the bounded
> coordinate is promoted before the top-tier exit.

To prove the lemma, choose an oriented path from \(u\) to the complement,
which exists by strong connectivity.  If every source on the prefix through
\(K_L\) were enabled at the original cap, its final source would be an
enabled top source with a descending edge.  Hence the first initially
disabled vertex appears as the target of a reaction whose source precedes
it on the path.  Since all three-species complexes have molecularity at
most two and only coordinate \(k\) is capped, initial disability means
that this target contains more copies of species \(k\) than the cap.
Producing the target makes it physically available for the next path step.

Lemma 3.1 is a reaction-path statement, not a probability bound.  Other
reactions can interrupt the carried prefix.  A valid stochastic theorem
must bound those interruptions on a physical clock and charge their
endpoints.  In the 453 dormant incidences no top seed exists at all; a
lower source layer must first create species \(k\).  This is exactly the
activation case in which tightness cannot be replaced by a finite box.

## 4. The flat mode really is a closed phase

> **Proposition 4.1 (rank-one top-shell reduction).**  In each of the 930
> rank-one flat incidences, suppressing the lower linkage leaves a
> weakly reversible CTMC on a one-dimensional affine stoichiometric class.
> The weighted workload
> \[
> H_w(x)=w\cdot x                                             \tag{4.1}
> \]
> is exactly invariant under this top linkage.  Every population class of
> the top-only chain is finite, and therefore every one of its closed
> irreducible components is positive recurrent.  No bounded box for the
> inactive coordinate is assumed.

Indeed, every complex of \(L_*\) lies in one D-tier, hence
\(w\cdot(y'-y)=0\) for every top reaction.  The support difference space
has rank one, and strong connectivity makes the reaction network weakly
reversible.  The certificate additionally checks that its primitive
stoichiometric direction is never supported only on the inactive
coordinate.  Since \(w\) is strictly positive on both active coordinates,
the nonnegativity constraints and fixed value of \(H_w\) bound the integer
parameter along the stoichiometric line.  Thus a top shell is finite even
though its size may grow with \(H_w\).

The eight possible rank-one top supports in the fixed coordinate convention
are

\[
\begin{gathered}
 \{2A,2B\},\ \{2A,A+B\},\ \{2B,A+B\},\
 \{2A,2B,A+B\},\\
 \{B,2A\},\ \{2A,B+C\},\
 \{2A,2C,A+C\},\ \{2B,2C,B+C\}.             \tag{4.2}
\end{gathered}
\]

This proves exact closedness, but not the uniform estimate needed by the
full network.  Finiteness of each moving shell does not bound, uniformly in
the shell, either a killed hitting time or the occupation of a lower-linkage
source.

There is a useful exact refinement of the 930 incidences:

\[
\begin{array}{l|r|r}
\text{lower-layer status}&\text{incidences}&\text{pairs}\\ \hline
\text{maximal lower source already enabled}&893&310\\
\text{top phase itself creates the inactive species}&2&2\\
\text{a strictly lower source must activate it}&25&25\\
\text{both lower and inactive-changing top reactions are off}&10&10
\end{array}                                                \tag{4.3}
\]

The pair columns again overlap.  The last row is not a stochastic-tail
problem.  At cap zero every complex of the lower linkage contains the
inactive species, so that linkage is identically disabled; the rank-one top
linkage preserves the inactive coordinate.  Proposition 4.1 then confines
the class to a finite top shell.  Thus those ten *incidences* cannot be an
escaping flag in a fixed communication class.  This does not certify all
ten support pairs, because the same pair may have other feasible failed
descriptors.

### 4.1 Reachability-aware pair composition

It is tempting to combine the last row of (4.3) with the affine and
one-active branches and announce ten more recurrent support pairs.  The
exact pair filter rules this out.

The affine branch first removes 151 pairs.  Among the rest, 1227 pairs have
only one-active **affine-feasible** failures.  The ordered branches are
disjoint, so their union contains 1378 pairs (1219 positive and 159 signed)
and leaves 1133.  On those remaining pairs, delete the one-active
descriptors and ask whether every feasible
multi-active failure is one of the ten zero-boundary incidences.  The exact
answer is

\[
 \boxed{0\text{ support pairs}.}                           \tag{4.4}
\]

Every one of the ten pairs also has a feasible cap-one or cap-two
two-active failure; several also have all-active failures.  Hence the
finite-boundary observation is a valid descriptor elimination but gives no
new pair-level closure by itself.  The executable result is deliberately
labelled a selector: composing descriptor-level stochastic theorems still
requires a common random-time Foster argument.

The published one-dimensional weak-reversible recurrence theorem is
consistent with Proposition 4.1, but its qualitative positive-recurrence
conclusion does not supply the shell-uniform killed resolvent or endpoint
moments required here.  In particular it cannot justify replacing these
growing shells by one fixed finite phase.

### 4.2 A killed occupation estimate that does hold

The first part of the required resolvent estimate can be proved without a
stationary start.  It is useful to state it separately so that the remaining
carrier problem is not confused with fast-phase mixing.

> **Proposition 4.2 (one-clock killed occupation).**  Let \(x_n\) realize
> one of the 893 rank-one flat descriptors for which a maximal lower source
> is enabled at the displayed cap, and let \(L_*\) and \(L_-\) denote
> respectively its top and lower linkages.  Put
> \[
> a_n=\max_{y\in L_-}(x_n\vee1)^y.                         \tag{4.5}
> \]
> The certificate checks that the maximal lower active weight is one in
> all 930 incidences, so \(a_n\to\infty\).  Let \(y\) be an enabled
> maximal lower complex.  Run only the top
> linkage, writing \(\widehat X^{(n)}\) for that chain.  After passage to a
> subsequence, there are \(T,\eta,p>0\) such that
> \[
> \mathbb P_{x_n}\left\{
>   \int_0^{T/a_n}(\widehat X^{(n)}_t)_y\,dt\ge\eta
> \right\}\ge p                                           \tag{4.6}
> \]
> for all large \(n\).  The same conclusion holds in the two incidences
> where \(L_*=\{2A,B+C\}\) first creates the missing cofactor, with \(y\)
> evaluated after that creation.  On these windows \(H_w\) is pathwise
> constant, the scaled active endpoint has moments of every fixed order,
> and the inactive endpoint either is constant or has uniformly bounded
> exponential moments.

Thus the proposition covers exactly the 893 seeded incidences and the two
top-activation incidences in (4.3).  It makes no occupation claim for the
25 incidences requiring a strictly lower activation layer or for the ten
identically disabled cap-zero incidences.

Consequently, if a single lower channel with source \(y\) and rate
\(\kappa>0\) is installed as a killing clock, then its probability of
ringing by \(T/a_n\) is bounded below:

\[
 1-\mathbb E\exp\left{-\kappa
       \int_0^{T/a_n}(\widehat X^{(n)}_t)_y\,dt\right}
 \ge p(1-e^{-\kappa\eta}).                                \tag{4.7}
\]

Here is a proof which exposes every scaling.  There are only three dynamic
templates, up to relabelling.

1. If \(L_*\subseteq\{2A,A+B,2B\}\), or its \(A,C\) or
   \(B,C\) version, its invariant shell has size \(N\) and
   \(a_n\asymp N\).  On time \(\tau=Nt\), the active fraction converges
   from every descriptor-compact initial ratio to
   \[
    \dot z=\sum_{u\to v}\kappa_{uv}(v_A-u_A)
              z^{u_A}(1-z)^{u_B}.                         \tag{4.8}
   \]
   The right side is quadratic.  Strong connectivity makes it point
   inward at every accessible endpoint; if all sources share a common
   active factor, descriptor compactness keeps the solution away from the
   factor-zero boundary.  Thus the solution remains in a compact interior
   interval on \([0,T]\).  The density martingale has quadratic variation
   \(O(N^{-1})\).  Every enabled maximal lower source contains one active
   molecule, so its propensity divided by \(a_n\) converges to a strictly
   positive continuous function of \(z\).  This proves (4.6).
2. For \(L_*=\{B,2A\}\), top-tier equivalence gives
   \(B\asymp A^2\).  With \(N\asymp A\) and \(\tau=Nt\),
   \(A/N\) converges to the Riccati equation
   \[
      \dot z=2\kappa_{B,2A}b-2\kappa_{2A,B}z^2,           \tag{4.9}
   \]
   where \(b=\lim B/N^2>0\).  Its solution is positive for every positive
   descriptor limit, the martingale quadratic variation is \(O(N^{-1})\),
   and a maximal lower source is \(A\) or \(A\) times one fixed cofactor.
3. For \(L_*=\{2A,B+C\}\), the two top reactions are both present and
   the two exact invariants reduce the top chain to a one-dimensional
   birth--death chain.  It is not literally an immigration--death chain
   and has no exact binomial--Poisson representation.  Exact D-tier
   equivalence makes the birth rate comparable to \(A_n^2\) and, up to the
   relevant stop, the death rate comparable to \(A_n^2 I\), where \(I\)
   is the population of the initially missing cofactor.  Upper and lower
   stopped comparisons with immigration--death chains therefore give a
   uniform endpoint exponential moment and positive cofactor occupation on
   the \(T/a_n\) window.  In the two cap-zero activation incidences
   \(a_n\asymp A_n\), and the first birth creates the cofactor at rate
   \(\asymp A_n^2\), so the same comparison proves the asserted
   post-creation occupation.

The stopped martingale estimates in the first two templates and the
explicit domination in the third give the endpoint assertions.  This proof
uses the actual transient chain, not its invariant distribution.

Proposition 4.2 is intentionally a **one-clock** result.  With every lower
channel restored, another maximal lower reaction may ring first and move
the carried source.  Iterating (4.7) requires a finite carrier/resolvent
argument which retains those reactions, while the 25 lower-layer activation
incidences begin below the scale \(a_n\).  Those are the obligations in
Section 6.

## 5. The exact rank-two exception

All 42 rank-two incidences have, in the fixed coordinate convention,

\[
 L_* = \{B,2A,B+C\},                                      \tag{5.1}
\]

and are carried by 14 positive support pairs.  This is not a hidden
one-dimensional phase.  Its top-only stoichiometric rank is two, it
preserves \(q=A+2B\), and its deficiency is zero.  Conditional on \(q\),
its invariant law is the product-Poisson law conditioned on the shell; the
transient dynamics are governed by the exact Riccati coordinate used in
`residual_pair_full_proof.md`.

The 14 lower partners are strongly connected supports inside
\(\{0,A,C,2C,A+C\}\).  The short-window part of the residual proof has a
plausible extension: positive \(q\)-sources have bounded fast-shell mean,
while strong connectivity forces an edge from \(\{A,A+C\}\) to
\(\{0,C,2C\}\), whose averaged negative intensity is of order
\(\sqrt q\).  That observation is not yet a theorem for all 14 pairs.
The existing global return workload was constructed only for
\(\{0,A,C\}\); the extra sources \(2C\) and \(A+C\) add quadratic and
mixed terms and invalidate its pointwise identity.  A new proper return
potential, with endpoint moments, is the first exact obligation before the
Riccati window can be reused.

The short-window assertion can in fact be made exact.

> **Proposition 5.1 (the Riccati window extends to all 14 partners).**  On
> a core with \(q=N\), \(A=O(\sqrt N)\), and a bounded exponential moment
> for \(C\), run the full chain for \(T/\sqrt N\).  For every one of the 14
> lower supports and every strongly connected orientation, the \(q\)-drift
> has a strictly negative limit, uniformly over core initial states.

To see this, split the lower complexes into

\[
 E_0=\{0,C,2C\},\qquad E_1=\{A,A+C\}.                    \tag{5.2}
\]

Every lower partner meets both sets, as the certificate checks.  Strong
connectivity forces an edge from \(E_1\) to \(E_0\).  If \(d_A\) is the
sum of rates on such edges sourced at \(A\), and \(d_{AC}\) the analogous
sum at \(A+C\), then

\[
 d_A+d_{AC}>0,
 \qquad
 {\cal L}_-q=g_+(C)-A(d_A+d_{AC}C),                       \tag{5.3}
\]

where \(g_+\) is a nonnegative polynomial of degree at most two.  The fast
linkage has the same exact Riccati coordinate as in the residual-pair
proof.  On accelerated time \(\tau=\sqrt N t\),

\[
 {A\over\sqrt N}\longrightarrow z,qquad
 \dot z=\alpha-\beta z^2.                                \tag{5.4}
\]

The fast \(C\)-generator at frozen \(z\) is immigration--death with mean

\[
 m(z)={y+2rz^2\over d}.                                   \tag{5.5}
\]

Here are the transient estimates needed to justify that statement with all
lower reactions retained.  Stop when \(q\notin[N/2,2N]\) or
\(A>2K\sqrt N\).  Then \(B\ge N/8\) for all large \(N\).  A lower reaction
sourced at \(2C\) cannot increase \(C\), because no target in
\(\{0,A,C,2C,A+C\}\) contains more than two copies of \(C\).  The total
\(C\)-birth intensity is bounded by

\[
 K_0N+K_1\{1+\sqrt N+(1+\sqrt N)C\},                    \tag{5.6}
\]

where the order-\(N\) term contains the fast immigration channels and the
second term contains every lower-linkage birth.
The fast death intensity contains \(dBC\ge(d/8)NC\).  Hence the stopped
process is dominated by a linear birth--death--immigration chain with
immigration \(b_0N\), per-particle birth \(b_1\sqrt N+b_2\), and
per-particle death \((d/8)N\).  For large \(N\) the death/birth ratio is
uniformly separated from one; the explicit branching-with-immigration
generating function (and a harmless finite adjustment for \(N<N_0\)) gives,
from every core start and for every sufficiently small \(\eta>0\),

\[
 \sup_N\sup_{\tau\le T}
 \mathbb E\exp\{\eta C(\tau/\sqrt N)\}<\infty.            \tag{5.7}
\]

For the accelerated generator \(G_N={\cal L}/\sqrt N\), use the scaled
linear corrector

\[
 h_N(C)={2C\over d\sqrt N},\qquad
 m_N={yB+r(A)_2\over dB}.                                \tag{5.8}
\]

The fast linkage then satisfies the exact identity

\[
 G_Nh_N={2B\over N}(m_N-C)+R_N,                           \tag{5.9}
\]

where \(R_N\) is the lower-linkage contribution.  Since lower jumps are
bounded and their sources lie in \(\{0,A,C,2C,A+C\}\), on the stop

\[
 |R_N|\le K\left\{N^{-1}+{1+C\over\sqrt N}
                      +{(C)_2\over N}\right\}.           \tag{5.10}
\]

The exponential bound (5.7) therefore gives
\(\int_0^T\mathbb E|R_N|\,d\tau=o(1)\).  Moreover
\(2B/N\to1\), \(m_N\to m(z)\), the endpoint difference of \(h_N\) tends
to zero in \(L^1\), and its martingale has quadratic variation
\(O(N^{-1/2})\).  Dynkin's formula therefore yields

\[
 \int_0^T\{C(\tau)-m(z(\tau))\}\,d\tau
       \longrightarrow0\quad\hbox{in }L^1.               \tag{5.11}
\]

Therefore

\[
 \mathbb E\{q(X_{T/\sqrt N})-q(X_0)\}
 \longrightarrow
 -\int_0^Tz(\tau)\{d_A+d_{AC}m(z(\tau))\}\,d\tau<0.    \tag{5.12}
\]

The inequality is strict uniformly over bounded nonnegative initial
\(z\).  If \(d_A>0\), use the minimal Riccati solution from zero.  If
\(d_A=0\), then \(d_{AC}>0\); strong connectivity of the fast linkage gives
either \(y>0\), or \(r>0\) when \(y=0\), so
\(z(\tau)m(z(\tau))>0\) for every \(\tau>0\).  The positive term
\(g_+(C)/\sqrt N\) vanishes by the exponential moment.  The same bounds
give all fixed moments of the number of \(q\)-changes in the window.
Riccati martingale bounds and the bounded \(q\)-change count make the
probability of the stop super-polynomial; the exponential \(C\)-moment and
the total-population Yule bound remove it.  (A bimolecular source cannot
increase total population in a binary network; every population-increasing
intensity is at most affine.)  Thus no
stationary start or deleted lower channel is hidden in (5.11).

Proposition 5.1 starts from the displayed core.  It does not return an
arbitrary state to that core.  Sources \(2C\) and \(A+C\) prevent simply
reusing the linear workload identity of the three-complex partner.  Thus
the global-return obligation stated above remains load-bearing despite the
now-complete short-window calculation.

## 6. Smallest missing analytic theorem

For the rank-one branch, the needed statement is the following; it is
recorded as a target, not asserted.

> **Uniform killed rank-one phase lemma (open).**  Let \(L_*\) be any of
> (4.2), in any strongly connected orientation with fixed positive rates,
> and let the second linkage be one of the certified compatible supports.
> Along any feasible two-active descriptor sequence, run the full CTMC on
> the \(H_w\)-clock until the first lower-linkage reaction or until the
> bounded coordinate reaches the next descriptor scale.  Prove a uniform
> alternative:
>
> 1. a descending lower reaction occurs with conditional probability at
>    least \(p>0\), and the episode has uniformly integrable physical
>    duration and workload endpoint cost; or
> 2. the bounded coordinate is promoted to a feasible higher-active
>    descriptor, with an endpoint moment bound that can be charged by the
>    higher-level Foster episode.

The smallest unresolved part is lower-source occupation in a growing
rank-one shell.  Per-shell recurrence is insufficient: one must control the
killed occupation measure uniformly from the actual target state, including
arbitrarily slow separation between adjacent source-rate tiers.  The 453
dormant incidences additionally require a lower-layer activation bound.

For the rank-two branch, the separate missing lemma is a proper return
potential for (5.1) with each of its 14 lower partners.  Until these two
estimates are proved, (1.1) is a rigorous structural reduction and not a
positive-recurrence result.

## 7. Reproduction

Run

```text
PYTHONPATH=src python3 -B src/two_active_phase_gate.py
PYTHONPATH=src python3 -B -m unittest tests/test_two_active_phase_gate.py -v
```

The test rechecks all 2388 incidences against the complete tier and affine
feasibility certificates, validates the unique flat linkage and its exact
rank, freezes the counts and incidence hash, and verifies the unique
rank-two support.
