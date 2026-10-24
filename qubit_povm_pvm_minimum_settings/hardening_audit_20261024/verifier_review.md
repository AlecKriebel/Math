# Fresh verifier reassessment of the two-input result

Checkpoint: 2026-10-24T15:15:11.570259+00:00. Completion estimate: **100% for this bounded verifier reassessment and implemented replay**. Remote CI completion is a separate root-task check. No mathematical source or frozen September package was changed by this review.

## Result

No mathematical counterexample or rejected proof was found. A materially stronger check is now complete: the pinned Lean kernel replayed the entire serialized dependency closure of these endpoints into an initially empty kernel environment:

- `Bell.two_input_convex_equality`
- `Bell.HilbertFiniteLabels.at_most_two_input_equality`
- `Bell.HilbertFiniteLabels.finite_source_projective_simulation`

**33,644 declarations from 1,271 compiled modules passed.** The actual run was `2026-10-24T15:11:39.962328+00:00` to `2026-10-24T15:12:58.759539+00:00`. Its authoritative receipt is [replay receipt](replay_runs/20261024T151139Z/receipt.json), with controls, main output, full dependency inventory and compiled-input hashes in the same directory. The source baseline was the successful final-package run `20260921T150935Z-9ebb22fc`. Every recorded source/checker hash and compiled module hash was unchanged throughout this replay.

This is additional verification using the **same pinned Lean kernel**, not a second kernel implementation and not a rebuild of Mathlib from source.

## Newly demonstrated issue: trust-zero import is insufficient

A small isolated fixture deliberately serializes a theorem claiming `False` whose stored proof is `True.intro`. Importing it with Lean 4.19.0 `--trust=0` accepts a new theorem using the invalid declaration; the axiom scan also reports no axioms. The successful import has exit code zero, recorded in [trust-zero probe](verifier_probes/trust_zero_probe.json). This fixture is explicitly separate from the production mathematics and never imported into it.

Therefore neither `--trust=0` nor an axiom scan, alone or combined, constitutes rechecking imported proof bodies. This is a concrete limitation of the verification mechanism, **not evidence that the actual project cache contained malformed proofs**. The original certificate disclosed trust in compiled dependencies, so this finding does not contradict its stated boundary.

The pinned import implementation constructs its constant map from serialized module data; the explicit replay implementation sends declarations back through the kernel. See the primary [Lean environment implementation](https://github.com/leanprover/lean4/blob/v4.19.0/src/Lean/Environment.lean) and [Lean replay implementation](https://github.com/leanprover/lean4/blob/v4.19.0/src/Lean/Replay.lean).

## Implemented strengthening

[ReplayClosure.lean](verifier_probes/ReplayClosure.lean) starts with three required theorem names, follows both types and proof/definition bodies, includes opaque bodies and complete mutual inductive blocks, and rejects missing, unsafe or partial dependencies. It checks allowed axiom names **and exact types/universe parameters** against a separately imported canonical compiler `Init` environment. Every closure declaration already present in that trusted environment must match its complete `ConstantInfo`, including constructors, inductive metadata and recursor rules.

The actual checking environment begins empty. The checker uses the unchanged pinned `Environment.replay` implementation, partitioning declarations by original module order. Cross-module prerequisites must already be kernel checked; inductive blocks must remain complete within their group. Between modules, `Environment.ofKernelEnv checked.toKernelEnv` discards only elaborator bookkeeping while retaining all checked kernel declarations under their original full names. Every final declaration is compared to the original complete `ConstantInfo`; all three endpoints must be present.

Four real controls pass: a valid proof is accepted; an invalid proof is rejected with a kernel type mismatch; retyping `propext` to `False` is rejected; replacing canonical `True` with a same-typed empty inductive is rejected. This last control prevents a same-name/same-type core-definition substitution from escaping the axiom-signature guard.

[run_replay.py](run_replay.py) requires a successful full-run receipt matching the requested source tree, checks the pinned compiler identity, executes controls and dependency discovery, hashes every consumed module, executes replay, and rejects changes in the source, checker, dependency inventory or compiled input bytes. Nonzero exits, recovered panics, error diagnostics and absent success markers fail closed. Its [temporary mock suite](test_run_replay.py) passes nine acceptance/rejection scenarios; those mock receipts are deleted and are not mathematical evidence.

For a fresh complete build in CI, from `bell_lean`:

```sh
python ../hardening_audit_20261024/run_replay.py --root .
```

The wrapper clears inherited Lean source/library search-path overrides. It gives a dedicated Lean worker a 256 MiB stack. The worker is necessary because Lean's stack-size option does not enlarge the operating-system main thread used by `--run`; this follows the pinned [runtime stack implementation](https://github.com/leanprover/lean4/blob/v4.19.0/src/runtime/stackinfo.cpp). The larger stack changes resources, not kernel checking rules.

## Failed attempts retained as failures

- The live workspace had an older aggregate `.olean`. The required combined endpoint was absent, and the checker rejected it. The successful replay instead used the preserved final certified extraction.
- A recursive graph collector exhausted interpreter stack. It was replaced with an iterative worklist.
- Replaying all modules in one elaborator environment caused recovered panics from duplicate normalized private proof names. The first diagnostic and full-log hash are retained in `verifier_probes/frontend_replay_collision.json`; this was never accepted as success. Module partitioning solves the bookkeeping collision without renaming proofs or bypassing checks.
- The first wrapper attempt correctly failed before replay on relative artifact-path resolution; paths now resolve against the selected proof root.
- Two complete wrapper attempts rejected the kernel's stack-limit error. Dedicated-worker replay then passed. Failed receipts remain in `replay_runs/` and are distinct from the successful run.

## Current CI and remaining trust boundary

The repository-root workflow now contains an active Lean job; the older workflow nested inside `bell_lean` was not a repository-root GitHub Actions workflow. Root also identified a clean-bootstrap defect: interpreting `Cache.Main.lean` presupposed imported helper `.olean` files. Building `Cache.Main` first is the appropriate repair; review of the change found no skipped proof check. The three new regression cases test ordering, helper failure and an error diagnostic despite exit zero. The reported verifier suite now has 53 passing tests. Remote CI must itself pass before claiming that pipeline successful.

The bootstrap repair changes two verifier files from the original 104-file snapshot. Thus **all current workspace inputs must not be described as identical to September**. Mathematical proof sources and the frozen release remain unchanged; the replay's 104-file identity statement applies to its selected preserved extraction, not to the newly hardened live verifier.

Remaining assumptions are specific:

1. The pinned compiler/kernel/runtime, canonical `Init`, machine and checker execution are trusted. This is not an independently implemented kernel.
2. Replaying proof objects checks their internal correctness. It does not establish that every Mathlib definition in a compiled artifact is the definition encoded by the pinned source checkout. Compiled hashes establish identity and stability, not authenticity. A separate clean Mathlib source rebuild would strengthen that correspondence further, at materially greater cost.
3. Git dependency pins and tracked-source cleanliness do not authenticate ignored `.olean` files. The new replay substantially reduces trust in their proof bodies, while the prior source/build receipts and explicit model contracts remain necessary.
4. Formal success does not prove that the chosen definitions express every sentence of the manuscript. The separate semantic review addresses the principal statement, finite shared randomness and model bridges; auxiliary manuscript arguments remain separately scoped.

For the user's main result, the highest-value bounded additions were continuous full-source project CI and this complete endpoint-closure replay. Both mechanisms are now implemented, and the local replay has passed. A full dependency-source rebuild or genuinely different proof checker is a possible further assurance project, not a missing step in the actual mathematical argument and not a prerequisite to preserving the existing result.
