# Model-value extension: source correspondence and self-audit

**Single-assistant self-audit. No independent agent or Lean kernel participated.**
The conclusions here are source inspection and exact finite evidence, not an
accepted-proof report. The baseline input is the all-dimensional archive with
SHA-256 `093043d7db11aea7d45c5896c4d16ae071184c92d4085757ef1d552b3c6f9255`.

## Statement checks

| Risk | Inspection / written connection | What remains unverified |
|---|---|---|
| Circular validity | `StrategyOn`, `CommutingOn` and `PurifiedStrategyOn` have only physical state/measurement conditions. Bell and privacy statements occur in theorem hypotheses/conclusions, not validity fields. | Lean elaboration and transitive axiom audit. |
| Restricting universal dimensions | Qq existentially quantifies arbitrary finite local types; Qqc existentially quantifies complete complex Hilbert carriers without finite dimension. The constructive `d`-dimensional witness is separate. | Size transport across larger Lean universes is not a separate endpoint. |
| Vacuous supremum | `bellSupremum` is actual real `sSup`; `bellSupremum_of_attained_bound` exhibits nonemptiness and boundedness. Every concrete value endpoint supplies a physical member. | Kernel checking of the membership/attainment chain. |
| Confusing closure with equality of models | Qqa is actual closure; sublevel-set continuity proves only the Bell bound on that closure. | No general Qqa-subset-Qqc or Qqc-closedness theorem is supplied. |
| Wrong Hilbert norm | `matrixCLM` acts on `EuclideanSpace`, using the pinned matrix/adjoint APIs. It does not identify plain coordinate functions with a Euclidean norm by assumption. | Coercions and complete-space instance elaboration. |
| Missing mixed-state bridge | The actual positive density square root is vectorized; the environment is explicit and both parties act by identity there. Full complex moments are proved equal before taking real parts. | Pinned `toContinuousLinearMap`/matrix extensionality proof details. |
| Wrong Bell normalization | Real Born coefficients are `chi(a+b)`, first-family reduced sum has no 1/d factor, and the augmentation is separate. The second family's literal lambda vector is retained. | Tactic normalization and correct rewrite API use. |
| Hidden outcome restrictions | PVM zero effects remain allowed. d>=2 is explicit where used; cyclic algebra allows d=1 with NeZero d. | No claimed support restrictions beyond those already recorded. |
| Assuming privacy | `BinaryPrivacyAt` is the property under test, quantified over all compatible finite purifications. `purifyStrategy` supplies nonvacuity. | Kernel proof of the actual post-measurement instrument equality. |
| Uniform outputs mistaken for private outputs | A new exact control has a uniform binary observed table and actual Eve success one, with nonuniform conditional Eve matrices. | Finite evidence is not a proof of all operational definitions. |
| Silent party swapping | New right-one-input strategy explicitly exchanges measurement roles, derives the entire behavior, and keeps the actual stored pure state/Eve guess. | Dependent alphabet and finite-instance elaboration. |
| General weighted-cycle spectrum assumed | Charpoly proof starts from actual Cayley-Hamilton and powers; prefix products are nonzero by the explicit weight hypothesis. | Finite-sum and polynomial coefficient API repairs may be required. |
| Default build omits an endpoint | Static dependency closure reaches all 66 source/audit files; 1,332 declarations have generated axiom queries. | Static scanning is not Lean parsing or kernel analysis. |
| Negative control silently skipped | New AST registry checks all 15 control paths and their expected outcomes; mutation tests reject omissions and wrong flags. | Controls have not actually run in Lean. |

## Source repairs made during inspection

These affect only newly authored source, not the earlier mathematical modules.

- Reduced the new real-behavior module's imports to the bound modules; explicit
  witness imports occur in the value assembly. Some second-family coefficient
  infrastructure already imports shared constructive helpers, so no new claim
  that the entire value-wrapper closure is witness-free is made. The earlier
  universal first-bound separation checks remain unchanged and pass.
- Replaced overloaded `rw` use on repeated score occurrences with `simp only`
  where all occurrences must be converted to the actual physical score.
- Made square-root nonzero hypotheses explicit in the binary SOS field arithmetic.
- Used the actual pinned `as_sum_range_C_mul_X_pow` polynomial API rather than a
  similarly named newer variant absent from the pinned revision.
- Added explicit normalization and the complex moment identity before finite
  model inclusion; there is no assumed isometry/embedding field.
- Updated the offline runner's old scope message: literal three-model values
  are now written, while general model inclusion and selected appendices remain.
- Added a registry audit and mutation tests covering unregistered validation
  files, omitted negative commands, wrong expected success/failure and a hidden
  placeholder in a control.

No manuscript error was established in this continuation. These are inspection
repairs to uncompiled candidates; they do not imply that all source problems
have been found.

## Executed evidence and its limitations

`model_bridge_preflight.json`: 9,906 Gaussian-rational checks and 37 negative
controls. The sample includes local dimensions (1,1), (1,4), (2,2), (2,3),
rank-one/rank-two/full-rank densities, non-real matrix moments and zero outcome
projectors. The second scalar-functional check uses arbitrary test coefficients,
**not** a new independent derivation of the manuscript lambda normalization;
that normalization remains covered by the retained cyclotomic test suite.

`model_cycle_charpoly_preflight.json`: 175 exact checks and 19 controls in d=1..7.
The determinant is expanded over all permutations, unlike the Lean source's
Cayley-Hamilton route. This shares Gaussian-rational arithmetic with the prior
new script and was written by the same assistant.

The original 392 d4, 12 first-SOS, 8 alternative word-reduction and 3,040 distinct
general checks with 38 controls passed on rerun. The two general batches each
repeat the one-input/binary checks; reported distinct totals deduplicate those
names. The latest machinery run passed 34 tests using mocked processes where
compiler output is tested. It did not launch Lean even for a smoke test.

These tests do not establish continuity, closure or any supremum theorem.
No numerical/finite certificate is imported as Lean evidence.

## Offline risk and repair instructions

Expect possible substantial repairs in dependent existential model instances,
Euclidean/continuous-linear-map coercions, noncommutative expression normalization,
CFC/spectral support lemmas inherited from the earlier source, operator-valued
binary privacy, and polynomial coefficient extraction. These are anticipated
risks, not observed compiler errors. No assertion that only syntax changes
remain is justified.

Retain the expanded statements and physical definitions during repair. Split
large tactic blocks into explicit equalities instead of adding unproved model
assumptions. A successful final report must contain actual clean-build logs,
all permitted transitive axiom sets, positive/negative Lean controls and an
independent mathematical comparison with the manuscript.
