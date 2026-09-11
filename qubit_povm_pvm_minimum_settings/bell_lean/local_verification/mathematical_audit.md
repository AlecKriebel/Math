# Independent adversarial audit of the equality chain

Checkpoint: 2026-09-11T01:42:48Z. Bounded audit completion estimate: 85%.
This percentage describes this manual review, **not** completion of the full
formalization. No Lean compiler was run by this reviewer. No source declaration
was modified. Source comments and earlier positive audit reports were treated
as claims to check, not as evidence of correctness.

## Outcome and scope

No counterexample to the stated rank-zero, rank-one, or high-rank mathematical
claims was found in this pass. Their principal mechanisms are coherent on the
explicit premises in the source. This is not a certification of elaboration,
the full paper, or all imported physical reductions.

Both concrete negative controls below were independently evaluated with exact
rational arithmetic (`fractions.Fraction`); their null equations, image
relations, normalization and failed-premise signs passed their assertions.

Closely reviewed: `Lorentz`, `ProjectiveFiber`, `RankOne`, `RankZero`,
`RankZeroSimulation`, `LocalSimulation`, `UphillDirection`, `IncidenceAlgebra`,
`IncidenceScores`, `IncidenceStationarity`, `IncidenceRank`, `GramLift`,
`FrameRealization`, `ResidualClosure`, `ResidualCoordinates`, `Purification`,
`Assembly`, and `Targets`. The first steps of arbitrary-output extremality and
the binary-party cone-circuit reduction were only interface-reviewed here.

## Claim and model

The advertised main equality is equality of the ordinary shared-randomness
convex hulls of complex two-qubit POVM and PVM strategy images, with two inputs
per party and arbitrary finite, input-dependent output alphabets. The source
does not replace this with raw-image equality, same-state simulation, or a
locality assertion. The four-part `MainClaims` definition keeps the one-input
equality, universal two-input equality, physical PVM Bell bound, and explicit
strict separation distinct.

## Rank one: mechanism and necessary boundary hypotheses

The map is

`phi(x) = (x2(x0+x3), x3(x0+x2), x2(x1+x3), x3(x1+x2))`.

The proposed projective injectivity proof covers the exceptional planes
`x2=0`, `x3=0`, `x0=x1`, and `x2=x3` before using the generic inverse. It first
shows the second point lies on the same exceptional plane, then uses a
homogeneous inverse whose reconstruction scalar is proved nonzero. In the
remaining case the generic scalar is nonzero by the four explicit case
exclusions. The rank-one stationarity argument then permits only one nonzero
image row among distinct transformed source rays; a strictly positive weight
cannot annihilate that row.

**Concrete negative control:** strict metric inequalities cannot simply be
dropped from projective injectivity. If `d=0`, take
`x=(0,1,0,1)` and `z=(0,2,0,1)`. Both satisfy the displayed null polynomial for
every `a,b,c`; their nonzero images are `(0,0,0,1)` and `(0,0,0,2)`, respectively,
but the sources are not proportional. This is **not** a counterexample to
`projective_fiber_injective`, which requires `d>0`. It demonstrates why boundary
strata must be removed by the physical support reduction before invoking this
theorem. The source's parameter construction derives the strict inequalities
from distinct future null rays in an invertible Alice frame.

`SameRay` allows negative as well as positive nonzero scale, so there is no
unjustified sign restriction hidden in the rank-one conclusion.

## Rank zero: orientation, scale and labels

The base-locus implication is valid even without strict metric inequalities:
when `x2=x3=0`, nullness forces `x0*x1=0`; the other branches follow directly
from the four product equations defining `phi=0`. Thus only the five specified
projective lines survive.

Invertibility makes the assignment of five source rays to those five lines a
permutation. The unique circuit has two positive and three negative entries.
Future orientation forces all ray scales positive, excluding sign reversal by
the unequal partition sizes. The common circuit coefficient then forces one
common scale; normalization fixes it to one. The separate label reconstruction
preserves both partitions and the padded binary zero label.

**Concrete negative control:** future orientation is essential to this
rigidity statement. Let `a=b=c=d=1/6`, and let the columns of `T` be
`-6*r2, 6*r1, -6*r0, 6*r3`, where `r0,...,r3` are the standard basis and
`r4=r0+r1-r2-r3`. Then `T` is invertible, every transformed ray is a null base
ray, and `timeFunctional(T*unitVector)=1`. However `T*r0=-6*r2` and
`T*r2=-6*r0`, so normalized positive ray-permutation rigidity fails.
Precisely the future-orientation premise fails for these two rays. The source
derives that premise from physical frame positivity.

The transport simulator uses one common distribution over complete
deterministic input assignments. It does not choose independent decompositions
for the four input pairs. Its conclusion is membership in the actual PVM hull,
using identity and zero projectors. Its symmetric capacity assumptions include
zero capacities, so no strict-positive-capacity condition is silently needed.

## High rank: dimension, normalization and finite score gap

For rank at least two, the kernel of the five-to-four row map has dimension at
most three. A rank-one endomorphism `W(y)=v*(z·y)` has a strictly positive
weighted second form for every nonzero `z`, provided `B(v,v)>0` and all five
weights are positive. Four coordinates of `z` and at most three homogeneous
compatibility constraints supply a nonzero choice. The construction obtains
`B(v,v)=1` from `v=Y^-1*unitVector` and the metric normalization; no extra
unsupported inertia theorem is required.

The correction by a scalar identity fixes the **full** mass derivative,
including the metric variation. Its cross term vanishes because the positive
multiplier vector belongs to the same compatibility kernel; nullness kills its
pure radial term. Thus the correction does not spend an extra positive
dimension or change the positive second form.

The exact identity

`F(G'Y') - F(GY) = sum_j lambda_j * (deltaY*r_j)^T G' (deltaY*r_j)`

follows by expanding the new null constraints, using both stationary
identities and equal normalization. The sign is consistent with maximizing the
Bell functional. Since the quotient by `t^2` tends to a positive number, a
once-differentiable feasible curve suffices; a twice-differentiable curve is not
needed. The source invokes a submersion theorem to integrate the tangent,
rather than inferring a feasible curve solely from a formal tangent.

## Physical bridge and strict multiplier positivity

The derivative of `E -> E^T J E` has right inverse
`H -> (1/2) J E^-T H` for symmetric `H`. Direct substitution verifies both
halves of its symmetrized derivative. A continuous local Gram lift preserves
the strict future and timelike inequalities. `FrameRealization` then performs
pointwise positive normalization and two-qubit purification, so the local
incidence table has the required actual physical interpretation.

The purification formula retains the Bob transpose:
`Tr(rho_C (M tensor N)) = Tr(M C N^T C*)`. This permits realization of a full
qubit assemblage with a pure two-qubit state even when the original state was
mixed; it is not claiming same-measurement purification of every mixed state.

Positive multipliers are derived from the Bell gap to actual deterministic
replacement strategies. Each replacement resets a whole input and is already
proved to lie in the PVM hull. The strict separator supplies a strict gap and
future timelike pairing supplies a positive denominator. No positivity oracle
or local-duality assumption appears in the residual theorem's signature.

## Remaining verification gap

The full arbitrary-output reduction, compactness/extreme-point extraction,
cone-circuit decomposition, all calculus API elaborations and all physical
matrix proofs still require a successful compiler run and axiom audit.
This report does not independently discharge those obligations. It also does
not compare every theorem of the PDF line by line with a checked declaration.
The strongest result here is an independent source-level validation of the
central rank-case mechanisms and concrete falsification controls establishing
the importance of their boundary hypotheses.

## Compiler checkpoint: rank-one chain

Timestamp: 2026-09-11T01:51:22Z.

Following the source review, the parent installed the pinned Lean 4.19.0 and
Mathlib toolchain. This reviewer then repaired and successfully compiled
`Bell.Lorentz`, `Bell.ProjectiveFiber`, and `Bell.RankOne`. Bounded rank-one
formalization repair completion: 100%; full-paper completion remains a separate
project-wide estimate. The main changes are narrow imports, reliable
evaluation of finite vector literals, explicit finite-index goals before
arithmetic automation, and a real scalar type annotation in the homogeneous
inverse helper. No mathematical premises were weakened and no axiom or `sorry`
was added.

`RankOneAxiomCheck.lean` checks the actual dependency sets of
`projective_fiber_injective`, `rank_one_positive_stationarity_impossible`, and
`transformed_rank_one_obstruction`. Each reports exactly `propext`,
`Classical.choice`, and `Quot.sound`; see `rank_one_axioms.log`. Successful
build output is retained in `lorentz_build.log`, `projective_fiber_build.log`,
and `rank_one_build.log`. This upgrades the rank-one chain beyond the earlier
manual-review status but does not certify the unfinished imported physical
reduction and final assembly.

## Compiler checkpoint: rank zero and a corrected missing helper premise

Timestamp: 2026-09-11T02:03:37Z. Bounded rank-zero repair completion: 100%.
`Bell.RankZero` and `Bell.RankZeroSimulation` now compile. The actual axiom
checks for `rank_zero_normalized_rigidity`, `metricTable_mem_convexPVM`, and
`rank_zero_transformed_table_mem` report exactly `propext`, `Classical.choice`,
and `Quot.sound`; see `RankZeroAxiomCheck.lean` and `rank_zero_axioms.log`.

Compilation exposed one important defect missed by the earlier informal read:
the intended block-preservation hypothesis `hπ` was mentioned in the proof of
`ternaryLabelMap_injective` but absent from its elaborated declaration type.
Lean section variables are not automatically included merely because a later
proof tries to reference them. Since `ternaryLabelMap` itself does not need
`hπ` to be defined, the original helper incorrectly attempted unrestricted
injectivity.

That unrestricted helper is false: for the permutation swapping coefficient
indices `0` and `3`, both ternary label `0` (coefficient index `2`) and ternary
label `1` (coefficient index `3`) map to label `0` after truncated subtraction
by `2`. The repair uses `include hπ in` to state the necessary partition
preservation premise explicitly. All existing callers already supply it from
the proved rigidity theorem. The top-level rank-zero simulation statement is
unchanged, and its successful axiom check verifies that this premise is
discharged rather than assumed externally. Thus this is a corrected helper
statement, not a counterexample to the paper's rank-zero conclusion.

Other repairs concern finite-index type inference and normalization, an
identity ring-homomorphism in a linearity proof, and restricting a circuit
rewrite to its intended side. Build logs are `rank_zero_build.log` and
`rank_zero_simulation_build.log`.

## Compiler checkpoint: combined incidence rank analysis

Timestamp: 2026-09-11T02:06:52Z. Bounded `IncidenceRank` repair completion: 100%.
The production `Bell.IncidenceRank` build succeeded after its production
dependencies were repaired by the team. The full normalized positive tangent,
high-rank local-maximum exclusion, rank-one exclusion and rank-zero block
simulation now elaborate in one module. Its statements were preserved.
Repairs concerned current finite-basis APIs, coercions of linear maps,
matrix-vector rewrite direction, product projections, and an ambiguous
universe on the one-element basis index. The successful output is retained in
`incidence_rank_build.log`; the global dependency/axiom audit remains the final
project-wide certification step.
