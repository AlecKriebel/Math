# Research log

## 2026-07-28 PDT

- Read the accepted full-list, frozen-projection, reverse-color, bridge,
  and coinductive-reciprocity packages, with special attention to the
  warning that a missing family transition need not be a graph nonedge.
- Recast the safe-color question as a safety game obtained by banning the
  exact root swaps \(S-u+b\), \(b\in N_{\overline G}(x)\).
- Proved the ban-avoidance forcing theorem: any nonempty eternal
  triple-family avoiding those swaps must retain the selected response
  \(S-u+x\).  The proof freezes \(u\); otherwise the projected complement
  contains the triangle \(xbc\), contradicting the accepted parameter-two
  theorem.
- Deduced that the earlier safe test is exactly restricted-kernel
  nonemptiness.  This does not prove that one of the three kernels is
  nonempty.
- Replaced unsafe sequential recomputation by one cumulative ban for an
  entire full core and proved an exact cumulative-kernel plus direct
  list-2-CNF characterization.  This is a reduction, not an existence
  theorem.
- Proved a retained finite-rank descent to the ban whenever a restricted
  kernel is empty, and classified the final entry as a corridor (with a
  direct-root degeneration or a forced \(G\)-diamond) or an
  anchor-restoration gate.
- Replayed the accepted equality control and the MMV-001/MMV-021
  gamma-two controls.  MMV-021 confirms the important boundary: an
  individually surviving color does not settle a multi-vertex full core.
- Exploratorily scanned the fixed MMV catalog and all connected unlabeled
  graphs through order eight.  These measurements are recorded only as
  `OBSERVED` in `NOTE.md` and are not used in a proof.
- Hostile review caught two local presentation defects before promotion.
  The ban-avoidance proof now handles anchors inside \(B_x\) explicitly:
  \(u\in B_x\) is impossible because it bans \(S\), other root anchors
  already lie in the frozen projection, and only outside vertices use the
  response-list definition.  The terminal corridor is described as a
  direct \(u\)-response, not a singleton-list response.

Outcome: the equality safe-color lemma remains open, but it is now exactly
the nonemptiness of at least one restricted kernel.  The two irreducible
branches are cumulative-kernel annihilation and an unsatisfiable ordinary
two-list coloring 2-CNF in a surviving cumulative kernel.
