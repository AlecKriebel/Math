# Order-12 k=4 AUTHOR v3 research log

## 2026-07-26T03:54:21-07:00

- Diagnosed the retained leaf `1111` failure as a pinned `drat-trim`
  backward-parser warning on a pseudo-unit deletion.  The raw binary DRAT
  remains preserved and its warning-fatal forward verification remains
  mandatory.
- Implemented the v3 six-phase protocol: raw forward replay, strict streaming
  deletion stripping, fresh normalized RUP-only forward replay, separate
  RUP-only backward LRAT conversion, and independent `lrat-check` replay.
  Normalization alone makes no proof claim.
- Hardened audit provenance, exact artifact inventories, resource and child
  records, warning parsing, v2/v3 separation, and the explicit boundary that
  read-only structural audit is not a fresh LRAT replay.
- Published immutable CNF and JSON records through external
  same-filesystem staging and atomic rename.  Explicit regressions cover
  both pre-rename missing-configuration states: an empty attempt directory
  and an `instance.cnf` with no configuration.  Both reconstruct from bound
  inputs, seal as retryable nonclaims, append bound reconciliation
  checkpoints, and audit cleanly while ignoring unpublished external staging
  residue.
- The final AUTHOR suite passed 29 of 29 tests in 133.544 seconds.  Its exact
  log SHA-256 is
  `fa7b9edf79f77114290634559d8a8aa25ba97d786ce954ddea4969a248cf7e9b`.
- No production case was launched, no new leaf was certified, the frozen v2
  attempt was not modified, and no commit or push was performed.
