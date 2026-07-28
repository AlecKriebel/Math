# Research log: exact mixed-\(P_4\) endpoint defect

- **2026-07-28 PDT.** Reconstructed accepted C-067, C-070, C-072,
  C-121, C-124, C-129, C-133, C-140, and C-144.  Audited the discovery
  mixed-\(P_4\) synthesis observations through order 20.

- **2026-07-28 PDT.** Tested the proposed singleton-defect recurrence.
  Found the precise obstruction: C-121 defects lie in the fixed
  \(a,b\)-ridge, so the opposite anchor already witnesses each relevant
  non-dominating pair.  The full-equality graph `HCOceRy` independently
  realizes two adjacent pure same-color singleton vertices, refuting any
  recurrence based only on singleton purity and clique structure.

- **2026-07-28 PDT.** Added an exact-static discovery encoding.  A single
  static negative role already made the tested mixed-\(P_4\) instances
  UNSAT.  This computation was used only to locate a smaller local core.

- **2026-07-28 PDT.** Re-examined C-121's endpoint defect core.  Its
  accepted 16 cases cover the branch \(dx_3\notin E(G)\).  Enumerating
  the previously unchecked branch \(dx_3\in E(G)\) adds 16 cases; the
  greatest restoration-compatible local kernel is empty in every case.
  Hence one endpoint defect, rather than one common double defect, is
  already impossible.

- **2026-07-28 PDT.** Wrote an ordinary-set verifier and a separate
  bitset verifier.  Both reproduce all 32 initial sizes, deletion-round
  sizes, and reference deletion ranks.  The ordinary-set verifier also
  reconstructs the `FDzro` gamma-two family/static boundary and the
  `HCOceRy` full-equality singleton boundary.

- **Current exact status.** Candidate universal exclusion of the exact
  **static** \(Y_3=P_4\) pattern.  This is not an exclusion of arbitrary
  family-list mixed paths, longer unit chains, the complete \(k=3\)
  branch, or the gamma--theta conjecture.  Independent hostile audit is
  still required before promotion to the campaign claim ledger.
