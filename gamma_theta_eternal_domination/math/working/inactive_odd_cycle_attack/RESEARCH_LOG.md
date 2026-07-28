# Research log: inactive odd-cycle attack

## 2026-07-28 PDT

- Reconstructed C-108's family-relative active set and the sharp C-109
  inactive-\(C_5\) static control.
- Built an exact one-guard SAT probe.  The first fixed-color experiments
  excluded an inactive \(C_5\), but were audited for planted residual-color
  bias before interpretation.
- Replaced residual colors by SAT variables, then removed the deletion
  coloring, deletion domination condition, full root, global
  \(\gamma\)-condition, and \(\alpha\)-bound entirely.
- Found exact controls showing that isolated dynamic inactivity, inactive
  edges, inactive three-vertex paths, rainbow inactive paths, and inactive
  \(C_4\)'s all occur.  This rejected a false vertexwise or length-two
  propagation theorem and isolated a genuinely odd-cycle mechanism.
- Reduced the \(C_5\) contradiction to a local template: an induced rim,
  one selected independent-triple witness per rim edge, the ten endpoint
  successor exclusions, domination on the template, and literal one-guard
  closure for template attacks.
- Enumerated all 52 set partitions of the five witnesses.  Every case was
  UNSAT.
- Generated 52 DRAT certificates (276,375 bytes total) and independently
  replayed all of them.  The clean-room checker reconstructed all 215,100
  input clauses byte for byte and verified complete partition coverage.
- Derived the structural corollary that, under
  \(\alpha(G)=\gamma^\infty(G)=3\) and \(\gamma(G-x)\ge3\), the
  family-relative inactive complement has no induced \(C_5\).  In the
  C-108 critical deletion branch, every remaining inactive odd hole has
  length at least seven.
- Preserved an exact 16-vertex parity control
  `OQifur}UO]}iTij]tpo}v`: both the full and deletion graphs have all five
  parameters equal to three, the greatest triple-kernel has 304 states, a
  root is full, and the inactive complement contains an induced \(C_4\).
- Universal bipartiteness remains open; direct witness-partition
  enumeration does not scale without a new shortening mechanism.
