# Research log: conditional DoubleLex implication audit

## 2026-07-26

- **05:39 PDT — Scope fixed.**  Began a read-only implication audit for the
  exact order-12 parameter-four DoubleLex formula.  Excluded every pending
  solver result and proof artifact from the premise set.
- **05:39 PDT — Exact formula binding checked.**  Recomputed the parent and
  DoubleLex SHA-256 values and DIMACS censuses.  Verified that, after their
  headers, the complete parent body is the exact prefix of the DoubleLex
  body and that the 765-clause suffix has SHA-256
  `328eeeaadc688bbce63fd3ffd952f86a4eb9209e6d0abf5542979fe54ebdbbe0`.
- **05:40 PDT — Accepted implication chain checked.**  Audited C-037,
  C-043, C-044, and C-045 and their hostile reviews.  Determined that strict
  DoubleLex UNSAT transfers through C-045 to parent UNSAT and through C-037
  to the complete connected \((12,4)\) exclusion.  C-043/C-044 are
  corroborating reductions, not extra scope.
- **05:41 PDT — Component scope separated.**  Reproved from C-003 and C-006
  that every disconnected order-12 parameter-four counterexample is exactly
  \(Q\mathbin{\dot\cup}K_t\), with \(Q\) a connected smaller parameter-three
  counterexample.
- **05:41 PDT — Lower-order evidence separated.**  Recorded that the
  campaign has strict complete coverage through order 9, while its local
  Table 9 reproduction does not certify the published search's
  exhaustiveness at orders 10 and 11.  The published MMV no-counterexample-
  through-11 result suffices as a paper-level premise but is not packaged to
  the campaign's stronger certificate standard.
- **05:41 PDT — Frontier gate identified.**  After hypothetical strict
  DoubleLex UNSAT, connected parameter five remains necessary for an
  order-12 frontier.  A strict campaign frontier additionally needs complete
  connected coverage at orders 10 and 11; accepting the published MMV
  frontier supplies that lower-order premise instead.
