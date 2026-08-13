# Marked scope and physical-boundary gluing for the hard-317 repair

**Scoped proof note (2026-08-11 PDT; audit pending).**  This note proves the
marked-state and boundary interface needed by the proposed hard-317 theorem.
It contains no atlas enumeration and does not certify a local hard kernel, a
pair, T3-2, or C3.  Its analytic input is a stopped hard-kernel estimate that
retains the boundary-causing reaction and pays the actual endpoint under one
common population potential.  The point proved here is that this input has
the correct scope and glues without an unproved boundary identification.

## 1. Setting and notation

Work in one closed irreducible class \(\Gamma\subseteq\mathbb N_0^d\) of a
binary stochastic mass-action network.  Thus every source and target complex
has molecularity at most two.  Fix a reference population
\(x^\circ\in\Gamma\).  For every species, augment the physical chain by the
reflected mark

\[
 D_i(0)=0,\qquad
 D_i^+=(D_i+\zeta_i)^+                              \tag{1.1}
\]

after a physical reaction with vector \(\zeta\).  Put \(H_i=X_i-D_i\), and
retain the actual mark through every reaction, including reactions hidden by
a physical-state renewal calculation.

The population potential used throughout the hard-317 composition is

\[
 F_\ell(x)=K_\ell+\sum_{i=1}^d\log(x_i!)+\ell\mathbin\cdot x,
 \qquad W_\ell(x)=F_\ell(x)^4,                       \tag{1.2}
\]

where \(\ell\) is fixed for the support pair and \(K_\ell\) is chosen so
that \(F_\ell\ge1\).  No proof mark, chart label, or boundary correction is
added to \(W_\ell\).

In the generalized Family-II chart, use the physical normalization

\[
 U=\hbox{spectator},\qquad V=\hbox{old active species},\qquad
 I=\hbox{top cofactor}.                              \tag{1.3}
\]

The proper linkage contains \(V+I\), no other complex contains \(V\), and
the lower linkage contains no \(V\).  At a no-fast base write

\[
 X=(u,n,0),\qquad R=V-n.                             \tag{1.4}
\]

Before strict service, \(R\ge0\).  A firing sourced at \(V+I\) lowers
\(R\) by one; such a firing from \(R=0\) is strict service.  The local
moving cutoff is

\[
 L(n)=\left\lfloor{n^{1/3}\over\log(n+e)}\right\rfloor.             \tag{1.5}
\]

Only the facts \(L(n)=n^{1/3+o(1)}\), \(L(n)^3/n=o(1)\), and bounded
reaction vectors are used below.

## 2. Reflected scope, properness, and nonexplosion

### Lemma 2.1 (reachable reflected lift)

On every marked state reachable from \((x^\circ,0)\),

\[
 0\le D_i\le X_i,\qquad H_i\le x_i^\circ,             \tag{2.1}
\]

and every \(H_i\) is pathwise nonincreasing.  Moreover
\(\widehat W_\ell(x,d):=W_\ell(x)\) is proper on the reachable marked
space.

#### Proof

Suppose \(0\le D_i\le X_i\) before one jump.  If
\(D_i+\zeta_i\ge0\), then

\[
 D_i^+=D_i+\zeta_i\le X_i+\zeta_i=X_i^+,
 \qquad H_i^+=H_i.
\]

If \(D_i+\zeta_i<0\), physical feasibility gives \(X_i^+\ge0\), while

\[
 D_i^+=0\le X_i^+,qquad
 H_i^+=X_i+\zeta_i<X_i-D_i=H_i.
\]

Induction proves (2.1).  For fixed \(x\), the reachable fiber has at most
\(\prod_i(x_i+1)\) elements because \(0\le d_i\le x_i\).  Finally,
\(\sum_i\log(x_i!)+\ell\cdot x\to\infty\) as \(|x|_1\to\infty\): the
factorial term dominates every fixed linear correction.  Hence physical
sublevels of \(W_\ell\), and therefore their marked lifts, are finite.
\(\square\)

### Lemma 2.2 (zero selected debt is finite in its own chart)

Let a statewise one-active \(V\)-chart require

\[
 I=0,\qquad V\ge N_*,\qquad 0\le U<L(V),              \tag{2.2}
\]

possibly together with finitely many fixed invariant caps.  The part of
this chart in the reachable reflected lift on which \(D_V=0\) is finite.
The same conclusion holds for a fixed-width chart, with \(U<L(V)\)
replaced by membership of the inactive coordinates in a finite
cross-section.

#### Proof

By Lemma 2.1, \(D_V=0\) implies

\[
 V=H_V\le x_V^\circ.                                \tag{2.3}
\]

There are only finitely many integer values of \(V\) in (2.3), and for
each such value (2.2) allows only finitely many values of \(U\).  The
cofactor is zero and the remaining caps range over finite sets.  The mark
fiber over every one of these populations is finite by Lemma 2.1.
\(\square\)

This lemma is deliberately chart-local.  If \(D_V=0\), \(V\) is bounded,
but another coordinate might be large.  Such a state is routed to the chart
for that coordinate; it is not called a finite exception in the unrestricted
state space.  Equivalently, in the usual bad-sequence formulation, a
divergent sequence assigned to a \(V\)-dominant chart must eventually have
\(D_V>0\).

### Lemma 2.3 (binary mass action is nonexplosive)

The physical CTMC, and hence its deterministic reflected lift, is
nonexplosive.

#### Proof

Put \(S(x)=1+|x|_1\).  A reaction which increases \(|x|_1\) cannot have a
bimolecular source, because its target also has molecularity at most two.
Its propensity is therefore bounded by \(C(1+S)\), and its positive jump is
bounded.  Summing the finitely many channels gives

\[
 {\cal L}S(x)\le C S(x).                             \tag{2.4}
\]

Stop on first reaching \(S\ge m\).  Dynkin's formula and Gronwall give
\(\mathbb E S(X_{t\wedge\tau_m})\le S(x)e^{Ct}\), and hence
\(\mathbb P(\tau_m\le t)\le S(x)e^{Ct}/m\).  Thus the population cannot
escape every finite sublevel in finite time.  Inside a fixed \(S\)-sublevel
there are finitely many states and the total reaction rate is bounded, so
even quadratic population-neutral reactions cannot accumulate infinitely
many jumps there.  This proves nonexplosion.  Adding a deterministic mark
to each physical jump creates no new clock and preserves the conclusion.
\(\square\)

## 3. Historical consistency and the no-history face

The positive-debt hypothesis of the hard kernel is not optional.  The next
lemma proves analytically why the supports usually called “no-history” are
vacuous for that hypothesis.

### Lemma 3.1 (an invariant face carries no reachable old-active debt)

Assume that every source complex in the proper linkage contains at least
one \(I\), and every complex in the lower linkage is \(I\)-free.  Then a
reachable marked state on \(I=0\) has \(D_V=0\).

#### Proof

In a nontrivial strongly connected orientation every complex has an
outgoing edge.  Thus the source assumption says that every proper complex
contains \(I\).  A proper reaction cannot fire from \(I=0\).  Every lower
reaction has \(\Delta I=0\), and it also has \(\Delta V=0\) because the
lower linkage contains no \(V\).  Hence the face \(I=0\) is forward
invariant and \(V\) is constant on it.

The face also cannot be entered from \(I>0\).  A proper firing leaves at
least the \(I\)-multiplicity of its target, which is at least one, while a
lower firing preserves \(I\).  Consequently any path ending on \(I=0\)
started on that face and used only \(V\)-preserving reactions.  Since the
reachable lift starts with \(D_V=0\), recursion (1.1) leaves \(D_V=0\)
along the whole path.  A singleton proper linkage has no firing and gives
the same conclusion. \(\square\)

No atlas count is involved: the lemma applies to every support satisfying
its two structural hypotheses.  It also shows exactly why a theorem begun
from an arbitrary unmarked point of this face would be false: the proper
service clock is identically zero there.

### Lemma 3.2 (strict physical service reduces the existing mark)

Start a local chart from \(V=n\) with \(D_V=d>0\).  Suppose the physical
path is stopped at the first firing that takes \(V\) below \(n\), and before
that firing \(V\ge n\).  Then throughout the preterminal path

\[
 D_V=d+V-n,                                          \tag{3.1}
\]

every exact physical return to \(V=n\) restores the selected mark to
\(d\), and the terminal firing \(n\to n-1\) changes the mark to \(d-1\).

#### Proof

The right side of (3.1) is positive before the terminal firing, so
reflection is inactive and (1.1) simply adds the same \(\Delta V\) to both
sides.  At the terminal firing, \((d-1)^+=d-1\). \(\square\)

Thus the local strict-service event is genuinely an old-debt service even
when \(d=1\).  It need not create a surplus below zero.  Other species'
marks may change during a physical self loop; Section 6 explains why this
does not obstruct a population-potential renewal.

## 4. The raw physical boundary partition

The partition must be made on the uncontracted physical path.  At each
no-fast return below the cutoff reset the local reserve to (1.4), retain the
same old-active level \(n\), and begin the next raw attempt.  An open
excursion starts when a firing produces an \(I\)-bearing state and ends at
strict service or the next included no-fast/upward endpoint.  Monitor every
physical firing, including those later erased as part of an exact return.

The phase immediately before a firing is part of the terminal label.  Give
events the following priority after the boundary-causing reaction has
fired.

1. \(D\): a strict service, namely a \(V+I\)-source firing from \(R=0\).
2. \(B\): during an open excursion, the first firing whose endpoint has
   \(U\vee I\vee R\ge L(n)\).  This includes a final cleanup which crosses
   the \(U\)-cutoff and happens to land on \(I=R=0\).
3. \(A\): a below-boundary, service-free return with \(I=0\) and \(R>0\).
4. \(P\): an **outer-base** \(U\)-boundary move, begun on \(I=R=0\),
   which never opens an excursion and ends with \(I=R=0\) and
   \(U\ge L(n)\).

Returns with \(I=R=0\) and \(U<L(n)\) continue the outer base chain.
The ordering makes these events disjoint.  The load-bearing distinction is
therefore

\[
 P\subseteq\{I=R=0\}\quad\hbox{and is outer-base labelled},\qquad
 B=\{\hbox{a boundary caused while the excursion is open}\}.       \tag{4.1}
\]

A \(B\)-endpoint may itself have \(I=R=0\); its path label, rather than
only its final coordinates, keeps it out of \(P\).  For example, an opening
\(0\to U+I\) from \(U=L(n)-1\) lands at
\((U,I,R)=(L(n),1,0)\) and is \(B\).  Likewise, a later cleanup which first
crosses the \(U\)-cutoff is still \(B\), even if its target is no-fast.

### Lemma 4.1 (only \(P\) is the exact promotion handoff)

Let \(b_*\) bound the absolute change of one population coordinate in one
physical reaction.  On \(P\),

\[
 L(n)\le U\le L(n)+b_*,\qquad V=n,qquad I=0.         \tag{4.2}
\]

Consequently, with \(s=L(n)\), the endpoint has exact tier scale

\[
 U=s^{1+o(1)},\qquad V=s^{3+o(1)},\qquad I=0,         \tag{4.3}
\]

which is the physical \((1,3,0)\) promotion interface.  No such
identification is asserted on \(B\).

#### Proof

Immediately before the first \(P\)-hit, \(U<L(n)\); the included reaction
has bounded jump, proving the first two bounds in (4.2).  The other two are
the definition of \(P\).  Since
\(L(n)=n^{1/3}/\log(n+e)+O(1)\), one has
\(n=L(n)^{3+o(1)}\), which proves (4.3).  A \(B\)-endpoint is instead
retained with its open-excursion label and sent through the global
reclassification of Lemma 6.2, whether or not its final cofactor and reserve
happen to vanish. \(\square\)

### Lemma 4.2 (auxiliary boundary endpoint bounds)

On \(B\), and also on \(P\),

\[
 U\vee I\vee R\le L(n)+b_*,\qquad
 V\le n+L(n)+b_*.                                   \tag{4.4}
\]

#### Proof

All three stopped coordinates are strictly below \(L(n)\) immediately
before their first boundary hit, and the boundary-causing physical reaction
has coordinate jumps bounded by \(b_*\).  Since \(V=n+R\), (4.4) follows.
\(\square\)

The definitions remain valid after diagonal renewal only if a prospective
boundary hit inside a would-be exact loop is retained as \(B\) or \(P\).
Deleting that hit and contracting the completed loop would change the
stopping law and is not allowed.

## 5. Paying an auxiliary boundary with the common fourth power

Assume the local hard kernel proves, for every fixed \(q\), the endpoint
moment bound

\[
 \mathbb E_{(u,n,0)}
 \bigl[(1+U_\sigma+I_\sigma+R_\sigma)^q\bigr]
 \le C_q(1+u)^{a_q},                                \tag{5.1}
\]

uniformly for \(u=n^{o(1)}\), where \(\sigma\) includes the
boundary-causing reaction.  Then, for every prescribed \(M\), Markov's
inequality with a sufficiently large fixed \(q\) gives

\[
 \mathbb P(P\cup B)=O(n^{-M}).                       \tag{5.2}
\]

Indeed, \(U_\sigma\vee I_\sigma\vee R_\sigma\ge L(n)\) on that event,
while \((1+u)^{a_q}=n^{o(1)}\) for fixed \(q\).

For \(y=X_\sigma\) on \(P\cup B\), Lemma 4.2 and the elementary
factorial increment bound give

\[
 |F_\ell(y)-F_\ell(u,n,0)|
 \le C L(n)\log(n+e).                               \tag{5.3}
\]

For \(a,b\ge0\),
\((b^4-a^4)^+\le C\{a^3|b-a|+|b-a|^4\}\).  Hence

\[
 \bigl(W_\ell(y)-W_\ell(u,n,0)\bigr)^+
 \le C F_\ell(u,n,0)^3L(n)\log(n+e)
      +C\{L(n)\log(n+e)\}^4.                       \tag{5.4}
\]

Combining (5.2)--(5.4), with \(M\) chosen after the fixed fourth-power
order, yields the following.  Here
\(F_\ell(u,n,0)=\Theta(n\log n)\) along a subpower start: the active
factorial gives the lower bound, while \(u=n^{o(1)}\) and the fixed linear
correction give the upper bound.

\[
 \mathbb E\!\left[
   (W_\ell(X_\sigma)-W_\ell(X_0))^+;P\cup B
 \right]
 =o\!\left(F_\ell(X_0)^3\log n\right).              \tag{5.5}
\]

This proves the required charge for the *actual* endpoint of every open
\(U\)-, \(I\)-, or \(R\)-boundary.  Equation (5.5) does not classify a
\(B\)-endpoint as a hard two-active row.  It says that its complete positive
common-\(W_\ell\) cost is already included, and negligible, in the
originating one-active episode.

## 6. Physical renewal is transparent to the marked gluing

### Lemma 6.1 (physical-diagonal renewal needs no mark equality)

Suppose a local proof erases exact physical returns \(x\to x\), retains the
elapsed physical time and every pre-return terminal event, and eventually
stops with finite mean duration.  Then its population-potential estimate
lifts to the reachable reflected chain even if the auxiliary mark after an
erased loop differs from its incoming value.

#### Proof

Reaction rates and the physical stopping rule depend only on the population
path.  The reflected mark is a deterministic functional of that same raw
path, so erasing a loop in the calculation neither changes its probability
nor licenses erasing its duration or an internal stop.  At a completed
physical loop, \(W_\ell(X)\) has exactly zero increment.  Retaining the
actual terminal mark therefore gives the same random variables

\[
 W_\ell(X_\sigma)-W_\ell(X_0),\qquad \sigma           \tag{6.1}
\]

as the raw marked chain.  No comparison between incoming and outgoing marks
appears in (6.1).  For the selected old-active coordinate, Lemma 3.2 gives
the stronger fact that its positive mark is exactly restored at every
pre-service physical base return. \(\square\)

### Lemma 6.2 (auxiliary-boundary rerouting has zero seam toll)

Assume a stopped episode from a marked bad-tube state satisfies

\[
 \mathbb E_{x,d}
 \left[W_\ell(X_\sigma)-W_\ell(x)+\eta\sigma\right]
 \le-\delta,                                         \tag{6.2}
\]

where its terminal partition includes \(D,A,P,B\), and the contribution on
\(B\) is evaluated at the actual endpoint as in (5.5).  At time \(\sigma\),
route the actual marked endpoint to any applicable global chart (or to a
generator-good region).  If the next chart uses the same \(W_\ell\), the
two increments telescope exactly:

\[
 [W_\ell(X_\sigma)-W_\ell(X_0)]
 +[W_\ell(X_\tau)-W_\ell(X_\sigma)]
 =W_\ell(X_\tau)-W_\ell(X_0).                       \tag{6.3}
\]

Thus \(B\) requires no descriptor identity and no handoff inequality.

#### Proof

The boundary-causing reaction belongs to the first episode, and the second
episode starts after it from the same physical and marked endpoint.  Apply
the strong Markov property there and use the algebraic identity (6.3).
All positive boundary cost was paid in (6.2), so none is deferred to the
router. \(\square\)

Only \(P\) may invoke the exact \((1,3,0)\) hard-row theorem of Lemma 4.1.
On \(B\), the router must inspect the actual population and mark.  It may
select a different one-active chart, a multi-active failed chart, or the
generator-good rule.  This is a finite global classification question, not
a local boundary theorem.

## 7. All-species common-potential gluing

The preceding results close the marked and boundary seams once the local
hard estimate is proved.  The following theorem states the exact conditional
composition.

### Theorem 7.1 (finite-mean marked gluing)

Let \(\widehat\Gamma_{x^\circ}\) be the reflected lift reachable from
\((x^\circ,0)\).  Suppose that, outside a finite set \(K\), its states are
covered by a generator-good set \(G\) and finitely many bad-chart sets
\(C_1,\ldots,C_m\), with the following properties.

1. For some \(a>0\),
   \[
   {\cal L}W_\ell(x)\le-a\quad\hbox{on }G.            \tag{7.1}
   \]
2. Each bad chart selects a population coordinate which is dominant in
   that chart.  Its zero-selected-debt part is contained in \(K\); for a
   one-active chart this is supplied by Lemma 2.2, and a no-history face is
   excluded by Lemma 3.1.
3. There are \(0<\eta\le a\) and \(\delta>0\) such that every remaining
   marked bad-chart state admits an all-reaction physical stopping time
   \(\sigma>0\) satisfying (6.2).  Endpoint and duration bounds are strong
   enough to remove localization.  Every boundary-causing reaction is
   included, \(P\) is routed by Lemma 4.1, and \(B\) is charged and rerouted
   by Lemma 6.2.

Then the marked process hits \(K\) in finite mean physical time from every
reachable state.  Its physical projection is positive recurrent on
\(\Gamma\).

#### Proof

Use \(\widehat W_\ell(x,d)=W_\ell(x)\), which is proper by Lemma 2.1.
From a point of \(G\), run until first entering \(K\) or a bad chart.
Localized Dynkin's formula and (7.1) give

\[
 \mathbb E[W_\ell(X_\rho)-W_\ell(X_0)+\eta\rho]\le0. \tag{7.2}
\]

If a bad chart is reached, append its episode (6.2).  Lemma 6.2 permits
the next chart to be chosen only after seeing the actual endpoint.  If
\(K\) is visited during an episode, record the hit and, solely for the
drift accounting, allow that last episode to finish; this can only
overestimate the target time.

At successive completed macroepisodes \(S_j\), conditional expectation and
the strong Markov property give a decrement at least \(\delta\) and a time
charge \(\eta\).  Stopping after \(r\) episodes yields

\[
 \delta\,\mathbb E(r\wedge N)
 +\eta\,\mathbb E S_{r\wedge N}
 \le W_\ell(X_0)+\delta,                            \tag{7.3}
\]

where \(N\) is the first terminal index.  Monotone convergence proves
\(N<\infty\) almost surely and
\(\mathbb E\tau_K<\infty\).

The target \(K\) is finite, and the chain is nonexplosive by Lemma 2.3.
If the physical class is an absorbing singleton, positive recurrence is
immediate.  Otherwise take one ordinary physical jump from a state of
\(K\), update the reflected mark, and apply the finite-mean hit just proved
from its successor.  There are only finitely many states in \(K\) and
finitely many successors, so the resulting positive return to \(K\) has
finite mean uniformly on \(K\).  Successive positive returns induce a
stochastic trace chain on the finite set \(K\).  Choose a recurrent state
\(k\) of that trace.  Its mean number of trace steps to return is finite,
and each trace step has mean physical duration bounded by the preceding
uniform maximum.  Hence \(k\) has finite mean positive marked return.  At
that return its physical projection \(x=\pi(k)\) has also returned, so the
first positive physical return to \(x\) occurs no later.  Irreducibility of
\(\Gamma\) then makes every physical state positive recurrent. \(\square\)

For a population state \(x\in\Gamma\) not yet supplied with a mark, choose
any finite physical reaction path from \(x^\circ\) to \(x\) and update
(1.1) along it.  This produces a reachable lift whose population marginal
has exactly the original law.  Hence the conclusion applies from every
physical initial state in the class.

## 8. What remains local, and what this note proves

This note proves, without a finite search:

1. a reachable one-active no-fast state is either in the positive-selected-
   debt scope of the hard kernel or in a classwise finite zero-debt part of
   that chart;
2. a structurally no-history \(I=0\) face cannot carry reachable positive
   old-active debt;
3. strict service lowers the existing reflected debt, while physical
   diagonal renewal requires no equality of all auxiliary marks;
4. only the no-fast \(I=R=0\) event \(P\) is the exact \((1,3,0)\)
   promotion handoff;
5. every open-excursion \(U\)-, \(I\)-, or \(R\)-boundary is an auxiliary
   event \(B\) whose actual common-\(W_\ell\) endpoint cost can be paid and
   then rerouted with zero seam toll; and
6. properness, nonexplosion, finite mean return, and the all-species debt
   gluing follow from the common stopped drift hypotheses.

The remaining load-bearing input is the analytic hard kernel itself: it
must prove (5.1), finite duration, and (6.2) for the exhaustive physical
terminal partition \(D,A,P,B\), uniformly along every relevant divergent
chart sequence and for the pair-fixed correction \(\ell\).  A global
hard-317 theorem must additionally prove that its generator-good and
episode-good charts exhaust every affine-feasible descriptor.  Neither
obligation is inferred here from atlas counts or bounded-depth path checks.
