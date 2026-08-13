# One-active certified-degree continuation without structural exits

**Proof-first analytic lemma, 2026-08-12 PDT.**  This note records the exact
finite continuation that removes the structural-exit branch from the
corrected S-superlevel episode in a one-active tier.  It uses only the
definition of the certified superlevel, binaryity, and the marked all-clock
identity.  It does not enumerate orientations, populations, or histories.

**Nondependency notice.**  The final outside-mixed composition does not use
this lemma.  Its one-active branch instead invokes the complete audited
symbolic exhaustion, including Q, invariant, B/B, and B/F0 alternatives.
This note is retained only as a correct auxiliary observation.

## 1. Certified source degree

Fix a one-active descriptor with active species \(X\).  Its primitive tier
weight has zero inactive coordinates, so the D-level of a complex is exactly
its active degree

\[
                              d_X(y)=y_X\in\{0,1,2\}. \tag{1.1}
\]

Let \(E\) be the global top stochastic source tier and let \(r\) be its
D-level.  For a linkage \(L\), the corrected superlevel is

\[
                   U_L(r)=\{y\in L:d_X(y)\ge r\}.     \tag{1.2}
\]

The corrected cut passes precisely when, for some linkage,

\[
              \varnothing\ne U_L(r)\subsetneq L,
              \qquad U_L(r)\subseteq E.              \tag{1.3}
\]

Choose the first edge \(e:y\to z\) on a directed path leaving \(U_L(r)\).
Then

\[
                  y\in E,\qquad d_X(z)<r\le d_X(y).  \tag{1.4}
\]

In particular, a pass is impossible at \(r=0\), because then \(U_L(0)=L\).
Every successful certified edge strictly lowers the integer active degree.

## 2. The continued all-clock rule

At a physical marked state \((x,t)\), take one ordinary all-clock jump.
If it is not the certified label \(e\), stop at the actual endpoint and
actual target.  If \(e\) fires, arrive at the actual marked state
\((x-y+z,z)\) and apply the following priority **before taking another
jump**.

Do **not** stop on a cap, tier, enabled-support, or active-set label change.
At that state, apply the following priority.

1. If the carried source \(z\) is rare, take one ordinary payoff jump and
   stop.
2. If the new descriptor is one-active and passes, choose its certified
   edge and continue the same rule.
3. If it is a B/B or B/F0 failure start, invoke the unconditional B/B or
   cap-free B/F0 completion from the actual mark.
4. If a second coordinate has become asymptotically active, invoke the
   unconditional two-active AA theorem from the actual mark.
5. If the process enters a closed invariant reduction, use its classwise
   recurrence theorem.

The reaction which creates a new mark is the terminal jump of the preceding
stage and is never counted again.

## 3. Termination after at most two successful pass edges

On a nonrare successful pass continuation, (1.4) replaces the current
active source degree \(r\) by a strictly smaller integer.  Binaryity gives

\[
                              2\longrightarrow1\longrightarrow0. \tag{3.1}
\]

At degree zero the corrected superlevel is the whole linkage, so another
pass is impossible.  Hence the rule uses at most two successful certified
edges before reaching a rare actual target or one of items 3--5.

Competitors do not create an uncharged branch.  At each stage, the one-jump
marked identity

\[
 D(x,t)=\log p_t-\sum_qp_q\log p_q-\log K_t+\sum_qp_q\log K_q
       \le\log p_t+C                                  \tag{3.2}
\]

already includes every competitor.  If \(a_i\) denotes the designated-label
probability, the exact recursion remains

\[
                         J_i=D_i+a_iJ_{i+1}.           \tag{3.3}
\]

Since each certified source lies in \(E\), \(a_i\ge a_*>0\).  At the first
rare carried source, (3.2) tends to minus infinity; all later positive terms
are multiplied by its source probability.  If no carried source becomes
rare, (3.1) forces entrance into an unconditional failed branch or a
classwise invariant reduction after at most two successful edges.

For the exact outside-mixed 18,496-pair universe, the frozen failure
certificate makes this endpoint list literal.  Every feasible one-active
failed descriptor is B/B or B/F0; every feasible two-active failed
descriptor is AA; there is no failed all-active descriptor.  A feasible
descriptor outside those rows passes the corrected cut.  Hence repeated
application of this section cannot produce an unnamed failure type.

## 4. Exact scope

This lemma proves a finite **one-active continuation skeleton**, not by
itself a global recurrence theorem.  Its item 3 requires the cap-free B/F0
theorem; item 4 requires the frozen unconditional AA local contract; and a
final common-potential theorem must verify that every exact failure endpoint
falls into those analytic domains.  The point proved here is narrower and
load-bearing: no passing one-active trace can circulate forever through
descriptor exits, because the certified successful edge strictly lowers the
integer active degree.
