# Proof-only audit B: a historically reachable zero-spectator obstruction

**Audit time:** 2026-08-11 21:49 PDT.

**Strict verdict: FAIL.**  The current two-level generalized Family-II
candidate is false even after imposing its repaired historical
positive-debt hypothesis.  An allowed exact proper pair has historically
reachable bases

\[
                         (U,V,I)=(0,n,0),\qquad D_V=n,
\]

at which the pure physical-return resolvent is of order (n), not order
one.  From those bases the upward terminal has probability bounded below
by a positive constant and the expected physical duration is of order
(n).  This contradicts (5.11), (7.2), (8.1), (8.2), and (8.2a) of the
candidate.

This is an exact counterexample to the proposed descriptor-local theorem,
not a counterexample to recurrence, T3-2, or C3.  It uses no bounded-depth
search or finite-box inference.  No incidence or pair promotion is
justified.

The audited canonical snapshot is

```text
two-level note   392359e1e3e72403e096837324f2da1679e5cb61d6d2bc0a41baddb3d030e359
source           c2ef19d8865cd42a91705461b78a61a9c4c6a9dd748484a5354e2624dda6e6f6
tests            a9c5c690ce1d176336f187a8847558deb05e35ddc3a3fe795fcdf06703394f81
scoped seam note be5fdf1b6c2118428893979c791c81235bac48e67bd2bdba21be44c00f0c6a46
```

## 1. The allowed strong network

Use the normalized supports

\[
 L_+=\{0,V+I\},\qquad L_0=\{I,2U,2I,U+I\}.             \tag{1.1}
\]

Take the complete directed graph on each support and give every reaction
rate constant one.  Both linkage digraphs are strongly connected.  The
finite support certificate confirms that (1.1) is one of the generalized
Family-II templates; that membership check is the only finite bookkeeping
used here.

Because every reaction has its reverse, the physical communicating class
containing the zero population is closed.  Choose

\[
                     x^\circ=(0,0,0),\qquad D(0)=0.                \tag{1.2}
\]

On the reachable reflected lift from (1.2), (D=X) pathwise: it is true
initially, and physical feasibility makes
((D+\zeta)^+=X+\zeta) after every reaction.  In particular, positive
physical (V) is positive selected reflected debt.

## 2. Exact historical reachability for every active level

The following fixed physical word maps a no-fast base to the next active
level:

```text
0 -> V+I,
I -> 2I,
2I -> 2U,
2U -> I,
0 -> V+I,
2I -> I,
V+I -> 0.
```

Indeed, beginning at ((U,V,I)=(0,n,0)), its successive states are

\[
\begin{aligned}
(0,n,0)&\longrightarrow(0,n+1,1)
\longrightarrow(0,n+1,2)\\
&\longrightarrow(2,n+1,0)
\longrightarrow(0,n+1,1)\\
&\longrightarrow(0,n+2,2)
\longrightarrow(0,n+2,1)
\longrightarrow(0,n+1,0).                         \tag{2.1}
\end{aligned}
\]

Every source is enabled at the displayed state.  Iterating (2.1) from
(1.2) proves that ((0,n,0)) is historically reachable for every
(n\ge1).  Since (D=X), it has (D_V=n>0).  Thus these bases satisfy
the candidate's repaired scope, and (u=0=n^{o(1)}).  This support is not
a no-history face: the proper zero complex is enabled on (I=0).

## 3. The pure renewal has order (n)

At (x_n=(0,n,0)), the only enabled base reaction is
(0\to V+I), of rate one.  It opens at

\[
                         y_n=(0,n+1,1).                            \tag{3.1}
\]

At (y_n), the immediate fast cleanup (V+I\to0) has mass-action
rate (n+1) and returns exactly to (x_n).  The complete list of
non-cleanup clocks enabled at (3.1) is

\[
 0\to V+I,qquad I\to2U,qquad I\to2I,qquad I\to U+I,             \tag{3.2}
\]

each of rate one.  Therefore the probability of the immediate pure return
in one trial is

\[
                         q_n={n+1\over n+5}.                       \tag{3.3}

The candidate's (Z^{\rm pure}) contains this event, so

\[
 {1\over1-Z^{\rm pure}(0)}\ge {1\over1-q_n}
                              ={n+5\over4}.                       \tag{3.4}
\]

For (1.1), the post-contraction lower escape degree in the candidate is
(d=2).  Equation (5.11) instead asserts

\[
             {1\over1-Z^{\rm pure}(0)}\le C(1+0)^{2-d}=C,         \tag{3.5}
\]

uniformly in (n).  Equations (3.4)--(3.5) are incompatible.  The error
is that the degree-two lower source (2U) used to define (d) is disabled
at (u=0).  Historical positive-debt transience guarantees eventual
escape for each fixed (n); it does not give a uniform escape probability
per pure traversal.

## 4. Fixed positive upward probability

After every immediate cleanup in (3.3), the chain is exactly back at
(x_n), so the strong Markov property gives independent identical trials.
Stop this trial sequence at the first reaction from (3.2).  Of the four
equal-rate alternatives, (I\to2U) has probability exactly (1/4),
independently of (n).  Its endpoint is

\[
                 (U,V,I)=(2,n+1,0),qquad R=1.                    \tag{4.1}

This is the candidate's service-free upward terminal (U^\uparrow).  It
is below every moving boundary for all large (n).  Consequently

\[
                        \mathbb P_{x_n}(U^\uparrow)\ge{1\over4}.   \tag{4.2}

This directly contradicts
(mathbb P(U^\uparrow)\le n^{-1+o(1)}) in (8.2), and hence also the
deduction (mathbb P(D)=1-o(1)) in (8.2a).  More generally, with fixed
positive rates the lower bound is

\[
 {\kappa_{I\to2U}\over
   \kappa_{0\to V+I}+\kappa_{I\to2U}
   +\kappa_{I\to2I}+\kappa_{I\to U+I}}>0.           \tag{4.3}
\]

Thus the obstruction is not a fine tuning of unit rates.

## 5. Physical duration also contradicts the theorem

The number (N_n) of trials before the first clock in (3.2) is geometric
with success probability (4/(n+5)), hence

\[
                         \mathbb E N_n={n+5\over4}.                \tag{5.1}

Each trial includes a fresh base holding time of mean one before
(0\to V+I).  These holding times are independent of the next-reaction
choice at (3.1).  If (sigma) is the candidate's physical terminal time,
then Wald's identity (or direct conditioning) gives

\[
                         \mathbb E_{x_n}\sigma
                         \ge {n+5\over4}.                         \tag{5.2}

Equation (7.2), at (u=0) and (p=1), asserts an (n)-independent upper
bound.  Therefore the repaired duration recursion cannot have the stated
base estimate on every historically reachable positive-debt start.

The same computation explains the failure of (8.1): the nominal
(O(n^{-1})) probability of one nonpure firing is amplified by
(Theta(n)) pure attempts.  It becomes order one, not a small
perturbation.

## 6. Audit of the requested seams

The path-labelled boundary repair itself survives this counterexample.
Only a direct outer-base crossing is called (P), while a cutoff hit after
opening is called (B); the two events are disjoint and the common
(W_\ell) increments telescope at the actual strong-Markov endpoint.
Likewise, the no-history lemma correctly excludes invariant (I=0) faces
that cannot carry positive old-active debt.

Those repairs do not address (1.1).  It has an enabled (I)-free proper
opening, genuinely carries reachable positive debt, and fails before any
moving boundary or potential-switch seam.  Endpoint-weighted entropy and
fourth-power Taylor conclusions cannot be invoked because their required
inputs (8.1), (8.2a), and (7.2) are false on (2.1).

## 7. Required proof-first repair

Any next theorem must classify pure renewal by the **enabled escape at the
actual base**, not by the maximal degree present somewhere in the lower
support.  In particular, the active axis (U=0) of (1.1) requires its own
physical macro-kernel.  On that axis, rare order-(n^{-1}) defects are
repeated order (n) times, so upward and service outcomes compete at order
one.  They cannot be treated as a small perturbation of a service-dominant
base chain.

A valid repair must either prove drift for this order-one macro-kernel under
the same common (W_\ell), or route it through a different already-proved
analytic chart.  Finite enumeration cannot repair the missing scale.

All analytic, descriptor-local, pair-level, and global flags must remain
false.
