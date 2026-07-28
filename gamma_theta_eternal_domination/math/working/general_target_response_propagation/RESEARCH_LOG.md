# Research log: general target-response propagation

## 2026-07-28 PDT

- Re-read the accepted parameter-three vertex-star proof C-106 and isolated
  the only facts used by its forced attacks: both endpoint states are
  independent, every non-\(x\) guard is nonadjacent to their shared vertex,
  and guards already installed in the destination state cannot answer the
  next destination attack.
- Observed that the same argument works for arbitrary \(k\).  Attack the
  vertices of \(T'-T\) one by one from \(T-v+x\).  An \(x\)-move always
  misses \(v\); a guard already in \(T'\) has no move edge; closure
  therefore replaces one remaining vertex of \(T-T'\) at every step.
- Wrote a self-contained proof and the equality-family active-set
  corollary in `math/lemmas/general_target_response_propagation.md`.
- Generalized the complete responder-color part of C-106.  In any proper
  deletion \(k\)-coloring, active colors are invariant on components of
  the maximum-independent \(k\)-set ridge graph.  A color common to all
  components extends over the target.  Therefore a critical full target
  at arbitrary \(k\) forces at least three ridge components with empty
  total responder-color intersection.
- Derived the exact all-\(k\) inactive-set identity: the component
  responder colors are precisely the colors absent from inactive support,
  and, under support coverage, their total intersection is precisely the
  colors absent from the whole inactive set.  The inactive complement
  subgraph is \(K_k\)-free.
- No clique partition, all-order coloring theorem, or conjecture resolution
  is claimed.  The note awaits independent hostile review.
