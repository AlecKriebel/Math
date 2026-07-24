# Research log

## 2026-07-24

- Started from the independently certified exact h=0 order-three profile
  with target `(2,-2,-4,-2)`.
- Recomputed the rank-18 first placement layer and its half-turn
  decomposition.  The fixed and anti-fixed kernel dimensions are 21 and
  15.
- Fixed the first canonical anti direction `y=e0`.
- Derived the six half-turn-odd second-digit equations as a rank-6 linear
  system in the 21 fixed coordinates.  Its canonical affine solution has
  dimension 15.
- Independently reconstructed and exactly replayed the 54-trit asymmetric
  witness.  All twenty displayed equations vanish through digit 2; digit 3
  is nonzero in 13 rows.
- Computed its labelled aggregate
  `(-2,-6,-6,-2,-2,-2,3,1,2,2,-1,1,-1,1,2,2,5,3)`.
  It is absent from the complete 1,756-row catalog.  Full labelled replay
  fails the exact zero-column-lag equation.
- Composed the exact phase system with the 15-dimensional slice.  The
  compact digit-3 model has 411 effective forms, 1,286 variables, and 860
  constraints.
- Ran the exact digit-3 model for 300 seconds with four workers and seed
  2668.  Result: `UNKNOWN`; 4,340,808 branches, 177,136 conflicts,
  300.008173 solver seconds, and 175,112,192-byte peak RSS.  No
  satisfiability or exclusion claim follows.
- Preserved a half-turn-fixed digit-2 control.  Its reduced exact digit-3
  CNF run was manually interrupted after 464.11 seconds, so its status is
  explicitly `INTERRUPTED_UNKNOWN`.  It is diagnostic only.
