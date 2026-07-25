# Research log

## 2026-07-24 19:35 PDT

- Started a proof-oriented `9 x 37` lane after completion of the exact
  18-orbit `h=0` profile census.
- Observed that every `h=0` local profile has entries only in
  `{0,1,2}` and that its normalized three-subsets admit the lossless conic
  representation `(q-t)^2=p(s)-1` over `F_3`.
- Derived the exact center/trit conversion `t=-p*u` on every active fiber.
- Introduced the rank-one antipodal quadratic-center family with arbitrary
  channel base quadratics and a shared projective opposite-class shape.
- Eliminated the first placement layer before enumeration.  The base
  parameter matrix has rank 17, the full structured matrix rank 18, and
  the remaining base kernel has dimension three.
- Exhausted all 29,524 projective shapes and all feasible amplitudes.  The
  resulting 2,922,804 coefficient-space incidences collapse to 324,756
  physical incidences and 65,601 distinct placements.  None is an exact
  second-placement witness.  The best point satisfies 16 of 18 active
  equations.
- Began hardening the theorem in a deterministic verifier and pinned
  certificate.  No external communication, commit, or push was performed.
- Replaced the ignored live production aggregate with the tracked frozen
  complete-classification certificate as the verifier input.
- Canonicalized the irrelevant choice of `R` when both channel amplitudes
  vanish.  The resulting exact accounting is 78,729 canonical
  shape/amplitude centers, 2,125,683 coefficient-space incidences,
  236,187 physical incidences before deduplication, and 65,601 distinct
  placements.
- Final reference replay: 2.06 seconds wall, 1.82 seconds user, 0.03
  seconds system, 98,156,544 bytes maximum resident memory, semantic hash
  `0c68683c63f9116179530430435e9da69728e198b7e5d8a2e63d8d69c8696a3c`.
