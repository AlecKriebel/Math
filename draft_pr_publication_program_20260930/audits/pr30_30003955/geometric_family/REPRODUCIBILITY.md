# Reproduction and artifact map

Run from the repository root:

```sh
/usr/bin/python3 draft_pr_publication_program_20260930/audits/pr30_30003955/geometric_family/reproduce.py
```

This uses Python 3.9.6 and standard-library modules only. It copies the old original checker and old independent suite into ignored tmp/reproduction and executes only those copies. Expected outputs are exactly 31 and 53,830 assertions and byte-identical frozen JSON. It runs the independent geometric controls, expecting 159,563 supplementary assertions and 50,068 prefix tuples. It separately runs the deliberately defective failure harness, expecting exit 1 and INTENTIONAL_MUTANT in stderr. That failure is recorded as expected failure, never a PASS. No package install, network access, Git mutation, ledger charge or canonical source write is needed for reproduction.

- `REPORT.md`: original-stage geometry verdict, universal proofs, exact original-step falsifier, and remaining gap.
- `PROPOSED_REPAIR.md`: reviewable local replacement preserving the stated genus bound, not a canonical edit or a future-head approval.
- `EARLY_GEOMETRY_SEAL.md`, `early_seal_receipt.json`: immutable early independent interpretation before old material; preliminary appearance-of-validity superseded by report.
- `original_inputs_receipt.json`, `exact_diff_read_receipt.json`: all fifteen frozen files, their original-head byte agreement, exact sixteen-path diff and actual merge base.
- `replay_receipts.json`, `original_checker_*`, `old_independent_suite_*`: original code replay outputs/results, exit codes and hashes; executions occurred in ignored copies.
- `geometric_controls.py`, `geometric_control_results.json`: independent ribbon and boundary-gluing templates, prefix controls and shortcut falsifiers. These are finite controls, not a universal proof engine.
- `failure_harness.py`, `failure_harness_*`: separate intentional mutant with actual nonzero exit/stderr and corrected-model explanation.
- `reproduce.py`, `reproduction_results.json`: one-command reproduction and actual run receipt.
- `primary_source_receipts.json`: downloaded primary hashes and exact visually checked pages; unavailable optional source attempt explicitly recorded.
- `VERDICT.json`, `RESEARCH_LOG.md`: machine-readable disposition and timestamped checkpoints with audit-completion estimates.
- `artifact_manifest.json`: complete first-party file roster, self-excluding by design. All foreign PDFs/pixels/replay copies and Python caches live in ignored tmp/ or are explicitly excluded transient __pycache__/ paths.

The old reviewed_partial and PARTIAL both retain SHA-256 ab85b2029c8f4e0e931aeac63ea42aad1a6a2e34f7425428e1f9224fd5bddd43. Old verdicts remain historical artifacts. The current result is HOLD_FOR_GEOMETRIC_PROOF_REPAIR on original head 53b6e68be6d2cc5966c25746618951d5dae2183b. Fixing that paragraph requires a fresh review of the revised artifact before promotion. Neither universal source question is solved or advertised as solved.
