# Research log: reverse-rank descent

## 2026-07-28 PDT

- Reconstructed the literal synchronous greatest-kernel horizons, accepted
  C-108 vertex-star propagation, accepted C-143 reverse endpoint
  domination, and the C-136--C-138 order-nine rank audit.
- Rejected equal-rank induction immediately: accepted graph
  ``HCOe`Z{`` has adjacent star endpoints of ranks one and two.
- Proved the finite-horizon form of C-108.  Transporting between
  independent source states at exchange distance \(m\) costs exactly at
  most \(m\) kernel rounds.
- Derived the all-\(k\) Lipschitz inequality for extended deletion rank.
  Found equality controls at both distances possible for \(k=3\):
  ``HCOe`Z{`` gives \(2-1=1\), and `HCRdnat` gives \(3-1=2\).
- Combined the Lipschitz theorem with C-143.  At a hypothetical asymmetric
  active edge, a deleting attack with a unique neighbor in the independent
  endpoint moves along one facet ridge to a reverse endpoint of exactly
  one lower rank.
- Proved that every rank-one or globally minimum-rank blocker must instead
  hit at least two endpoint guards.  This isolates the precise collision
  branch and does not eliminate it.
- Located `HEjejrr` as an exact rank-two to rank-one single-hit descent
  control outside campaign equality.
- Replayed `GEjbug` as the sharp rank-one collision boundary:
  the deleting attack hits two endpoint guards and all successors fail
  domination.  Its \(\gamma=i=2<3\) defect is essential to its status as a
  boundary control.
- Explored, but did not promote, the stronger claim that a rank-one
  collision is impossible under well-coveredness.  Direct constrained
  searches on fixed disjoint and one-pivot endpoint templates through ten
  vertices returned UNSAT, but no coverage proof or human reduction of
  the multi-hit branch was obtained.  The statement remains open and is
  deliberately absent from the candidate theorem.
