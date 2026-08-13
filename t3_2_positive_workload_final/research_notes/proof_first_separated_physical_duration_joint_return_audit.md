# Hostile audit of the separated physical-duration lemma

**Independent proof-first audit, 2026-08-12 PDT.**  The exact audited
target is
`proof_first_separated_physical_duration_joint_return.md`, SHA-256
`504b87e600c382e9c82b88cf0ea88f87a6a4b6c7783202cc9cc2faa79fefc640`
(277 lines, 9904 bytes).  The target was not edited during this audit.

**Verdict: STRICT PASS ON ITS STATED KILLED-BRANCH SCOPE.**  The duration
argument does not enumerate carrier populations and remains uniform for
critical and supercritical carrier offspring laws.  The open reaction count
has an exponential tail after order \(a\), every open holding rate is at
least order \(a\), and the contracted base trace has a bounded-jump killed
drift with order-\(b\) absorption time.  Expanding literal returns and adding
holding times preserves every fixed moment.

The words *complementary killed branch* in lines 32--34 are essential, not
cosmetic.  Without that exclusion, (4.4) and hence (5.1) are false in
general.  Section 7 below records the obstruction and the exact condition
that later compositions must preserve.

## 1. Audit dependencies and conventions

The two frozen dependencies named by the target have the asserted hashes:

\[
\begin{array}{c|c}
\text{file}&\text{SHA-256}\\ \hline
\texttt{proof\_first\_separated\_clean\_base\_green\_audit.md}
&\texttt{96c72e11a6105013b8d7b6e2309da7c2dbebccfa0b72640bfb3cfe6cf1608b36}\\
\texttt{proof\_first\_separated\_first\_mark\_resolvent\_lemma.md}
&\texttt{d4c4baff29ffda942798f28fc69d4b30ab25ee2c8e13d1960a4ee20b6d772506}
\end{array}
\]

As in those inputs, a zero-displacement edge is deleted: it contributes
nothing to the generator of the state process.  The count \(\nu\) therefore
counts state-changing reactions, and a holding time means time to the next
state change.  All constants may depend on the fixed finite reaction graph
and its fixed positive rate vector, but not on \(a,b\), or the carrier
population inside the localized episode.

## 2. Uniformity of the open source comparison

At an open state, every nontrivial edge sourced at \(q=A+C\) has propensity

\[
                         \kappa_{qz}AC.
\]

After aggregation over nontrivial \(q\)-edges, its coefficient is a fixed
positive number.  This conclusion is independent of the orientations and
relative strengths of those edges: all of them have the same \(AC\)
factor.  Strong connectivity supplies a nontrivial exit unless the whole
state lies in the already-routed frozen/invariant alternative.

For the six possible lower source types, the total lower-to-\(q\) rate
ratio is bounded, up to fixed rate constants, by

\[
 {1\over AC},\quad {B\over AC},\quad {B^2\over AC},\quad
 {1\over A},\quad {C\over A},\quad {B\over A}.
\]

The moving tube bounds each applicable expression by
\(C\varepsilon_a\).  Falling factorials only decrease the numerator of
these upper bounds.  Summing the fixed finite edge set gives

\[
 {\Lambda_{\rm lower}(X)\over\Lambda_q(X)}
       \le K\varepsilon_a,
 \qquad
 \mathbb P(q\text{-source next}\mid\mathcal F_n)
       \ge {1\over1+K\varepsilon_a}.                 \tag{2.1}
\]

Thus the target's (1.4) and (2.2) are valid for arbitrary fixed strong
orientations.  They do not assume comparable individual edge constants.

## 3. The active clock defeats carrier criticality

A \(q\)-sourced state change lowers \(A\) by exactly one.  A lower-sourced
state change changes \(A\) by either zero or one, the latter only when its
target is \(q\).  Consequently, for a small fixed \(t>0\), (2.1) gives,
uniformly at every preterminal open state,

\[
 \mathbb E\!\left[e^{t\Delta A}\mid\mathcal F_n\right]
 \le {e^{-t}+K\varepsilon_a e^t\over1+K\varepsilon_a}
 \le e^{-\gamma}                                      \tag{3.1}
\]

for all sufficiently large \(a\), with fixed \(\gamma>0\).

The optional-stopping step in the target can be made literal by killing the
one-step kernel at \(\nu\).  Iteration of (3.1) yields

\[
 \mathbb E\!\left[
   e^{t(A_n-A_0)+\gamma n};\ \nu>n\right]\le1.          \tag{3.2}
\]

On \(\{\nu>n\}\), the included lower active boundary has not been crossed,
so \(A_n>a/2\), while a launch has \(A_0\le a+1\).  Hence

\[
 \mathbb P(\nu>n)
       \le \min\{1,e^{t(a/2+1)-\gamma n}\}.             \tag{3.3}
\]

Tail summation gives \(\mathbb E\nu^r\le C_ra^r\) for every fixed integer
\(r\ge1\).  This argument neither dominates nor even measures total carrier
progeny.  In particular, critical or supercritical offspring only makes an
included \(C\)- or \(A\)-boundary arrive sooner; it cannot defeat the
negative active clock.

## 4. From embedded length to physical open time

Before the included endpoint, \(A\ge a/2\), \(C\ge1\), and the aggregate
nontrivial \(q\)-rate is at least \(ca\).  Conditional on the embedded path,
the holding times have the laws \(E_i/\Lambda(X_i)\), where the \(E_i\) are
unit exponentials.  Minkowski's inequality gives

\[
 \left\|\sum_{i<\nu}{E_i\over\Lambda(X_i)}
       \right\|_{L^r(\,\cdot\mid X_0,\ldots,X_{\nu-1})}
 \le {C_r\nu\over a}.                                 \tag{4.1}
\]

Combining (4.1) with (3.3) proves the uniform fixed-moment bound for one
long open excursion.  The holding time preceding the crossing reaction is
included because its pre-jump state is still in the tube.  No time after
the included endpoint is charged.

## 5. Contracted base trace and compact states

For a clean \(k=0\) completion, the audited ledger forces exactly

\[
             cB\to jB\quad\hbox{or}\quad cB\to q\to jB,
             \qquad c,j\le d.                         \tag{5.1}
\]

After literal population returns are contracted, every trial sourced at
the maximal degree \(dB\) is either killed or has \(j<d\), hence lowers
\(B\).  The directed cut out of the literal-return block has a fixed
positive conditional probability: edges with source \(dB\) share their
falling-factorial factor and edges with source \(q\) share their \(AC\)
factor.  Thus the diagonal literal-return inverse is uniformly geometric.

At a large base, the aggregate probability of using source \(cB\),
\(c<d\), is \(O((1+B)^{c-d})\).  Such a source is the only way a surviving
\(k=0\) completion can increase \(B\), and every displacement is bounded by
two.  It follows that, after contraction,

\[
 \mathbb P(\hbox{kill or }\Delta B\le-1\mid B)\ge\epsilon,
 \qquad
 \mathbb P(\Delta B>0\mid B)\le {C\over1+B}.            \tag{5.2}
\]

For small fixed \(s>0\), killed mass contributes zero, negative moves cost
at most \(e^{-s}\), and the bounded positive moves in (5.2) contribute only
\(O((1+B)^{-1})\).  Therefore the killed exponential kernel contracts by a
fixed factor outside a fixed compact set.

On the compact set, the stated killed-branch hypothesis says precisely
that there is no closed continuing zero-loss class.  The finite
substochastic kernel then has spectral radius below one.  Equivalently,
after grouping a fixed number of trials, it has a uniform chance to be
killed or to reach the exterior contraction.  Patching this finite block
to the exterior supermartingale gives

\[
 \mathbb P(N_B>n)\le C e^{s b-\gamma' n},
 \qquad
 \mathbb E N_B^r\le C_r(1+b)^r.                       \tag{5.3}
\]

This verifies the nontrivial compact-state step behind the target's
(4.2)--(4.4).  When \(d=0\), every continuing \(k=0\) completion is literal;
the same statement is simply the geometric directed-cut inverse on the
killed branch.

## 6. Literal expansion and the random sum of clocks

Each contracted trial expands into a conditionally geometrically dominated
number of literal returns, uniformly over the entrance state.  If \(M_B\)
is the resulting number of actual base macros, standard conditional
geometric-moment induction applied to (5.3) gives

\[
                         \mathbb E M_B^r\le C_r(1+b)^r. \tag{6.1}
\]

Every nonfrozen base holding rate is bounded below by a fixed positive
constant.  Conditional Minkowski, now applied to the random sum of at most
\(M_B+1\) base clocks, proves

\[
                         \mathbb E T_B^r\le C_r(1+b)^r. \tag{6.2}
\]

A preceding \(k=0\) macro has at most one open \(q\)-holding time, of rate
at least \(ca\); the geometric literal expansions have already been counted
in \(M_B\).  There is at most one terminal long open excursion, controlled
by Section 4.  Adding these random sums proves the target's (5.1), including
the terminal launch clock and harmless endpoint off-by-one terms.

## 7. Why the killed-branch qualifier must be retained

Strong connectivity alone does **not** give the compact contraction in
Section 5.  For example, take the strong directed cycle on complexes

\[
                         0\longrightarrow B\longrightarrow q
                         \longrightarrow0.              \tag{7.1}
\]

Every clean completed word preserves \(A\).  At compact \(B\), the clean
base trace can circulate forever.  Moreover, while the state is open after
\(B\to q\), the always-enabled source \(0\) marks with probability of order
\(1/a\) before the order-\(a\) \(q\)-clock.  Thus an episode which waits for
that first mark can have order-\(a\), rather than order-\(b\), duration; a
remote moving spectator guard does not repair a uniform compact Green
bound.  This is the active-invariant/no-history alternative excluded in
lines 32--34 of the target.

Accordingly, later synthesis may cite (5.1) only after making the same
dichotomy explicit:

1. on the complementary branch, the clean compact kernel is genuinely
   killed and the present strict PASS applies; or
2. the active-invariant/no-history class is routed to its separate argument
   and this duration lemma is not invoked there.

Subject to that already-stated routing, (4.2)--(4.6) contain no hidden
uniformity gap.

## 8. Compatibility with the normalized moving tube

The normalized-phase lemma uses
\(\bar\delta_a=e^{-h_a/2}\), with pre-jump bounds

\[
 A\in(a/2,2a),\qquad
 C<c_0\bar\delta_a a,qquad
 1+B^p<c_0\bar\delta_a a.
\]

Choosing its fixed \(c_0\) small enough turns these into the target's
\(C/A<\varepsilon_a\) and \(m(B)/A<\varepsilon_a\), up to fixed constants
already absorbed in (2.1).  Both rules include the crossing reaction, and
both stop a marked path at its next actual \(C=0\) return rather than
starting another base macro.  Hence the duration proof and normalized
terminal proof concern the same physical episode.

Finally, separated entrances have \(b=o(a)\) for \(p=1\),
\(b=o(a^{1/2})\) for \(p=2\), and dynamically constant \(B\) for \(p=0\).
Since \(G_\ell(a,b,0)\ge ca\log a\) and \(h_a\to\infty\), the verified first
moment satisfies

\[
             \mathbb E_x\tau=o\!\left(G_\ell(x)^3h_a\right).
\]

This is the exact duration input required by the fourth-power Foster lift.
