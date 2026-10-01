# Research log — independent matrix Fitting falsification

- 2026-10-01 05:46:18 UTC — Checkpoint, estimated local audit completion 90%.
  Independently proved the finite-degree recovery, product-factor isolation,
  validity of a C-basis kernel presentation, and fixed-embedding bridge.
  Eight exact rational edge cases passed. Identified the nonzero-nilpotent
  determinant interpretation trap. No sibling reports read.
- 2026-10-01 05:49:12 UTC — Checkpoint, estimated local audit completion 100%.
  Added d=0 and simultaneous basis-change recovery checks; all nine examples
  pass. Recorded the precise proof and three wording/implementation safeguards
  in report.md, alongside exact reproducible code/results. No local logical
  counterexample or unresolved local gap. Global Mohan Kumar applicability
  remains with the parent's separately assigned source audit.

Route mechanism: algebra recovery -> Fitting presentation -> product
localization -> Wiebe criterion -> regular-embedding presentation invariance.
Status: verified within stated local scope. Evidence: proof in report.md;
exact computations in check_fitting.py and check_results.json. No external
communication, canonical edit, or Git operation occurred.
