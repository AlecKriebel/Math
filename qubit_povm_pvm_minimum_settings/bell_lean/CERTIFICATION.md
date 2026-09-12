# Lean verification certificate — 10 September 2026

**PASS: the main mathematical conclusions are verified end to end in Lean.**
The complete project source was rebuilt locally using the pinned compiler and dependencies. The two independent statement-contract files and all public theorem dependency queries passed in the same run. The proof and verifier inputs were unchanged throughout that run.

## Executed evidence

| Check | Result |
|---|---|
| Run | `20260911T022153Z-2ea5f99b` |
| Started (UTC) | `2026-09-11T02:21:53.738243+00:00` |
| Finished (UTC) | `2026-09-11T02:32:26.427687+00:00` |
| Mathematical modules | **58**, freshly rebuilt, followed by the `Bell` umbrella |
| Theorem/lemma declarations in those modules | **685**, including 10 private helpers |
| Public theorem dependency reports | **675 / 675 passed** |
| Expanded statement contracts | **25 / 25 passed** across two files |
| Compiler controls | Valid proof accepted; deliberately invalid proof rejected with a type error |
| Final source and dependency checks | Passed; all protected fingerprints unchanged |
| Exact algebra and verifier preflight | All 13 stages passed |
| Existing manuscript artifact verifier | Passed, including all artifact hashes |

The authoritative records are [kernel_report.json](reports/runs/20260911T022153Z-2ea5f99b/kernel_report.json), [axiom_audit.json](reports/runs/20260911T022153Z-2ea5f99b/axiom_audit.json), and [statement_audit.json](reports/runs/20260911T022153Z-2ea5f99b/statement_audit.json). These immutable run-specific records identify the certified run above. [latest_run.json](reports/latest_run.json) and the top-level copies may identify a later rerun; they are not substituted for this certificate’s fixed evidence. All **123 executed commands**, exit codes, log hashes, and protected source hashes are retained in [the run directory](reports/runs/20260911T022153Z-2ea5f99b/kernel_report.json).

Source-snapshot manifest SHA-256: `736d3758b247c60f679291606fc112444721aa25241a1eb394d40a9eba43d1c1`.

Every public theorem's transitive dependencies contain only some subset of `propext`, `Classical.choice`, and `Quot.sound`. There are no admitted proofs, `sorryAx`, custom mathematical axioms, or source-level kernel bypasses in the production formalization. The fresh build logs contain ordinary nonfatal linter warnings; no proof errors or recovered panic diagnostics passed the runner. The one intentionally failing compiler-control file is labelled `SmokeInvalid.lean` and is not a production proof.

## Mathematical scope

The verified development starts from actual positive semidefinite complex qubit matrices, normalized states and measurements, and Born probabilities. It proves the reductions and reconstructs physical strategies before deriving the unconditional endpoints:

- For two inputs per party and arbitrary finite input-dependent outputs, the ordinary shared-randomness convex hulls of qubit POVM and PVM behaviors coincide.
- Every such POVM behavior has a finite mixture representation using one common random index that selects a complete projective state-and-measurement strategy.
- One input on either side cannot separate the hulls; all architectures with at most two inputs on each side have equality.
- An explicit physical 3×2 POVM strategy attains `20√2 + 16/25`. Every projective behavior, including its convex hull, has score at most `289/10`, which implies the manuscript's stated upper bound.
- Strict separation therefore requires at least (3,2) or (2,3), and the threshold is attained.
- Appendix B's strengthened physical value `(16+8√7813)/25` is attained.

The unconditional combined theorem is `Bell.main_claims_with_strengthening`. The [claim-to-theorem map](docs/CERTIFIED_COVERAGE.md) gives the exact endpoints and source files. [Statements.lean](validation/Statements.lean) and [PhysicalContracts.lean](validation/PhysicalContracts.lean) expose the model, quantifiers, exact constants and boundary cases rather than merely checking theorem names.

The model includes arbitrary mixed qubit states, finite dependent output alphabets, zero and identity projectors, unused labels, and shared randomness choosing whole strategies. The certification concerns these formal mathematical conclusions. It does not assert same-state simulation, equality of raw strategy ranges, a global POVM optimum, bibliographic priority, or formalization of every prose sentence or unused alternative argument in the manuscript.

The manuscript's dimensions-at-most-two and stochastic-postprocessing conventions are represented by a fixed two-dimensional ambient carrier and finite convexification. Separate generic smaller-Hilbert-space embedding and stochastic-channel closure declarations are not endpoints of this development. The [independent correspondence review](local_verification/final_statement_review.md) explains the standard embedding and deterministic-mixture interpretation. The current repository manuscript sources are fingerprinted in [manuscript_correspondence.json](reports/manuscript_correspondence.json).

## Repairs and independent review

The incoming cloud archive had not been compiled. Local repairs resolved reserved identifiers, pinned Mathlib API differences, finite-index normalization, matrix/type inference, continuity and differential elaboration, and proof dependency ordering. The physical definitions and final theorem hypotheses were retained.

Two intermediate corrections deserve explicit notice:

1. `ternaryLabelMap_injective` needs the partition-preservation hypothesis `hπ`. The uncompiled archive implicitly dropped that hypothesis. An arbitrary permutation can violate injectivity after truncated relabeling. The corrected helper includes the hypothesis, and the main rank-zero argument proves and supplies it; no main theorem gained an assumption.
2. A malformed grouped declaration `leftSum rightSum : Operator` was split into the two intended operator fields. All physical positivity and normalization conditions remain enforced.

The original tensor-formula contract needed an explicit `Matrix.of` wrapper and product-index types; the empty-input contract needed an explicit natural-number reduction. Both preserve their statements and were independently reviewed. The strengthened-witness proof was also repaired to avoid a recovered simplifier panic; the runner now rejects such diagnostics even when a process exits zero.

Independent adversarial agent reviews examined the [mathematical rank branches](local_verification/mathematical_audit.md), [physical interfaces](local_verification/interface_audit.md), [final statement correspondence](local_verification/final_statement_review.md), [contract repairs](local_verification/final_statement_followup.md), and [verifier dependencies](local_verification/final_dependency_followup.md). The [final receipt review](local_verification/final_receipt_review.md) checks the successful run's evidence independently. These reviews supplement the kernel checks; they are not external peer review.

The stronger rational projective bound uses a complete exact sum-of-squares certificate, not a numerical optimizer's output. The separate [compiler-free preflight](reports/preflight/validation_summary.json) includes 1,387 exact physical-interface checks and 27 negative controls. The [repository artifact run](local_verification/repository_exact_verification.log) also passed. These computations are supplementary evidence and are not substituted for Lean proofs.

## Reproduction and trust boundary

- Lean: `leanprover/lean4:v4.19.0`, full compiler commit `6caaee842e9495688c1567e78c0e68dbb96942aa`.
- Mathlib: `c44e0c8ee63ca166450922a373c7409c5d26b00b`; all dependency commits are fixed in `lake-manifest.json`.
- Local platform: macOS arm64. The optional exact checks used Python 3.14.6, SymPy 1.14.0 and PyYAML 6.0.3.

With Lean/Lake installed and network access for the pinned dependencies, from `bell_lean` run:

```sh
bash scripts/check.sh --bootstrap --serial
```

With the dependencies already present, omit `--bootstrap`. See [OFFLINE_RUN.md](OFFLINE_RUN.md) for complete setup and receipt interpretation. The pinned cache tool is interpreted by Lean to avoid an older native linker's incompatibility with the local macOS loader; no dependency source was changed.

This checks the project's Lean sources against pinned dependencies. Normal trust remains in the Lean kernel/compiler binary and runtime, the machine/filesystem, and the producer of the pinned Mathlib build cache. It is not a bootstrap rebuild of all third-party software. The machine runner's manuscript-review flag marks the boundary of automated type checking; the separate correspondence reviews address that boundary explicitly.

## Provenance

Input: `bell_lean_mathematical_audit_20260910.zip`, SHA-256 `cbaa94b0f9b6c254dca19a8d4757600d53368b4747097d93d6e99c7ba1a851c5`. The original import is recorded in repository commit `2608fd5d0`; subsequent commits preserve the repairs and checkpoints on `main`.

Historical uncompiled-source status documents, earlier reports and nested archives remain labelled as historical. Static reports deliberately keep their own `kernel_checked: false` flags because those scripts do not invoke Lean; the full-run receipts above are the verification authority. `SHA256SUMS.txt` supplies separate byte-integrity checks.

No outside individual was contacted and no new immutable GitHub/Zenodo release was created. Research author: **Alec Kriebel**, [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).

## Referee correction and scope clarification — 11 September 2026

The subsequent independent referee confirmed the main equality and the physical endpoints, and found a manuscript ambiguity: positive pairings in the scalar metric normal form do not imply Lorentz signature. The paper now states explicitly that signature `(1,3)` is a separate prerequisite and chooses the future cone to contain `u`. The physical Gram-frame hypothesis already enforced in the Lean closure is unchanged.

The principal behavior-set equality, finite projective simulation, minimum-setting classification, explicit separation and strengthened attained value are formalized; selected auxiliary arguments are specialized or replaced. In particular, this certificate does not claim formalization of every mathematical statement in the paper. The [coverage limits](docs/CERTIFIED_COVERAGE.md#auxiliary-mathematics-outside-the-certified-scope) list the referee's specific examples.

The original manuscript fingerprints in the earlier correspondence receipt identify the version originally reviewed. The corrected manuscript, unchanged production proof inputs, rechecked counterexample and matrix contract, and new PDF builds are recorded in the [referee response](../referee_response_20260911/RESPONSE.md). Historical source PDFs and immutable release packages are preserved.
