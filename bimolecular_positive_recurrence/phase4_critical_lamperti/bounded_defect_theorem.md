# Bounded-defect theorem and exclusion of a critical Lamperti branch

## 1. Statement

Fix a mixed, bimolecular, strongly connected one-linkage complex graph and a
quadratically safe nonempty species set \(I\). Put \(J=\mathcal S\setminus
I\) and

\[
q(y)=q_I(y),\qquad M(x)=\sum_{i\in I}x_i.
\]

On a compact top-composition sector assume

\[
x_i\ge \eta M\quad(i\in I),\qquad \eta>0,
\]

and stop when the exact \(J\)-configuration leaves a fixed finite box, an
\(I\)-coordinate falls below \(\eta M/2\), a catalytic fractional drain
occurs, or a prescribed finite set is reached.  On every closed no-exit
component of this stopped regime exactly one of the following occurs.

1. **Conservation.**  There is an exact linear conservation law
   \(M+b\cdot X_J\).  In the special zero-reward case below it is the explicit
   token law
   \[
   M-\sum_{D\in K}X_D.
   \]

2. **Strict corrected-square drift.**  There is a finite regenerative phase
   variable \(\phi\), a bounded Poisson corrector \(h(\phi)\), constants
   \(c,C,N_0>0\), and a macrostep \(\sigma\) such that, for
   \(Y=M+h(\phi)\),
   \[
   \mathbb E[Y_\sigma^2-Y_0^2]\le -cM,
   \qquad
   \mathbb E\sigma\le C,
   \qquad M\ge N_0.
   \]

There is no nonconservative recurrent phase class with a critical coefficient
\(\Xi=2a+v\ge0\).  If the leading mean reward is zero, the corrected
increment is identically zero on the recurrent phase graph and the explicit
token conservation law holds.

## 2. Exact slow-fast decomposition

The safe-support theorem gives

\[
q(y)\in\{0,1\}\quad(y\in\mathcal C)
\]

and every positive-source reaction satisfies \(q(y')\le q(y)\).  Consequently

\[
R_{00}:0,\qquad R_{01}:+1,\qquad R_{10}:-1,\qquad R_{11}:0
\]

are the possible increments of \(M\).  Inside the finite defect box an
enabled \(q=0\) source has bounded propensity.  An enabled \(q=1\) source
contains one active \(I\)-particle, so its propensity is between \(cN\) and
\(CN\), uniformly on the compact composition sector.  Here and below all
constants may depend on the finite graph, the positive rate vector, the
box, and \(\eta\), but not on \(N\).

The finite fast graph consists of the \(q=1\)-source transitions.  A fast SCC
containing a death edge has a reusable negative cycle.  Repeated finite-state
minorization before the next slow event then gives a catalytic fractional
drain, with failure probability exponentially small in \(N\).  This is the
already certified F1 branch.

Suppose therefore that no fast SCC contains a death edge.  Death edges cross
the condensation DAG, so a fast relaxation contains at most a fixed number
of deaths.  Every fast target/source phase and every defect configuration is
then contained in a genuinely finite transient/absorbing CTMC.  Its
absorption probabilities, reward moments and mean absorption times are
rational functions of \(N\), the top composition, and the rate constants.
The transient block is an M-matrix.  Its inverse is a ratio of directed-tree
polynomials with positive coefficients.  Hence, uniformly on the compact
composition sector,

\[
P_N=P_0+O(N^{-1}),
\]

and all first three reward moments are bounded.  A competing slow event
during a fast relaxation has probability \(O(N^{-1})\): the total slow rate
is bounded, the fast rate is at least \(cN\), and the expected number of fast
jumps before absorption is uniformly bounded.

## 3. Nonpositivity of every limiting macrotransition

A slow epoch starts in a terminal fast phase, fires one \(q=0\)-source
reaction, and includes the complete ensuing fast relaxation.

* A \(q=0\to0\) trigger contributes zero to \(M\).  Every subsequent fast
  death can only reduce the reward.  Its complete reward is therefore at
  most zero.

* A \(q=0\to1\) trigger contributes \(+1\).  Its target \(q=1\) complex is
  present.  In a strongly connected mixed linkage there is a directed path
  from that target to a \(q=0\) complex.  Every source on the initial
  \(q=1\) part of this target-following path is fast and enabled.  A terminal
  fast class without a death would therefore contradict reachability of
  \(q=0\).  Thus relaxation contains at least one death before returning to
  a terminal slow phase.  The complete reward is at most \(1-1=0\).

This is a pathwise assertion for the limiting macrotransition.  It is not an
average sign comparison and uses no comparison of unrelated rate monomials.

## 4. Service-token dichotomy

Assume first that no unary \(q=1\) complex occurs.  Every \(q=1\) complex is
then uniquely of the form

\[
I_i+D,
\]

where \(D\in J\).  Let \(K\subseteq J\) be the set of all such service
species.

If no \(q=0\) complex contains a species of \(K\), then every \(q=1\) complex
contains exactly one \(K\)-particle and every \(q=0\) complex contains none.
Therefore, edge by edge,

\[
W(x)=M(x)-\sum_{D\in K}x_D
\]

is conserved.  This is checked by `xi_certificate.py` without solving an
asymptotic sign problem.

Otherwise a \(q=0\) complex contains a service species.  Whenever that
complex is present, a corresponding \(I_i+D\) source is enabled.  Its fast
relaxation removes an \(I\)-particle without a preceding \(q=0\to1\) birth,
so the associated macrotransition has strictly negative reward.  Strong
connectivity of the complex graph implies reachability of this phase from
every terminal slow phase: take a directed complex path and replace each
maximal \(q=1\) segment by its fast absorption.  On a closed no-exit component
this gives a path in the limiting slow kernel.  Hence every recurrent class
of \(P_0\) contains a strict negative transition.

If a unary \(q=1\) complex occurs, it is enabled throughout the top sector.
A target-following path from it to \(q=0\) produces an unpaired death.  Either
this repeats and gives the catalytic branch, or it reaches an exit.  Thus the
unary case is also strict and never critical.

The service-token alternatives are mutually exclusive.  In the conservation
case all macrorewards are zero.  In the strict case all macrorewards are
nonpositive and at least one transition in every recurrent class is
negative.

## 5. Poisson correction and square drift

Let \(\pi\) be the stationary distribution of an irreducible recurrent class
of \(P_0\), and let \(r(s,s')\le0\) be its limiting macroreward.  Set

\[
d_0(s)=\sum_{s'}P_0(s,s')r(s,s'),
\qquad b_0=\sum_s\pi(s)d_0(s).
\]

In the nonconservative branch, positivity of \(\pi\) and the strict negative
transition imply \(b_0<0\).  Solve exactly

\[
(I-P_0)h=d_0-b_0,
\]

with one normalization.  Then the corrected increment

\[
\Delta Y=r(s,s')+h(s')-h(s)
\]

has conditional leading mean \(b_0\) at every recurrent phase.  The
\(O(N^{-1})\) kernel error and the bounded reward moments give, for all large
\(N\),

\[
\mathbb E[\Delta Y\mid s]\le \frac12b_0,
\qquad
\mathbb E[(\Delta Y)^2\mid s]\le C.
\]

Since \(h\) is bounded and \(Y=M+O(1)\),

\[
\begin{aligned}
\mathbb E[Y_\sigma^2-Y^2\mid s]
 &=2Y\,\mathbb E\Delta Y+
   \mathbb E[(\Delta Y)^2]\\
 &\le b_0Y+C\\
 &\le -cM
\end{aligned}
\]

outside a finite set.  Mean physical duration is bounded because a terminal
phase has an enabled slow reaction with rate at least the smallest positive
rate constant, while fast relaxation has mean duration \(O(N^{-1})\).
Transient phases are assigned the usual finite Bellman hitting corrector.

## 6. Why the Lamperti critical coefficient cannot occur

Suppose \(b_0=0\).  Every recurrent transition has reward at most zero and
every stationary phase has positive mass.  Hence every recurrent transition
with positive probability has reward exactly zero.  The reward is therefore
a finite coboundary with zero corrected increment on every recurrent edge,
so

\[
v=0.
\]

The service-token dichotomy then excludes the strict architecture and gives
the exact conservation law.  Thus the apparent formal branch

\[
b_0=0,\quad v>0,\quad \Xi=2a+v\ge0
\]

is not realizable by a nonconservative bounded-defect class.  The
nineteen-order false counterexample failed for precisely this reason: its
numerically tiny negative leading reward was obscured, but exact tree
arithmetic found the strict edge.

The argument compares no independent rate monomials.  Strictness comes from
a nonpositive pathwise reward and a reachable negative transition; zero
forces an edgewise invariant.
