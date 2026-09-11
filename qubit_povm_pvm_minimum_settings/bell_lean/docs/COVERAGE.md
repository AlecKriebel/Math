# Claim-by-claim coverage register — continuation v0.2.0

**Every Lean entry below is uncompiled proof source. None is kernel-verified.**
“Unconditional” describes the written theorem's explicit assumptions, not an
executed proof result. “Full algebraic source” does not mean the physical
incidence bridge has been proved.

The paper correspondence is to the retained 34-page July 2026 PDF, matching the
original v1.1.0 release and the DOI's listed PDF checksum.

## Main endpoints

| Endpoint | Exact source declaration / state |
|---|---|
| Witness attains L₀ | `Bell.witness_value`; written physical construction, exact regression checks, uncompiled |
| Global PVM bound | `Bell.projective_global_upper_bound`; now an unconditional physical source attempt via the stronger 289/10 SOS, uncompiled |
| Strict 3×2 convexified separation | `Bell.three_by_two_separation`; unconditional source attempt, uncompiled |
| One-input equality | `Bell.one_input_equality`; unconditional source attempt, uncompiled |
| Universal two-input equality | `Bell.UniversalTwoInputEquality` remains a proposition with no unconditional proof-source derivation |
| Minimum input architecture | `Bell.minimum_inputs_of_two_input_equality` still explicitly takes the missing equality as a premise |
| Complete main conjunction | `Bell.main_claims_of_two_input_equality` is conditional, not a proof of `MainClaims` |
| Appendix B physical attainment | `Bell.StrengthenedAttainment` remains unresolved; scalar formulas do not establish attainment |

## Modules and exact boundaries

| Module | Written content | Boundary still relevant |
|---|---|---|
| `Quantum` | Complex fixed-qubit states/effects/measurements, Born behaviors, separate raw/hull sets, Gram positivity, PVM-to-POVM inclusions | No compactness or general dimension-embedding theorem |
| `Expectation` | General tensor algebra, positive state expectations from PSD matrices, Born nonnegativity/normalization/nonsignaling | No duality or smooth incidence reconstruction |
| `Convexity` | Finite-mixture inequality, actual convex-hull linear bound, scalar filtering identity, binary spectral weights | Not full physical filtering, compact separation, or stochastic-postprocessing closure |
| `Scalars` | Original strict gap, deficit/robustness identities and inequalities, scalar upper bound, strengthened radical comparison/family bound | Original deficit hypotheses are not derived from all states; superseded as the chosen separation route by the SOS |
| `Witness` | Actual complex-qubit explicit strategy, normalization/positivity, exact Born probabilities/correlations/value and membership | Not Appendix B's nonmaximal-entanglement construction |
| `Discrimination` | Ideal score operators, dual PSD slacks, complementary slackness, arbitrary ideal POVM upper bound and attainment | Fixed ideal operators, not general POVM strong duality |
| `ProjectionSupport` | Complex 2×2 Cayley–Hamilton, zero effect in every ternary qubit PVM, projection-to-Hermitian-involution bridge | Not the extremal POVM rank-square theorem |
| `SOSAlgebra` | Generic rational LDL-to-operator-squares identity and positive expectation evaluation | Needs the explicit coefficient identity supplied by the certificate module |
| `SOSCertificate` | Literal rational 12×12 Gram/LDL data and positive-pivot proof attempts | Coefficient proof bodies uncompiled; independent integer/rational checks have passed |
| `ProjectiveSOS` | Universal involution operator identities for all three possible auxiliary support pairs | Physical state/support/Born mapping is in `ProjectiveBound` |
| `ProjectiveBound` | Full actual-PVM source path to 289/10, paper U, convexified separation and margin >1/50 | Uncompiled; it does not use or prove two-input equality |
| `Transportation` | General bounded three-label flow, capacities and exact row/column equations, including endpoints | Physical table identification is separate |
| `LocalSimulation` | Actual identity/zero PVM strategies, complete-strategy finite mixtures, general transportation-table realization | Does not derive a general physical residual point's rank-zero form |
| `ClassicalProduct` | Arbitrary finite dependent response assignments; common mixture weights; zero-marginal handling | A general classical table calculation, linked to Born behaviors in `OneInput` |
| `OneInput` | Physical one-input equality, either party, zero input counts, arbitrary declared finite output counts | Not the one-*binary*-party two-input theorem |
| `Lorentz` | Five-ray algebra, metric/null polynomials, generic inverse, base-locus algebra, Hessian square-completion polynomial | Not the physical Pauli/steering coordinate representation or differentiation theorem |
| `ProjectiveFiber` | Full generic/exceptional projective injectivity source via four explicit quadratic inverse maps | Uncompiled; strict coefficient hypotheses are not yet obtained from every physical point |
| `RankOne` | Distinct null-source rays plus the projective-fiber source theorem rule out positive rank-one stationarity | Metric Jacobian identification and physical multiplier positivity missing |
| `RankZero` | Positive ray assignment, finite permutation, circuit scale/partition, normalization, metric-to-transport identification | General physical point-to-algebraic-data bridge missing |
| `Relabeling` | Actual output permutations of PVM strategies and convex hulls | Not arbitrary many-to-one stochastic output maps |
| `RankZeroSimulation` | Correct padded binary/ternary permutations and actual PVM-hull membership for the transformed algebraic table | Requires the stated normalized null/base/future hypotheses; does not assume their physical derivation |
| `UphillDirection` | Explicit rank-one positive family, at most three linear compatibilities, nonzero kernel, normalization preserving q | Must derive physical bilinear/compatibility hypotheses and integrate the resulting tangent |
| `Targets` | Faithful proposition definitions and original explicitly conditional assemblies | Definitions are not proofs |
| `Assembly` | New assembly with the remaining universal-equality premise explicit | No unconditional `MainClaims` proof |

## Outstanding foundations and physical bridges

The missing two-input route is not just the final case split. It still needs:

1. Compact strategy and hull geometry, attainment, extreme exposed maximizers,
   stochastic postprocessing, and the support-function converse.
2. The one-binary-party Lorentz cone circuit simulation and all degeneracies;
   physical common-span filtering and extremal binary/ternary reduction.
3. The actual complex Pauli/steering-to-incidence representation, inverse-metric
   factors, Lorentz signature, strict domain, local physical reconstruction,
   independent differentials and smooth two-sided physical curves.
4. Finite POVM strong duality, normalization multiplier identification, and
   strict positivity through deterministic replacement.
5. Differentiation of the incidence inverse metric, identification of q,
   physical compatibility dimension/basis and normalization, then the analytic
   contradiction between an uphill physical curve and local maximality.
6. The links from ranks one and zero of the physical metric differential to
   the source modules' explicit algebraic hypotheses, including output embedding
   back into arbitrary declared alphabets.
7. Unconditional universal equality and minimum-input assembly, followed by
   the entire build and axiom audit.

No axiom or assumed `MainClaims` record is used to skip this list. The conditional
assembly makes the remaining top-level premise obvious, but that premise is the
substantial universal theorem itself, not a minor bookkeeping lemma.

## Evidence discipline

`reports/declarations.json` is a static source inventory. The polynomial checks
verify identities using exact arithmetic; the enumerations verify their actual
finite grids. `reports/kernel_report.json` records that Lean was not invoked.
A future successful subset build would certify the written declarations only.
The model-fidelity review remains important even after compilation: actual
complex qubits, shared randomness over complete strategies, all declared labels,
no ancilla, and the distinction between raw images and convex hulls must stay intact.
