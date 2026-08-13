# The one-active Bellman/Flat0 all-clock prelude

**Proof-first seam theorem, 2026-08-12 PDT.**  This note closes the
one-active interface in which one linkage is Bellman-available and the
other linkage is flat of active degree zero.  It uses no orientation,
reaction-history, rate, or population-box enumeration.  The only finite
object is the literal inactive phase of one fixed terminal chart.

The conclusion is local: a Bellman/Flat0 terminal chart has coercive
negative marked-factorial reward, positive physical structural-exit flux,
or a finite closed no-history class.  It is therefore suitable for the
terminal-Green composition.  No recurrence claim is made for a support
superset or by deleting either linkage.

## 1. Setting and exact marked reward

Write the active species as \(X\), and the two bounded species as \(U,V\).
Fix a closed irreducible population class, arbitrary strongly connected
orientations of two disjoint linkage supports, and arbitrary positive
labelled rates.  In the one-active chart,

\[
                    X=n\longrightarrow\infty,\qquad
                    (U,V)\in B,                       \tag{1.1}
\]

where \(B\subset\mathbb N_0^2\) is the finite padded inactive phase fixed by
the chart.  A reaction which leaves the padded phase, changes the active
set, changes the enabled-source/source-order cell, or hits a declared shell
is retained as a physical structural-exit reaction.

Let \(L_f\) be the **Flat0** linkage:

\[
                         y_X=0\qquad(y\in L_f).       \tag{1.2}
\]

Let \(L_b\) be the **Bellman** linkage.  Thus \(L_b\) has complexes \(q,c\)
such that

\[
 q_X=1,\qquad c_X=0,\qquad
 q_U\le c_U,\qquad q_V\le c_V.                       \tag{1.3}
\]

After every physical reaction carry its actual target \(t\).  Necessarily
\(x\ge t\).  Put

\[
             F(x,t)=\sum_{i=X,U,V}\log((x_i-t_i)!),
             \qquad W=1+F.                           \tag{1.4}
\]

For the next labelled reaction \(y\to z\), exact factorial cancellation
gives

\[
 F(x-y+z,z)-F(x,t)=\log{(x)_t\over(x)_y}.             \tag{1.5}
\]

Writing \(K_y\) for the sum of the labelled rates with source \(y\),
\(\lambda_y=K_y(x)_y\), \(\Lambda=\sum_y\lambda_y\), and
\(p_y=\lambda_y/\Lambda\), the expected reward of one ordinary all-clock
jump is

\[
 D(x,t)=\log p_t-\sum_y p_y\log p_y-\log K_t
                         +\sum_y p_y\log K_y
       \le \log p_t+C_K.                             \tag{1.6}
\]

The current target is enabled, so \(p_t>0\).  The finite source menu also
gives every fixed source-weighted positive moment of (1.5), exactly as in
the marked entropy--Bellman identity.

## 2. The Bellman-target episode

Suppose first that the current target \(t\in L_b\).  Strong connectivity
gives a simple path

\[
                  t=y_0\longrightarrow y_1\longrightarrow
                     \cdots\longrightarrow y_m=c.    \tag{2.1}
\]

Run it with all clocks retained, stopping at the actual endpoint of the
first undesignated reaction or structural exit, and, on designated success,
taking one final ordinary all-clock jump at \(c\).  Every prescribed source
is physical because it is the actual target of the preceding prescribed
reaction.

On success the population before the final jump is

\[
                              z=x-t+c\ge c.           \tag{2.2}
\]

Consequently (1.3) makes \(q\) enabled at \(z\).  The inactive coordinates
remain in one finite padded phase unless an exit has already been recorded,
while \(z_X\to\infty\).  Hence

\[
 p_c(z)\le {\lambda_c(z)\over\lambda_q(z)}
           ={K_c(z)_c\over K_q(z)_q}
           \le {C\over z_X}\longrightarrow0.         \tag{2.3}
\]

Let \(D_i\) be (1.6) at the \(i\)-th success-prefix state, let \(a_i\) be
the all-clock probability of the designated label there, and let \(J_i\)
be the expected remaining marked reward, stopping on a deviation.  Then

\[
                          J_m=D_m,\qquad
                          J_i=D_i+a_iJ_{i+1}.          \tag{2.4}
\]

If \(j\) is the first success-prefix source whose probability tends to
zero, every \(a_i\) with \(i<j\) is bounded below, \(D_j\to-\infty\), and,
when \(j<m\), \(a_j=O(p_{y_j})\to0\).  Thus the positive tail after \(j\)
vanishes and

\[
                              J_0\longrightarrow-\infty. \tag{2.5}
\]

This is the one-active Bellman corollary of the exact all-clock recursion;
the proof uses only (2.3), not a second diverging coordinate.  A prefix
which changes the chart either has the same rare-source reward or reaches
its exit-causing reaction with probability bounded below.  Therefore the
episode has coercive negative reward or positive physical exit flux.  It
has at most ten jumps, uniformly bounded physical-time moments, and every
fixed positive endpoint-increment moment.

## 3. Finite Flat0 phase before Bellman access

Now let the current target \(t\in L_f\).  While no degree-one source of
\(L_b\) is enabled and no \(L_b\)-reaction has fired, every possible source
has \(X\)-degree zero.  Record the phase by

\[
                             e=(u,v,t),               \tag{3.1}
\]

including the finitely many chart flags.  The set \(E\) of such phases is
finite because \((u,v)\in B\), and every transition within \(E\) is a
physical \(L_f\)-reaction.  Its rate depends on \(e\) and the fixed labelled
rates, but not on \(n\).

Make the following events absorbing in this finite phase graph.

1. **Top access:** a state is reached at which some \(L_b\)-source of
   \(X\)-degree one is enabled.
2. **Bellman launch:** an \(L_b\)-reaction with degree-zero source fires;
   include that reaction and retain its actual target mark.
3. **Structural exit:** include the reaction which leaves the chart.
4. **Closed no-access class:** the phase enters a closed communicating
   class \(C\subset E\) from which none of 1--3 is possible.

This is an exhaustive finite-state decomposition.  On the transient part,
the jump kernel is independent of \(n\).  If no closed no-access class is
reachable, its substochastic transition matrix has spectral radius less
than one.  Consequently the absorption jump count \(N\) has a geometric
tail, uniformly in \(n\):

\[
                       \mathbb P(N>k)\le C\rho^k,
                       \qquad 0<\rho<1.              \tag{3.2}
\]

At every transient phase the carried target is an enabled Flat0 source.
Its outgoing labelled propensity is at least the smallest positive labelled
rate, since its falling factorial is a positive integer.  Each physical
holding time is therefore conditionally dominated by one fixed exponential.
Equation (3.2) proves every fixed moment of the prelude duration.

No reward is accumulated per attempted jump.  It telescopes.  Before top
access, both the mark and every internal source have \(X\)-degree zero, so
\(X=n\) is unchanged.  The start and pre-absorption endpoint range over the
same finite inactive marked phase.  Therefore

\[
                \left|F(X_{N},T_{N})-F(x,t)\right|\le C_B. \tag{3.3}
\]

If a degree-zero Bellman launch is the absorbing jump, its target may have
\(X\)-degree zero or one, but

\[
 (X_N)_X-(T_N)_X=n;
\]

the \(X\)-factorial still cancels exactly, and (3.3) remains true after
enlarging the finite inactive endpoint phase by one bounded reaction.  The
same observation gives all positive moments of the prelude endpoint cost.

## 4. The two absorbing charges

At a top-access phase the current target \(t\in L_f\) has degree zero and
bounded inactive stoichiometry.  Hence \(\lambda_t\le C_B\).  An enabled
degree-one source \(r\in L_b\) has

\[
                            \lambda_r\ge c_B n        \tag{4.1}
\]

for all large \(n\).  Take one ordinary all-clock jump and stop at its
actual endpoint and target.  Equations (1.6) and (4.1) give

\[
                           D(x,t)\le-\log n+C_B.      \tag{4.2}
\]

Thus no conditioning on the top reaction is used: the next jump itself has
coercive negative expected marked reward even if a Flat0 or degree-zero
competitor wins it.

At a Bellman-launch endpoint, begin the episode of Section 2 from the
launch reaction's actual target.  The launch jump belongs to the prelude and
is not counted again.  Its accumulated prefix reward is bounded by (3.3),
while (2.5) tends to minus infinity.  Hence the concatenated prelude and
Bellman-target episode also has expected reward tending to minus infinity.

There are finitely many transient phases, actual Bellman targets, and simple
paths.  Sequential coercivity therefore gives, uniformly over this finite
menu and outside a finite set,

\[
               \mathbb E_{x,t}[W(X_\tau,T_\tau)-W(x,t)]\le-2, \tag{4.3}
\]

unless a structural-exit reaction is recorded.  Equations (3.2), the
holding-time bound, and the Bellman episode estimates give

\[
 \sup\mathbb E\tau^q<\infty,\qquad
 \sup\mathbb E[((W(X_\tau,T_\tau)-W(x,t))^+)^q]<\infty \tag{4.4}
\]

for every fixed \(q<\infty\).  As usual, a small uniform
\(\eta>0\) turns (4.3)--(4.4) into

\[
 \mathbb E_{x,t}
 [W(X_\tau,T_\tau)-W(x,t)+\eta\tau]\le-1.           \tag{4.5}
\]

Every physical jump is counted exactly once.  The final jump of the prelude
creates the mark from which the appended Bellman path begins; it is not the
first jump of that path.  A competitor which terminates the Bellman path is
included there and only its endpoint starts the next rule.

## 5. Closed no-access phases are finite no-history classes

Let \(C\subset E\) be a closed no-access class.  No source of \(L_b\) is
enabled anywhere in \(C\): a degree-one source would be top access, and an
enabled degree-zero source has an outgoing labelled reaction of positive
rate and would be a Bellman launch.  No physical structural-exit reaction is
enabled from \(C\), by its closure.  Thus every physical reaction from \(C\)
belongs to \(L_f\) and preserves \(X\) exactly.

The population states represented by \(C\) form a finite closed set: \(X\)
has its fixed entrance value and \((U,V)\) lie in the finite padded phase.
If \(C\) is reachable inside a closed irreducible population class
\(\Gamma\), irreducibility and the closure of \(C\) force \(\Gamma=C\).
Therefore \(\Gamma\) is finite and positive recurrent.  Equivalently, such
a phase cannot carry a one-active escaping occupation.  This is the exact
no-history alternative; it is not an assertion that a merely rare Bellman
linkage may be deleted.

## 6. The seam theorem

> **Theorem 6.1 (Bellman/Flat0 prelude).**  Fix a one-active terminal chart
> of a reduced binary network with two strongly connected active linkage
> supports.  Suppose one linkage satisfies (1.3) and the other satisfies
> (1.2).  For every strongly connected orientation and every fixed positive
> labelled rate vector, every actual target mark admits a finite-menu,
> all-clock physical stopping rule with the common proper marked potential
> (1.4).  Exactly one of the following holds:
>
> 1. the rule satisfies the uniform physical-time drift estimate (4.5);
> 2. it records a physical structural-exit reaction with probability bounded
>    below on its finite phase; or
> 3. the physical class is a finite closed no-history class on which \(X\)
>    is constant.
>
> In particular a terminal Bellman/Flat0 chart cannot support an escaping
> fixed-class occupation.

The proof remains valid at arbitrary fixed inactive caps.  Its constants may
depend on the chart, orientation, rates, and fixed irreducible class, but not
on the diverging active population \(n\).  The finite phase is used only to
prove (3.2); no stochastic estimate is inferred from a finite support
enumeration.

## 7. Hostile checks

The construction survives the two apparent counterexamples.

* The Flat0 linkage may make arbitrarily many reactions before Bellman
  access.  Equation (3.3) bounds the **telescoped** marked reward, while
  (3.2) controls duration and count.  No cost is multiplied by the number
  of attempts.
* The Bellman linkage may initially be disabled.  The proof never conditions
  on its activation.  It either uses the unconditional next-jump entropy
  charge (4.2), includes the first degree-zero Bellman launch and follows its
  actual target, records the causing structural exit, or identifies a
  genuinely closed finite no-history class.

Thus neither rare activation nor faster Flat0 waiting leaves an uncharged
reaction.
