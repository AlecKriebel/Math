# PR468 independent reproduction log

- 2026-10-12 04:05 UTC — Read both frozen checker programs before execution;
  no network, file mutation, or non-standard packages in either. Read only
  computation scope from the frozen README/proof, with no newly commissioned
  review consulted. Audit completion estimate: 10%.
- 2026-10-12 04:09 UTC — Reproduced both checkers normally and optimized,
  byte-identical to their recorded outputs; all 24 manifest entries match,
  covering 15 unchanged files. Confirmed assertion-removal false acceptance.
  Initial verdict written and sent to the parent. Audit completion: 35%.
  Strongest verified result: finite recorded outputs reproduce. Exact gaps:
  independently reformulated controls, hardened runtime conditions, mutation
  rejection after repair. Universal proof and priority are outside this task.
- 2026-10-12 04:11 UTC — Corrected the ninth negative control to corrupt the
  actual paired-boundary calculation. All nine mutations reject normally and
  all nine are accepted by optimized original programs. Separate hardened
  copies preserve all 27 conditions and original stdout; all 18 mutation
  executions reject in the hardened copies. Frozen input bytes unchanged.
  Assigned audit completion estimate: 70%.
- 2026-10-12 04:13 UTC — Independent bitmask/exponent-vector/rational-circuit
  controls pass: three finite fields, four Flores dimensions, 100 distinct-seed
  moves, 3548 complements, 580 persistent faces, 30 middle-move identities and
  52 explicit edge-move witnesses. Normal/optimized outputs match. All 576 small
  F2 matrices agree with exhaustive image enumeration; two invalid fillings
  and twelve mutation executions reject. Final scope and distribution report
  written. Assigned audit completion: 100%. Strongest verified result and
  universal-proof boundary are stated in INDEPENDENT_VERDICT.md.
