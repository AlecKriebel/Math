> **Historical delivery record — 17 September 2026.** The uncompiled status below describes the original cloud delivery. See the current root README, `progress.json`, and accompanying local verification report for the repaired source and actual compiler results.

# Evidence log index

## Current source-only continuation: 17 September 2026

`source_expansion_2026-09-17/` contains the current executed non-Lean checks:

- `witness_regeneration.json`: deterministic reconstruction of the two new
  small witnesses, compared to stored JSON.
- `external_evidence.json`: exact bracket/literal, inverse, generation, scalar-
  kernel, and small Dynkin checks, including corrupted-witness rejection.
- `direct_flag.json`: fresh raw bracket/Jacobi and special flag identities.
- `original_literal_check.log`: original exported Lean literals match.
- `static_scan.json`, `runner_controls.json`: non-Lean source/runner tests.
- `final_gate.json`: expected nonzero refusal to claim the absent final theorem.

`runs/<UTC>/` records actual calls to the new validation runner. So far only
static/metadata/final-gate modes have run. Their `commands` arrays contain no
Lean invocation. An earlier static parser self-test failed and was repaired;
those failures are not Lean compiler failures.

`latest_source_check.json` is mutable after future local runs. It is not
expected to remain byte-identical after reproduction.

## Historical files inherited from the previous checkpoint

Top-level files such as `fresh_original_verifier.log`, `environment_probe.json`,
`connector_setup_failures.json`, `milestone_gate.log`, and
`direct_flag_final_check.log` describe the previous session. In particular:

- The original C++ verifier and corrupt-Smith-certificate control passed then.
  They were not rerun in this source-only continuation.
- The failed Lean setup/CI/download attempts happened then. No such retry or
  remote write was attempted during this continuation.
- The old uncompiled milestone gate is not evidence that the new source was
  passed to Lean. No present source module has been compiled.

The previous machine-readable checkpoint is retained as
`reference/previous_progress_2026-09-16.json`. The outer `history/` folder stores
the previous local Git metadata/bundle, not the current source revision.
