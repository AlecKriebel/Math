# Hostile audit of the cap-free B/F0 killed resolvent and common-W closure

**Audit date:** 2026-08-12 PDT.

## 1. Verdict

The proposed cap-free B/F0 construction based on

\[
 H(v,a)=R^a((v-a)!)^\theta                                  \tag{1.1}
\]

is **CONDITIONALLY SOUND** for \(0<\theta<1\), with a sufficiently large
fixed \(R\), a finite-core corrector, and the exact absorbing sections
specified below.  It can supply the relative exponential marked-factorial
overshoot needed to append the B-service episode.

The proposed global conclusion is **NOT YET PROVED** by sequential
compactness alone.  A corrected-tier passing episode can physically disable
its old top source and land in a B/F0 or B/B phase before earning its rare-
target charge.  The killed continuation must be appended in the same
episode, or a separate finite/countable reward-kernel theorem must charge
the transition.  A terminal-chart-exit or graph-SCC shortcut is invalid.

## 2. Exact one-dimensional reduction

Write \(X\) for the active coordinate and \(U,V\) for the inactive
coordinates.  In a B/F0 failure choose the B witness

\[
                 q=X+U,\qquad c_X=0,\qquad q_U\le c_U,
                 \quad q_V\le c_V.                         \tag{2.1}
\]

The case \(q=X\) is immediate access.  In the nonaccess case \(q=X+U\),
the diverging \(X\) forces \(U=0\).  Any enabled source that remains inside
the Flat0 phase must then lie in

\[
                              \{0,V,2V\}.                   \tag{2.2}
\]

A target containing \(U\) is top access.  A degree-zero B-linkage reaction
is a Bellman launch.  Any other named promotion may be made an absorbing
boundary.  Consequently the nonabsorbed kernel is a genuine one-species
binary mass-action kernel, carrying the actual pure-flat target as its mark.

If that target has \(V\)-degree \(a\in\{0,1,2\}\), physicality gives
\(a\le v\).  Thus the factorial in (1.1) is always defined.  An inconsistent
phase \(a>v\) is unreachable and must not be added to the core matrix.

## 3. Outer \(H\)-contraction

Let \(D\in\{0,1,2\}\) be the largest degree of an enabled pure source among
both internal and killing labels outside the finite core.  The complex
\(DV\) is unique in the binary universe; disjoint linkage supports preserve
that uniqueness.  Parallel labels merely split its fixed total out-rate.

For an internal jump \(dV\to eV\), exact cancellation gives

\[
 {H(v-d+e,e)\over H(v,a)}
 =R^{e-a}\left({(v-d)!\over(v-a)!}\right)^\theta .          \tag{3.1}
\]

A dominant \(D\)-source internal target has \(e<D\).  If \(a=D\), its
ratio is at most \(R^{-1}\); if \(a<D\), it tends to zero polynomially.
A dominant \(D\)-source kill contributes zero to the survival kernel.
For a lower source \(d<D\), the source-probability factor and (3.1) give

\[
 O\!\left(v^{-(D-d)+\theta(a-d)}\right)=o(1),               \tag{3.2}
\]

uniformly over \(a\le D\), provided \(0<\theta<1\).  Hence \(R\) can be
chosen so that the killed survival kernel \(Q\) has strict \(H\)-drift
outside a finite set.

Self labels, if retained at all, must be contracted or included in the
fixed dominant-source fraction.  Strong connectivity supplies a positive
nonself or killing fraction, so a large \(R\) still leaves a strict margin.

## 4. Finite core and closed no-kill components

Raw \(H\) need not contract on the finite core.  The proof must first make
every closed no-kill communicating component absorbing.  For each remaining
core state it must prove access to a killing section or to the outer drift
region.  Only then is the finite substochastic core matrix transient and
\(I-Q_{\rm core}\) a nonsingular M-matrix.  Solving its finite inequalities
gives the required core corrector.

A closed no-kill component is not necessarily a finite population class.
It can be an infinite one-species class at fixed \(X\), for example a parity
class under two-particle moves.  The correct conclusion is that its maximal-
degree one-species mass-action chain is positive recurrent.  If it is
reachable in a closed irreducible physical class, that class is confined to
the fixed \(X\) component and cannot support the alleged \(X\to\infty\)
escape.

The physical absorption time can be uniformly controlled: an edge leaving
the pure noaccess support has source \(dV\), so at \(v\ge d\) its hazard is
bounded below by a positive constant, while the finitely many lower states
are covered by the core minorization.  The embedded reaction count, however,
need not have uniform moments.

For example, take internal \(2V\to V\) and killing \(V\to U\), with fixed
positive rates.  From \(v\gg1\), the internal rate is order \(v^2\) and the
kill rate is order \(v\).  The expected number of internal jumps before
killing grows on the order of \(v\), although the physical time stays
bounded.  Therefore a cap-free theorem must not inherit the old finite-
phase assertion of uniformly bounded jump-count moments.

## 5. Exact relative factorial overshoot

At a pure internal endpoint, and also at an access or Bellman-launch target,
the active and newly created coordinate residuals cancel against the actual
target mark.  The only changing residual factorial is the \(V\) factorial.
Thus

\[
 e^{\theta\Delta F_{\rm prelude}}
   =R^{a_0-a_\tau}{H(V_\tau,a_\tau)\over H(v_0,a_0)}.       \tag{5.1}
\]

Since \(a_0,a_\tau\in\{0,1,2\}\), a killed-resolvent estimate

\[
             \mathbb E H(V_\tau,a_\tau)\le C H(v_0,a_0)   \tag{5.2}
\]

gives a uniform relative exponential moment of the positive marked-\(F\)
overshoot.  This is stronger than the polynomial moments required by the
physical-time Foster lemma.

The uniform estimate is relative to the starting factorial weight.  One
must not state an absolute bound on \(H(V_\tau,a_\tau)\) independent of
arbitrary \(v_0\).  Likewise the usual resolvent interpolation is

\[
 (I-Q)^{-1}H_{\theta'}\le C H_\theta,\qquad
                     0<\theta'<\theta<1,                    \tag{5.3}
\]

not an unweighted uniform Green bound.

For B/F0 starts with bounded \(v_0\), (5.2) supplies a superexponential
moving-boundary tail.  Split the access endpoint at
\(V_\tau\le X^\alpha\), \(0<\alpha<1\).  On the first event the B witness
gives the required rare terminal relative to \(X\); on the complement the
tail from (5.2) dominates every positive marked-F moment.  This is the exact
way in which relative overshoot protects the appended Bellman charge.

If instead \(v_n\to\infty\) along the sequence of episode starts, the state
sequence is two-active and must use the frozen unconditional AA rule from
the outset.  A proof may not call \(v_n\) a bounded cap merely because each
individual value is finite.

## 6. Explicit obstruction to naive global compactness

The pair

\[
 \{0,2A,2B\}\mid\{A,B,A+B,A+C\}                           \tag{6.1}
\]

belongs to the exact 6,654 failure set.  It has a corrected-cut passing
one-active descriptor with \(C\) active,

\[
                 w=(0,0,1),\qquad (A,B,C)\text{-caps}=(1,0,2),
                 \qquad E=U_L=\{A+C\}.                     \tag{6.2}
\]

Choose a strong orientation containing \(A+C\to B\).  At

\[
                         x=(1,0,N),                         \tag{6.3}
\]

this certified edge has nonvanishing probability and produces

\[
                         x'=(0,1,N-1).                      \tag{6.4}
\]

The old top source \(A+C\) is disabled.  At \(x'\), the only enabled
sources are \(0\) and \(B\), both constant scale, so the actual target
\(B\) is not rare.  Deleting the structural-exit test from the old
corrected-tier proof therefore makes its terminal-ratio argument false.

The endpoint (6.4) is a B/F0 phase.  The cap-free killed continuation is
exactly the natural repair: append it before declaring the episode complete.
What is not legitimate is to stop at (6.4), cite a common potential, and
invoke sequential compactness.  That leaves the exit reward uncharged.

More generally, an exact finite replay of all certified one-active passing
edges in the 6,654 family whose firing disables every old top-S source finds
endpoint profiles of three kinds:

\[
                   2820\ \mathrm{B/F0},\qquad
                    612\ \mathrm{B/B},\qquad
                    792\ \mathrm{pass}.                     \tag{6.5}
\]

These are support/descriptor edge incidences, not stochastic trajectories.
The 792 passing endpoints show that the global closure cannot be asserted
from the B/F0 lemma alone.  At such an endpoint one must prove either that
the actual target is already rare relative to a newly enabled source or
append the next physical rule.  The complete continuation must have a
uniform expected-reward bound; a graph-only SCC test is insufficient.

## 7. Exact repair requirements

A publication-ready common-\(W\) completion of the 18,496 branch must state
and prove all of the following.

1. The B/F0 internal state includes the actual pure target mark and only
   physically reachable phases \(a\le v\).
2. The killed kernel includes all labels; parallel and self labels are
   aggregated or contracted explicitly.
3. Closed no-kill components are removed before the finite-core M-matrix is
   inverted, and are proved classwise positive recurrent at fixed \(X\).
4. The resolvent gives the relative boundary estimate (5.2), uniform
   physical duration, and positive marked-F overshoot moments, but makes no
   false uniform embedded-count claim.
5. Starts with \(V\to\infty\) are routed to the unconditional two-active AA
   theorem by a literal subsequence split.
6. Every corrected-tier passing structural exit is charged by an appended
   B/B, B/F0, newly rare-target, or further killed continuation.  The proof
   must terminate this concatenation with negative expected common-\(W\)
   reward; sequential compactness and terminality do not supply that fact.

Until item 6 is proved for the exact passing-exit family, the cap-free
one-dimensional lemma is a valid local repair but not a complete global
recurrence proof.
