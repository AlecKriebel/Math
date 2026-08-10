# Research log

## 2026-08-09 -- clean-room start

- Read the locked `sd_0`, admissible-rooting, `W_TC`, `S_TC`, level, ordinary
  `T`, and open-JC definitions.
- Read the frozen weak-class theorem and its explicit four-leaf pair.  That
  pair is used only as a convention regression and never admitted into the
  standard-strong search universe.
- Fixed the first bounded target at 3--5 leaves and at most two
  reticulations.  Exact finite exclusions will be labelled by this bound;
  numerical algebra will not be called proof.

## 2026-08-09 -- exact bounded census closed

- Exhaustively generated 136,560 five-leaf/two-reticulation mixed candidates;
  2,370 are `S_TC` and 2,520 are weak-but-not-strong.  Across three through
  five leaves there are 2,821 `S_TC` topologies and 1,667 ordinary-`T` classes.
- An independent graph-atlas route reproduced every internal-core count.
- A coloured-incidence GraphMatcher implementation found no isomorphic
  duplicates among the 5,533 stored weak or strong records.
- All 24,897 admissible rootings of the bounded `S_TC` records give the same
  effective displayed-tree split map after root-edge multiplication.
- The frozen weak pair was replayed exactly: five admissible rootings, two
  tree-child, nonisomorphic, non-`T`, and all fourteen nonconstant JC orbit
  coordinates equal modulo the certified quadratic polynomial.

## 2026-08-09 -- algebraic and numerical attacks

- Proved the strict three-leaf separator
  `q011*q101*q110-q123^2`: zero on trees and strictly positive on the open
  3-sunlet cube.
- Screened every one of 2,133 dimension/flattening-compatible directed
  four-leaf non-`T` relations; no numerical candidate survived.
- Built two-prime rank/marginal/algebraic-matroid profiles for all 1,605
  five-leaf `T` representatives.  Fitted all 3,032 equal-profile unordered
  pairs and 1,000 sampled profile-dominant one-sided directions; no candidate
  survived.
- Refined the forty closest five-leaf near misses at five fresh source points
  and twenty target starts.  The close one-sided fits approached boundary
  parameters; none fit all five points at `1e-10`.
- These negative model searches remain `NUMERICALLY OBSERVED`, not proofs.

## 2026-08-09 -- definitions update

- Refreshed the definitions lock after the explicit nonvacuous `S_TC`
  existence clause was added.  New SHA-256:
  `c3382650fa004d90b2122aff1c95524590b31e436d77d4b804293184aa925b09`.
- The implementation had enforced this convention from the start; all counts
  are unchanged.
- The lock's local tail-incidence criterion agrees with exhaustive rooting
  enumeration on every rootable graph through four leaves.
