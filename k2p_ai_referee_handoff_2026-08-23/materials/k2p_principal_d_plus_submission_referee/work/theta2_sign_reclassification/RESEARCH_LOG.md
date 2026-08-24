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

