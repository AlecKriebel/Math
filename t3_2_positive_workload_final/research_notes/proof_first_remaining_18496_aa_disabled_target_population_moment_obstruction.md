# AA disabled-target obstruction to a one-jump population-moment bound

**Proof-first hostile addendum, 2026-08-12 PDT.**  This note records a
literal two-active AA witness showing that the one-jump population-moment
obstruction is not confined to the one-active B/F0 prelude.  It supplements,
without changing, the frozen global hostile-requirements note

~~~text
research_notes/proof_first_remaining_18496_hybrid_potential_hostile_requirements.md
e3eacec9f2f26ff3739e16d77f773944d05095621bb272c978c0d69897217a8b
~~~

It makes no recurrence claim.

## 1. Exact support row

Take

\[
 L_1=\{0,2A,A+B\},
 \qquad
 L_2=\{A,B,2B,A+C\}.                                \tag{1.1}
\]

The authoritative 18,496-pair certificate contains this pair with a
two-active AA failure row

\[
 w=(0,1,3),\qquad c=(0,2,2),                         \tag{1.2}
\]

so A is bounded at zero and B,C are active.  Both linkage classifiers are
C.  The relevant finite bytes are

~~~text
src/outside_mixed_remaining_18496_certificate.py
314f378664052cabe23910e118c9a43acf99884ccb5c63b61daf014a206e4c63
tests/test_outside_mixed_remaining_18496_certificate.py
28d3cf0087bcd77e24d6dbfa280b226b34d3d026c35e743bc10487c829667769
~~~

This is a support/descriptor identity only.

## 2. Strong orientation and physical marked state

Choose on the second linkage the directed cycle

\[
                 A\longrightarrow B\longrightarrow2B
                 \longrightarrow A+C\longrightarrow A,             \tag{2.1}
\]

with arbitrary fixed positive labelled rates.  Choose any strong cycle on
the first linkage.  At

\[
                         x_n=(0,n,n^3),               \tag{2.2}
\]

the enabled second-linkage sources are B and \(2B\), of respective orders
\(n\) and \(n^2\); A and \(A+C\) are disabled.  The first linkage contributes
only its zero-source clocks, of order one.  Consequently the labelled edge

\[
                         2B\longrightarrow A+C        \tag{2.3}
\]

has all-clock probability bounded below by a fixed positive constant.

The actual mark \(2B\) is physical: it is the target of the preceding edge
\(B\to2B\), and the population in (2.2) is reached from
\((0,n-1,n^3)\) when that edge fires.  Its probability need not be uniform;
positive reachability is enough to invalidate a claimed uniform bound over
physical marked states.

## 3. Exact population-factorial cost

Put \(P(x)=\sum_i\log(x_i!)\).  The endpoint of (2.3) is

\[
                       x'_n=(1,n-2,n^3+1).
\]

Exact factorial cancellation gives

\[
 \begin{aligned}
 P(x'_n)-P(x_n)
   &=\log{(n^3+1)(n-2)!\over n!}\\
   &=\log{n^3+1\over n(n-1)}
     =\log n+o(1).
 \end{aligned}                                      \tag{3.1}
\]

Since (2.3) has probability bounded away from zero,

\[
 sup_{x,t}\mathbb E_{x,t}[(\Delta P)_+]^q=\infty
 \qquad(q>0)                                         \tag{3.2}
\]

for the one-jump rule even within the AA profile.  The target \(A+C\) was
disabled before the jump, so the enabled-target source-probability
comparison does not apply.

## 4. Exact repair requirement

At the endpoint in (3.1), the newly enabled source \(A+C\) has propensity
of order \(n^3\), larger than the residual \(2B\)-source scale \(n^2\).  In
the cycle (2.1), its edge to A removes C and pays the activation debt.
Therefore this example does not oppose recurrence.  It proves that an AA
episode may not stop at (2.3), at a descriptor change, or merely because the
actual target has changed.

The required theorem must append the all-clock killed top-source kernel
through the newly enabled \(A+C\) phase and retain the exact combined
population increment.  More generally, every disabled-target activation
must be paired with its physical high-source service before an
episode-level positive population-moment bound is asserted.  No terminal
chart-exit shortcut supplies that pairing.
