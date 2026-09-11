# Focused mathematical-interface review

**Scope:** a manual reading of selected source arguments plus new independent
exact tests of their formulas and interfaces. This is not an exhaustive referee
review, Lean elaboration, or a certified source-to-manuscript correspondence.
All mathematical Lean source modules and statement-contract source are unchanged
from the incoming preflight ZIP.

## Observational model and shared randomness

Inspected `Quantum`, `Expectation`, `ClassicalProduct`, `StrategyMaps`,
`SmallOutputEncoding`, `ResidualStrategy`, and the final assembly interfaces.
The definitions use complex qubit operators, positive trace-one joint states,
normalized local measurements, and ordinary convex hulls of complete physical
strategy ranges. The intended conclusion is not raw-image equality, same-state
simulation, or a claim that all two-input quantum correlations are local.

New tests include a genuinely complex PVM strategy with exact CHSH score 14/5,
and whole-strategy finite mixtures with input-dependent output alphabets.
Identity/zero projectors, repeated-label merging, deterministic maps, and zero
branch weights are included. A PR-box scope control demonstrates why choosing
an unrelated local decomposition separately for each input pair does not
establish a common local mixture. It is deliberately not a quantum fixture.

An additional interface control distinguishes **zero effect padding** from
**zero coefficient padding**. A negative Bell functional can gain an artificial
maximum if an unused label receives a free zero coefficient. The inspected
residual path correctly pulls the entire Bell functional back through the
coarsening map; no source repair was indicated. The control tests the incorrect
alternative independently, not by mutating or compiling a Lean file.

## Complex Pauli coordinates and purification

Inspected `QubitCoordinates`, `Purification`, `SteeringRepresentation`, and
`FrameRealization`. The imaginary Pauli coordinate is retained, and the
coefficient-state identity contains Bob's transpose in the correct position.
New tests use six distinct rational genuinely complex pure state/measurement
fixtures with invertible effect frames and different Schmidt spectra.

Direct joint 4-by-4 Born traces are compared to full padded coefficient tables,
future/null constraints, normalization, local-unitary covariance, complete
complex conjugation, and party swapping. Formula controls reject removing the
transpose and replacing it by an adjoint. These finite examples do not prove
all singular-state or purification cases.

## Extremality, common spans, and active labels

Inspected `MeasurementGeometry`, `ExtremeMeasurement`, and
`CommonSpanFiltering`. The key two-sided filtering identity must use the changed
state normalizations as branch probabilities, and one operator must work for
both local inputs. The new checker constructs three exact nontrivial complex
filter examples, validates each physical branch, and reconstructs the complete
behavior using the same two weights throughout. Equal half/half weighting is
rejected when the true branch weights differ.

These checks do not establish compactness, extreme-point existence, every
support-preserving perturbation, or the universal support-count reduction.
Those long quantified arguments remain uncompiled source.

## Binary-party cone circuits

Inspected `ConeCompression`, `ConeCircuits`, `CircuitRealization`, and
`BinaryParty`. The new enumeration completely checks the vertices of four
explicit finite rational balanced-ray polytopes. It includes duplicate
geometric rays under different labels, collinear/rank-one sums, and the
parallel-axis boundary. Every enumerated vertex is realized through the
appropriate nonsingular whitening or singular collinearity identities.

The resulting 31 vertices are an exhaustive enumeration **only of those four
finite input sets**, not all possible Lorentz cones or physical measurements.
The arbitrary-support circuit extraction and universal convex decomposition
arguments are still Lean proof attempts, not validated by this finite catalogue.

## Incidence normalization and coupled directions

Inspected `GramLift`, `IncidenceAlgebra`, `IncidenceDifferential`,
`IncidenceRank`, `ImplicitCurve`, and `ResidualClosure`. In polynomial coordinates
`P=gY`, the mass derivative contains **both** `g δY` and `δg Y`. Independent exact
checks verify the full derivative, explicit derivative right inverses, radial
normalization, general symmetric Gram directions, and finite score gaps. Controls
reject dropping the metric term, reversing a gap sign, and omitting the
Minkowski matrix from the Gram right inverse.

The strongest added fixture is the explicit physical rank-three coupled saddle
in `RANK_THREE_STRESS_TEST.md`. Its direct Born score strictly increases along a
certified real interval even though the fixed-measurement state problem and all
four single-measurement optimization problems are separately optimal. This
checks the intended sign and coupled-direction mechanism without relying on a
numerical optimizer to certify the result. It is not a POVM/PVM separation.

## Outstanding verification boundary

No new counterexample or mathematical blocker was identified in the inspected
interfaces. This statement is limited to the work above. In particular:

- The entire Lean development, imported API uses, and all statement contracts
  still require elaboration, kernel checking, and a real dependency audit.
- The all-points rank-one projective-fiber obstruction was not independently
  re-proved in this pass. Neither was the full arbitrary-input rank-zero
  reconstruction.
- Finite examples and algebraic identities do not certify the quantifiers,
  openness arguments, limit arguments, Gram-lift construction, or the actual
  application of the implicit-function theorem.
- No new certificate establishes that every top-level declaration has the
  intended mathematical meaning. The existing independent Lean statement
  contracts are useful, but remain uncompiled too.

The new tests reduce the risk of specific convention and algebra mistakes.
They do not replace the first real compiler run or justify describing the paper
as formally verified.
