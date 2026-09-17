# Adversarial extension statement contract

Written 2026-09-14 before the new proofs. All source is uncompiled.
Canonical manuscript Git blob: `bbd0667c934d5a34dd9c8ced50df91515cb1308c`.
Relevant labels: `eq:gval-model`, `eq:value-conditioned`, `eq:d4-entropy`,
`sec:framework`, and the no-value-only endpoint robustness corollary.

## Exact models

An extended behavior is the REAL array r(x,y,a,b,g), with g in Z_d x Z_d,
one fixed Eve measurement, no extra Eve input. Its bipartite behavior is the
sum over g. Success at (x*,y*) is sum_(a,b) r(x*,y*,a,b,(a,b)).

The finite model quantifies arbitrary finite Alice, Bob, and Eve coordinate
spaces. It has a positive trace-one state on (A x B) x E, d-outcome PVMs on
A and B (zero effects allowed), and an arbitrary d^2-outcome POVM on E.
Eve effects are positive and sum to identity; they are NOT required to be
idempotent. The extended Born rule is Re trace(rho ((M_a tensor N_b) tensor Q_g)).
The post-measurement sandwich / partial-trace formula is proved equal to this
rule; it is not replaced by a guessed success formula.

The approximate model is the actual product-topology closure of these full
extended behaviors. It is NOT the set of all extensions of a marginal in Qqa,
and NOT the closure of the subset already satisfying Bell equality.

The commuting model uses an arbitrary complete complex Hilbert space, a unit
vector, two PVM families, and a bounded positive complete Eve POVM. All THREE
party families commute across parties. No same-party commutation is required.
Positivity of a bounded Eve effect is its self-adjointness and nonnegative
quadratic form at every vector. The product Born formula is derived nonnegative.

No validity definition contains maximality, a scalar upper bound, a fixed
witness, equality spectrum, or target probabilities. Bell equality occurs only
in the subset used for value-conditioned optimization.

## Optimization

Use actual real sSup of success values among extended behaviors whose marginal
Bell score equals the already defined betaQ/betaQa/betaQc for that functional.
Before applying conditionally-complete-order lemmas, prove boundedness (success
between 0 and 1) and exhibit a physical member of the equality subset.

The flattened supremum ranges over all realizations AND all POVMs; it is the
supremal adversarial optimization in eq:gval-model. It does not assert a
maximizing realization exists. For a fixed finite realization, any separate
claim replacing a POVM supremum by a maximum needs a compactness theorem.
Do not imply that fixed-realization maximum existence has been formalized merely
by flattening the overall supremum.

Required endpoints for BOTH augmented families, all d>=4:

    1/d^2 + 2 sin(pi/d) sin(3 pi/d)/(d^2(d-1)) <= Gval_mu <= 1
    1/d^2 < Gval_mu,     mu = q, qa, qc.

The lower bound uses one explicit finite tensor strategy with E=C^1 and a
deterministic guess of a suitable output pair. Its entire extended behavior
must be proved in each model. The qc membership may use an actual explicit
embedding; a generic Qqa subset Qqc theorem is NOT needed or claimed.
At d=4 additionally target Gval_mu>=3/32 and the resulting conditional
min-entropy bound <=5-log(3)/log(2), NOT equality to the worst-case entropy.

## Scope and auditing

This adds the adversarial model/supremum layer, not a solution of the unknown
worst-case guessing optimization. The earlier finite and arbitrary-Hilbert
upper bounds remain source candidates. All new named declarations are included
in the standard import graph and generated axiom queries. Negative controls
must detect missing Eve normalization, assuming the witness is worst possible,
and replacing positivity by projectivity. No Lean invocation is planned here.

## Appendix continuation contract (source Fourier calculations)

`GeneralSourceFourier.lean` will implement the literal source coefficients from
`app:attainment`, using the integer triangular exponent k(k+1)/2, the forward
shift X, and the positive-character clock Z. It will derive the coefficient DFT,
the two `eq:source-fourier` sums and the displayed qutrit expression. These
identities are NOT by themselves a proof that the source Bob tuple is a PVM or
that it equals the canonical polar formula. The previous independently supplied
physical attaining strategies retain their separate validity proof candidates.

## Finite fixed-realization optimum

A separate Gram-factor compactness argument will prove that for any fixed finite
Eve space and any fixed collection of conditional matrices, the real linear POVM
objective attains its maximum over all complete POVMs. Gram factors parameterize
ALL positive effects by their positive square roots; their normalization bounds
individual entries by a dimension-dependent radius. No bound of two or qubit
carrier is reused. This is a finite-dimensional statement and does not assert
attainment of a worst-case realization or an arbitrary-Hilbert Eve optimum.
The general Gram-compactness pattern was inspected in the repository's separate
`Bell/QuantumCompactness.lean`; no theorem from that project is imported here.
