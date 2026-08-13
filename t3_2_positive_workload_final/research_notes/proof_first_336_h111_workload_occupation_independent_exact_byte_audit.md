# Independent exact-byte hostile audit: homogeneous workload occupation

**Audit date:** 2026-08-12 PDT.

## 1. Frozen target and verdict

The immutable target is

~~~text
research_notes/proof_first_336_h111_workload_occupation_theorem.md
SHA-256 e3c484cdbda44949ba070dae6c911a2c7de465064857b61b5d9883e9dd03bdff
484 lines / 20,247 bytes
~~~

> **STRICT PASS.**  The target proves its direct-death occupation macro for
> all 312 homogeneous incidences of the residual level-set family, under
> arbitrary fixed strongly connected labelled orientations, arbitrary fixed
> positive rates, and every closed irreducible population class.  Combined
> with the pinned workload-only physical-time Foster theorem, this proves
> positive recurrence for the complete homogeneous family.

The proof is analytic.  Finite code supplies only the exact support and
dead-ray identities; it enumerates no orientations, rates, populations, or
stochastic histories.  The 24 anisotropic incidences are outside this target.

## 2. Exact dependencies and support scope

Every dependency named by the theorem rehashes exactly:

~~~text
workload-only physical-time Foster theorem
8cf2a8d41f0fab64bf34b6608fa7cf6b0f1b385a30f4a01afeb10c7732851b2a

its independent strict audit
9d8fc8b5e15178e7a8305422ba7fd08e6875e851c37951207815d5d84babcc67

carrier/dyadic activation theorem and two strict audits
f4d8cc40ccea1c6d9e0df9302f75c8cc1d58dd7c89669fd19ad48fc4bca735b0
30d780d5853a956bd1502fae8517483caac9f0bd77606f6f6bc13caccb56d783
219a21a59f57a839d52c4fa0c7cdac3df3dacdac47e16655db957f0a8a026c62

all-lower-support common-catalyst theorem and two strict audits
81a48c007e092570cd500d8f124c0546538d44f7e62599100ecf00480f401496
5a85a422345a2dd8d640dcd2986f31cd035d293d8bfbb9735941915e547c39f8
4fbf8fd6384940e5a8919270e4da6a2cbe2885fb465b68957ec51ce592f979f2

residual support certificate and tests
4149b682d1222bd3327548b0eb95921f7aae20663816b345b48285239c12f93d
6f5802976d4de479a0728648248a2291f5d518e04de29b9b7053802eb7f1b9c2
~~~

The focused certificate replay gives exactly 312 homogeneous incidences and
360 dead pure rays:

\[
       360=168\text{ two-carrier}+144\text{ dyadic}
                         +48\text{ common-catalyst}.                 \tag{2.1}
\]

Exactly 270 rays have the bulk species in the lower support.  The 48
common-catalyst rays have the four relative lower patterns (XY,XZ,YZ,XYZ),
twelve each.  Thus the pinned activation dependencies have literal support
coverage; no optional lower support or bulk-source case is silently omitted.

## 3. Symbolic boundary partition

For a homogeneous quadratic rank-two top support, a pure (X)-vertex is
top-dead exactly when (2X) is absent.  A two-species face (Y=0) is dead
only when every top complex contains (Y); the only possible quadratics are
(X+Y,Y+Z,2Y), and rank two forces all three.  Conversely that support is
dead on the whole face.

Outside the latter common-catalyst case, the maximal dead sets are pure
vertices.  Their small normalized wedges can have disjoint compact closures.
Bounded reaction displacement then makes the first large-population wedge
exit land in the common activated complement, never another wedge.  In the
common-catalyst case the entire dead face is assigned directly to the
all-lower-support theorem.  Therefore the partition has no overlap and no
zero-time handoff.

At every activated boundary point some top source is enabled.  A directed
walk in the strong top graph successively produces every coordinate that is
missing.  In the sourcewise decomposition

\[
       \dot z_i=P_i(z)-C_i(z),\qquad P_i\ge0,qquad C_i(z)\le K_i z_i,
                                                                    \tag{3.1}
\]

an already positive coordinate stays positive, while a missing target
coordinate has strictly positive derivative at its first producing edge.
The walk enables every complex.  Rank two in the constant-sum plane forces
all three species to occur, so the top trajectory enters the simplex
interior.

If the common catalyst is absent from the lower support, its zero face is
invariant for the full process and the top linkage is dead there.  The
remaining open-unary linkage has the standard positive killed-resolvent
linear Foster function.  This is an exact fixed-class reduction, not an
unproved activation alternative.

## 4. Activation dependencies and complete clocks

The carrier/dyadic dependency first constructs a base activation-or-return
time with bounded expected duration and birth count while every death remains
live.  Only afterward is it truncated at the (L)-th direct death.  Hence
the prelude debt is independent of (L), and the endpoint labels
fractional-return (F), death-ledger (D), and activated (I) are disjoint.
Its literal low-phase proof covers the lone-(Z) dyadic resistance-two state
and order-workload favorable lower clocks.

The catalyst dependency works on the whole dead face.  Its protected-label
coupling covers every lower support, includes the fractional-return branch,
and has a complete expected ledger rather than a first-death restart.  It
already appends its own catalyst-shell service.  The full theorem correctly
does not send catalyst endpoints through the separate noncatalyst service
window.

## 5. Deterministic permanence and uniform service

The top ODE is autonomous, weakly reversible, and has one linkage class.
Its rank-two stoichiometric subspace is the entire plane of constant total
population, so its positive normalized class is the simplex interior.

The cited Boros--Hofbauer Theorem 4.2 was checked directly against
arXiv:1903.03071v2.  It states permanence for every weakly reversible
single-linkage mass-action system with bounded kinetics, with no deficiency
restriction.  Fixed positive rates satisfy bounded kinetics.  Thus every
positive top trajectory eventually remains in a compact interior set and
has infinite occupation in every coordinate.

The theorem does not apply permanence directly to a boundary start.  It
first proves interior entrance by (3.1).  For any death coordinate (d) and
any (M), each activated start therefore has a finite horizon with
(int z_d>M+1).  Polynomial-flow continuous dependence extends this to a
relative neighborhood, and a finite subcover of the compact activated set
gives one common horizon (T(M)).  This proves the exact uniform statement

\[
          \inf_{z(0)\in\mathcal A}\int_0^{T(M)}z_d(s)\,ds>M.        \tag{5.1}
\]

No pointwise-to-uniform inference is missing.

## 6. Stochastic fluid window and death compensator

At activated workload (N), run physical time (T/N) and scale population
by (N).  Quadratic top clocks then give order-one fluid drift, predictable
density quadratic variation (O(N^{-1})), and an (O(N^{-1})) falling-
factorial correction.  All lower clocks together have only (O(1)) stopped
compensator on this interval, so their density perturbation is (o(1)).
Doob, Gronwall, and localization give uniform (L^1) convergence to the top
flow, including activated boundary starts.

Top reactions preserve workload.  Exiting the localization interval
([N/2,2N]) requires at least (N/2) population-changing lower events, while
their stopped compensator is bounded.  The counting-process exponential
martingale therefore makes this exit probability tend uniformly to zero.

For a direct-death species (d), exact compensation under the time change is

\[
 \mathbb E D_{{\rm win},d}
   =\delta_d\mathbb E\int_0^{\zeta_N}Z_d^N(s)\,ds.                 \tag{6.1}
\]

Equations (5.1), the uniform fluid estimate, and vanishing localization
error make (6.1) arbitrarily large, while expected births and physical
duration are \(O(N^{-1})\).  The first ordinary all-clock jump appended after
the window has mean holding time at most \(1/\beta\), adds at most one birth,
and makes the block contain a genuine reaction.  No top or lower clock is
suppressed.

## 7. Expected ledger and workload-Foster handoff

On (F), the exact pathwise workload identity already gives net service at
least half the initial workload.  On (D), the prelude has at least (L)
deaths; all prelude births are charged once by the uniform expectation
bound.  On (I), the service window supplies conditional mean death service
(D_0), and its births plus the final-jump birth are charged once.  Therefore

\[
 \mathbb E(D_\tau-B_\tau)
 \ge L\{\mathbb P(F)+\mathbb P(D)\}
       +D_0\mathbb P(I)-C_B-o(1).                                \tag{7.1}
\]

The prelude debt does not depend on (L), so (L,D_0) can be chosen after
that bound.  The complete episode has uniformly finite expected duration.
Choosing the service slack larger than a fixed multiple of that duration
gives

\[
  \mathbb E\{H(X_\tau)-H(x)+\eta\tau\}\le0.                       \tag{7.2}
\]

Birth integrability gives endpoint-workload integrability.  Outside the
low-direct-death set, the workload generator is already strictly negative
and the one-jump rule applies.  Every episode contains a physical jump, so
nonexplosion makes episode time diverge on non-hitting.  These are exactly
the hypotheses of the pinned workload-only Foster theorem; no terminal-chart
or drift-or-exit SCC argument is used.

## 8. Nonexplosion and final scope

Only constant births can increase total population.  Unary transfers and
all quadratic top reactions preserve it, while deaths decrease it.  Thus
workload is pathwise dominated by initial workload plus a constant-rate
Poisson process.  Each bounded workload sublevel contains finitely many
states and has bounded binary hazards, proving nonexplosion.

The theorem therefore covers every homogeneous rank-two level-set pair in
the certified 312-incidence family, with the open-unary invariant faces
handled separately as stated.  It makes no claim on the 24 anisotropic rows.

## 9. Reproduction and render

The target hash, line count, byte count, dependency hashes, and visible
control-byte scan were replayed.  Pandoc and Tectonic produced clean
letter-paper PDFs for the target and this audit.  All pages were rasterized
and visually inspected for clipping, overlap, malformed equations, broken
code blocks, and missing glyphs.  No mathematical, exact-byte, dependency,
or rendering obstruction remains.

> **FROZEN VERDICT: STRICT PASS.**
