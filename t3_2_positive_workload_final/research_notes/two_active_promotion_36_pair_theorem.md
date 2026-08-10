# The 36 promotion-only support pairs

## 1. Exact scope and certified status

After the four already certified disjoint branches are removed, the exact
promotion selector contains 36 support pairs with no affine-feasible
one-active failure. Every selected pair has exactly one feasible failed
descriptor, and that descriptor is two-active. The disjoint split is

\[
\begin{array}{c|r|r}
\text{failed phase}&\text{incidences}&\text{pairs}\\ \hline
\text{enabled top seed}&20&20\\
\text{dormant finite shell}&16&16
\end{array}                                             \tag{1.1}
\]

There are 32 positive-invariant pairs and four signed pairs. Their pair
fingerprint is

```text
f2ad8cbe4b9ca7f36c39bed4bfe5aaafc6a9152eaf300390b5c25ba546519137
```

This note proves the physical-time theorem for exactly these 36 pairs. Two
independent audits checked the stopping rules, endpoint estimates, arbitrary
strong orientations, and common-potential composition. The narrowly scoped
analytic and pair-level flags are true. Global T3-2 remains uncertified, and
its executable flag remains false.

## 2. One common proper potential

For a fixed selected network, put

\[
 {\cal F}_\ell(x)=\sum_{i=1}^3\log(x_i!)+\ell\cdot x.   \tag{2.1}
\]

Choose \(\ell=0\) in the eight seeded rows with no wholly top linkage. In
the other rows there is one reversible two-complex whole-top linkage. Choose
\(\ell\) by detailed balance on that linkage:

\[
 \ell\cdot(z-y)=\log{\kappa_{zy}\over\kappa_{yz}}.     \tag{2.2}
\]

The supports which occur are

\[
 \{A,B+C\},\ \{B,A+C\}\quad\hbox{in twelve seeded rows}, \tag{2.3}
\]

and

\[
 \{A,B\}\quad(5\text{ dormant rows}),\qquad
 \{B,2A\}\quad(11\text{ dormant rows}).               \tag{2.4}
\]

After adding a network-dependent constant, (2.1) is nonnegative and proper
on \(\mathbb N_0^3\). A fixed linear correction does not change any strict
D-tier logarithmic gap. Consequently the usual Anderson--Kim source-tier
argument applies to every passing descriptor for the same \({\cal F}_\ell\).
Only the single failed descriptor listed in (1.1) needs a stopped episode.

## 3. The twenty enabled-seed rows

All network complexes in these rows have descriptor weight zero or one.
More strongly, the exact descriptor partition places every occurring top
source of both linkages in one D-tier block. Along an exact realizing
sequence write \(N\) for any one of their source monomials. Exact D-tier
equivalence, not merely equality of normalized logarithmic weights, gives
finite positive ratios between *all* these source monomials. The inactive
coordinate has cap zero and stays bounded along a finite actual-target path,
while every enabled lower source has rate \(O(1)=o(N)\). Thus a whole-top
competitor cannot hide a subpower refinement inside the displayed top tier.

Choose an enabled vertex \(y_0\) in the proper top subset of one linkage.
Strong connectivity supplies a simple directed path

\[
 y_0\longrightarrow y_1\longrightarrow\cdots
 \longrightarrow y_j,                                 \tag{3.1}
\]

stopped at the first target outside the global top tier. If an intermediate
top target needs the inactive species, it is an actual target and therefore
is enabled for the next edge. Along the prescribed path the inactive count
never exceeds a support-dependent constant and active populations change by
only \(O(1)\). Thus every prescribed edge has rate at least \(cN\), and the
total rate of all top-sourced competitors is at most \(CN\). The path length
is at most the number of complexes in its linkage. It follows from the
successive exponential races that

\[
 \mathbb P\{\text{(3.1) fires before every competitor}\}\ge p>0. \tag{3.2}
\]

Stop on completion of (3.1) or on the first competing reaction. The duration
is stochastically bounded by a fixed sum of exponentials of mean \(C/N\).
Every top-to-top competitor changes \({\cal F}_\ell\) by \(O(1)\): exact
tier equivalence controls its factorial ratio, including a newly created
inactive molecule. A top-to-lower competitor is already favorable. A
lower-source competitor has probability \(O(N^{-1})\); its positive
factorial cost is at most \(O(\log N)\), and the sharper
propensity-times-log estimate

\[
 u\log^+(v/u)\le v/e                                  \tag{3.3}
\]

also covers a refined subpower subsequence.

The final edge in (3.1) has a top source and a weight-zero target. Hence

\[
 \Delta_{y_{j-1}\to y_j}{\cal F}_\ell
 =-\log N+O(1).                                        \tag{3.4}
\]

Combining (3.2)--(3.4) gives a physical stopping time \(\tau_N\) with

\[
 \mathbb E\Delta{\cal F}_\ell\le-p\log N+O(1),
 \qquad
 \mathbb E\tau_N^m=O(N^{-m})                           \tag{3.5}
\]

for every fixed \(m\). The number of population jumps before the endpoint
is pathwise bounded, so every endpoint moment required for localization is
automatic after scaling the two active coordinates.

## 4. The sixteen dormant finite-shell rows

The inactive coordinate is \(C\) in all sixteen rows. The exact support
certificate proves:

1. the wholly top linkage is one of the two supports in (2.4);
2. the proper linkage contains \(2C\);
3. at \(C=0\), its enabled source set is one of
   \(\{0\},\{A\},\{0,A\}\), or is empty; and
4. the empty case occurs in exactly two incidences.

### 4.1 Whole-shell endpoint and interior estimates

For \(A\leftrightarrow B\), put \(H=A+B\) and use the correction (2.2).
The exact generator identity and \(\log u\le u-1\) give

\[
 {\cal L}_*{\cal F}_\ell\le\kappa_{AB}+\kappa_{BA}.    \tag{4.1}
\]

The chain is an Ehrenfest birth--death chain on its finite \(H\)-shell. An
exponential supermartingale in the two boundary strips gives, from every
exact-tier compact interior start and for every fixed \(L,m\),

\[
 \mathbb P\{(A_t/H,B_t/H)\text{ leaves a fixed larger interior set}
              \text{ for some }t\le L\log H\}
 \le C_{L,m}H^{-m}.                                    \tag{4.2}
\]

For \(B\leftrightarrow2A\), put \(H=A+2B\) and
\(N\asymp\sqrt H\). The independently audited estimates (3.4), (6.4), and
(6.5) of *rank_one_multichannel_carrier.md* give the corresponding
statements: uniform scaled endpoint moments at independent bounded-rate
clocks, super-polynomial interior retention through \(L\log N\), and
uniformly bounded expected net \({\cal F}_\ell\)-cost. Thus, in both
templates,

\[
 \mathbb E[{\cal F}_\ell(X_S)-{\cal F}_\ell(X_0)]\le C \tag{4.3}
\]

at a bounded finite sequence of independent \(0\)-source waits or killed
\(A\)-source occupation windows. Equation (4.1) proves this directly for
the unimolecular shell; the stopped semigroup estimate proved in the
corrected-factorial endpoint theorem gives it for \(\{B,2A\}\).

### 4.2 The finite priority macrochain

The sixteen rows have the exact disjoint split

\[
 7\ \hbox{with unique enabled source }0,\qquad
 7\ \hbox{with enabled source }A,\qquad
 2\ \hbox{disabled}.                                  \tag{4.4}
\]

The seven unique-\(0\) rows have proper support contained in
\(\{0,C,2C,AC,BC\}\). Four have the equal-scale whole shell
\(\{A,B\}\); the other three have \(\{B,2A\}\) and therefore are not
invocations of the earlier weight-one cap-zero theorem. All seven are
covered directly by the priority proof below. The seven \(A\)-enabled rows
also have whole shell \(\{B,2A\}\). The final two rows are handled in
Section 4.3.

The two whole-shell templates have different physical scales.  We contract
only the conservative whole-shell motion and retain every proper-linkage
reaction.  If the successive proper reactions are \(y_k\to z_k\), define
the reflected workload debt

\[
 D_{k+1}=\bigl(D_k+h(z_k)-h(y_k)\bigr)^+,
 \qquad h(y)=w\mathbin{\cdot}y,\qquad D_0=0.             \tag{4.5}
\]

A negative increment larger than the current \(D_k\) is a *surplus exit*.
Before the first surplus exit the cumulative proper-linkage workload
increment equals \(D_k\), whereas a surplus endpoint has cumulative
increment at most \(-1\).  Whole-shell reactions preserve \(h\), remain
present in physical time, and do not change \(D\).

For \(A\leftrightarrow B\), every present \(AC\)- or \(BC\)-source clock
has order \(N\) whenever \(C>0\).  Let \({\cal M}\) be the nonempty set of
these workload-one vertices.  Since the proper linkage is strongly
connected and \({\cal M}\) is a proper set, no nonempty subset of
\({\cal M}\) reachable from an actual target can be closed.  Its first
edge to workload zero has an exponential tail on the \(N\)-clock, with all
internal \({\cal M}\)-edges and all whole-shell jumps retained.
More explicitly, on the interior tube the aggregate exit hazard is at
least \(cN\), whereas the total internal proper-linkage hazard is at most
\(CN\).  The number of internal \({\cal M}\to{\cal M}\) reactions before
each exit consequently has a uniform geometric tail and moments of every
fixed order.  These internal reactions preserve \(C\) and \(H_w\), and
exact D-tier equivalence gives an \(O(1)\) corrected-factorial increment
per reaction.  Present \(C\)-only source clocks have order one, so their
probability of interrupting one such block is \(O(N^{-1})\).

The only nonabsorbing macrostates needed in this case are

\[
 R=(C=0,D=0),\qquad P=(C>0,D=1),\qquad Q=(C>0,D=0).     \tag{4.6}
\]

At \(R\), the only enabled proper source is \(0\).  Its target either is
\(C\)-only, giving \(Q\), or lies in \({\cal M}\), giving \(P\).  The first
\({\cal M}\)-exit from \(P\) either consumes the last \(C\) and returns to
\(R\), or retains \(C\) and reaches \(Q\).  From \(Q\), the next
\({\cal M}\)-exit is surplus.  If every trial from \(R\) returned to \(R\),
then \(0\) together with all reachable vertices of \({\cal M}\) would be a
closed proper subset of the directed proper linkage, omitting \(2C\).
Strong connectivity rules this out.  Neutral restarts therefore have a
geometric tail with a network-dependent parameter bounded away from zero.

For \(B\leftrightarrow2A\),

\[
 A\asymp N,\qquad B\asymp N^2.                         \tag{4.7}
\]

Here \(BC\) is the unique workload-two proper vertex.  Whenever \(C>0\),
every \(BC\)-source channel has order \(N^2\), and each of its targets has
workload at most one.  Consequently

\[
 h(z)-h(BC)\le-1                                      \tag{4.8}
\]

for every such edge.  At \(C=0\), take \(A\), rather than \(0\), as the
base source whenever \(A\) is present: its clocks have order \(N\), while
a \(0\)-source clock has order one.  If \(A\) is absent, \(0\) is the only
enabled base source.  Thus an order-one wait never hides an enabled
order-\(N\) proper reaction.

An entry from \(0\) creates at most two debt units, and an entry from \(A\)
creates at most one. Equation (4.8) confines the nonabsorbing priority
macrochain to

\[
 R_0=(C=0,D=0),\quad R_1=(C=0,D=1),\quad
 P_d=(C>0,D=d),\ d=0,1,2,                              \tag{4.9}
\]

where \(R_1\) occurs only when \(A\) is present.  If a \(BC\)-reaction
retains \(C\), at most two such reactions clear all old debt and the next
one is surplus.  If it consumes the last \(C\), its target is \(0\), with
workload drop two, or \(A\), with workload drop one, so the endpoint is
\(R_0\) or \(R_1\).

Any closed service-free macroclass would be contained in the base/reset
set generated by \(\{0,A,BC\}\); all other targets either give surplus or
enter a \(BC\)-priority run which does.  Such a class would project to a
proper closed subset of the proper-linkage digraph.  This is impossible
because the digraph is strongly connected and contains \(2C\).  Equivalently,
the possible neutral resets \(b\to BC\to b\), \(b\in\{0,A\}\), and mixtures
of them always have an outgoing edge.  Every edge leaving \(A\) has the
same order-\(N\) scale as the other \(A\)-source edges, every edge leaving
\(0\) has the same order-one scale as the other \(0\)-source edges, and
every edge leaving \(BC\) has the same order-\(N^2\) scale as the other
\(BC\)-source edges.  Thus each visit has a fixed positive escape
probability.  An \(A\)- or \(AC\)-source reaction while \(BC\) is enabled
has probability \(O(N^{-1})\) before the next \(BC\)-reaction.  It is
retained as a physical interruption and is not counted as service.
Likewise, when \(A\) is the leading cap-zero source, a simultaneous
\(0\)-source reaction interrupts its \(O(N^{-1})\) window with probability
\(O(N^{-1})\).  All still lower \(0,C,2C\) clocks during a \(BC\)-block
have smaller probability.

In either shell, the finite priority macrochain has an absorbing surplus
state accessible from every non-disabled starting state and no other
closed class.  Hence there are constants \(C<\infty\) and \(q\in(0,1)\),
depending on the network and rates but not on \(N\), such that

\[
 \mathbb P\{\text{no surplus in the first \(K\) macrotransitions}\}
 \le Cq^K+O(N^{-1}).                                   \tag{4.10}
\]

Choose \(K\) so the first term is below \(1/8\), and stop at surplus, at
the first lower-priority interruption, or after \(K\) macrotransitions.
Before surplus the positive endpoint workload is at most two.  Enlarging
\(K\), if necessary, gives some \(\delta>0\) such that, for all large \(N\),

\[
 \mathbb E\Delta H_w\le-\delta,
 \qquad |\Delta H_w|\le C_K.                           \tag{4.11}
\]

All clocks remain physical.  A \(0\)-source wait occurs only when no
proper \(A\)-source is present and has fixed exponential moments.  An
\(A\)-source wait is an \(O(N^{-1})\) killed occupation window; an
equal-shell top exit has duration \(O(N^{-1})\); and a \(BC\)-priority exit
has duration \(O(N^{-2})\).  The whole shell evolves throughout.  With
\(K\) fixed, the duration has moments of every fixed order, the inactive
count is bounded by the number of retained proper jumps, and the
whole-shell endpoint has every fixed scaled active moment.  No
inactive-coordinate truncation is used.

For completeness, a killed \(BC\)-window has uniformly bounded
whole-shell factorial cost without any scale matching.  The exact
\(\{B,2A\}\) corrected-factorial inequality gives

\[
 {\cal L}_*{\cal F}_\ell\le C(1+A)=O(N)                \tag{4.12}
\]

on the interior tube.  Its duration is \(O(N^{-2})\), so Dynkin's formula
charges \(O(N^{-1})\).  The \(A\)-windows and independent \(0\)-clock
endpoints are covered by (4.3).  Thus the scale-separated contraction has
not hidden a positive top-shell endpoint cost.

On the interior event,

\[
 \log(A\vee1)=\log N+O(1),\qquad
 \log(B\vee1)=
 \begin{cases}
   \log N+O(1),&L_*=\{A,B\},\\
   2\log N+O(1),&L_*=\{B,2A\}.
 \end{cases}                                           \tag{4.13}
\]

Hence every bounded lower jump has

\[
 \Delta{\cal F}_\ell=\Delta H_w\log N+O(1).           \tag{4.14}
\]

Equations (4.2)--(4.3), the deterministic transition cap, and
(4.11)--(4.14) give

\[
 \mathbb E\Delta{\cal F}_\ell\le-c\log N+O(1).        \tag{4.15}
\]

The exceptional interior-exit probability is super-polynomial, while the
factorial oscillation on the finite whole shell is polynomial times
\(\log N\); its endpoint contribution is therefore \(o(1)\).
Every lower-priority interruption has a bounded workload jump and
factorial cost \(O(\log N)\); its \(O(N^{-1})\) probability therefore
contributes \(O(\log N/N)=o(1)\).

### 4.3 The two disabled rows

If the enabled set in item 3 is empty, the proper linkage is identically
disabled at \(C=0\), and the whole linkage preserves \(C=0\) and its finite
workload shell. On a fixed closed irreducible class, that workload has one
fixed value. The class is therefore finite, so no divergent sequence in the
class realizes the displayed descriptor.

## 5. Classwise composition

> **Theorem 5.1.** Give either linkage of any of the 36 selected
> support pairs an arbitrary strongly connected orientation and arbitrary
> positive rates on its present edges. Then every closed irreducible
> population class is positive recurrent.

Fix a closed irreducible class \(\Gamma\). If a divergent sequence in
\(\Gamma\) lies in a passing source-tier cone, the standard generator
estimate for the fixed potential (2.1) tends to \(-\infty\). If it lies in
the unique failed cone, Section 3 or Section 4 gives a physical episode with

\[
 \mathbb E_x\{\Delta{\cal F}_\ell+\eta\tau\}\le-1      \tag{5.1}
\]

outside a finite set; the disabled alternative is not divergent in
\(\Gamma\). A bad-sequence contradiction turns these sequence estimates
into one finite exceptional set. The common-entropy physical-time gluing
theorem then gives finite mean hitting of that set.

Nonexplosion is elementary here and in the full binary class: a reaction
which increases total population has a source of molecularity at most one,
so the positive part of the total-population generator is bounded by
\(C(1+|x|)\). Local finiteness and finite mean return from the finite target
give positive recurrence of \(\Gamma\).

The two independent audits certify the exact selector and show that it is
disjoint from all earlier ordered branches. The ordered residual arithmetic
is therefore

\[
 (1871,191)\longmapsto(1839,187).                       \tag{5.2}
\]

## 6. Audit obligations

An independent replay should check, in this order:

1. that every prescribed seeded path retains all top competitors and that
   its lower-source positive logarithmic cost is uniformly integrable;
2. the exact unimolecular endpoint inequality (4.1) and the boundary
   supermartingale (4.2);
3. that the dormant actual-target path can be restarted after every faster
   top exit without silently deleting a reaction;
4. the reflected-debt coefficient in (4.5) and (4.10)--(4.11), including
   base states with source \(A\) rather than \(0\);
5. the lift from (4.11) to the common factorial drift (4.15); and
6. the fixed-class treatment of the two disabled rows and the disjoint
   36-pair selector.

Both independent replays passed all six checks. In particular they verified
the exact \(7+7+2\) dormant split, the priority SCC argument for arbitrary
strong digraphs, and the \(O(\log N/N)\) interruption charge. No
counterorientation or adverse rate choice remains at this scope.
