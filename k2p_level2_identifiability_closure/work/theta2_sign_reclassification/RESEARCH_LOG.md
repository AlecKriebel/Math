# Research log: theta2 revoked sign family

## 2026-08-21T18:12:00Z — independent full-map replay

Derived the source restriction without consulting the revoked rooted witness
table.  Each of the four theta2 repairs has the unique coefficientwise-zero
triple `(0,1,2)`.  Replayed all 2,528 transported rows, all exact graph
nonrelations, and all 85 target strict-negative Bernstein classes.  Independent
report payload:
`871656d3b8a20b14de0e3bcb586329f9ef976d619d777962c673b9a0a1e3ebd6`.

Completion estimate for this family: 90%.

## 2026-08-21T18:16:00Z — mutation closure

Ten fail-closed mutations all failed as required: omitted/reassigned truth
rows, missing/wrong target presentations, altered Bernstein coefficient and
tensor count, relation multiplicity reassignment, wrong source-zero and graph
relation counts, and Python optimized mode.  Mutation payload:
`8a361d4bb79fad685c36e8d85314115ca1bc0754d70a0d9337e4e433eeb8a62e`.

Completion estimate for this family: 100%.  Restoration-child sign rows remain
a separate, currently active correction task.

## 2026-08-26 — mutation evidence qualification hardened

Requalified the same nine resealed certificate attacks and optimized-verifier
attack against a required clean production-verifier baseline.  All 10/10 cases
exited exactly one at their named semantic diagnostics and produced no success
artifact.  Eight negative controls reject wrong diagnostics, tracebacks,
missing imports, timeouts, signals, non-one exits, and false success artifacts.
The producer now requires caller-owned external output, writes atomically, and
removes stale PASS output before optimized-mode refusal.

The authoritative suite passed in 296.06 seconds with 326,434,816 bytes maximum
RSS.  Report payload:
`9d4a1753c7b51b868e20fb828fc418c8ba75ad5b956f04664b239ab7fd73c688`.
All 2,528 truth rows, 85 Bernstein classes, graph relations, transports, and
censuses are unchanged.  Completion estimate for this family remains **100%**.
