# The positive-\(Q\) trace for the fifteen equal-depth one-active pairs

## 1. Scope and claim boundary

This note treats the coefficient-sensitive part of the fifteen support
pairs selected by `src/one_active_remaining_structure.py`.  It proves the
physical sign on the seventy-five active-\(C\) equality rows.  It does not
promote the fifteen pair-level recurrence count: the eight companion
one-active rows and the common-potential composition with the remaining
tier regions are recorded separately in Section 7.

After relabelling the active species to \(C\), every equality row has

\[
 L_0=\{0,A+C,B+C\},\qquad
 L_1=T\subseteq\{A,B,2A,A+B,2B\}.                    \tag{1.1}
\]

The directed graph on each displayed support is arbitrary and strongly
connected, and all labelled channel rates are positive.  Each of the
fifteen possible supports \(T\) contains at least one unary and at least
one quadratic complex.  Propensities use falling factorials.

The finite regression reports a positive-debt word and a first-surplus
word of the same slow-before-fast depth two.  That equality does **not**
give a critical reflected random walk.  One unary-to-quadratic reaction
already lowers positive debt by one at depth one.  A second such reaction
is needed only because the regression insists on crossing \(D=0\) and
recording a surplus exit.

## 2. The exact level

Put

\[
 M=A+B,\qquad Q=C-A-B=C-M.                            \tag{2.1}
\]

Every reaction in \(L_0\) preserves \(Q\).  A reaction \(y\to z\) in
\(T\) changes it by

\[
 \Delta Q=|y|-|z|\in\{-1,0,1\}.                     \tag{2.2}
\]

Thus unary-to-quadratic reactions move \(Q\) toward the origin on a large
positive shell, while quadratic-to-unary reactions move it away.

For \(N\geq0\), the \(L_0\)-shell \(Q=N\) is

\[
 \Gamma_N=\{(a,b,N+a+b):a,b\in\mathbb N_0\}.         \tag{2.3}
\]

Its unique base is \(z_N=(0,0,N)\).  The base is regenerative for the
\(L_0\)-chain: wait for a reaction sourced at \(0\), then follow the full
busy excursion until \(M=0\) again.

## 3. Exact shell law and the sign before perturbation

The linkage \(L_0\) is weakly reversible and deficiency zero.  Let
\(K_0,K_{AC},K_{BC}>0\) be its directed matrix-tree weights and set

\[
 u=K_{AC}/K_0,\qquad v=K_{BC}/K_0,\qquad s=u+v.
\]

The conditional product-form law on \(\Gamma_N\) is

\[
 \pi_N(a,b,N+a+b)
 =\frac1{Z_N}\frac{u^a v^b}{a!b!(N+a+b)!},\qquad
 Z_N=\sum_{m\ge0}\frac{s^m}{m!(N+m)!}.               \tag{3.1}
\]

For fixed \(r,t\geq0\),

\[
 \mathbb E_{\pi_N}[(A)_r(B)_t]
 =u^rv^t\frac{Z_{N+r+t}}{Z_N}.                       \tag{3.2}
\]

In particular,

\[
 \mathbb E_{\pi_N}A=\frac{u}{N}+O(N^{-2}),\qquad
 \mathbb E_{\pi_N}B=\frac{v}{N}+O(N^{-2}),           \tag{3.3}
\]

whereas every quadratic falling-factorial moment is \(O(N^{-2})\).

Let \({\cal E}_{12}\) be the set of directed channels in \(T\) from a
unary to a quadratic complex.  Strong connectivity and the presence of
both degrees imply \({\cal E}_{12}\ne\varnothing\).  If a unary source is
\(A\), respectively \(B\), write \(r_y=u\), respectively \(v\), and put

\[
 a_-:=\sum_{y\to z\in{\cal E}_{12}}\kappa_{yz}r_y>0. \tag{3.4}
\]

The stationary \(T\)-hazard therefore satisfies

\[
 \mathbb E_{\pi_N}{\cal L}_TQ
 =-\frac{a_-}{N}+O(N^{-2}).                           \tag{3.5}
\]

Every rate and orientation changes \(a_-\), but cannot change its strict
positivity.  Quadratic-to-unary channels contribute only to the
\(O(N^{-2})\) term.  Hence no choice of positive rational rates can reverse
the leading sign.

## 4. Regenerative perturbation with all reactions retained

Let \(\Lambda>0\) be the aggregate rate of the channels sourced at \(0\)
in \(L_0\).  For the \(L_0\)-chain, a cycle from \(z_N\) consists of an
\({\rm Exp}(\Lambda)\) base wait and a busy part.  Stripping the common
\(C\) molecule turns the busy part into a two-state transient
unimolecular particle system.  Its per-particle clocks are multiplied by
\(C=N+M\geq N\).  Strong connectivity of \(L_0\) makes the single-particle
killing chain phase type.  Consequently, for every fixed \(p\),

\[
 \mathbb E(\text{busy time})^p=O(N^{-p}),\quad
 \mathbb E\int (M)_1\,dt=O(N^{-1}),\quad
 \mathbb E\int (M)_2\,dt=O(N^{-2}).                  \tag{4.1}
\]

The last estimate includes overlapping \(0\)-source immigrants: a second
immigrant must arrive during an \(O(N^{-1})\) busy interval.  More
generally, the probability of reaching \(M\geq k\) before returning to
zero has a geometric-factorial bound uniform in \(N\).  This supplies
uniform integrability of every fixed endpoint and occupation moment.

Now retain every reaction in \(T\).  Fix \(\rho\in(0,1/4)\), and define
\(\tau_N\) to be the first of

\[
 \{\hbox{the positive return to }M=0\},\qquad
 \{M\geq\rho N\},\qquad
 \{Q\leq N/2\},\qquad
 \{Q\geq2N\}.                                        \tag{4.2}
\]

The last three endpoints are retained physical states.  They are genuine
multi-scale exits, not finite-box truncations: an inactive coordinate is
of active order, the positive level has already made a macroscopic
descent, or the level has made a macroscopic upward excursion which is
charged explicitly.  Equivalently, before any boundary one may stop
first at a degree-changing \(T\)-reaction and append the physical return
or boundary hit; no clock is suppressed during the append.

Only unary-to-quadratic reactions can increase \(M\).  Their total rate is
at most linear in \(M\); quadratic reactions cannot increase \(M\).
Together with the phase-type \(L_0\) killing blocks, this gives, for all
sufficiently large \(N\),

\[
 \sup_N\mathbb E_{z_N}\tau_N^p<\infty,\qquad
 \sup_N\mathbb E_{z_N}
 \left(1+\frac{M_{\tau_N}+C_{\tau_N}}N\right)^p<\infty
                                                               \tag{4.3}
\]

for every fixed \(p\).  A direct construction is to expose consecutive
single-particle killing blocks.  During one block a unary birth has
probability \(O(N^{-1})\); after such a birth the same estimate restarts
from at most two particles.  Quadratic and degree-preserving reactions may
change the particle labels, but do not increase \(M\), and every label has
a finite top path to \(0\).  Iteration up to \(M=\rho N\) gives a
subcritical geometric bound.  Reaching that boundary requires order \(N\)
successful immigration or unary-birth races against order-\(N\) top
clocks.  Hence, for every \(k<\infty\),

\[
 \mathbb P_{z_N}\{M_{\tau_N}\geq\rho N
                 \text{ or }Q_{\tau_N}\notin(N/2,2N)\}
 =O(N^{-k}).                                         \tag{4.4}
\]

The boundary overshoot is bounded because every population jump is
bounded, and (4.3) makes every fixed polynomial endpoint cost on (4.4)
negligible.  This argument retains the physical quadratic clocks; they
only insert label changes or deaths and never increase \(M\).

The probability of two or more \(T\)-reactions in the same busy excursion
is \(O(N^{-2})\).  The probability that the first degree-changing
\(T\)-reaction is quadratic-to-unary is also \(O(N^{-2})\), by (4.1).
Kac's cycle identity applied to (3.3) gives the first-order coefficient of
the unary-to-quadratic event.  Since
\(\pi_N(z_N)=1+O(N^{-1})\),

\[
 \begin{aligned}
 \mathbb E_{z_N}(Q_{\tau_N}-N)
   &=-\frac{a_-}{\Lambda N}+O(N^{-2}),\\
 \mathbb E_{z_N}(Q_{\tau_N}-N)^2
   &= \frac{a_-}{\Lambda N}+O(N^{-2}).                \tag{4.5}
 \end{aligned}
\]

These are full-reaction stopped-cycle expansions; (4.4) is included in
their remainders.  A unary conversion followed by
a degree-changing reaction, a reversal after a unary birth, and a boundary
carrier launched near the return time all contain a second lower-during-
fast contest and are part of the \(O(N^{-2})\) remainder.

## 5. Strict quadratic trace drift

At an ordinary base endpoint \(M=0\), one has \(Q=C\geq0\); the boundary
endpoints in (4.4) have negligible quadratic contribution.  Combining the
two lines of (4.5),

\[
 \begin{aligned}
 \mathbb E_{z_N}\bigl[Q_{\tau_N}^2-N^2\bigr]
 &=2N\,\mathbb E_{z_N}(Q_{\tau_N}-N)
   +\mathbb E_{z_N}(Q_{\tau_N}-N)^2\\
 &=-\frac{2a_-}{\Lambda}+O(N^{-1}).                  \tag{5.1}
 \end{aligned}
\]

Therefore there are \(N_0<\infty\) and \(\delta>0\), depending on the
oriented network and rates, such that

\[
 \mathbb E_{z_N}\bigl[Q_{\tau_N}^2-N^2+\delta\tau_N\bigr]
 \leq-\delta,\qquad N\geq N_0.                       \tag{5.2}
\]

This is the required positive-\(Q\) physical-time sign.  In particular,
the equality of the two canonical surplus-word exponents cannot produce a
null or transient reflected level on these rows.

## 6. Relation to reflected debt

On a fast \(L_0\) carrier, entries add one to both \(D\) and \(M\), top
exits at positive debt subtract one from both, and top conversions preserve
both.  Thus \(D-M\) is unchanged by the carrier dynamics until a surplus
exit.  A unary-to-quadratic \(T\)-reaction raises \(M\) by one and hence
lowers positive base debt by one after the carrier is drained.  It occurs
at one slow-before-fast contest.  A quadratic-to-unary reaction can create
one unit of base debt, but first requires two simultaneous cofactors and is
one order rarer.  The canonical depth-two surplus word from \(D=1\) is
just two consecutive depth-one debt reductions.

## 7. A single proper potential for all eighty-three rows

The quadratic trace need not be glued to the rest of the atlas as a
separate potential.  Fix any network-dependent linear corrector
\(\ell\in\mathbb R^3\), add a constant \(K\), and put

\[
 F_\ell(x)=K+\sum_i\log(x_i!)+\ell\cdot x,\qquad
 V(x)=F_\ell(x)^2,                                   \tag{7.1}
\]

where \(K\) is large enough that \(F_\ell\geq1\).  This \(V\) is proper.
On the base \(z_N\),

\[
 F_\ell(z_N)=N\log N+O(N),\quad
 F_\ell(z_{N-1})-F_\ell(z_N)=-\log N+O(1).           \tag{7.2}
\]

The event \(Q_{\tau_N}=N-1\) has probability
\(a_-/(\Lambda N)+O(N^{-2})\); every nonzero event other than this leading
one has total probability \(O(N^{-2})\), with the uniform endpoint moments
from (4.3)--(4.4).  Therefore

\[
 \mathbb E_{z_N}\{V(X_{\tau_N})-V(z_N)\}
 =-\frac{2a_-}{\Lambda}(\log N)^2+O(\log N).         \tag{7.3}
\]

In particular, the same proper \(V\), rather than \(Q^2\), pays the
physical duration with a diverging margin.  Beginning at any fixed
inactive population on the same positive-\(Q\) shell, first run the full
physical cleanup to \(M=0\).  The no-\(T\) cleanup lowers \(F_\ell\) by
\(M\log N+O_M(1)\); a \(T\)-interruption has probability \(O_M(N^{-1})\)
and has all fixed moments.  Appending the base cycle preserves (7.3), with
constants allowed to depend on that fixed inactive state.

The dependence on the inactive state is not a hidden finite-box
assumption.  In a bad-sequence proof, a genuinely one-active sequence has
eventually fixed inactive coordinates.  If either inactive coordinate is
unbounded, the exact source-rate subsequence has at least two active
coordinates and is routed to the corresponding multi-active descriptor.

The fifteen pairs have eighty-three feasible failures.  The seventy-five
rows treated above are the five capped active-\(C\) rows on each pair.  The
remaining eight rows consist of

* six direct-enabled rows with no positive-debt base; and
* two zero-source seed rows with zero-contest service and strictly deeper
  debt creation.

For a direct row, mark an enabled active-degree-one source and follow a
shortest top path to its first lower target.  Strong connectivity makes the
fast path phase type.  A completed path has

\[
 \Delta F_\ell=-\log X+O(1),                         \tag{7.4}
\]

whereas a lower-during-fast interruption has probability \(O(X^{-1})\)
and positive \(F_\ell\)-cost \(O(\log X)\).  Endpoint and duration moments
are uniform from the fixed inactive start.  Hence

\[
 \mathbb E\Delta V
 =2F_\ell\,\mathbb E\Delta F_\ell
   +\mathbb E(\Delta F_\ell)^2
 \leq-cF_\ell\log X                                  \tag{7.5}
\]

for all sufficiently large \(X\).

For either zero-source row, start at the actual target of the \(0\)-edge
and run the finite lower/top return prefix with all clocks retained.  A
failed seed attempt returns to the exact capped face; the number of
attempts is geometric.  At the first enabled unpaired top exit, (7.4)
holds.  Positive interrupted-carrier cost is again \(O(\log X/X)\).
Thus (7.5) holds for these two rows as well.

Finally, along every feasible descriptor of these pairs which is not one
of the eighty-three failed rows, the Anderson--Kim top-source argument
gives the usual strict factorial drift for \(F_\ell\).  For bounded jumps,

\[
 {\cal L}V=2F_\ell{\cal L}F_\ell+
 \sum_r\lambda_r(\Delta_rF_\ell)^2.                  \tag{7.6}
\]

On a passing source-rate sequence, the second term is
\(o(F_\ell|{\cal L}F_\ell|)\): every
\(\Delta_rF_\ell=O(\log(2+|x|))\), while
\(F_\ell\asymp |x|\log(2+|x|)\), and the strict top-source logarithmic
ratio diverges.  Thus the passing-region drift also remains strict for the
same \(V\).

At a boundary in (4.2), the exact descriptor has at least two active
coordinates, has already lost a fixed fraction of \(Q\), or is a
super-polynomially rare larger positive-\(Q\) restart.  In the first case
every affine-feasible descriptor of these fifteen pairs passes the
top-source test; in the last case the same critical episode restarts at
the new level.  The squared-factorial estimate (7.6) charges the promoted
endpoint, while (4.4) makes the upward-restart \(V\)-cost summable.

These estimates give the following exact composition statement, subject
only to independent verification of the stopped regenerative estimates
(4.3)--(4.5).

> **Candidate pair theorem.**  Give each linkage of any of the fifteen
> selected support pairs an arbitrary strongly connected orientation and
> arbitrary positive channel rates.  Then every closed irreducible class
> is positive recurrent.

Indeed, if no finite exceptional set admitted a random-time
\(V+\)duration inequality, choose a bad state sequence in one closed
class and pass to its exact D-tier/source-rate descriptor.  An infeasible
descriptor cannot occur in that affine class.  A passing descriptor is
excluded by (7.6); one of the seventy-five equality rows is excluded by
(7.3); and one of the eight companion rows is excluded by (7.5).  This
exhausts the finite descriptor table.  The episode endpoints have the
moments used above, so the statewise selector gives

\[
 \mathbb E_x[V(X_\tau)-V(x)+\tau]\leq-1              \tag{7.7}
\]

outside a finite classwise set.  Only source-molecularity-zero or
source-molecularity-one reactions can increase total population, at an
affine rate, so the chain is nonexplosive.  Random-time Foster then gives
finite mean return to the finite set.

## 8. Claim status and universal interface

The argument above explains what a universal 1,227-pair theorem would have
to prove.  For every arbitrary strong orientation, classify reflected
creation and debt-reduction histories by their first nonzero
slow-before-fast coefficient.  Strict kinetic separation plugs directly
into the common squared-factorial potential \(V\).  Equality cannot be
settled by a Hamilton-cycle exponent table; for the exact fifteen-pair
equality family it is resolved by the invariant \(Q\) and the shell trace
(4.3).  Any other equality family would require its own coefficient
identity.

No assertion in this note promotes the remaining 1,212 pairs.  The
canonical regression is not an arbitrary-orientation theorem, a box exit
is not automatically a promotion, and no count is inferred from kinetic
depth alone.

The positive-\(Q\) stopped-trace theorem is proved here, while the
fifteen-pair composition theorem is labelled candidate until an independent
audit checks (4.3)--(4.5), the two seed episodes, and the squared-potential
gluing estimate (7.6).  The global T3-2 flag remains false.
