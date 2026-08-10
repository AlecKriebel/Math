# Reflected level processes for the one-active repair

## 1. The exact monotone coordinate

At a failed one-active descriptor, let $X$ be the unique active species.
The highest active degree is one: a complex $2X$ would be an enabled strict
top source and would make the descriptor pass. Hence every reaction has

\[
 \Delta X\in\{-1,0,1\}.                               \tag{1.1}
\]

Augment the physical chain by a reflected debt $D$, initialized at zero,
and update it after each reaction by

\[
 D^+=\begin{cases}
 D+1,&\Delta X=1,\\
 (D-1)^+,&\Delta X=-1,\\
 D,&\Delta X=0.
 \end{cases}                                          \tag{1.2}
\]

Put

\[
 H=X-D.                                                \tag{1.3}
\]

Then $0\le D\le X$, $H\ge0$, and $H$ is pathwise nonincreasing. It
decreases by one exactly when an $X$-exit fires at $D=0$. Entries and
debt-cancelling exits leave $H$ unchanged. This identity is immune to
nested entries and does not require a genealogical matching rule.

The failed uniform old-debt lemma tried to force a bounded-time decrease of
$H$. The nested-entry obstruction shows that the probability of such a
decrease can vanish with $X$. The correct object is instead the physical
chain killed on the first strict $H$-decrease.

## 2. A fixed-level killed process

Before the killing time, a level $H=h$ satisfies

\[
 X=h+D.                                                \tag{2.1}
\]

Suppose first that the two inactive coordinates range in a finite set $E$
which is structurally closed for the leading dynamics. More generally, one
may stop on a boundary only when that boundary has separately been proved
to enter a controlled multiscale flag. On the retained states the killed
level process has the finite-phase form

\[
 \{(D,e):D\in\mathbb N_0,\ e\in E\}.                  \tag{2.2}
\]

Because active degree is at most one, every top-source rate is affine in
$h+D$; every lower-source rate is independent of $h+D$. Population jumps
are bounded.

An arbitrary fixed inactive box is not legitimate here. An accelerated
immigration--death coordinate can leave every fixed box while remaining
tight and of order one. Nor does an unbounded but subpower coordinate
automatically receive positive weight in a coarse active-weight vector.
Every boundary outcome must therefore be retained and classified by the
full D-tier/source-rate flag. It may be genuine promotion, a recurrent
countable phase, or a return to another one-active chart.

The local stochastic gate is consequently:

> **Fixed-level gate.** Starting at $D=0$, prove that the killed process
> reaches either a strict $H$-decrease or an explicitly controlled boundary
> flag in finite mean physical time, with the endpoint moments needed by
> the common-potential gluing theorem.

This formulation is a source-rate subsequence alternative. It does not use
tightness as finite support and does not call every finite-box exit
promotion.

## 3. Polynomial, not uniform, accessibility

Fix a finite prescribed reaction-word state set and stop when the word
succeeds or any competing reaction leaves that set. With $N=h+D$, every
race rate is a polynomial of degree at most one in $N$. Finite first-step
equations show that every word-hitting probability is a rational function
of $N$. Consequently it is either identically zero or has an expansion

\[
 p_N=cN^{-m}+O(N^{-m-1})                               \tag{3.1}
\]

for some integer $m\ge0$ and $c>0$. Equivalently, the exponent counts the
number of lower clocks which must beat transient $N$-speed clocks, after
closed fast classes have been contracted. Matrix-tree or Cramer formulas
make (3.1) an exact finite certificate once the stopped state set and word
are specified.

Equation (3.1) is only an accessibility statement. It does not prove that
the first accessible negative word dominates positive unresolved words,
nor does it control a repeated process whose debt $D$ is unbounded. The
nested-entry example demonstrates both why the exponent matters and why a
uniform lower bound is false.

## 4. Two legitimate closure routes

### 4.1 Repeated absorption

Prove directly that a correctly closed level process, killed at a strict
decrease or a controlled boundary flag, has finite mean endpoint time from
every $D=0$ state. The mean may grow arbitrarily with $h$. Once every
boundary continuation is composed and the trace endpoints have finite
$h$-shells, the shell-adapted theorem in
*scalarization_and_foster_lemmas.md* absorbs that growth into

\[
 U(h)=\sum_{j\le h}c(j).                               \tag{4.1}
\]

This route needs an almost-sure strict decrease at the completed endpoint,
but no uniform service probability and no bound on raw fast-jump counts.

### 4.2 Rare macroscopic descent

Stop one bounded-duration primary attempt. If a probability of order
$N^{-m}$ produces a potential drop of order $N^m$, while the expected
positive endpoint cost is $o(1)$, the rare-event lemma in
*shell_dependent_episode_foster.md* gives a uniform negative expected
episode. The nested-entry network uses $m=2$ and $W=C^2$.

These routes may be combined: use a polynomial Foster function to return
large $D$ to a bounded debt core, and a finite number of rare-word trials
inside that core to obtain the strict $H$-decrease.

## 5. Exact remaining theorem

A universal one-active theorem would follow from the following statement.

> **Candidate reflected-level theorem.** For every finite binary
> weakly-reversible support pair with at most two linkage classes, every
> one-active failed source-rate flag, every strong orientation and every
> positive rate vector, the associated fixed-level process has exactly one
> of these alternatives:
>
> 1. a strict $H$-decrease has finite mean hitting time;
> 2. a finite-time endpoint enters a separately controlled multiscale flag,
>    with the moments needed to compose its continuation; or
> 3. an affine invariant with strictly positive $X$-coefficient, or a
>    bounded coboundary for the active reward, bounds $X$ on the inactive
>    phase and makes the level finite.

The third alternative cannot be restricted to invariance of $X$ itself.
For example, the weakly reversible cycle
$0\to X+U\to V\to0$ preserves $X-U$, not $X$. On a bounded $U,V$ phase
that invariant still bounds $X$, and the active reward is a bounded
coboundary. This is a finite-level alternative, not a service episode.

The finite support certificate should record the slow-before-fast exponent
of every negative word and every positive unresolved word. The analytic
proof must additionally rule out a null/transient reflected level, control
every boundary continuation, and retain one common endpoint potential.
Until those steps are proved, this is a repair program rather than a T3-2
theorem.
