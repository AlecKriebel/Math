# Corrected tier-pass charts under the common marked factorial potential

**Proof-first standalone theorem, 2026-08-12 PDT.**  This note proves the
marked all-clock estimate for every fixed chart which passes the corrected
S-tier-superlevel cut.  It closes a potential-switch seam: the same marked
potential used by the available/available and local Bellman episodes also
handles a passing tier chart.

The proof is analytic.  The finite descriptor list is used only to obtain a
finite chart cover.  No orientation, rate vector, reaction history,
population box, or path is enumerated.

## 1. Marked one-jump identities

Fix a reduced binary network, one fixed strongly connected orientation of
each linkage, and positive labelled rates.  For a source complex \(y\), put

\[
 K_y=\sum_{e:s(e)=y}\kappa_e,\qquad
 \lambda_y(x)=K_y(x)_y,\qquad
 \Lambda(x)=\sum_q\lambda_q(x),\qquad
 p_y(x)={\lambda_y(x)\over\Lambda(x)}.                \tag{1.1}
\]

After every physical reaction retain its actual target \(t\) as the mark.
Then \(x\ge t\), so \(t\) is an enabled source.  Put

\[
                    F(x,t)=\sum_i\log((x_i-t_i)!),
 \qquad W(x,t)=1+F(x,t).                              \tag{1.2}
\]

If the next labelled reaction is \(y\to u\), its endpoint is
\((x-y+u,u)\), and

\[
 F(x-y+u,u)-F(x,t)=\log{(x)_t\over(x)_y}.             \tag{1.3}
\]

Consequently the expected increment of one ordinary all-clock jump is

\[
\begin{aligned}
 D(x,t)
 &=\sum_y p_y(x)\log{(x)_t\over(x)_y}\\
 &=\log p_t-\sum_y p_y\log p_y-\log K_t
       +\sum_y p_y\log K_y
 \le\log p_t+C_K.
\end{aligned}                                         \tag{1.4}
\]

The finite source set also gives, for every fixed \(q<\infty\),

\[
 \sum_y p_y(x)
   \left[\log{(x)_t\over(x)_y}\right]_+^q\le C_q.     \tag{1.5}
\]

Indeed, on a positive-increment term, with
\(R=(x)_t/(x)_y\ge1\),
\(p_y\le (K_y/K_t)R^{-1}\), and
\(R^{-1}(\log R)^q\) is bounded on \([1,\infty)\).  Thus (1.5) follows
after summing over the finite source set.  These are exact
falling-factorial identities.  They include every competing clock and every
parallel label.

## 2. Literal top-S sources have nonvanishing physical probability

Fix one tier/cap chart and an escaping sequence \(x_n\) in it.  Let \(E\)
be its global top stochastic tier.  By the definition of an S-tier,
every \(y\in E\) is eventually enabled and, after passing to a
source-ratio subsequence,

\[
 0<\ell_{yq}:=\lim_n{(x_n)_y\over(x_n)_q}<\infty
                         \qquad(y,q\in E),            \tag{2.1}
\]

whereas

\[
                 {(x_n)_q\over(x_n)_y}\longrightarrow0
                    \qquad(y\in E,\ q\notin E
                    \text{ enabled}).                \tag{2.2}
\]

Since there are finitely many sources and all \(K_q\) are fixed positive
constants, (2.1)--(2.2) imply

\[
             \liminf_n p_y(x_n)>0\qquad(y\in E).      \tag{2.3}
\]

Thus a literal top-S source cannot have vanishing all-clock probability.
If a proposed descending edge has a source whose probability vanishes, that
source is not in the global top S-tier of the fixed chart; it cannot be the
edge certified by the corrected cut.

## 3. The corrected cut and its physical edge

Let \(r\) be the D-tier level occupied by \(E\).  For a linkage \(L\), put

\[
       U_L(r)=\{q\in L:q\text{ lies at or above D-level }r\}.          \tag{3.1}
\]

The corrected S-tier-superlevel condition is

\[
 \varnothing\ne U_L(r)\subsetneq L,\qquad U_L(r)\subseteq E           \tag{3.2}
\]

for at least one linkage \(L\).  Strong connectivity supplies a directed
path from \(U_L(r)\) to its complement.  Let

\[
                              e:y\longrightarrow z     \tag{3.3}
\]

be the first exiting edge.  Then

\[
                   y\in U_L(r)\subseteq E,\qquad
                   z\text{ lies strictly below D-level }r.           \tag{3.4}
\]

For this fixed labelled edge,

\[
 a_e(x_n):={\kappa_e(x_n)_y\over\Lambda(x_n)}
           ={\kappa_e\over K_y}p_y(x_n)
           \ge a_*>0                                  \tag{3.5}
\]

for all large \(n\), by (2.3).

## 4. The depth-two all-clock episode

Start from an arbitrary actual mark \(t\).  Take the next ordinary physical
jump with every clock active.

* At the actual endpoint of this first jump, first test every named
  structural exit (bounded-coordinate cap, enabled-source support,
  active-coordinate set, or tier chart).  If one occurs, record that
  physical exit and stop.  This exit test has priority over every
  continuation rule.
* If there is no structural exit and the jump is not the designated label
  \(e\), stop at its actual population endpoint and actual target.
* If there is no structural exit and \(e:y\to z\) fires, write its actual
  endpoint as \(x'=x-y+z\), take one final ordinary all-clock jump from the
  marked state \((x',z)\), and stop at that jump's actual endpoint and
  target.  At this second endpoint test the same named structural exits;
  if one occurred, record that final physical jump as the exit jump.

The episode has one or two ordinary jumps.  A competitor is the terminal
jump of this episode and initializes the next state-selected rule only
after its endpoint; no reaction is counted twice.

On the nonexit success branch, bounded displacement preserves every strict
D-comparison.  The cap/support chart is unchanged, so every source in \(E\)
which was used in the tier comparison remains enabled.  From
(3.4), for any such \(q\in E\),

\[
 {p_z(x'_n)}
 \le {\lambda_z(x'_n)\over\lambda_q(x'_n)}
 \longrightarrow0.                                  \tag{4.1}
\]

In an all-active chart this is immediate: every coordinate diverges, every
source stays enabled under bounded displacement, and falling factorials
differ from the corresponding monomials by a relative \(1+o(1)\).
In a boundary chart, failure of an \(E\)-source to remain enabled is exactly
the declared physical structural exit.

Let \(J_n\) be the expected total \(F\)-increment of the episode on a
nonexit sequence.  First-step conditioning gives the exact Bellman identity

\[
                  J_n=D(x_n,t)+a_e(x_n)D(x'_n,z).     \tag{4.2}
\]

Equation (1.4) gives \(D(x_n,t)\le C_K\).  For all sufficiently large
\(n\), the upper bound \(\log p_z(x'_n)+C_K\) is negative.  Hence (1.4),
(3.5), and (4.1) give

\[
                  J_n\le C_K+a_*\{\log p_z(x'_n)+C_K\}
                         \longrightarrow-\infty.      \tag{4.3}
\]

If designated success causes a structural exit, (3.5) gives a fixed
positive probability of its physical exit jump.  We have therefore proved
the exact alternative

\[
 \boxed{\text{coercive negative common-}W\text{ reward}
        \quad\text{or}\quad
        \text{positive physical structural-exit flux}.}             \tag{4.4}
\]

Here is the literal state selection, including exits.  Put in the menu the
depth-two rule for every labelled directed edge; the menu is finite.  At a
marked state in a terminal chart, first select a rule whose designated
first-jump label leaves the chart, if one exists, maximizing that label's
all-clock probability.  If none exists, select the rule with the smallest
exact expected \(F\)-increment (ties are broken by a fixed ordering).

Uniformity is now sequential.  If neither a common exit probability nor a
common negative margin existed outside a finite chart subset, an escaping
violating sequence would have a subsequence with fixed mark, certified edge,
cap phase, and limiting source ratios.  If the certified \(e\)-endpoint
leaves the chart, the exit-first rule has probability at least
\(a_e\ge a_*\), a contradiction.  Otherwise its exact score is (4.2) and
tends to \(-\infty\) by (2.3)--(4.3), so the minimum-score rule has no larger
score, again a contradiction.  Thus the finite menu realizes (4.4); the
argument does not require a run-time guess of an asymptotic tier ratio.

## 5. Moments, duration, and physical-time Foster form

The episode has at most two jumps.  Applying (1.5) at its one or two marked
starts gives every fixed moment of its positive \(F\)-increment.  At each
stage the current mark is enabled, so the total hazard is at least the
minimum positive source out-rate \(K_*>0\).  Conditional waiting times are
therefore dominated by exponentials of rate \(K_*\), and the episode
duration has every fixed moment, uniformly over the chart.  In particular,
every episode contains at least one actual jump and has strictly positive
physical duration almost surely; there are no zero-time chart handoffs.

The potential \(W=1+F\) is nonnegative and proper on the marked state space:
marks range over a finite binary set, and an escaping population makes at
least one residual factorial diverge.  The sequential finite-menu argument
after (4.4) therefore yields, outside a finite chart subset,

\[
 \mathbb E_{x,t}
   [W(X_\tau,T_\tau)-W(x,t)+\eta\tau]\le-1            \tag{5.1}
\]

for one fixed \(\eta>0\), or else the selected exit-first rule has a fixed
positive probability of recording a physical structural exit.  The endpoint
is actual and integrable in either case.

### Theorem 5.1

Fix a reduced weakly reversible binary network, a closed population class,
one orientation, and fixed positive labelled rates.  On every tier/cap
chart satisfying the corrected S-tier-superlevel condition (3.2), the
common marked factorial potential \(W=1+F\) admits the depth-two all-clock
state-selected rule above.  Along every escaping sequence, the rule has
either the physical-time Foster estimate (5.1) or positive physical
structural-exit flux.

In particular, every all-active tier-pass chart is covered without a
potential switch.  This is a local drift-or-exit contract.  It composes
directly with adjacent common-\(W\) rules if those episodes tile the complete
relevant trace with no omitted entrance or recharge gap.  If such a gap is
present, one must instead verify the incoming charged-seam condition of the
terminal Green--Foster theorem; unweighted structural-exit flux alone does
not pay an unbounded entrance toll.

The exact charged-seam dependency just named lies in `research_notes/`.
Its filename is the concatenation of

~~~text
proof_first_terminal_chart_
green_foster_duality.md
~~~

Its SHA-256 is the concatenation of

~~~text
899aa11e15d3e23f629bf06cdfac3a05a
47915f5a90378bb8d91982ae0ed6211
~~~

## 6. Exact scope boundary

This theorem treats passing descriptors.  It makes no claim on a descriptor
which fails the corrected cut, including the residual 336 level-set family;
those charts require their separate global pair theorem.  It also does not
infer a recurrence result from the finite descriptor count.  Its only
finite input is the exact graph implication (3.2)--(3.4).

The proof uses the literal global top S-tier.  It does not replace \(E\) by
the global top D-tier when that tier is disabled, and it does not select an
edge sourced merely in the part of \(U_L(r)\) outside \(E\).  These two
distinctions are exactly what make (2.3) and (3.5) valid.
