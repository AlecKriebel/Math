# Composite mutation probe research log

## 2026-08-25 — checkpoint 1 (35%)

- Scope fixed to the revised corrected-composite mutation runner and its
  production independent verifier in the isolated referee tree.
- The isolated tree will remain unmodified. Complete mutant ledgers, logs, and
  reports are confined to this scratch directory and deleted case-by-case where
  their full bytes are not needed after hashing.
- Static trace identifies verifier-facing row checks for physical ports,
  restoration parent/transport evidence, and theta2 restoration descendants.
- Next checkpoint: execute four complete-ledger mutations covering port,
  canonical parent, explicit reversed direction, and inherited-child census.

## 2026-08-25 — checkpoint 2 (100%)

- Executed the four bounded complete-ledger attacks through the untouched
  production verifier in 85.23 wall-clock seconds. All four failed at the
  intended semantic row gate; none reached checksum diagnostics or created a
  verifier report.
- Confirmed the live direction preimage: changing only transport direction from
  `source_to_target` to `target_to_source` changed the binding hash and caused
  `RAW4_RESTORATION_EVIDENCE:2185`.
- Independently recomputed both frozen v2 mutation-report payloads. Their 22
  semantic records are internally valid with zero survivors, but the 18 cases
  outside the bounded fresh selection were not rerun here.
- Source hashes were identical before and after. No isolated file changed, and
  all disposable mutant ledgers were deleted.
- Exact findings, commands, diagnostics, paths, lines, hashes, and runtimes are
  frozen in `AUDIT_RESULT.md` and `bounded_probe_report.json`.
