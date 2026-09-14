# Labeled incoming current and orbit-reward checkpoint

Timestamp: 2026-09-14 14:53 UTC. Implementer: incoming subagent.
This is an implementation/translation checkpoint, not an independent final adversarial review.
Local task completion estimate: 100%. Final Channel reward cast/reindex match clean built.
Stage 3 contribution: the entire incoming-current, stationary normalization,
feature centering, and labeled orbit-reward part has kernel proofs; physical
Poisson/coefficient-solution identification is maintained separately.

## Definitions and statement checks

`Active.kernel` is used without replacement: its two terms continue from the
same target or choose a target uniformly from the current nonempty cache and
then sample outside that target. `State n` contains actual cache/target pairs;
no quotient of unlabeled ranks is used to count incoming predecessors.

`Incoming.nu0_kernel` proves, for every real matrix P and n≥2,

    (ν₀ K(P))(B,v) = (Σ i∈B, P(v,i)) / (n 2^(n−2)).

No looplessness hypothesis is needed for this particular identity: the original
kernel explicitly excludes diagonal sources, and v∉B excludes them on the
right. `nu0_stationary` specializes to the complete loopless kernel;
`nu0_perturbation` specializes to its actual signed linear perturbation.
`nu0_sum` independently proves the printed weights sum to one.

The continue branch counts caches B and B\{i}, with rank weights k and k−1.
The stop branch counts caches B∪{v} and (B\{i})∪{v}, with respectively n−k−1
and n−k allowable old targets. The cache-rank weight cancels the actual
retargeting denominator. Empty or full boundary families contribute exactly
zero; the proof never constructs an invalid empty-cache state.

`sum_state_powerset` reindexes the actual labeled states by target and subsets
of its complement, permitting the empty subset only with a proved zero term.
`OrbitMoments.orbit_linear`, `orbit_square`, and `orbit_cross` prove the raw
moments by one-, two-, and three-label inclusion counting. The previously
proved normalized averages remain available and compile.

`nu0_feature_zero` proves ν₀F=0 for all coefficient sequences and all symmetric,
zero-diagonal, row-balanced δ. It does not presume feature-map injectivity.
Column balance follows from symmetry and row balance as in Active.lean.

`frobeniusSq δ` is exactly Σ_v Σ_i δ(v,i)^2. `sum_rowNorm` proves that the
row norms in the fixed-target orbit sums add to this quantity. No division by
a norm is performed, so zero δ is included in every reward identity.

`Reward.nu0_perturbation_feature` proves for every N≥3 and n=N+1 that the actual
ν₀ΔF equals frobeniusSq δ times

    Σ_{j<N−1} choose(N−2,j) a(j+1) / [2^(N−1)(N+1)]
    − Σ_{j<N−2} choose(N−3,j) b(j+2) / [2^(N−2)(N+1)].

`Reward.nu0_perturbation_coeff_feature` specializes the preceding theorem to
the actual zero-extended Channel coefficients, proving exactly

    ν₀Δ(feature δ (coeffA N c) (coeffB N c))
      = frobeniusSq δ * ↑(dotProduct (reward N) c).

`Reward.frobeniusSq_pos` proves strict norm positivity for every nonzero δ.

The exact powers, signs, and two distinct channel ranges follow from Pascal
identities and the orbit counts; the k=0, k=1, and k=N boundary terms are
proved to vanish. No finite-size fitting or assumed scalar occurs.

## Trust and remaining dependencies

Clean checked command at the core checkpoint:

    lake build SymmetricSector.Incoming SymmetricSector.Reward

Principal completed theorem axiom reports contain only `propext`,
`Classical.choice`, and `Quot.sound`. The files contain no `sorry`, `admit`,
project axioms, `native_decide`, or external computed-answer assertions.

The incoming/reward theorem alone does not identify F with GΔGq. That needs the
actual first Poisson identification, actual feature intertwining, coefficient
solution equation, and physical inverse uniqueness, proved in the separate
bridge modules. It also does not imply the full fixation Hessian theorem,
coverage/collision representation, stationary perturbation theorem, or
complementary tangent-sector positivity.
