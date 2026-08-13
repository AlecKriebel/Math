# The repaired one-active Bellman/Flat0 all-clock prelude

**Proof-first seam theorem, 2026-08-12 PDT.**  This note replaces, rather
than edits, the earlier draft of the Bellman/Flat0 prelude.  It closes the
one-active interface in which one linkage has an available lower terminal
and the other linkage is flat of active degree zero.  It enumerates no
orientation, rate vector, reaction history, or population box.  Its only
finite object is the inactive phase of one already fixed terminal chart.

The marked all-clock theorem used below is frozen at SHA-256

    157e94cd035dec9a41947129dfcbbab0ebc6e72c01abde6bcf6626052954f1ed,

and its Q/U/C bridge is frozen at SHA-256

    014a317602b60c765dc9a9eb98f0921ba3fd8f779221e271e0dd7f53e245f54c.

The proof below does not invoke the two-active wording of that theorem.  It
repeats the dimension-free marked identity and the one-active endpoint
argument explicitly.

## 1. Setting and the marked identity

Write the active species as \(X\), and the two bounded species as \(U,V\).
Fix a closed irreducible population class, arbitrary strongly connected
orientations of two disjoint linkage supports, and arbitrary positive
labelled rates.  In the one-active chart,

\[
             X=n\longrightarrow\infty,\qquad (U,V)\in B,       \tag{1.1}
\]

where \(B\) is the fixed finite padded inactive phase.  A reaction that
leaves the padded phase or changes any declared active-set, enabled-source,
source-order, lattice, or shell datum is retained as a physical structural
exit, including its actual endpoint and target.

Let \(L_0\) be flat of active degree zero,

\[
                         y_X=0\quad(y\in L_0),          \tag{1.2}
\]

and let \(L_b\) contain complexes \(q,c\) such that

\[
 q_X=1,\qquad c_X=0,\qquad q_U\le c_U,\qquad q_V\le c_V. \tag{1.3}
\]

After each physical reaction carry its actual target \(t\), so \(x\ge t\),
and put

\[
 F(x,t)=\sum_{i=X,U,V}\log((x_i-t_i)!),\qquad W(x,t)=1+F(x,t). \tag{1.4}
\]

For a complex \(y\), let \(K_y\) be the sum of labelled rates out of \(y\),
\(\lambda_y(x)=K_y(x)_y\), \(\Lambda=\sum_y\lambda_y\), and
\(p_y=\lambda_y/\Lambda\).  If the next reaction is \(y\to z\), exact
factorial cancellation gives

\[
 F(x-y+z,z)-F(x,t)=\log{(x)_t\over(x)_y}.              \tag{1.5}
\]

Consequently the expected reward of one ordinary all-clock jump is

\[
 D(x,t)=\log p_t-\sum_y p_y\log p_y-\log K_t+
                         \sum_y p_y\log K_y
        \le \log p_t+C_K.                              \tag{1.6}
\]

The current target is enabled.  Finiteness of the binary source menu also
gives, for every fixed \(r<\infty\),

\[
 \sup_{x,t}\sum_y p_y(x)
       \left[\log{(x)_t\over(x)_y}\right]_+^r<\infty.  \tag{1.7}
\]

This is the source-entropy bound \(s(1+\log(1/s))^r\le C_r\).

## 2. A Bellman mark needs no prelude

Suppose the current target \(t\) belongs to \(L_b\).  Choose a simple
directed path, supplied by strong connectivity,

\[
             t=y_0\longrightarrow y_1\longrightarrow\cdots
                        \longrightarrow y_m=c.         \tag{2.1}
\]

Retain all clocks, continue only when the designated label fires, stop at
the actual endpoint of the first competitor or structural exit, and on
designated success take one final ordinary jump at \(c\).  On success the
pre-final population is

\[
                           z=x-t+c\ge c.                \tag{2.2}
\]

Thus (1.3) enables \(q\) at \(z\), and in the fixed inactive phase

\[
                    p_c(z)\le {K_c(z)_c\over K_q(z)_q}
                              \le {C\over z_X}\to0.     \tag{2.3}
\]

Let \(D_i\) be (1.6) at a success-prefix state, \(a_i\) the probability of
the next designated label, and \(J_i\) the expected remaining stopped
reward.  The literal all-clock recursion is

\[
                         J_m=D_m,\qquad J_i=D_i+a_iJ_{i+1}. \tag{2.4}
\]

At the first prefix source whose probability tends to zero, its \(D_i\)
tends to minus infinity.  Earlier designated probabilities stay bounded
below after source-ratio compactification, and a later positive tail is
multiplied by \(a_i=O(p_{y_i})\to0\).  Hence

\[
                              J_0\longrightarrow-\infty, \tag{2.5}
\]

unless a fixed prefix reaches a structural exit with probability bounded
below.  The episode has bounded depth, all fixed positive endpoint-reward
moments by (1.7), and all fixed physical-duration moments because the
carried target supplies a fixed positive lower bound on the total hazard.

This proof uses only one diverging coordinate.  It is the exact
one-active corollary of the frozen marked theorem.

## 3. The finite phase before Bellman access

Now suppose the carried target lies in \(L_0\).  If any \(X\)-degree-one
source of \(L_b\) is enabled already, declare **top access** immediately.
Otherwise record the phase

\[
                     e=(U,V,t,\hbox{fixed chart flags}). \tag{3.1}
\]

The phase set \(E\) is finite.  Until absorption, the only in-chart
population transitions are \(L_0\) reactions.  Degree-zero \(L_b\)
reactions and structural exits remain as competing absorbing hazards.
Every such rate depends on \(e\) and the fixed labelled rates, but not on
\(n\).

Use four disjoint absorbing sections, with structural exit given first
priority.  Thus any reaction that causes a declared exit is classified in
\(E_{\rm out}\), even if its endpoint would also enable a top source or the
reaction is itself a Bellman launch.

1. \(E_{\rm out}\), structural exit: include the exit-causing reaction and
   its actual endpoint.
2. \(A\), top access: after a **nonexit** in-chart flat jump, a positive-
   \(X\)-degree \(L_b\) source is enabled.  Stop the finite phase before
   taking the next jump.
3. \(B\), Bellman launch: a degree-zero-source \(L_b\) reaction fires and
   does not cause a declared exit.  Include that reaction and retain its
   actual target.
4. \(C\), closed no-access class: enter a closed communicating class of
   flat phases from which none of the first three sections is possible.

Declare every such closed class \(C\) absorbing.  The remaining embedded
kernel \(Q\) is a finite transient substochastic matrix.  Therefore,
unconditionally on which absorbing section is reachable,

\[
             \rho(Q)<1,\qquad
             \mathbb P_e(N>k)\le C_0\rho_0^k           \tag{3.2}
\]

for some \(\rho_0<1\), uniformly over the finite set of starting phases.
This corrects the false formulation that required no closed class to be
reachable: closed classes have already been made absorbing.

The current flat target is enabled and has an outgoing positive labelled
rate.  Its falling factorial is a positive integer.  Thus the total hazard
is uniformly bounded below, and (3.2) gives

\[
                    \sup_{n,e}\mathbb E_e N^r<\infty,
                    \qquad
                    \sup_{n,e}\mathbb E_e \sigma^r<\infty             \tag{3.3}
\]

for every fixed \(r<\infty\), where \(\sigma\) is the finite-phase
absorption time.

The flat reward does not accumulate per attempt.  It telescopes.  Before
absorption the active population is \(n\), the initial and final inactive
phases lie in a finite set, and both the carried mark and every flat source
have \(X\)-degree zero.  Hence

\[
                 |F(X_\sigma,T_\sigma)-F(x,t)|\le C_B             \tag{3.4}
\]

on entry to \(A\) or \(C\).  The same bound holds after a degree-zero
Bellman launch or structural-exit jump: in (1.5) the initial mark and the
source both have active degree zero, irrespective of the target.  Thus the
prelude has uniformly bounded positive endpoint reward.

## 4. The two coercive absorbing sections

At \(A\), the current flat target has bounded propensity, while an enabled
degree-one source \(r\in L_b\) has propensity at least \(c_B n\).  Take one
ordinary all-clock jump and stop at its actual endpoint.  No selected
reaction is awaited.  Equations (1.6)--(1.7) give

\[
             \mathbb E[\Delta F\mid A]\le-\log n+C_B,              \tag{4.1}
\]

with uniformly bounded positive moments.  A fast top reaction may preempt
an exit, but this only creates the coercive unconditional charge (4.1); no
uniform exit probability is asserted at an \(A\)-phase.

At \(B\), the included launch reaction is the terminal jump of the finite
prelude.  Its actual target initializes the path in Section 2.  It is not
counted again.  The bounded prefix (3.4) plus (2.5) tends to minus infinity,
unless the appended physical path has positive structural-exit probability.

Let \(a_e,b_e,c_e\) be the probabilities, from a fixed finite starting
phase, of absorption in \(A\cup B\), \(E_{\rm out}\), and \(C\),
respectively.  Before \(A\), all competing hazards have degree zero, so
these are constants independent of \(n\), with

\[
                         a_e+b_e+c_e=1.                \tag{4.2}
\]

The exhaustive split is as follows.  If \(c_e>0\), Section 5 shows that the
fixed irreducible population class is finite.  Otherwise \(c_e=0\).  If
\(a_e>0\), the corresponding finite mixture of (4.1) and (2.5) is
coercively negative, unless one of the finitely many Bellman continuations
has positive structural-exit probability.  All complementary rewards have
bounded positive part by (1.7) and (3.4), so they cannot offset that
divergence.  Finally, if \(c_e=0=a_e\), then \(b_e=1\): the rule records a
physical exit.  These three cases exhaust (4.2).  This phasewise dichotomy
does not infer a uniform exit probability along phases at which a
degree-one hazard grows like \(n\).

## 5. Closed no-access phases are finite physical classes

In a closed section \(C\), no \(L_b\) source is enabled: a degree-one source
would be top access, and an enabled degree-zero source has a positive
Bellman-launch hazard.  No structural exit is enabled, and every enabled
reaction belongs to \(L_0\), stays in \(C\), and preserves \(X\).

For the entrance value \(X=n\), the populations represented by \(C\) form
a finite closed physical subset.  If it is reachable in a closed
irreducible population class \(\Gamma\), irreducibility forces
\(\Gamma=C\).  Thus \(\Gamma\) is finite and positive recurrent.  In
particular, in an infinite class supporting an alleged one-active escape,
\(c_e=0\) for every reachable phase.  This justifies the use of the first
two cases after (4.2) without deleting a merely rare linkage.

## 6. Repaired prelude theorem

> **Theorem 6.1 (Bellman/Flat0 prelude).**  Fix a terminal one-active chart
> of a reduced binary two-linkage network.  Suppose one linkage satisfies
> (1.3) and the other satisfies (1.2).  For every strongly connected
> orientation, every fixed positive labelled rate vector, and every actual
> carried target, there is a finite-menu all-clock stopping rule using the
> single proper marked potential (1.4) such that, outside a finite set, at
> least one of the following applies:
>
> 1. for some \(\eta>0\),
>    \[
>       \mathbb E_{x,t}[W(X_\tau,T_\tau)-W(x,t)+\eta\tau]\le-1; \tag{6.1}
>    \]
> 2. the rule records a physical structural-exit reaction with a positive
>    phasewise probability; or
> 3. the fixed irreducible population class is finite.
>
> The endpoint is always the actual endpoint and target of the last
> included reaction.  For every fixed \(r<\infty\), the duration and the
> positive endpoint increment have uniformly bounded \(r\)-th moments.

Uniformity in (6.1) follows by contradiction over the finite phase, target,
and simple-path menu.  Once the expected reward is below \(-2\), (3.3) and
the bounded Bellman depth permit a common sufficiently small \(\eta>0\).
On a terminal Green trace the second alternative has zero normalized flux,
and the third cannot carry escape; hence the negative alternative excludes
an escaping Bellman/Flat0 occupation.

Every physical jump is counted exactly once.  In particular, a Bellman
activation is the terminal jump of the preceding finite prelude, and its
actual target begins the next Bellman episode.  It is never also counted as
the first jump of that episode.  This nonoverlap is why the failed
conditional-activation counterexample does not apply.
