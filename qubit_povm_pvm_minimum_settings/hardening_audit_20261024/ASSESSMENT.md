# Strengthening confidence in the main two-input equality

The fresh adversarial review found no missing mathematical premise in the main equality. Its statement remains equality of ordinary finite convex hulls for complex local dimension at most two, with arbitrary finite input-dependent outcomes. One random selector chooses complete projective strategies, including the state. It does not assert equality of raw sets or same-state simulation.

## Concrete improvements in this checkpoint

1. The repository-root workflow now runs the complete pinned Lean source build, all required contracts, the public axiom audit and verifier preflight tests. Previously the active workflow ran exact artifacts and PDFs only; the Lean workflow was nested inside the standalone package and was not discovered by GitHub in this monorepo. GitHub searches [the repository-root workflow directory](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows).
2. The first genuinely clean online-bootstrap CI run exposed a missing helper-compilation step. `scripts/run_lean.py` now builds `Cache.Main` before interpreting it. Three regression tests cover ordering, failure, and error diagnostics with a zero exit code; all 53 runner tests passed. The previous September prepared-cache runs remain valid. Their successful results were not evidence that the online-bootstrap path had been exercised.
3. `MainEndpointProbe.lean` independently expands the actual source and target tensor trace formula, both families of projectors, and one common finite normalized distribution. It passed locally and is now an active CI step.
4. `run_replay.py` and `verifier_probes/ReplayClosure.lean` explicitly recheck the dependency proof objects for the main equality, the combined Hilbert/finite-label equality, and actual finite source-projective simulation. They start from an empty checked kernel environment and admit only standard axioms with canonical core signatures. See the run-specific receipts for execution status; source review alone is not replay success.

## Successful replay evidence

[Run 20261024T151139Z](replay_runs/20261024T151139Z/receipt.json) passed in 79 seconds against the exact September final-extraction proof snapshot. It rechecked **33,644 declarations across 1,271 compiled dependency modules**, including the three required endpoints. All consumed module hashes, protected source hashes and checker hashes remained unchanged. The four actual kernel controls passed; nine mocked driver scenarios checked failure handling. The wrapper tests do not substitute for the actual Lean execution.

The replay is also wired into CI after a fresh complete source build and the expanded physical endpoint contract. The earlier pre-hardening source_identity.json records 104 matches; the subsequent bootstrap fix changes two verifier scripts, with all production mathematical sources unchanged.

## Why the extra replay matters

Pinned Lean 4.19 imports serialized constants without rechecking every proof body. In an isolated negative fixture, `--trust=0` accepted an imported malformed proof of False, and its axiom listing was empty. This is a demonstration of the imported-artifact trust boundary, not a theorem admitted into the project. The deliberately malformed fixture is outside all production proof modules and never imported by them.

The replay tool uses the pinned Lean kernel, checks the complete safe type-and-value dependency closure, checks mutual inductives and generated recursors/constructors, compares canonical Init declarations, and verifies the complete resulting declarations. Its positive control must pass; malformed proof, retyped standard axiom, and altered core inductive controls must fail. It partitions declarations by original module and resets only frontend asynchronous bookkeeping between modules, retaining all previously kernel-checked constants under their original names. This avoids a pinned frontend private-name collision without disabling kernel checks.

The Python wrapper requires a matching successful full-source-build receipt, verifies the compiler identity, hashes the consumed compiled modules before and after, and rejects missing success markers, nonzero exits, panic/error diagnostics, changed inputs or changed checker source. Failed development attempts are retained and are not counted as success.

This is an independent replay pass using the same Lean kernel, not a second kernel implementation. It reduces reliance on the validity of imported proof bodies. It does not independently establish that every compiled Mathlib definition matches its published source text. The compiler/kernel/runtime, canonical Init and replay driver remain trusted.

## What would still add assurance or mathematical content

- **Highest assurance follow-up:** reproduce with all dependencies rebuilt from pinned sources on a separately provisioned machine. A distinct kernel implementation would provide additional implementation diversity. Neither is an identified missing lemma in the existing proof.
- **Human semantic review:** an independent expert can inspect the model definitions, exact quantifiers and correspondence with the intended physics. The present independent reviews are separate AI-agent reviews. No external reviewer has been contacted.
- **Optional mathematical strengthening:** prove an explicit Carathéodory bound of at most D+1 complete projective branches, where D is the full behavior-table dimension. This makes shared randomness quantitative; the existing theorem already establishes exact finite simulation. It is not required for the equality.
- Completing the unused general SDP/KKT, full manifold/Hessian/inertia or all auxiliary manuscript calculations would expand coverage, but would not fill a dependency gap found in this main result.

## Historical package and reproduction

The September local ZIP and certificates are preserved. Its online bootstrap needs the missing preparatory command, executed from the extracted project before `python reproduce.py --bootstrap`:

```sh
(cd bell_lean && lake build Cache.Main)
```

This writes only `.lake` dependency/build outputs, which the shipment manifest excludes; it does not alter shipped source files. The current repository runner performs this step itself. The already-tested `--dependency-cache` path is unaffected.

The additive October checker is outside that frozen ZIP. From a repository checkout with a successful current full-source runner receipt, run:

```sh
cd qubit_povm_pvm_minimum_settings/bell_lean
python scripts/run_lean.py --bootstrap --serial
lake env lean ../hardening_audit_20261024/MainEndpointProbe.lean
python ../hardening_audit_20261024/run_replay.py --root .
```

Detailed reviews: [semantic](semantic_review.md) and [verifier](verifier_review.md). Initial source identity, subsequent verifier changes, actual CI runs and replay evidence are recorded separately so that historical receipts are not silently promoted to evidence for modified files.
