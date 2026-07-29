# Research log: QQ1 bow-tie global coupling

## 2026-07-28 — global transport found

- Started from accepted C-166, C-167, C-174, and C-177.
- Observed that two distinct completions \(d,d'\in C_{xr}\) can never
  occur together in a retained state: their common-nonneighbor set
  contains the nonadjacent pair \(x,r\), contradicting C-174's clique
  conclusion for a supported pair.
- Used that obstruction at the attack \(d'\) from
  \(\{u,d,w\}\) to force the unique retained response \(d\to d'\).
  This transports every hot vertex to every completion.
- Derived that the union of all completion-specific hot sets is one
  clique, then combined C-167 and C-177 into a complete
  \(H\)-by-\(Z\) polarized/support matrix.
- Audited all vertex collisions.  In particular, a hot vertex cannot
  equal a distinct completion because it misses its seed completion,
  while the completion set is a clique.  The overlap \(C\cap Z\) is
  explicitly allowed.
- No omitted response was converted into a graph nonedge.
- Exact control `FCQe_` nonvacuously realizes transport to a completion
  outside a hot vertex's original seed fiber.
- Estimated completion of this bounded global-coupling task: **95%**
  discovery-side; hostile review remains.  Estimated progress toward
  eliminating canonical QQ1: **70%** as a workload estimate, not a
  probability.

## 2026-07-28 — finite-audit scope corrected after hostile review

- Hostile review passed Theorem 1.1 and Corollaries 2.1 and 3.1, but
  identified an exact overstatement in the census scope: the nonedge
  \(H\)-by-\(Z\) branch counted cells without independently checking
  C-177's activity hypotheses and polarized conclusions.
- Narrowed both the note and machine-readable scope to what the
  checker actually verifies: global transport, retained bridge
  incidence, and the full supported-fan conclusions on edge cells.
- The nonedge polarization remains a symbolic consequence of accepted
  C-177.  The `FCQe_` example is now explicitly described only as a
  transport control.
