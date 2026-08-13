# Independent exact-byte audit: cap-free B/F0 killed resolvent

**Audit date:** 2026-08-12 PDT.

## 1. Frozen target and verdict

The audited target is

~~~text
research_notes/proof_first_remaining_18496_cap_free_bf0_killed_resolvent_theorem.md
5e8ce1d09c794014093bc9b84b9563f9348530acc741bb12b2c8446e2a560783
539 lines / 20193 bytes
~~~

The verdict on these exact bytes is **STRICT PASS AS A LOCAL ONE-ACTIVE
B/F0 CONTRACT**.

The theorem replaces the bounded inactive-cap prelude by an actual
countable-phase killed resolvent.  It includes all physical clocks, carries
the actual reaction target as the mark, and never stops merely because a
cap, tier, enabled-support, or active-set label changes.  Its alternatives
are literal: either the no-kill phase is the entire fixed-
\(X\), fixed-\(U\) irreducible class and is positive recurrent, or an
almost surely finite completed episode has coercive marked-factorial reward,
uniform positive reward moments, and integrable physical duration.

This is not by itself a recurrence theorem for the 6,654 failure pairs.
The target states that publication boundary explicitly.

## 2. Exact reduction and actual-mark handoff

Write the active coordinate as \(X\).  The B linkage has a witness

\[
 q_X=1,\qquad c_X=0,\qquad q_U\le c_U,\quad q_V\le c_V,       \tag{2.1}
\]

and the Flat0 linkage has zero \(X\)-degree.  Along the audited sequence,

\[
 X\longrightarrow\infty,
 \qquad \log(1+U)+\log(1+V)=o(\log X).                       \tag{2.2}
\]

If \(q=X\), or \(q=X+U\) with \(U>0\), the current actual mark is still in
the Flat0 linkage.  The target correctly does not start a same-linkage B
path from that mark.  It takes one ordinary all-clock marked jump instead.
The marked source hazard is at most \(C(1+U+V)^2\), while the enabled B
witness has hazard at least \(cX\), so the exact entropy identity gives

\[
 \mathbb E\Delta F\le-\log X+2\log(2+U+V)+C\longrightarrow-\infty. \tag{2.3}
\]

The only prefix case is therefore \(q=X+U\), \(U=0\).  Before absorption,
\(X,U\) are constant and every nonabsorbed source and target is in
\(\{0,V,2V\}\).  The two absorbing events have disjoint priority: a B
reaction is type 1 even if its target contains \(U\); only a non-B Flat0
reaction creating \(U\) is type 2.  The causing reaction is included once.
Type 1 continues from its actual B target, and type 2 takes the ordinary
access-payoff jump.  No target is fabricated and no activation clock is
conditioned away.

## 3. Terminal operator and killed Green function

For a nonabsorbed marked state \((v,s)\), the relative weight is

\[
                       w_\theta(v,s)=((v-s)!)^\theta,
                       \qquad 0<\theta<\tfrac14.             \tag{3.1}
\]

If absorption fires from source \(y\), the terminal weight relative to the
constant prefix factor \((X!)^\theta\) is exactly

\[
 \widehat w_\theta(y;X,v)
   =\left\{{(X-y_X)!(v-y_V)!\over X!}\right\}^{\!\theta}.    \tag{3.2}
\]

This formula is exact because all pre-absorption sources have \(y_U=0\),
and the actual target cancels from the marked factorial.  In particular, a
degree-one B terminal contributes the favorable \(X^{-\theta}\) factor.

For a nonabsorbed pure-\(V\) jump, the target also cancels:

\[
 {w_\theta(v-y+u,u)\over w_\theta(v,s)}
       =\left\{{(v-y)!\over(v-s)!}\right\}^{\!\theta}.        \tag{3.3}
\]

The hostile replay confirms the two-step outer contraction.  Lower source
degrees are suppressed by their propensity ratios; a maximal source is
weight-neutral only when the carried mark has the same degree, and its
nonself strong-connectivity edge then either absorbs or leaves a strictly
lower mark.  Hence two retained maximal-source steps contract.  Absorbing
degree-one and degree-zero labels have uniformly bounded terminal weighted
norm by the sourcewise estimate

\[
                         C{r^{1-\theta}\over1+r}\le C.        \tag{3.4}
\]

On the finite marked core, every nonabsorbed row is entrywise nonincreasing
in \(X\): only absorbing B hazards acquire the extra linear \(X\) term.
Absence of a reachable closed no-kill class makes the largest core kernel,
at \(X=1\), transient.  Its Green matrix is finite.  The core inverse and
outer contraction therefore prove the uniform resolvent bound

\[
              (I-P)^{-1}S\widehat w_\theta\le C_\theta w_\theta. \tag{3.5}
\]

This gives the exact exponential relative marked-factorial estimate and all
fixed moments of the positive prefix reward.

## 4. Stopped survival maximum

The derivative from the earlier audited candidate adds the needed estimate
which does not use the favorable terminal \(X^{-\theta}\) factor.  Let
\(\rho_M\) be the first nonabsorbed phase with \(V\ge M\).  Stopping the
same Green series at \(\rho_M\wedge\sigma\), with boundary payoff
\(w_\theta\) at \(\rho_M\) and zero at absorption, gives

\[
 \mathbb E_{v,s}
   [w_\theta(V_{\rho_M},S_{\rho_M});\rho_M<\sigma]
       \le C_\theta w_\theta(v,s).                         \tag{4.1}
\]

The first-hit boundary operator has uniformly bounded weighted norm:
entrance jumps are bounded, the outer two-step contraction is uniform in
the threshold, and the same finite-core inverse applies.  Since every mark
has \(S\le2\), hitting \(V\ge M\) costs factorial weight at least that of
\(M-O(1)\).  Thus

\[
 \mathbb P_{v,s}\{\sup_{r<\sigma}V_r\ge M\}
 \le C\exp\{\theta v\log(2+v)-cM\log(2+M)\}.              \tag{4.2}
\]

This is precisely the missing distinction between a terminal overshoot
bound and a pre-absorption survival maximum.  It validates both uses in
Section 7: the exponentially small high endpoint tail when
\(M=2r_0+O(1)\), and uniform tightness of prefix endpoints from bounded
initial \(V\).

## 5. Duration and closed no-kill alternative

For physical time, \(L(v)=1+\log(v+e)\) has negative killed generator
outside a finite core.  A maximal unary or binary source lowers \(v\) at
rate at least \(cv\) or \(cv^2\), while every upward jump has lower source
degree.  Finite-core killed transience supplies a bounded corrector.  Dynkin
and induction on powers of \(L\) yield the sharp estimate

\[
                         \mathbb E\sigma^m
             \le C_m\{1+\log(2+v)\}^m.                    \tag{5.1}
\]

The theorem correctly does not claim a uniform embedded jump count; a pure
death prefix can take linearly many jumps even while its physical time is
only logarithmic.

If the nonabsorbed phase has a reachable closed class, it is a closed
physical subset of the fixed irreducible population class.  Irreducibility
forces equality with the full class, so \(X,U\) are fixed.  The remaining
one-species binary chain has a highest-source strict downward edge of linear
or quadratic rate, while all upward sources have lower degree.  The stated
factorial-exponential Foster function proves nonexplosion and positive
recurrence.  This branch requires no episode handoff.

## 6. Low, middle, and high ledger

In the transient branch, exact factorial telescoping gives order
\(-r_0\log r_0\) reward when the residual inactive population falls below
half its start.  In the middle band, the appended B/access completion gives
\(-a\log(2+r_0)+C\).  On the high event, (4.2) gives exponentially small
probability, while (3.5) supplies uniform integrability of the positive
prefix reward and source entropy controls the finite appended rule.
Consequently

\[
                       \mathbb E\Delta F
                \le-a_0\log(2+V_0)+C.                     \tag{6.1}
\]

When \(V_0\) is bounded, (4.2) makes prefix endpoints uniformly tight.
On a fixed bounded endpoint set the appended payoff is
\(-a\log X+C\); the complement has uniformly integrable positive reward.
Therefore

\[
                       \mathbb E\Delta F
                \le-a_1\log X+C.                          \tag{6.2}
\]

The logarithmic duration bound is smaller than the available negative term
in the large-\(V\) regime, and bounded when \(V\) is bounded.  One fixed
\(\eta>0\) therefore gives the physical-time ledger in Theorem 1.1.  All
endpoints are physical and every jump is charged exactly once.

## 7. Composition boundary

The exact conclusion certified by this audit is the cap-free B/F0 local
contract, together with the qualitative B/B corollary stated in the target.
It supplies neither a terminal-chart SCC argument nor a potential-switching
theorem.

For the intended 18,496-pair composition, the separate exact bridge proves
that every pair is globally nonmixed, so the frozen one-active symbolic
exhaustion routes one-active sequences directly through Q, flat/invariant,
B/B, B/F0, or D/F0.  This bypasses corrected-pass descriptor exits in the
one-active branch.  The unconditional AA theorem handles every feasible
two-active row.  The corrected S-superlevel pass is consequently needed
only for the all-active complement, where there are no inactive caps.  These
are separate dependencies; the present theorem does not silently prove
their global composition.
