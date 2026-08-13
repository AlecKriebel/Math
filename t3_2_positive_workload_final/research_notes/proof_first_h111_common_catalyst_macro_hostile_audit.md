# The homogeneous common-catalyst macro: hostile audit and exact repair target

**Proof-first seam audit, 2026-08-12 PDT.**  This note isolates the weakest
remaining stochastic statement for the homogeneous residual level-set family
after the workload-only physical-time Foster theorem.  It does not assert
that statement as proved.  Its purpose is to rule out a tempting false
activation shortcut and to state a ledger-based repair which is exactly as
strong as the global Foster interface requires.

## 1. Exact kernel and workload ledger

On a dormant pure-\(X\) ray, the exceptional homogeneous support is

\[
                    T=\{X+Y,Y+Z,2Y\}.                         \tag{1.1}
\]

The lower linkage is \(R=\{0,Y,Z\}\), with an arbitrary strongly
connected labelled graph and arbitrary positive rates.  Put

\[
\begin{aligned}
 H&=X+Y+Z,\\
 B_t&=\text{number of lower births by time }t,\\
 D_t&=\text{number of direct lower deaths by time }t,
\end{aligned}
\]

and define the exact net ledger

\[
                              G_t=D_t-B_t.              \tag{1.2}
\]

Every top reaction and every lower unary transfer preserves \(H\), so

\[
                         H(X_t)-H(X_0)=-G_t.             \tag{1.3}
\]

No activation cost may be discarded from this identity.

When \(Y\ge1\), set \(z_X=X,z_Y=Y-1,z_Z=Z\).  All three top
propensities have the common factor \(Y\):

\[
 (x)_{X+Y}=Yz_X,\qquad (x)_{Y+Z}=Yz_Z,\qquad
 (x)_{2Y}=Yz_Y.                                      \tag{1.4}
\]

Thus

\[
                         \mathcal L_T=Y\mathcal L_{\rm lin}, \tag{1.5}
\]

where \(\mathcal L_{\rm lin}\) is the generator of \(H-1\)
independent particles on the strongly connected three-state graph inherited
from \(T\).  Top dynamics alone preserve at least one catalyst once
\(Y\ge1\).

## 2. A first-death activation rule is false

Consider the strongly connected cycles

\[
 X+Y\longrightarrow Y+Z\longrightarrow2Y\longrightarrow X+Y,
 \qquad
 0\longrightarrow Y\longrightarrow Z\longrightarrow0,   \tag{2.1}
\]

and start from \((X,Y,Z)=(N,0,0)\).  The sole direct-death species in
the lower cycle is \(Z\).  After the first \(0\to Y\) birth, use top
operational time

\[
                              a(t)=\int_0^tY(s)\,ds.           \tag{2.2}
\]

For the one-particle top chain started at \(X\), at small operational
time \(a\),

\[
 p_Z(a)=\kappa_1a+O(a^2),\qquad
 p_Y(a)=\tfrac12\kappa_1\kappa_2a^2+O(a^3).             \tag{2.3}
\]

Consequently the typical top-only profile has
\(Z\asymp Na\) and \(Y\asymp1+Na^2\).  The direct-death
compensator accumulated before a fixed positive operational time contains

\[
 \int {Z\over Y}\,da
 \asymp \int_{N^{-1/2}}^{a_0}{da\over a}
 \asymp \log N.                                      \tag{2.4}
\]

Thus the probability of reaching a fixed top-interior operational time
before the first \(Z\to0\) death is not uniformly positive; it decays
polynomially, with a rate-dependent exponent.  The exponent can be made
arbitrarily large by changing the fixed death/top rate ratio.

This is not a recurrence obstruction.  It is an obstruction to stopping on
the **first** lower death and treating every such stop as a failed activation
attempt.  On the dominant first-death branch the initial seed birth and the
death cancel, so \(G=0\).  That branch cannot pay a positive physical-time
toll.  A compound-geometric restart based on a uniform no-death activation
probability is therefore unavailable.

There is a second literal obstruction to a direct permanence citation.  The
whole face

\[
                              \{Y=0\}                         \tag{2.5}
\]

is dead for \(T\), not merely the pure \(X\) vertex.  An endpoint with
\(Y=0\) and \(Z\asymp H\) cannot be declared a top-fluid interior
entry.  The lower linkage must remain in the boundary prelude.

## 3. Favorable lower-event dichotomy

The lower interference has an exact structural sign.  At a state with
\(Y\ge1\), a lower event sourced at \(Y\) either is a direct death,
which raises \(G\), or is a transfer to \(Z\), which may remove the
last catalyst.  Its adverse-transfer hazard is \(O(Y)\).  In operational
time \(da=Y\,dt\), its compensator over a fixed interval is \(O(da)\),
uniformly in \(H\).

A lower event sourced at \(Z\) is never an uncharged obstruction:

* if \(Z\) has a direct edge to zero, that event raises \(G\);
* otherwise, because the only nonzero lower vertices are \(Y,Z\) and
  the lower graph is strongly connected, every path from \(Z\) to zero
  starts with a \(Z\to Y\) transfer, which recreates catalyst.

On \(Y=0\), the same alternative says that macroscopic \(Z\) supplies
either direct service at rate \(\Theta(H)\) or catalyst reseeding at that
rate.  This boundary step, rather than top permanence by itself, is the
correct handoff.

## 4. Exact minimal prelude theorem still required

Fix \(\rho>0\) and let

\[
 \mathcal I_\rho=\{x:X,Y,Z\ge\rho H(x)\}.              \tag{4.1}
\]

The precise repair target is the following alternative.

> **Ledger-or-interior prelude.**  There exist fixed
> \(L,\rho,C_\tau,C_G>0\), with \(L>C_G\), such that, from every
> sufficiently large dormant
> low-direct-death state, one can construct an all-clock stopping time
> \(\sigma\) with actual endpoint satisfying
> \[
>     \mathbb E\sigma\le C_\tau,\qquad
>     \mathbb E(G_\sigma)^-\le C_G,                        \tag{4.2}
> \]
> and with the disjoint endpoint alternatives
> \[
>     G_\sigma\ge L
>       \qquad\text{or}\qquad X_\sigma\in\mathcal I_\rho. \tag{4.3}
> \]

No lower reaction is forbidden in this statement, and no positive lower
bound on the probability of the interior alternative is required.

Before the first catalyst appears, \(T\) is dead.  The open linear lower
phase has a finite-mean hit of \(Y\) or a return to zero transverse mass;
on a return, births and deaths cancel in \(G\).  After \(Y\ge1\),
(1.5) and the favorable-event dichotomy of Section 3 reduce (4.2)--(4.3)
to a bounded-operational-time assertion: either the direct-death ledger
crosses \(L\), or the irreducible linear particle phase reaches a compact
three-coordinate interior.  This is the load-bearing step; it has not been
proved merely by writing the factorization (1.5).

## 5. Why this prelude is sufficient

On the ledger alternative, the workload reward is already at least
\(L\).  On the interior alternative, run the full chain for a fixed
top-fluid horizon \(T/H\).  The initial normalized populations lie in a
compact interior set.  Single-linkage permanence and the density-dependent
limit then expose either direct-death coordinate for any prescribed fixed
mean count, while expected new births and elapsed physical time are
\(O(H^{-1})\).  Choose the conditional expected service target
\(D_0>C_G\).  If \(P_I\) is the probability of the interior alternative,
then the complete expected net ledger is bounded below by

\[
 L(1-P_I)+D_0P_I-C_G
 \ge \min\{L,D_0\}-C_G>0.                              \tag{5.1}
\]

The two alternatives therefore yield one complete episode with

\[
             \mathbb E(D_\tau-B_\tau)\ge a>0,\qquad
             \mathbb E\tau\le C'<\infty.                   \tag{5.2}
\]

Taking \(\eta<a/C'\) gives

\[
             \mathbb E[H(X_\tau)-H(x)+\eta\tau]\le0, \tag{5.3}
\]

which is exactly the occupation macro in the frozen workload-only
physical-time Foster theorem.  Neither a bounded reaction word, an
exponential attempt bound, nor a uniform no-death activation probability is
needed.

## 6. Frozen verdict boundary

The first-death/geometric-activation shortcut is **strictly invalid** for
arbitrary positive rates.  The common-catalyst factorization and fixed-level
stationary law do not by themselves prove the global macro.  The exact
remaining theorem is (4.2)--(4.3), with the full lower linkage retained.
Once that prelude is proved, the interior service argument and the global
workload-only Foster theorem compose without a chart seam.
