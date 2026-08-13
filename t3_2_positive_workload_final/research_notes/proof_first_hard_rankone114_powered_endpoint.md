# The powered rank-one endpoint on the hard 114 rows

**Proof-first scoped corollary, 2026-08-12 PDT. Audit status: pending.**
This note applies the audited corrected-factorial rank-one endpoint and its
audited positive-overshoot strengthening to every closed rank-one
two-active row on the hard 333 pairs.  The finite table is used only to
verify the structural input and the common-correction compatibility.

## 1. Scope and one potential

There are 114 such incidences on 38 pairs.  Their activation split is

\[
 110\ \text{lower-top seeded},\qquad
 2\ \text{top-phase activation},\qquad
 2\ \text{lower-layer activation}.                 \tag{1.1}
\]

Every top shell is one of the rank-one supports treated in the corrected
factorial endpoint theorem: a reversible two-node shell or a homogeneous
directed triple \(\{2X,X+Y,2Y\}\).  Choose the pair correction \(\ell\)
by detailed balance in the reversible case and by the unique directed-fluid
center in the triple case.  If the pair also has an all-active failed cone,
the whole-top mask is identical there, so this is literally the same
correction in both dimensions.

Put

\[
 G_\ell=K_\ell+\sum_i\log(X_i!)+\ell\cdot X\ge1,
 \qquad W_\ell=G_\ell^4.                            \tag{1.2}
\]

## 2. Corrected-factorial endpoint

For every seeded or top-activation row, the all-reaction carrier theorem
gives a physical stopping time \(\tau\), a divergent exact-tier gap
\(g_n\), an indicator \(I_n\), and a remainder \(Y_n\) such that

\[
 \Delta G_\ell\le-I_ng_n+Y_n,qquad
 \mathbb P(I_n=1)\ge p_0>0,                         \tag{2.1}
\]

while \((Y_n^+)^r\) is uniformly integrable for every fixed \(r\).
The endpoint theorem retains all competing clocks and the actual terminal
reaction.  Its physical duration and population displacement have arbitrary
fixed moments at the stated descriptor scale.

The two lower-layer activation rows use the finite activation block from
the same theorem.  Its reflected workload has a fixed negative service
coefficient, and the factorial conversion gives

\[
                   \mathbb E\Delta G_\ell\le-c\log N.         \tag{2.2}
\]

The shell endpoint again has arbitrary fixed moments.

The positive-overshoot strengthening is load-bearing.  On every shell in
this scope, if \(Z=G_\ell-\min_{\rm shell}G_\ell\), exact convexity and the
inward paired drift give, for some fixed \(\theta>0\),

\[
 {\cal L}_*e^{\theta Z}
     \le-cs_ne^{\theta Z}+Cs_n.                    \tag{2.3}
\]

The same bound holds at the killed carrier endpoints after polynomial
size bias.  Therefore

\[
             \sup_n\mathbb E\{(\Delta G_\ell)^+\}^r<\infty   \tag{2.4}
\]

for every fixed \(r\).  This is stronger than the original first-moment
endpoint statement and is exactly the strengthening independently replayed
in the easy-promotion common-potential theorem.

## 3. Fourth-power lift

In (2.1), \(g_n=o(G_\ell)\); in (2.2), \(\log N=o(G_\ell)\).  The negative
part of a stopped increment has the corresponding fixed moments, while
(2.4) controls every positive Taylor remainder.  Expanding exactly,

\[
 \Delta W_\ell
 =4G_\ell^3\Delta G_\ell
  +6G_\ell^2(\Delta G_\ell)^2
  +4G_\ell(\Delta G_\ell)^3+(\Delta G_\ell)^4,       \tag{3.1}
\]

shows that the leading negative term dominates all other terms.  The
physical duration is lower order.  Consequently

\[
 \mathbb E_x[W_\ell(X_\tau)-W_\ell(x)+\tau]
       \le-cG_\ell(x)^3 h_n,                        \tag{3.2}
\]

where \(h_n=g_n\to\infty\) on direct rows and
\(h_n=\log N\) on the two lower-layer rows.

### Theorem 3.1

Every one of the 114 closed rank-one two-active hard incidences, under every
strong orientation and every fixed positive rate vector, has an
all-reaction physical stopped block satisfying (3.2), with arbitrary fixed
endpoint and duration moments.  It uses the same pair-fixed correction as
the compatible all-active theorem and hence the same physical
\(W_\ell\) at every endpoint reclassification.

This is a local row theorem.  It makes no pair or global recurrence claim
before independent audit and full descriptor composition.

