# Proof-only audit A: compact spectator bases defeat the pure renewal bound

**Audit date:** 2026-08-11 PDT.

**Scope.**  This audit checks the analytic two-level renewal in
`two_active_dormant_407_two_level_repair.md`.  It uses the finite support
certificate only to identify an admitted normalized template.  It does not
infer a stochastic assertion from a finite path search and does not modify
any certification flag or pair count.

The audited bytes were

```text
note    392359e1e3e72403e096837324f2da1679e5cb61d6d2bc0a41baddb3d030e359
source  5dab6d1837462b86d4a468bda3dcccc7c684fa8807f3af429f387edba569b99f
tests   a9c5c690ce1d176336f187a8847558deb05e35ddc3a3fe795fcdf06703394f81
```

## Verdict

**STRICT FAIL.**  Equation (5.11) is false uniformly in the old-active
level at a historically reachable positive-debt base.  Its failure makes
the upward-return estimate (8.2) and the duration estimate (7.2) false for
the candidate theorem as stated.

This is not a counterexample to recurrence, T3-2, or C3.  It is an exact
counterexample to the proposed descriptor-local stopped theorem and to its
pure-renewal/compact-transience mechanism.  No incidence or pair can be
promoted from the audited bytes.

## 1. Network and closed class

Use the admitted normalized support

\[
 L_+=\{0,V+I\},\qquad L_0=\{I,2U,2I,U+I\}.             \tag{A.1}
\]

Take the complete directed graph on each support and give every reaction
rate constant one.  These are strong orientations.  Because every reaction
has its reverse, the set reachable from

\[
                         x^\circ=(0,0,0)                         \tag{A.2}
\]

is a closed irreducible physical class.

All calculations below use ordinary stochastic mass-action falling
factorials, exactly as in the candidate note.

## 2. The bad bases are historically reachable with positive debt

For every \(n\ge0\), the following enabled physical word maps
\((U,V,I)=(0,n,0)\) to \((0,n+1,0)\):

```text
0 -> V+I,  I -> 2I,  2I -> 2U,  2U -> I,
0 -> V+I,  2I -> I,  V+I -> 0.
```

Indeed, its successive physical states are

\[
\begin{aligned}
(0,n,0)&\to(0,n+1,1)\to(0,n+1,2)\to(2,n+1,0)\\
       &\to(0,n+1,1)\to(0,n+2,2)\to(0,n+2,1)
         \to(0,n+1,0).                              \tag{A.3}
\end{aligned}
\]

Starting the reflected lift at \((x^\circ,0)\), reflection is inactive
after the first positive \(V\)-increment in this word.  Thus (A.3) also
maps \(D_V=n\) to \(D_V=n+1\).  Iteration proves that

\[
                  (U,V,I,D_V)=(0,n,0,n)                         \tag{A.4}
\]

is reachable for every \(n\).  In particular, these bases satisfy the
historical positive-debt hypothesis and have the required subpower
spectator start \(u=0=n^{o(1)}\).

## 3. Exact failure of the pure-renewal bound

At the base \((0,n,0)\), the only enabled reaction is the proper opening
\(0\to V+I\), of rate one.  Immediately after it the state is

\[
                         (U,V,I)=(0,n+1,1),
                         \qquad R=1.                 \tag{A.5}
\]

The enabled reactions and their rates at (A.5) are

\[
\begin{array}{c|c}
\text{reaction}&\text{rate}\\ \hline
V+I\to0&n+1\\
0\to V+I&1\\
I\to2U&1\\
I\to2I&1\\
I\to U+I&1.
\end{array}                                                       \tag{A.6}
\]

The first row is an immediate pure exact cleanup.  Hence one raw base
attempt is an immediate pure return with probability

\[
                         p_n={n+1\over n+5}.                       \tag{A.7}
\]

In particular \(Z^{\rm pure}(0)\ge p_n\), and therefore

\[
 {1\over1-Z^{\rm pure}(0)}
       \ge {1\over1-p_n}={n+5\over4}.                             \tag{A.8}
\]

For (A.1), the post-diagonal degree used in the note is \(d=2\), because
the lower support contains \(2U\).  The exact-pair line of (5.11), at
\(u=0\), instead asserts

\[
 {1\over1-Z^{\rm pure}(0)}\le C(1+0)^{2-d}=C                    \tag{A.9}
\]

with \(C\) independent of \(n\).  Equations (A.8)--(A.9) contradict one
another.

The precise error is the invocation of “finite compact transience” after
(5.11).  At this compact spectator base the nominal degree-two escape
source \(2U\) is disabled.  Historical positive-debt transience says that
an exit eventually occurs for each fixed \(n\); it does not give an
\(n\)-uniform probability of exiting before a pure return.  The fast
cleanup rate is of order \(n\), so that probability is only of order
\(n^{-1}\).

## 4. Upward return has probability at least one quarter

At (A.5), the immediate reaction \(I\to2U\) has probability

\[
                         a_n={1\over n+5}.                         \tag{A.10}

It sends (A.5) to

\[
                         (U,I,R)=(2,0,1),                         \tag{A.11}

which is immediately the included upward terminal \(U^\uparrow\) under
Sections 1--2 of the candidate.  No later dynamics or service reaction can
change its label, because the stopped kernel ends at this first \(I=0,R>0\)
endpoint.

For every \(m\ge0\), the event consisting of \(m\) immediate pure retries
followed by the immediate branch (A.10) is disjoint from the corresponding
events for other \(m\).  Consequently

\[
 \mathbb P_{(0,n,0)}(U^\uparrow)
     \ge\sum_{m=0}^{\infty}p_n^m a_n
     ={a_n\over1-p_n}={1\over4}.                                 \tag{A.12}
\]

This directly contradicts

\[
                  \mathbb P(U^\uparrow)\le n^{-1+o(1)}           \tag{A.13}

in (8.2).  The contradiction uses an unbounded analytic geometric sum, not
an exhaustive path check.

## 5. The physical duration grows linearly

Let \(N_n\) be the number of raw base attempts up to and including the
first attempt whose first opened-state reaction is not the immediate pure
cleanup in (A.7).  The strong Markov property gives

\[
                         \mathbb E N_n={1\over1-p_n}
                                      ={n+5\over4}.               \tag{A.14}

At every base the only enabled clock has rate one.  Thus each of these
attempts contains a mean-one base holding time.  Since the stopped episode
cannot finish before that first non-pure branch,

\[
                         \mathbb E_{(0,n,0)}\sigma
                         \ge {n+5\over4}.                         \tag{A.15}

Equation (7.2), with \(p=1\) and \(u=0\), asserts an upper bound independent
of \(n\).  Equation (A.15) disproves it.  The moment-kernel recursion
(7.1a)--(7.1c) is algebraically correct, but its asserted macro-moment input
(7.1b) fails here because the pure-renewed holding-time moment is already
of order \(n\).

## 6. Consequences and repair boundary

The analytic target/source identity in Lemma 5.2, the large-interruption
tail mechanism, and the formal two-stage resolvent algebra do not repair
(A.8).  Their application presupposes the false pure-renewal estimate
(5.11).  Likewise the common-potential conclusion (8.7) is not established
by this snapshot because its proof uses both the false upward estimate and
the false duration input.  This audit does not assert that (8.7) itself is
false for every orientation or rate vector in (A.1).

A valid repair must treat spectator bases at which the advertised
post-contraction escape source is disabled.  They cannot be placed in a
finite global exception: (A.4) contains infinitely many old-active levels
inside one fixed closed class.  Possible repairs would need a different
effective trace which retains the order-one defect law after the
\(\Theta(n)\) pure retries, or a separate physical episode for this
singular compact-spectator regime.  Merely changing a finite certificate,
or appealing again to qualitative compact transience, cannot prove the
claimed \(n^{-1+o(1)}\) upward probability.

All analytic, descriptor-local, pair-level, and global certification flags
must remain false.
