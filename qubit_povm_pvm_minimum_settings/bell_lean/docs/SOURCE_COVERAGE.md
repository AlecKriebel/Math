> **Historical cloud-stage document.** Statements below about missing compilation or unfinished targets describe the incoming archive. Current local verification and the precise certified scope are recorded in [CERTIFICATION.md](../CERTIFICATION.md); this document is retained as research provenance.

# Source coverage — uncompiled end-to-end draft

Every entry below means **proof source present, not accepted by Lean**. This map
covers the principal theorem route and its operational/attainment consequences.
It does not claim a separate formal declaration for every prose remark or every
unused alternate proof in the paper.

| Claim or proof obligation | Source modules / principal declarations |
|---|---|
| Actual complex fixed-qubit physical model and convexification | Quantum; Expectation; Convexity; Targets |
| Original explicit attained 3×2 value | Witness; Scalars |
| Global PVM bound, support patterns, shared-randomness separation | ProjectionSupport; SOSAlgebra; SOSCertificate; ProjectiveSOS; ProjectiveBound |
| Zero-/one-input equality with finite dependent alphabets | ClassicalProduct; LocalSimulation; OneInput |
| Ordinary hull compactness, extreme maximizing behavior | EntrywiseTopology; FiniteConvexCompactness; QuantumCompactness |
| Full complex Pauli cone and inverse coordinate maps | QubitCoordinates; MeasurementGeometry |
| Exact qubit purification and mixed-state assemblages | Purification; ProductLocality; SteeringRepresentation |
| Complete-strategy input/output transformations | StrategyMaps; SmallOutputEncoding; Relabeling |
| Independent active effects and rank-one nondeterministic effects | ExtremeMeasurement |
| Common-span filtering with non-equal branch weights | CommonSpanFiltering; MeasurementSpans |
| Independent binary-PVM-party simulation | ConeCircuits; CircuitRealization; ConeCompression; BinaryParty |
| Binary/ternary padding, zero labels, frame invertibility | ResidualEncoding; ResidualStrategy |
| Physical deterministic resets and strict gap identity | DeterministicGap; DeterministicInput; IncidenceScores |
| Polynomial incidence chart and finite score identity | IncidenceAlgebra |
| Six-constraint strict derivative and explicit right inverse | IncidenceDifferential |
| Stationarity derived from actual local maxima | IncidenceStationarity |
| First-order implicit feasible curve and score improvement | ImplicitCurve |
| Local physical reconstruction by Gram lift | FrameRealization; GramLift; ResidualCoordinates |
| Projective fibers and rank-one obstruction | Lorentz; ProjectiveFiber; RankOne |
| Labelled rank-zero common PVM mixture | Transportation; RankZero; RankZeroSimulation |
| High-rank compatible normalized uphill tangent | FiniteLinearAlgebra; UphillDirection; IncidenceRank |
| Actual physical residual closure | ResidualClosure; ResidualStrategy |
| Arbitrary-output equality and minimum setting conclusion | Assembly: `two_input_convex_equality`, `main_claims`, `minimum_inputs` |
| Finite full-strategy mixture, one-binary-party consequence, Bell bounds | SimulationCorollaries |
| Stronger explicit Appendix B physical strategy | StrengthenedWitness: `strengthened_attainment` |
| Stronger-family scalar upper comparison | Scalars: `strengthened_family_bound` |

## Alternative arguments used in the source

The main PVM bound uses the inherited rational SOS certificate, which is stronger
than the paper's displayed upper bound. The multiplier step uses deterministic
physical score gaps rather than a separate semidefinite-program duality proof.
The mixed-state reduction uses exact qubit assemblage purification. The uphill
step uses a polynomial finite-gap identity and a C¹ implicit curve rather than
a second-order matrix-inverse Taylor argument. These substitutions are intended
to preserve the principal statements, not to narrow them.

## No silent assumption of universal equality

`Targets.lean` retains the original proposition definitions and conditional
helpers for compatibility. The new final theorem in `Assembly.lean` supplies
source attempts for those premises instead of accepting them as arguments.
The static signature check records the exact final headers in
`reports/source_completion/source_inventory.json`.

This is a source-level observation. It is not proof that the dependency chain
elaborates, that each tactic succeeds, or that the definitions faithfully encode
every intended physical convention. Those remain subjects of the later compiler
and mathematical review.
