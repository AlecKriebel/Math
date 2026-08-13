# Exact-byte audit: homogeneous workload

**Independent audit date:** 2026-08-12 PDT.

## 1. Frozen target and verdict

The immutable target is

~~~text
research_notes/proof_first_336_h111_workload_occupation_theorem.md
SHA-256 e3c484cdbda44949ba070dae6c911a2c7de465064857b61b5d9883e9dd03bdff
484 lines / 20,247 bytes
~~~

> **STRICT PASS.** The target proves the all-clock direct-death occupation
> macro for every one of the 312 homogeneous incidences in the residual
> level-set family, for every strong labelled orientation, every fixed
> positive rate vector, and every closed irreducible population class. In
> combination with its pinned workload-only physical-time Foster theorem,
> this proves positive recurrence for the complete homogeneous family.

This is an analytic replay. No orientation, rate, population box, or reaction
history was enumerated. The finite certificate is used only for the
\(168+144+48=360\) dead-ray support identity.

## 2. Exact scope and dependencies

The target's frozen dependencies rehash exactly as follows.

~~~text
workload physical-time Foster theorem
8cf2a8d41f0fab64bf34b6608fa7cf6b0f1b385a30f4a01afeb10c7732851b2a

workload theorem exact-byte audit
9d8fc8b5e15178e7a8305422ba7fd08e6875e851c37951207815d5d84babcc67

carrier/dyadic activation theorem
f4d8cc40ccea1c6d9e0df9302f75c8cc1d58dd7c89669fd19ad48fc4bca735b0

carrier/dyadic exact-byte audits
30d780d5853a956bd1502fae8517483caac9f0bd77606f6f6bc13caccb56d783
219a21a59f57a839d52c4fa0c7cdac3df3dacdac47e16655db957f0a8a026c62

all-lower-support common-catalyst theorem
81a48c007e092570cd500d8f124c0546538d44f7e62599100ecf00480f401496

common-catalyst exact-byte audits
5a85a422345a2dd8d640dcd2986f31cd035d293d8bfbb9735941915e547c39f8
4fbf8fd6384940e5a8919270e4da6a2cbe2885fb465b68957ec51ce592f979f2

residual support certificate and tests
4149b682d1222bd3327548b0eb95921f7aae20663816b345b48285239c12f93d
6f5802976d4de479a0728648248a2291f5d518e04de29b9b7053802eb7f1b9c2
~~~

The target assumes exactly a homogeneous quadratic rank-two upper support
and an open unary lower support. It neither imports the 24 anisotropic rows
nor claims that a finite support count proves a stochastic estimate.

## 3. Boundary classification and entrance

A proper coordinate face is upper-dead precisely in the two cases stated in
the target. A pure \(X\)-ray is dead iff \(2X\notin T\). If the face
\(Y=0\) is dead, every upper complex contains \(Y\), so the only possible
quadratics are \(X+Y,Y+Z,2Y\); rank two forces all three. Conversely this
support kills that face.

Outside the common-catalyst case, small closed wedges about the finitely many
dead pure vertices can be chosen disjoint. Bounded reaction vectors and their
positive normalized separation imply that a first large-population wedge
exit lands in the common activated compact set, not another wedge. In the
common-catalyst case the entire face neighborhood is passed to the pinned
all-lower-support theorem, so no overlapping wedge declaration is used.

At an activated boundary point, an enabled source exists. Following a
directed spanning walk in the strong upper graph produces every missing
target coordinate. The sourcewise decomposition

\[
 \dot z_i=P_i(z)-C_i(z),\qquad P_i\ge0,
 \qquad C_i(z)\le K_i z_i                              \tag{3.1}
\]

keeps each newly positive coordinate positive by variation of constants.
Rank two in the total-degree-two plane forces all three species to occur, so
the trajectory enters the relative interior in finite time. This closes the
boundary-to-interior step without assuming an initially positive state.

## 4. Deterministic permanence and uniform service

Once the normalized top trajectory is positive, its stoichiometric class is
the full simplex interior: the upper difference space has rank two and lies
in \(\{v:\sum_i v_i=0\}\). The upper network is weakly reversible and has
one linkage class. Boros--Hofbauer Theorem 4.2 therefore gives permanence;
there is no deficiency hypothesis.

I independently checked the theorem statement in the primary arXiv version
1903.03071v2, corresponding to DOI 10.1137/19M1248431. It applies to every
weakly reversible single-linkage mass-action system with bounded kinetics on
each positive stoichiometric class and asserts entry into a compact forward
invariant subset. Constant positive rates satisfy bounded kinetics.

For every direct-death coordinate \(d\), permanence implies

\[
                 \int_0^\infty \phi_d(s;z)\,ds=\infty.             \tag{4.1}
\]

This pointwise fact becomes uniform over the compact activated set exactly as
the target states. For each initial \(z\), choose a finite horizon giving
exposure above \(M+1\); finite-time continuous dependence gives the same
exposure above \(M\) on a relative neighborhood. A finite subcover and the
nonnegativity of the integrand give one common horizon \(T(M)\), including
boundary initial conditions. There is no unjustified uniform-permanence
claim at time zero.

## 5. Stochastic fluid window

Starting at workload \(N\), use \(Z^N(s)=N^{-1}X(s/N)\). Quadratic upper
propensities are order \(N^2\), their density jumps are order \(N^{-1}\), and
the physical window is \(T/N\). Hence the upper density martingale has
predictable quadratic variation \(O(N^{-1})\). The falling-factorial to
monomial error is \(O(N^{-1})\) in the fluid drift.

Before localization at workload \([N/2,2N]\), lower unary intensity is at
most \(CN\). Its count over physical time \(T/N\) has bounded compensator,
so its density perturbation is \(o(1)\). Doob, Gronwall, and compactness give
the uniform convergence asserted in the target.

Only births and direct deaths change workload, by one. Leaving
\([N/2,2N]\) therefore needs at least \(N/2\) such events, while their
stopped compensator is bounded by a constant depending on \(T\). The
counting-process exponential martingale makes the localization-exit
probability vanish uniformly.

The exact labelled death compensator then gives

\[
 \mathbb E D_{{\rm win},d}
 =\delta_d\mathbb E\int_0^{\zeta_N}Z_d^N(s)\,ds,
                                                               \tag{5.1}
\]

so the mean service can be made arbitrarily large by first choosing the
deterministic exposure and then taking \(N\) large. In contrast, the mean
birth count and window duration are respectively at most \(\beta T/N\) and
\(T/N\). Appending the next all-clock jump is legitimate: the total hazard
is at least the constant birth rate \(\beta>0\), its mean holding time is at
most \(1/\beta\), it adds at most one birth, and any death is favorable.
Thus the block always contains an actual jump and keeps an actual endpoint.

## 6. Expected workload ledger

The carrier/dyadic prelude supplies a birth and duration debt bounded by
constants independent of the chosen death threshold \(L\). Its alternatives
are disjoint: fractional return \(F\), at least \(L\) deaths \(D\), or an
activated endpoint \(I\).

On \(F\), the exact identity \(H_t-H_0=B_t-D_t\) gives net service at least
\(H_0/2\). On \(D\), gross deaths are at least \(L\). On \(I\), the strong
Markov property and (5.1) give the chosen uniform mean service \(D_0\) from
the random activated endpoint. Charging all expected births globally is a
valid lower bound and yields

\[
 \mathbb E(D_\tau-B_\tau)
 \ge L\{\mathbb P(F)+\mathbb P(D)\}
       +D_0\mathbb P(I)-C_B-o(1)
 \ge\min\{L,D_0\}-C_B-o(1).                          \tag{6.1}
\]

The constants \(L,D_0\) are chosen only after the prelude debt is fixed.
This avoids circular threshold selection. The complete mean duration has a
uniform bound \(C_*\), so choosing the ledger slack above
\(C_*/(C_*+1)\) gives

\[
             \mathbb E(D_\tau-B_\tau)
                  \ge\eta\mathbb E\tau,
 \qquad \eta=(C_*+1)^{-1}.                           \tag{6.2}
\]

Birth integrability and \(H(X_\tau)\le H(x)+B_\tau\) give endpoint
integrability. The catalyst theorem supplies the identical workload contract
on its whole face neighborhood; its catalyst-free invariant face is an open
unary network and is positive recurrent directly.

## 7. Final Foster composition

Outside the direct-death boundary, the exact generator identity gives the
one-jump physical-time inequality. Inside it, Sections 3--6 give the macro.
Every episode contains at least one off-diagonal jump, has positive duration,
and uses the same proper workload \(H\). The pinned workload theorem tiles
these episodes and uses nonexplosion to rule out infinitely many episodes in
finite physical time. It then proves finite mean hit of a finite workload set
and finite mean return to a state in each closed irreducible class.

No marked potential, chart entrance charge, bounded neutral reaction depth,
or terminal Green seam appears.

**Frozen verdict: STRICT PASS.**
