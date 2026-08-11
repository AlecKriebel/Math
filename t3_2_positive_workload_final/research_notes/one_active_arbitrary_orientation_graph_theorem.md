# Arbitrary-orientation graph theorem for the candidate one-active table

## 1. Scope and exact partition

This note proves the finite graph/resistance part of the candidate
one-active repair for arbitrary strongly connected directed linkage graphs.
It does **not** infer aggregate stopped probabilities from selected words,
does not prove a promotion continuation, and does not certify pair
recurrence or T3-2.

The exact selector and regression are in
`src/one_active_relative_debt_cegar.py`, function
`graph_architecture_certificate`, with focused tests in
`tests/test_one_active_relative_debt_cegar.py`.  The frozen incidence-row
hash is

```text
15fb66321d495bbe6fc63bbdf28c17a2975eea8bb23ca0dc08f22c868ec457c2
```

After relabelling the active species as $C$, all 3,297 feasible failed
incidences on the 1,227 candidate support pairs split as follows:

\[
\begin{array}{l|r}
\text{graph category}&\text{incidences}\\ \hline
\text{mixed linkage has the source }C&1695\\
\text{Family I: origin service of resistance }0&710\\
\text{Family I: origin service of resistance }1&75\\
\text{Family I: no historical positive-debt origin}&185\\
\text{Family II: axis service of resistance }0&24\\
\text{Family II: no historical positive-debt axis base}&6\\
\text{Family III: origin service of resistance }0&234\\
\text{Family III: origin service of resistance }1&40\\
\text{Family III: origin service of resistance }2&16\\
\text{Family III: no historical positive-debt origin}&90\\
\text{open wholly-top phase: service of resistance }1&210\\
\text{open wholly-top phase: no historical positive debt}&12
\end{array}
\tag{1.1}
\]

The first ten rows sum to 3,075 mixed-phase incidences.  The final 222
rows have a genuine countable neutral top phase.  Their graph routing is
proved in Section 7, while their probabilities and moments require the
separate $\{0,U\}$ resolvent contract.  They are not silently treated as
a finite graph.

## 2. Relative debt and the theorem

Start a local episode with old reflected $C$-debt $d>0$ and set the
relative active displacement to $r(0)=0$.  Until the first $r<0$,

\[
 D_C(t)=d+r(t),
\tag{2.1}
\]

so this first negative displacement is exactly a strict reduction of old
debt.  A degree-zero reaction has resistance one if it fires while some
active-degree-one source is enabled; active-source reactions have
resistance zero.  At a no-fast base let $m_-$ be the least resistance to
$r<0$, and $m_+$ the least resistance of a return to the same no-fast
set with $r>0$.  In the wholly-top phase there is no no-fast base; there
$m_-$ and $m_+$ instead count lower-source firings before, respectively,
strict descent and a positive return to the face $B=0$.

> **Theorem 2.1 (arbitrary-orientation relative resistance).**  In every
> incidence in (1.1), for every strongly connected orientation of
> each linkage support and every historically consistent positive-debt
> base, one of the following holds.
>
> 1. A mixed linkage contains the physical source $C$.  A zero-resistance
>    top path strictly reduces debt directly; there is no no-fast base.
> 2. The no-fast base is the origin or one of the exact invariant axis
>    states in Family II.  Then
>    
>    \[
>      0\le m_-\le2,
>      \qquad m_+\ge m_-+1.
>    \tag{2.2}
>    \]
> 3. The displayed base is frozen or supports only neutral carrier pairs,
>    and no positive reflected debt is historically reachable there.
> 4. The wholly-top linkage is $C\rightleftarrows A+C$.  Either the
>    other linkage has a pure-$A$ lower vertex and
>    $m_-=1<m_+$, or the face $B=0$ is closed and carries no historical
>    positive debt.
>
> Every debt-reduction witness in item 2 stays below total inactive
> population five.  The bound five is sharp for this construction; a
> claimed universal bound four is false.

No bounded CEGAR is used in the proof.  The executable table only verifies
that the finite support alternatives below exhaust the atlas.

## 3. Direct physical-$C$ rows

In the 1,695 direct rows, some **mixed** linkage contains $C$ and at
least one degree-zero complex.  Since $d>0$ implies $C\ge1$, the source
$C$ is enabled.  Follow a simple directed path in that strong linkage
from $C$ to a lower complex.  Before its first lower target the path uses
only active-degree-one sources; top-to-top edges have active reward zero,
and the first top-to-lower edge has reward $-1$.  The path therefore
reduces old debt at resistance zero.  Following a complex path is physical:
after firing $y\to z$, the next path source $z$ is present.

The qualifier “mixed” is essential.  In the 222 open rows the source $C$
lies in the wholly-top pair $C\leftrightarrow A+C$, whose reward is
identically zero.  Those rows are not included in this direct argument.
The exact table further splits the 1,695 rows into 1,030 with one
lower-only and one mixed linkage, and 665 with two mixed linkages.

## 4. Family I: one mixed linkage with both cofactors

Here one linkage is lower-only and the mixed linkage has the two top
sources $A+C,B+C$.  Thus a fast source is enabled exactly when
$M=A+B>0$, and the unique no-fast base is the origin.

If the lower-only linkage contains $0$, follow its first edge away from
$0$; the resulting nonzero lower complex enables a top carrier, whose
first mixed-linkage exit lowers $r$.  This costs zero.  If the mixed
linkage contains $0$ and another nonzero lower complex, take a simple
path from $0$ to such a complex.  Either it reaches a lower complex
before entering the top, or one entry is followed by an exit to that
complex.  In both cases the remaining nonzero cofactor supplies one extra
active exit.  Again $m_-=0$.  These are the 710 rows.

If neither linkage contains $0$, the origin is frozen and cannot carry
historical positive debt.  The only remaining support alternative is

\[
 T=\{0,A+C,B+C\},
\tag{4.1}
\]

paired with one of nine lower-only strong supports, each containing a
degree-one and a degree-two complex but not $0$.  Strong connectivity of
the lower linkage gives a directed cut edge $u\to q$ from a unary to a
quadratic complex.  A simple top-only path in (4.1) lets the free
$0$-entry place its cofactor at $u$.  Fire $u\to q$ once, at
resistance one.  There is now inactive mass two but only one fresh active
molecule, so two active exits give $r=-1$.  Thus $m_-=1$ in the 75
residual rows.

For the matching upward bound, decompose a positive origin-return word at
its intermediate origin visits and retain one positive primitive
excursion.  Its initial lower reaction is the sole free launch.  With no
paid reaction, every later reaction is an active-source conversion or
exit; at least one exit is needed to return to the origin, so its reward is
nonpositive.  Hence the resistance-zero rows have $m_+\ge1$.

In the residual case write $I,E,L$ for the numbers of active entries,
active exits, and lower-to-lower firings in a primitive excursion.  Since
the mixed lower support is only $0$,

\[
 \operatorname{resistance}=(I-1)+L.
\tag{4.2}
\]

If this is at most one and $I-E>0$, then either $I=1,E=0$, in which
case one paid lower edge cannot remove the nonzero cofactor because the
lower linkage omits $0$; or $I=2,L=0,E\le1$, in which case two
$0$-entries leave mass two and one exit cannot return to the origin.
Thus $m_+\ge2>m_-=1$.

## 5. Family II: the exact invariant axis

Here the sole top source is $B+C$, so the no-fast set is $B=0$.  The
atlas leaves only the five support types proved in detail in
`research_notes/one_active_family_ii_axis_graph_theorem.md`.  In four
types the first linkage is $A\leftrightarrow A+B$, so $A$ is an exact
population invariant.  In the fifth, every reaction preserves $A+B$.
On a fixed class \(\Gamma\), the apparent spectator therefore has an
exact conserved value \(a_\Gamma\).  The atlas label \(0,1,2\) is the
availability category \(\min\{a_\Gamma,2\}\); label \(2\) permits every
fixed \(a_\Gamma\ge2\).  It is not an unbounded counter inferred to lie
in a box, and constants may depend on \(a_\Gamma\).

Every historically consistent base has a zero-resistance route which
creates $B$ without increasing $C$, followed by a $B+C$-exit.  A
zero-resistance primitive return can have only one lower launch before
$B>0$, followed solely by $B+C$-exits.  The launch adds at most one
active molecule and at least one exit is required, so its reward is
nonpositive.  Hence $m_-=0<m_+$.  The remaining six rows are frozen or
have only a forced neutral entry/exit pair and cannot carry historical
positive debt.

## 6. Family III: two singleton mixed linkages

The two top sources are $A+C$ and $B+C$, one in each mixed linkage.
Thus the unique no-fast base is the origin.  Exactly 82 rows contain no
zero source and are frozen.  In another eight rows the only zero linkage is
$0\leftrightarrow A+C$, while the other linkage has no source $A$ or
$2A$; the reachable $A$-axis consists only of neutral carrier pairs,
so positive debt cannot return to the origin.

If a zero-containing linkage also has a nonzero lower vertex, the simple
path argument from Section 4 gives $m_-=0$.  It covers 234 rows, and the
primitive-launch argument gives $m_+\ge1$.

It remains to take

\[
 L_A=\{0,A+C\},\qquad L_B=\{B+C\}\cup S,qquad 0\notin S.
\tag{6.1}
\]

If $A\in S$, strong connectivity and the fact that the exact neutral
support $\{A,B+C\}$ is absent give either an outgoing $A$-edge to a
different lower complex or a $B+C$-exit to a lower complex other than
$A$.  After the free $0\to A+C$ entry, use that one paid edge.  A
quadratic target carries two consecutive active exits; a unary $B$
target has a $B+C$-exit to a nonzero lower target and hence also carries
the required second exit.  If the paid edge is $A\to B+C$, the first
exit and the nonclosed-support alternative carry two more exits.  In all
cases $m_-\le1$.  Primitive counting gives
$(I-1)+L\le1\Rightarrow I+L\le2$; the cases $I=1$ and $I=2$ cannot
return the inactive population to zero with $I>E$.  Thus
$m_+\ge2$.  These are the 40 depth-one rows.

If $A\notin S$ but $2A\in S$, the exact selector leaves only

\[
\begin{split}
S\in\{&\{2A,2B,A+B\},\{B,2A,A+B\},\\
      &\{B,2A,2B\},\{B,2A,2B,A+B\}\}.
\end{split}
\tag{6.2}
\]

Fire $0\to A+C$ twice.  Strong connectivity gives a directed cut edge
leaving the vertex set $\{2A,B+C\}$.  If that edge is sourced at $2A$,
fire it directly as the second paid reaction; its lower target is
$B,A+B,$ or $2B$ and supports three consecutive active exits.  If the
cut edge is sourced at $B+C$, first fire $2A\to B+C$ as the second paid
reaction and then take the cut edge as an active exit.  Its nonzero lower
target supports the remaining exits.  Hence $m_-\le2$.

For a positive primitive origin return,

\[
 \operatorname{resistance}=(I-1)+L,qquad I>E.
\tag{6.3}
\]

Resistance at most two implies $I+L\le3$.  If $I=1$, the first $A$
cannot be removed with no exit.  If $I=2$, the second entry must again be
$0\to A+C$; one lower firing and at most one exit cannot drain its
nonzero target.  If $I=3,L=0$, the first two entries are forced to be
$0\to A+C$.  An $A+C$-exit before the third entry either revisits the
origin, contrary to primitivity, or leaves only one $A$, forcing the third
entry to be $0\to A+C$; the remaining exit cannot drain mass two.
Without that interspersed exit, either all three entries are
$0\to A+C$, requiring three exits, or the third is
$2A\to B+C$.  In the latter case the first $B+C$-exit has a target in
$S$, which contains neither $0$ nor $A$; one further active exit cannot
drain it.  Thus $m_+\ge3>m_-$.  These are the sixteen depth-two rows.

## 7. The 222 wholly-top rows

The wholly-top linkage is forced to be

\[
 C\rightleftarrows A+C.
\tag{7.1}
\]

It preserves the active count and, after stripping $C$, is the countable
immigration--death phase $0\rightleftarrows A$.  The other linkage has
the sole top source $B+C$.  Partition its lower support as

\[
 P\subseteq\{0,A,2A\},\qquad
 Q\subseteq\{B,A+B,2B\}.
\tag{7.2}
\]

The exact table has $Q\ne\varnothing$ in all 37 normalized support types.
In 35 types, or 210 physical incidences, also $P\ne\varnothing$.
Strong connectivity gives the following dichotomy.  If some directed
edge leaves $P$ for $Q$, use the neutral top phase to put $A$ at its
source and fire that edge once.  It creates $B$ without increasing $C$,
and one $B+C$-exit gives $r=-1$.  Otherwise a directed cut out of $P$
contains an edge $P\to B+C$, and a directed cut from
$P\cup\{B+C\}$ to $Q$ must contain an edge $B+C\to Q$.  Fire the first
edge, then that exit, then one further $B+C$-exit.  The rewards are
$+1,-1,-1$.  In both cases $m_-=1$.

A return to $B=0$ after at most one lower-source firing cannot have
positive reward.  A lower-to-lower firing has reward zero, while an entry
to $B+C$ has reward $+1$ but returning to $B=0$ requires at least one
active exit of reward $-1$.  Hence $m_+\ge2$ for arbitrary strong
orientations.

The remaining two support types, giving twelve physical incidences, are

\[
 \{B,2B,A+B,B+C\},\qquad \{B,A+B,B+C\}.
\tag{7.3}
\]

Here $P=\varnothing$.  On $B=0$ the wholly-top phase changes only $A$,
whereas every source in the mixed linkage requires $B$.  Thus this face
is closed, all its reactions have active reward zero, and no historical
positive active debt is reachable there.

Section 7 is only the graph/resistance statement.  Turning the 210 routes
into aggregate probabilities uses the factorial-tail resolvent of the
countable $0\rightleftarrows A$ phase; it is not a finite-box argument.

## 8. Why population four is not a valid CEGAR cutoff

Consider

\[
 \{0,A+C\},\qquad \{2A,2B,A+B,B+C\},
\tag{8.1}
\]

with the strong orientations

\[
 0\leftrightarrow A+C,qquad
 2A\to B+C\to2B\to A+B\to2A.
\tag{8.2}
\]

The depth-two word

\[
 0\to A+C, 0\to A+C, 2A\to B+C,
 \underbrace{B+C\to2B,\ldots,B+C\to2B}_{4\text{ exits}}
\tag{8.3}
\]

has relative rewards

\[
 1,2,3,2,1,0,-1
\tag{8.4}
\]

and inactive populations

\[
 A,2A,B,2B,3B,4B,5B.
\tag{8.5}
\]

Only the second $0$-entry and $2A\to B+C$ are paid, so its resistance
is two.  In this directed graph no resistance-two service can stop before
the fourth repeated exit.  Thus population cutoff four would delete a
valid shortest witness.  The analytic construction uses at most five, and
the executable bounded regression's cutoff seven is conservative.

## 9. Exact carrier bound for the moving cutoff

There is a deterministic part of the three-interruption estimate which
does follow from the graph theorem.  Consider a primitive raw attempt in
Families I--III, stopped at its first no-fast return or first $r<0$, and
write

\[
 M=A+B,qquad K=\#\{\hbox{paid degree-zero firings}\}.
\tag{9.1}
\]

In Families I and III, \(M_0=0\).  In Family II, write
\(M_0=a_\Gamma\) for the exact classwise invariant; it need not be at most
two.  In Families I and III the first launch
from the origin is the only free degree-zero firing.  In Family II every
zero-contest path before launch remains in its exact invariant slice of
mass \(a_\Gamma\).  Thereafter each degree-zero firing while a carrier is
enabled is paid.  Consequently there are at most $K+1$ degree-zero
firings which can increase inactive mass, and each increases $M$ by at
most two.

Let $I$ and $E$ be the active entries and exits before the stop.  Entries
are among those degree-zero firings, so $I\le K+1$.  Before the first
negative reward, $E\le I+1\le K+2$.  In Families I--III every top
cofactor has inactive degree one.  Top-to-top conversions preserve $M$,
and a top exit increases it by at most one.  Hence, pathwise,

\[
 \sup_{t\le\tau}M_t
 \le M_0+2(K+1)+(K+2)
 =M_0+3K+4.
\tag{9.2}
\]

The same count also controls active overshoot:

\[
 r^+\le I\le K+1.
\tag{9.2a}
\]

In particular, once a moving boundary satisfies
\(L>M_0+10\), a finite mixed carrier attempt cannot hit it with
\(K\le2\).  Since \(M_0\) is fixed on \(\Gamma\) and
\(L_n=n^{1/8}\to\infty\), this holds for all sufficiently large \(n\).
This is the exact
carrier-conservation input behind the third-interruption remainder.  It
does not apply to a zero-resistance countable phase: direct-$C$ rows and
the wholly-top rows instead require their factorial phase-maximum bound.

For clarity, the probability estimate still needs an analytic Green
bound.  On the active clock and below $M<L$, the paid lower-reaction
intensity is bounded by

\[
 \lambda_{\rm paid}\le {C(1+M)^2\over N}
 \le {CL^2\over N}.
\tag{9.3}
\]

If the ordered carrier segments have uniformly bounded killed occupation
and endpoint-weighted moments, the ordered compensation formula and
(9.3) give, for every fixed $q$,

\[
 \begin{split}
 \mathbb P\{K\ge3,\ \sup_{t\le\tau}M_t<L\}
 &\le C\left({L^2\over N}\right)^3,\\
 \mathbb E[(1+K)^q;K\ge3,\ \sup_{t\le\tau}M_t<L]
 &\le C_q\left({L^2\over N}\right)^3.
 \end{split}
\tag{9.4}
\]

Equation (9.4), not the inactive-mass bound alone, is what controls the
active overshoot in (9.2a) when $K$ is large.  It remains conditional on
the stated weighted resolvent/occupation hypothesis.  Word resistance
alone does not prove that hypothesis.

## 10. Conditional stochastic corollary and remaining gate

Theorem 2.1 is a graph theorem, not a probability theorem.  It yields the
following corollary only under a separately proved killed-resolvent
contract.  Suppose a full-reaction regenerative attempt realizes the
displayed $m=m_-$ with aggregate probability at least $aN^{-m}$, every
same-base upward endpoint has aggregate probability at most
$bN^{-(m+1)}$, neutral attempts return to the same finite base phase,
and duration and factorial endpoint moments satisfy the hypotheses of the
fourth-power interface.  Then repetition to the first nonneutral endpoint
has downward probability $1-O(N^{-1})$, duration of the certified
polynomial order, and strict drift for the common potential
$(1+\mathcal F_{\ell})^4$.

None of those aggregate statements follows from one word.  In particular,
the 222 open rows require the countable $\{0,U\}$ regeneration/resolvent
estimate, and every promotion exit requires the same-potential stopped
access contract.  Those analytic obligations, pair recurrence, and global
T3-2 all remain false in the executable flags.
