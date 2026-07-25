# Research log

## 2026-07-24

- Audited whole-case reuse across all `2^18` case-26 pair-parity quotient
  states.
- Identified the exact support reflection `j -> 40-j`.  Verified
  coefficient by coefficient over the integers that normalized lag `k`
  changes by `(-1)^k`.
- Proved that the affine long-pair parity coset excludes zero: its
  variation rank is 18, and adjoining the offset raises the rank to 19.
  Therefore every quotient has an odd noncentral long pair and reflection
  acts freely on every fiber.
- Fixed one such orientation to obtain a `19+18` join.  This reduces the
  complete principal work from `5*2^37` to `3*2^37` rows, a 40% saving,
  with no memory increase.  The split attains the exact two-list optimum
  for 37 remaining binary variables.
- Proved that the quotient graph relation has all `2^18` Walsh
  frequencies, each with multiplicity four; a sparse-frequency cache does
  not exist.
- Verified that the direct short-quotient tensor graph is `K_18`, giving
  treewidth at least 17.
- At the pinned quotient, verified that the four polar coefficient
  families generate `M_10(F_3),M_10(F_3),M_10(F_3),M_8(F_3)` and each
  contains a full-rank scalar combination.  This blocks the obvious
  uniform low-rank/common-block diagonalization.
- No whole quotient census or integer exclusion was performed.
