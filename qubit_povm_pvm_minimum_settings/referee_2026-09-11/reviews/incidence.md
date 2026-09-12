# Independent adversarial referee report: incidence and residual closure

Date: 2026-09-12 UTC (review requested 2026-09-11 local time).
Scope: primary manuscript §§5–9 and corresponding appendices; actual source in `bell_lean/Bell/ResidualCoordinates.lean`, `ResidualEncoding.lean`, `FrameRealization.lean`, `GramLift.lean`, `IncidenceAlgebra.lean`, `IncidenceDifferential.lean`, `IncidenceRank.lean`, `IncidenceStationarity.lean`, `IncidenceScores.lean`, `ImplicitCurve.lean`, `FiniteLinearAlgebra.lean`, `UphillDirection.lean`, `RankOne.lean`, `RankZero.lean`, `RankZeroSimulation.lean`, `ProjectiveFiber.lean`, and `ResidualClosure.lean`. Also inspected the connecting `ResidualStrategy.lean`, `Lorentz.lean`, `DeterministicGap.lean`, and simulator theorem interfaces. Parent review separately rebuilds and audits trust/dependencies.

**Verdict:** I found no remaining central proof gap, circular optimization premise, unhandled rank branch, or generic-position restriction in the current incidence-to-residual-closure chain. The source proves the necessary residual exclusion with an alternative analytic argument. It does **not** literally formalize every mathematical assertion or every named intermediate theorem of the primary paper. There is also a manuscript domain-equivalence ambiguity that admits an exact counterexample under its unqualified reading; the Lean proof does not make that invalid inference.

## 1. Concrete finding: qualify the strict-domain equivalence

**Manuscript location:** `paper/main.tex:1036–1049`, Definition “Strict residual domain.” It requires signature `(1,3)` and then says, “Equivalently for this normal form, all products between distinct rays are positive.”

Interpreted as an equivalence replacing *all* the preceding conditions, this is false. Set

\[
a=d=6/25,\quad b=c=3/100,\quad e=1/25.
\]

All four sums `a+b`, `c+d`, `a+c`, `b+d` equal `27/100 < 1/2`; all five parameters are positive. In the fixed five-ray circuit the ten distinct-ray products, in lexicographic pair order, are

\[
1/2,6/25,3/100,23/100,3/100,6/25,23/100,1/25,23/100,23/100.
\]

All five rays are null. Nevertheless, for

\[
u=(1,1,0,0),\qquad v=(2,-2,5,-5),
\]

one has

\[
u^Tgu=1,\quad u^Tgv=0,\quad v^Tgv=12/5,
\quad (su+tv)^Tg(su+tv)=s^2+(12/5)t^2.
\]

The form therefore has a two-dimensional positive subspace and cannot have signature `(1,3)`.

This is not a refutation of the intended conditional equivalence: **assuming Lorentz signature already**, positive pairings of distinct null rays express a common cone orientation. The definition can be repaired by saying “Under the signature condition, the common-cone and distinctness requirements are equivalent to positivity of all distinct-ray products.” Its current wording can be read either way and should be clarified.

The companion `computations/StrictDomainCounterexample.lean` imports Mathlib only and proves the scalar inequalities, circuit, five null equations, all ten positive pairings, and positive-plane identity over exact reals; `evidence/strict_domain_counterexample.log` records the compilation and axiom outputs. The geometric inference excluding one-positive-direction signature is stated above, rather than disguised as a formal inertia theorem.

**No impact on the audited equality route:** `Bell/Lorentz.lean:97–111` defines `StrictParameters` using precisely scalar inequalities, with a comment at lines 13–17 explicitly warning that this does not assert Lorentz signature. `ResidualClosure.lean:54–68` independently requires a real invertible frame `E` with `EᵀJE = g`, normalization, and concrete frame positivity. The source never reconstructs a physical frame from scalar inequalities alone. `ResidualCoordinates.lean:93–110` derives those inequalities from an actual positive invertible frame, in the valid direction.

## 2. What the current residual exclusion actually proves

`ResidualClosure.no_strict_residual_maximum` (`ResidualClosure.lean:54–105`) is a contradiction theorem about an **actual global raw-POVM maximizer** in a concrete residual frame whose score is strictly above **every element of the complete convex PVM set**. Its hypotheses do not contain stationarity, a positive-multiplier oracle, tangent integrability, or an assumed no-uphill conclusion.

The proof obtains those facts as follows:

1. `GramLift.physical_maximum_is_incidence_maximum` (`GramLift.lean:189–202`) derives a constrained local maximum from the global maximum, using `eventually_feasible_mem_rawPOVM` (`:161–185`). The latter proves actual local realizability, not just formal satisfaction of the equations.
2. `IncidenceStationarity.exists_incidence_stationarity` (`IncidenceStationarity.lean:161–171`) derives both stationarity identities. Its Lagrange argument uses the proved surjectivity of the actual constraint derivative. The abnormal-objective-multiplier case is explicitly excluded (`:20–44`).
3. `IncidenceScores.multipliers_positive_from_physical_separator` (`IncidenceScores.lean:110–134`) derives positive multipliers from deterministic replacements that belong to the physical PVM hull. It does not assume the gaps independently. The exact identity behind this step is `F(I)-F(reset_j)=2 λ_j B(r_j,u)` (`DeterministicGap.lean:81–90`). `ResidualClosure.frame_future_pairing` (`:18–40`) supplies the strictly positive denominator from null/timelike physical geometry.
4. Rank zero is dispatched to membership in the same labelled PVM hull; rank one contradicts positive stationarity via the full projective-fiber theorem; all remaining ranks are at least two and contradict the proved constrained local maximum (`ResidualClosure.lean:96–105`). The split is exhaustive for natural-number rank and does not need an additional assumed rank bound.

The upstream geometric premises are not silently imposed as genericity conditions. `ResidualEncoding.encoded_frame_invertible` (`ResidualEncoding.lean:178–216`) derives invertibility from effect independence, the two/three active-support counts and common-span filtering. `ResidualStrategy.no_strict_extreme_binary_ternary` (`ResidualStrategy.lean:133ff`) explicitly constructs both frames, preserves the original alphabets through `paddingMap`, and transports the maximum and strict-separator hypotheses. The separate reduction referee must still validate the general-strategy-to-extreme-residual route; that is outside this report's main scope.

## 3. Analytic and physical stress tests

### Coordinate conventions and physical reconstruction

The formalization uses `z=(g,Y)` with `Y=g⁻¹P`, rather than the paper's `(P,g)`. `probabilityBlock z = gY` and the six constraints are defined at `IncidenceAlgebra.lean:271–285`. This is an honest change of variables on invertible `g`; invertibility of both factors is derived from invertibility of `P` (`IncidenceStationarity.lean:124–136`).

`FrameRealization.lean:111–142` retains the factor `1/2` in the steering frame and proves the full trace/probability identity. Its `UnnormalizedAssemblage` is normalized by an explicit inverse congruence (`:49–91`) and purified into a complex two-qubit strategy. It is not a larger-dimensional model. `frame_table_mem_rawPOVM` (`:246–259`) returns membership in the actual raw POVM set and proves every declared table entry, including the unused third binary output.

The Gram lift has an explicit derivative right inverse (`GramLift.lean:107–132`), a local continuous lift (`:137–157`), and an open positive-frame set (`FrameRealization.lean:144–163`). Reconstruction is pointwise; the proof needs continuity of the local coordinates, not a differentiable purification. No positive lower bound on every **joint** probability is assumed, so zero joint probabilities do not create an artificial boundary exclusion.

### Derivative surjectivity, compatibility, and normalization

`IncidenceDifferential.lean:109–156` proves actual strict derivatives. `nullDerivative_seed_preimage` (`:172–187`) constructs preimages of arbitrary five null derivatives, and the radial direction `(0,Y)` changes mass by one while preserving the null derivatives (`:190–202`). These yield surjectivity onto all six constraints (`:205–219`), including normalization.

`FiniteLinearAlgebra.lean:104–149` proves the annihilator criterion and then solves the metric increment from the genuine transpose-kernel compatibility equations. It does not move the central problem into an assumed solvability premise.

`IncidenceRank.exists_positive_normalized_tangent` (`:85–131`) first finds a compatible metric increment and then subtracts the **full** mass derivative, which includes the metric term. The shift preserves the positive quadratic score because the multiplier lies in the actual kernel. This avoids the easy mistake of normalizing only `W` while forgetting the `H` contribution.

`ImplicitCurve.exists_level_curve` (`:20–42`) constructs a two-sided, once-differentiable level-set curve from the proved strict derivative. `polynomial_score_gap` (`IncidenceAlgebra.lean:297–314`) and `quadratic_gap_limit`/`eventually_score_improvement` (`ImplicitCurve.lean:55–101`) prove actual strict improvement at sufficiently small nonzero parameters. The final contradiction with local maximality uses a nontrivial punctured neighborhood (`:106–128`).

### Exceptional fibers and rank zero

`ProjectiveFiber.projective_fiber_injective` (`:488–535`) handles, in order, `x₂=0`, `x₃=0`, `x₀=x₁`, `x₂=x₃`, and the generic complement. Each exceptional branch proves that a projectively equal target comes from the same source plane, then uses an explicit homogeneous inverse with its weight proved nonzero. Intersections are included by the ordered case split. No same-plane or generic-position premise is smuggled into the final theorem.

The rank-one assembly (`IncidenceRank.lean:166–195`) obtains its nonzero image generator from rank one, not as an extra assumption. Zero rows are retained, and positive stationarity excludes exactly-one-live-row configurations (`RankOne.lean:40–77`).

Rank zero preserves the five-ray permutation explicitly. `RankZero.lean:127–199` proves the unequal-cardinality sign argument; `:201–230` proves that normalization fixes the common positive scale to one. `RankZeroSimulation.lean:102–158` converts the ray permutation into per-input output permutations, fixes the padded zero binary label, and proves membership in the **same** labelled physical PVM hull. The transport table is identified entrywise before invoking the simulator (`RankZero.lean:248–275`).

## 4. Manuscript coverage: equivalent proof versus literal formalization

| Manuscript assertion | Source coverage and limit |
|---|---|
| §5 normal metric, circuit, full probability table | Formalized by `Lorentz`, `ResidualCoordinates`, `ResidualEncoding`, `ResidualStrategy`, and `IncidenceScores`; actual frame construction is checked. |
| §5 Lorentz representation lemma's displayed `L_ΞᵀJL_Ξ=|det Ξ|²J` and `Pᵀg⁻¹P=4|det Ξ|²h` | The required physical encoding/nullness/invertibility is proved by a different steering construction. I did not find named formal theorems asserting these entire displayed matrix identities. Do not claim literal coverage merely from related determinant/null lemmas. |
| §6 local physical completeness | The exact consequence required for optimization—every sufficiently nearby feasible table lies in raw POVM—is formalized. The source does not state that the reconstructed strategy is a smoothly varying genuine residual strategy. |
| §6 smooth real 14-dimensional manifold | The constraints are proved smooth, their derivative surjective, and each tangent has a C¹ feasible curve. There is no packaged 14-dimensional manifold theorem in the inspected source. The standard mathematical consequence is not itself a checked exported statement. |
| §7 multiplier existence | Derived from Lagrange multipliers and regularity. Uniqueness of all six multipliers is not separately exported here. |
| §7 finite POVM duality and determinant-pullback/KKT lemma; Appendix E | Bypassed by the deterministic-gap proof. General dual attainment and the paper's complete KKT identity are not formalized by the incidence source. |
| §7 strict multiplier positivity | Fully proved for the relevant physical strict separator, using the exact replacement gap. |
| §8 full Hessian statement and inertia `(4,12)`; Appendix F | Universal bilinear square completion is formalized (`Lorentz.lean:316–323`), but not its complete identification with the second derivative of inverse matrices or the full ambient inertia. The alternative proof uses the exact finite polynomial gap and an explicit positive rank-one family (`UphillDirection.lean:129–140`). |
| §8 Fredholm compatibility | Proved directly via annihilators and actual metric increments. Full `dim H_K=16-k` is unnecessary and not separately asserted. |
| §9 rank-one projective fiber theorem; Appendix G | Full injectivity including every exceptional divisor is formalized. Generic algebraic identities and base-locus classification are also proved, not sampled. |
| §9 rank-zero rigidity and simulation; Appendix H | Proved with permutation and labels retained and exact transport membership. |
| §9 residual obstruction required for universal equality | Closed theorem `no_strict_residual_maximum`, with physical and analytic hypotheses derived downstream/upstream as described above. Global equality additionally requires the other referees' model, compactness, separation and residual-reduction checks. |

Thus “certifies the universal equality using a checked alternative proof” is compatible with the inspected source. “Proves all the math in the primary paper” is too broad unless the manuscript/coverage contract explicitly excludes or marks the bypassed intermediate assertions.

## 5. Verification status and remaining gap

This was a source-semantic review with adversarial analysis of the definitions and proof interfaces, not reliance on previous certification summaries. No `sorry`, `admit`, custom `axiom`, or unsafe shortcut was observed in the audited incidence family. Parent review owns the full clean build and transitive axiom audit. The standalone domain counterexample is independently compiled from Mathlib-only imports; its exact rational checks require no sampled data.

Final checkpoint (2026-09-12T03:59:51Z): the companion Mathlib-only Lean probe compiled successfully with exit code 0; the printed theorem dependencies are only `propext`, `Classical.choice`, and `Quot.sound`. Best-guess completion toward this assigned incidence referee task: **100%**. Strongest verified mathematical finding: the current source contains a closed physical residual-maximizer contradiction, while unqualified replacement of Lorentz signature by pairwise positivity is disproved. Remaining substantive scope gap: formal coverage of the manuscript-only intermediate identities/manifold/inertia/duality statements, not a discovered gap in the alternative equality proof.
