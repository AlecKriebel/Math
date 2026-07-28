# Research log

## 2026-07-28 PDT

- Restated the proposed greatest-family reciprocity property separately
  from mutual matching, family base orderability, and matroid basis
  exchange.
- Tried to prove reciprocity by reversing forced moves, by using the union
  characterization of the greatest fixed point, and by applying C-108
  twice.  Each route fails to coordinate future attacks after the reverse
  exchange.
- Scanned connected graphs without the condition \(\gamma=\alpha\) and
  located `GEjbug`, an exact greatest-family countermodel with
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3)\).
- Wrote a clean ordinary-set verifier.  It recomputes the full parameter
  tuple, the 41-state greatest triple-family, all 205 obligations, and the
  explicit failed attack at the reverse exchange.
- Exhausted all 131,072 labeled two-vertex extensions that keep `GEjbug`
  induced.  Exactly 36 extensions restore eternal equality; all 3,136
  independent-state pairs in them satisfy reciprocity.  This remains an
  observed extension-class result pending an independent replay.
- Built an exact bounded-fixed-point SAT formulation for a disjoint
  triple-pair violation.  Discovery instances through order nine were
  UNSAT, consistent with the independent ordinary-set scan; no proof logs
  were promoted.
- Proved the conditional payoff: equality reciprocity would make the
  C-108 active-response relation undirected.  It does not alone supply the
  missing cross-component color intersection or eliminate arbitrary
  2-SAT bicycles.

